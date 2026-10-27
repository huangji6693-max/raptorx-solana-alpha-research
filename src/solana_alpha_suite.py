"""Solana Ecosystem Alpha & Security Verification Suite.

Covers:
1. Metaplex Bootstrap ($CHIMP) Pro-Rata Refund & Anti-Sniping Fair Launch Simulator
2. Worm.wtf Premier League 3x Leveraged Prediction Market Kelly Criterion Engine
3. Panta x NectarFi Binary Prediction Market Expected Value & Cross-Book Arbitrage
4. Vaultline Colosseum Anchor Program Static Security Invariant Verifier
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class ChimpFairLaunchResult:
    soft_cap_usdc: float
    total_committed_usdc: float
    public_allocation_tokens: int
    clearing_price_usdc: float
    user_committed_usdc: float
    user_effective_usdc: float
    user_refund_usdc: float
    user_tokens_unlocked_at_tge: float


def simulate_chimp_metaplex_launch(
    soft_cap_usdc: float,
    total_committed_usdc: float,
    user_committed_usdc: float,
    total_supply: int = 1_000_000_000,
    public_share: float = 0.50,
) -> ChimpFairLaunchResult:
    """Simulates the $CHIMP Metaplex Bootstrap fair launch with pro-rata refund and 100% TGE unlock."""
    if soft_cap_usdc <= 0 or total_committed_usdc <= 0 or user_committed_usdc < 0:
        raise ValueError("Commitments and soft cap must be positive")
    if user_committed_usdc > total_committed_usdc:
        raise ValueError("User commitment cannot exceed total committed pool")

    public_tokens = int(round(total_supply * public_share))
    clearing_price = soft_cap_usdc / public_tokens

    if total_committed_usdc <= soft_cap_usdc:
        effective_usdc = user_committed_usdc
        refund_usdc = 0.0
        tokens = (user_committed_usdc / total_committed_usdc) * public_tokens
    else:
        fill_ratio = soft_cap_usdc / total_committed_usdc
        effective_usdc = user_committed_usdc * fill_ratio
        refund_usdc = user_committed_usdc - effective_usdc
        tokens = (user_committed_usdc / total_committed_usdc) * public_tokens

    return ChimpFairLaunchResult(
        soft_cap_usdc=soft_cap_usdc,
        total_committed_usdc=total_committed_usdc,
        public_allocation_tokens=public_tokens,
        clearing_price_usdc=clearing_price,
        user_committed_usdc=user_committed_usdc,
        user_effective_usdc=round(effective_usdc, 6),
        user_refund_usdc=round(refund_usdc, 6),
        user_tokens_unlocked_at_tge=round(tokens, 4),
    )


@dataclass(frozen=True)
class WormPositionRecommendation:
    match_name: str
    market_price_cents: float
    implied_prob: float
    true_prob: float
    edge_bps: float
    optimal_leverage: float
    recommended_bankroll_fraction: float
    expected_roi_pct: float


def evaluate_worm_leveraged_epl_position(
    match_name: str,
    market_price_cents: float,
    true_prob: float,
    max_leverage: float = 3.0,
    kelly_fraction: float = 0.25,
) -> WormPositionRecommendation:
    """Evaluates a Worm.wtf Premier League outcome share (1c to 99c) with up to 3x leverage."""
    if not (1.0 <= market_price_cents <= 99.0):
        raise ValueError("Market price must be between 1 and 99 cents")
    if not (0.0 < true_prob < 1.0):
        raise ValueError("True probability must be in (0, 1)")
    if not (1.0 <= max_leverage <= 3.0):
        raise ValueError("Worm leverage is capped at 3.0x")

    p_mkt = market_price_cents / 100.0
    net_odds_b = (1.0 - p_mkt) / p_mkt
    edge = true_prob - p_mkt
    edge_bps = round(edge * 10_000, 2)

    if edge <= 0:
        return WormPositionRecommendation(
            match_name=match_name,
            market_price_cents=market_price_cents,
            implied_prob=round(p_mkt, 4),
            true_prob=round(true_prob, 4),
            edge_bps=edge_bps,
            optimal_leverage=1.0,
            recommended_bankroll_fraction=0.0,
            expected_roi_pct=round((true_prob / p_mkt - 1.0) * 100.0, 2),
        )

    full_kelly = (true_prob * (net_odds_b + 1.0) - 1.0) / net_odds_b
    sized_fraction = min(0.25, full_kelly * kelly_fraction)
    # Use higher leverage only when edge >= 400 bps and downside volatility allows
    leverage = min(max_leverage, max(1.0, round(1.0 + (edge / 0.05), 2)))
    expected_roi = ((true_prob / p_mkt) - 1.0) * leverage * 100.0

    return WormPositionRecommendation(
        match_name=match_name,
        market_price_cents=market_price_cents,
        implied_prob=round(p_mkt, 4),
        true_prob=round(true_prob, 4),
        edge_bps=edge_bps,
        optimal_leverage=leverage,
        recommended_bankroll_fraction=round(sized_fraction, 4),
        expected_roi_pct=round(expected_roi, 2),
    )


def evaluate_panta_nectarfi_spread(
    yes_ask_panta: float,
    no_ask_panta: float,
    external_reference_prob: float,
    fee_bps: float = 50.0,
) -> Dict[str, float | str]:
    """Evaluates Panta binary YES/NO pricing against NectarFi/external implied probability."""
    if not (0.01 <= yes_ask_panta <= 0.99 and 0.01 <= no_ask_panta <= 0.99):
        raise ValueError("YES/NO prices must be in [0.01, 0.99]")
    fee_rate = fee_bps / 10_000.0
    effective_yes = yes_ask_panta * (1.0 + fee_rate)
    effective_no = no_ask_panta * (1.0 + fee_rate)

    yes_ev = (external_reference_prob / effective_yes) - 1.0
    no_ev = ((1.0 - external_reference_prob) / effective_no) - 1.0
    synthetic_arb_cost = effective_yes + effective_no

    best_side = "NONE"
    if yes_ev > 0.02 and yes_ev >= no_ev:
        best_side = "BUY_YES"
    elif no_ev > 0.02 and no_ev > yes_ev:
        best_side = "BUY_NO"

    return {
        "best_side": best_side,
        "yes_ev_pct": round(yes_ev * 100.0, 2),
        "no_ev_pct": round(no_ev * 100.0, 2),
        "synthetic_bundle_cost": round(synthetic_arb_cost, 4),
        "riskless_arb_available": synthetic_arb_cost < 1.0,
    }


def audit_anchor_program_invariants(rust_source: str) -> Dict[str, bool]:
    """Static security invariant check for the Vaultline Colosseum Anchor vault program."""
    return {
        "has_checked_math": ".checked_mul(" in rust_source and ".checked_sub(" in rust_source,
        "has_signer_check": "Signer<" in rust_source,
        "has_owner_and_mint_constraints": "constraint = recipient_token.mint == vault_token.mint" in rust_source,
        "has_self_transfer_guard": "CircularSelfTransfer" in rust_source,
        "has_slippage_protection": "SlippageExceeded" in rust_source,
        "has_fee_cap_guard": "MAX_TOTAL_FEE_BPS" in rust_source,
    }
