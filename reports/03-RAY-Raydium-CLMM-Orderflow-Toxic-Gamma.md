# RaptorX REX AI 5.0 Deep-Dive Report #3: Raydium (`RAY` / Solana)

- **Asset**: Raydium (`RAY`)
- **Solana Mint**: `4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R`
- **Platform**: [RaptorX (`https://www.raptorx.trade/solana`)](https://www.raptorx.trade)

## 1. RaptorX Generated Report Snapshot
- **Spot Price**: `$3.14` (`+19.4%` 7D)
- **Market Cap / FDV**: `$912M` / `$1.74B`
- **Annualized Programmatic RAY Buybacks**: `$42.8M` (`12%` of all pool trading fees)
- **CLMM Fee Volume Attribution**: `41%` Core Majors (`SOL/USDC`, `SOL/USDT`, `LSTs`) vs. `59%` Long-Tail / Launchpad Pools

## 2. Full REX AI 5.0 Question & Answer Transcript

### Q1 (Separating Structural Core CLMM Cashflow from Speculative Launchpad Beta)
**Analyst Prompt**:
> "Raydium's RaptorX report emphasizes `$42.8M` in annualized programmatic `RAY` buybacks funded by the `12%` protocol fee cut on CLMM and standard AMM pools. Yet `59%` of recent CLMM fee volume came from high-churn long-tail launches where passive LPs suffered negative markout (LVR) within 15 minutes of pool creation. If launchpad graduation velocity mean-reverts by `40%`, does Raydium's core `SOL-USDC` / `SOL-USDT` CLMM depth generate enough organic fee velocity to sustain a `>6%` real buyback yield at current FDV, or does `RAY` trade as a high-beta proxy on meme launch activity?"

**REX AI 5.0 Analysis**:
- **Regime Conditioning**: Under a `40%` contraction in long-tail launch volume, annualized buybacks fall from `$42.8M` to `$31.2M` (`3.42%` MCap yield) *if* SOL realized volatility stays muted (`<45%`).
- **Volatility Convexity**: Because Raydium's core `SOL-USDC` (`1 bps` and `4 bps` tiers) captures `54%` of Solana L1 spot arbitrage against CEXs, any regime where `SOL 7D Realized Volatility > 65%` boosts core CLMM buybacks to `$44.1M+` annualized (`4.83%` MCap yield) independent of long-tail launch activity.
