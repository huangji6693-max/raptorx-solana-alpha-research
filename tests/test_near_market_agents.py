import unittest
from near_market_agents import (
    TranscriptSentence,
    audit_python_source,
    check_brand_name_availability,
    deduplicate_csv_records,
    generate_video_clips,
    run_pay_per_use_media_generator,
)


class TestNearMarketAgents(unittest.TestCase):
    def test_brand_checker_standard_and_known_conflict_and_variations(self):
        # 1. Known brand conflict (Apple)
        conflict = check_brand_name_availability(
            ["Apple"],
            extensions=[".com", ".io", ".ai"],
            platforms=["x", "instagram", "tiktok"],
            trademark_countries=["US"],
        )[0]
        self.assertEqual(conflict.domains["apple.com"], "taken")
        self.assertEqual(conflict.social_handles["x"], "taken")
        self.assertEqual(conflict.trademarks[0]["reg_number"], "3928818")
        self.assertIn("not legal advice", conflict.disclaimer)

        # 2. Novel brand + variations + gated platform transparency
        novel = check_brand_name_availability(
            ["ZephyrQuantNova"],
            extensions=[".com", ".io", ".ai"],
            platforms=["x", "github", "instagram", "tiktok"],
            trademark_countries=["US", "EU"],
            suggest_variations=True,
        )[0]
        self.assertEqual(novel.domains["zephyrquantnova.com"], "available")
        self.assertEqual(novel.social_handles["x"], "available")
        self.assertIn("couldn't confirm", novel.social_handles["instagram"])
        self.assertIn("couldn't confirm", novel.social_handles["tiktok"])
        self.assertEqual(len(novel.suggested_variations), 3)

    def test_media_generator_happy_path_safety_decline_and_partial_revision(self):
        # 1. Image variations
        img_res = run_pay_per_use_media_generator(
            brief="3 product photos of a ceramic mug on a wooden table",
            media_type="image",
            count=3,
            aspect_ratio="1:1",
        )
        self.assertEqual(img_res.status, "completed")
        self.assertEqual(len(img_res.artifacts), 3)

        # 2. Partial revision of file #2 only
        rev_res = run_pay_per_use_media_generator(
            brief="3 product photos of a ceramic mug on a dark walnut table",
            media_type="image",
            count=3,
            aspect_ratio="1:1",
            existing_artifacts=img_res.artifacts,
            replace_indices=[2],
        )
        self.assertEqual(rev_res.artifacts[0].uri, img_res.artifacts[0].uri)
        self.assertNotEqual(rev_res.artifacts[1].uri, img_res.artifacts[1].uri)
        self.assertEqual(rev_res.artifacts[2].uri, img_res.artifacts[2].uri)

        # 3. Celebrity without consent declined
        dec_res = run_pay_per_use_media_generator(
            brief="Image of Taylor Swift holding our coffee mug",
            media_type="image",
        )
        self.assertEqual(dec_res.status, "declined")
        self.assertIn("consent", dec_res.declined_reason.lower())

    def test_video_clipper_retention_and_fallback_and_sentence_boundaries(self):
        sentences_with_ret = [
            TranscriptSentence(0.0, 12.5, "Welcome back to the channel everyone.", retention_score=0.35),
            TranscriptSentence(12.5, 28.0, "Here is the exact three-step secret that doubled our conversion rate.", retention_score=0.94),
            TranscriptSentence(28.0, 45.0, "Second, never ignore how latency impacts checkout abandonment.", retention_score=0.88),
        ]
        res_ret = generate_video_clips(sentences_with_ret, num_clips=2, requested_formats=["9:16", "1:1"])
        self.assertTrue(res_ret.used_retention_heatmap)
        self.assertFalse(res_ret.fallback_disclosed)
        self.assertEqual(len(res_ret.clips), 2)
        for clip in res_ret.clips:
            self.assertTrue(clip.transcript_excerpt.endswith("."))

        # Fallback without retention data + unsupported format explanation
        sentences_no_ret = [
            TranscriptSentence(0.0, 10.0, "Today we are discussing standard configurations."),
            TranscriptSentence(10.0, 25.0, "Why do 90% of critical production deployments fail on day one?"),
        ]
        res_fb = generate_video_clips(sentences_no_ret, num_clips=1, requested_formats=["9:16", "Imax-70mm"])
        self.assertFalse(res_fb.used_retention_heatmap)
        self.assertTrue(res_fb.fallback_disclosed)
        self.assertIn("Imax-70mm", res_fb.unsupported_formats_explained)

    def test_agentpact_csv_dedupe_and_python_security_audit(self):
        raw_csv = "id,email,role\n1,Alice@Example.com,admin\n2,bob@example.com,user\n3,alice@example.com,editor\n"
        deduped = deduplicate_csv_records(raw_csv, key_columns=["email"])
        self.assertEqual(deduped["total_input_rows"], 3)
        self.assertEqual(deduped["unique_output_rows"], 2)
        self.assertEqual(deduped["duplicates_removed"], 1)

        vuln_py = 'import subprocess, pickle\nsubprocess.run(cmd, shell=True)\npickle.loads(data)\neval(user_input)\ncursor.execute(f"SELECT * FROM users WHERE name = {u}")\n'
        findings = audit_python_source(vuln_py)
        self.assertEqual(len(findings), 4)


if __name__ == "__main__":
    unittest.main()
