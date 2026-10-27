import os
import unittest
from solana_alpha_suite import (
    audit_anchor_program_invariants,
    evaluate_panta_nectarfi_spread,
    evaluate_worm_leveraged_epl_position,
    simulate_chimp_metaplex_launch,
)


class TestSolanaAlphaSuite(unittest.TestCase):
    def test_chimp_metaplex_pro_rata_refund_and_100pct_unlock(self):
        res = simulate_chimp_metaplex_launch(
            soft_cap_usdc=250_000.0,
            total_committed_usdc=1_000_000.0,
            user_committed_usdc=4_000.0,
            total_supply=1_000_000_000,
            public_share=0.50,
        )
        self.assertEqual(res.public_allocation_tokens, 500_000_000)
        self.assertAlmostEqual(res.clearing_price_usdc, 0.0005)
        self.assertAlmostEqual(res.user_effective_usdc, 1_000.0)
        self.assertAlmostEqual(res.user_refund_usdc, 3_000.0)
        self.assertAlmostEqual(res.user_tokens_unlocked_at_tge, 2_000_000.0)

    def test_worm_leveraged_epl_position_positive_and_negative_edge(self):
        pos = evaluate_worm_leveraged_epl_position(
            match_name="Arsenal vs Liverpool",
            market_price_cents=46.0,
            true_prob=0.56,
            max_leverage=3.0,
        )
        self.assertEqual(pos.edge_bps, 1000.0)
        self.assertEqual(pos.optimal_leverage, 3.0)
        self.assertGreater(pos.recommended_bankroll_fraction, 0.0)
        self.assertGreater(pos.expected_roi_pct, 60.0)

        neg = evaluate_worm_leveraged_epl_position(
            match_name="Chelsea vs Man City",
            market_price_cents=65.0,
            true_prob=0.55,
            max_leverage=3.0,
        )
        self.assertEqual(neg.recommended_bankroll_fraction, 0.0)

    def test_panta_nectarfi_spread_and_arb(self):
        ev = evaluate_panta_nectarfi_spread(
            yes_ask_panta=0.42,
            no_ask_panta=0.59,
            external_reference_prob=0.52,
            fee_bps=50.0,
        )
        self.assertEqual(ev["best_side"], "BUY_YES")
        self.assertGreater(ev["yes_ev_pct"], 20.0)
        self.assertFalse(ev["riskless_arb_available"])

    def test_vaultline_anchor_program_invariants(self):
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        rust_path = os.path.join(repo_root, "programs", "multihopper_vault", "src", "lib.rs")
        with open(rust_path) as f:
            src = f.read()
        invariants = audit_anchor_program_invariants(src)
        for k, passed in invariants.items():
            self.assertTrue(passed, f"Anchor security invariant failed: {k}")


if __name__ == "__main__":
    unittest.main()
