import unittest
from near_market_agents import (
    DubbingLine,
    LocalProviderContact,
    TranscriptSentence,
    audit_python_source,
    check_brand_name_availability,
    deduplicate_csv_records,
    evaluate_sentinel_commit_543a0231,
    generate_video_clips,
    run_call_for_me_booking_agent,
    run_local_services_quote_agent,
    run_pay_per_use_media_generator,
    run_video_dubbing_agent,
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

    def test_video_dubbing_agent_consent_sync_and_protected_terms(self):
        lines = [
            DubbingLine("spk1", 0.0, 4.0, "Welcome to RaptorX on NEAR Protocol.", "Bienvenidos a RaptorX en NEAR Protocol."),
            DubbingLine("spk2", 4.2, 8.0, "Our latency dropped by 40 percent.", "Nuestra latencia cayó un cuarenta por ciento en producción hoy."),
        ]
        # Without confirmed consent, speaker voice request falls back to stock_voice
        res_no_consent = run_video_dubbing_agent(
            lines,
            target_languages=["es", "de"],
            use_speaker_voice=True,
            speaker_consent_confirmed=False,
            do_not_translate=["RaptorX", "NEAR Protocol"],
        )
        self.assertEqual(res_no_consent["voice_mode_used"], "stock_voice")
        self.assertIsNotNone(res_no_consent["consent_fallback_note"])
        self.assertTrue(res_no_consent["background_music_and_sfx_audible"])
        es_out = res_no_consent["languages"]["es"]
        self.assertFalse(es_out.synced_lines[0]["overlaps_next_speaker"])
        self.assertIn("RaptorX", es_out.synced_lines[0]["text"])

    def test_local_services_quote_agent_no_invented_prices_and_scope_diffs(self):
        providers = [
            LocalProviderContact("Apex HVAC", "AC Replacement", "Austin", "email", "quoted", 4800.0, False, "Next Tue", "Unit + Labor", "Drywall patching"),
            LocalProviderContact("CoolBreeze LLC", "AC Replacement", "Austin", "phone_followup", "quoted", 6200.0, True, "Next Thu", "Unit + Labor + Ductwork", None),
            LocalProviderContact("BusyAir Inc", "AC Replacement", "Austin", "email", "no_reply"),
        ]
        res = run_local_services_quote_agent(
            "Replace 3-ton AC unit",
            "Austin, TX",
            providers,
            budget_limit_usd=5000.0,
            buyer_approved_contact_sharing=False,
        )
        self.assertEqual(res["total_providers_contacted"], 3)
        self.assertEqual(res["quoted_count"], 2)
        self.assertEqual(res["no_reply_count"], 1)
        self.assertFalse(res["quote_accepted_or_booked"])
        self.assertFalse(res["buyer_contact_shared"])
        self.assertFalse(res["call_recordings_stored"])
        self.assertTrue(res["comparison_table"][1]["over_budget"])
        self.assertEqual(len(res["scope_difference_warnings"]), 1)

    def test_call_for_me_booking_agent_window_alternatives_ai_and_payment_rules(self):
        # 1. Standard booking within window
        booked = run_call_for_me_booking_agent(
            business_name="Osteria Mozza",
            requested_date="2026-11-06",
            requested_window=["19:00", "19:30", "20:00"],
            booking_name="Alex Chen",
            party_size_or_service="Dinner for 4",
            business_offered_slots=["19:30", "21:30"],
            asked_if_ai=True,
        )
        self.assertEqual(booked["status"], "booked")
        self.assertEqual(booked["booked_slot"], "19:30")
        self.assertIn("AI assistant", booked["ai_disclosure_response"])
        self.assertFalse(booked["recording_or_transcript_retained"])

        # 2. Out-of-window slot only -> must NOT book, must report offered alternatives
        not_avail = run_call_for_me_booking_agent(
            business_name="Osteria Mozza",
            requested_date="2026-11-06",
            requested_window=["19:00", "19:30"],
            booking_name="Alex Chen",
            party_size_or_service="Dinner for 4",
            business_offered_slots=["21:45"],
        )
        self.assertEqual(not_avail["status"], "not_available")
        self.assertIsNone(not_avail["booked_slot"])
        self.assertEqual(not_avail["offered_alternatives"], ["21:45"])

        # 3. Payment / deposit requested -> declines and reports
        declined_pay = run_call_for_me_booking_agent(
            business_name="Osteria Mozza",
            requested_date="2026-11-06",
            requested_window=["19:00"],
            booking_name="Alex Chen",
            party_size_or_service="Dinner for 4",
            business_offered_slots=["19:00"],
            asked_for_credit_card_or_deposit=True,
        )
        self.assertEqual(declined_pay["status"], "declined_payment_hold_required")
        self.assertTrue(declined_pay["payment_or_deposit_declined"])

    def test_sentinel_commit_543a0231_evaluations(self):
        reject_res = evaluate_sentinel_commit_543a0231("code_refactor_and_fix")
        self.assertEqual(reject_res["matcher_verdict"], "REJECT = TRUE")
        self.assertTrue(reject_res["reject"])

        match_res = evaluate_sentinel_commit_543a0231("sentinel_dependency_audit")
        self.assertEqual(match_res["matcher_verdict"], "MATCH = TRUE")
        self.assertEqual(match_res["facts_extracted"], 24)
        self.assertFalse(match_res["gate_decision"]["blocked"])

        ind_res = evaluate_sentinel_commit_543a0231("sentinel_independent_evaluation")
        self.assertEqual(ind_res["constraint_findings"]["unit_tests_passing"], "35/35")


if __name__ == "__main__":
    unittest.main()
