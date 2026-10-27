# Premier League Predictions on Worm.wtf: Quantitative 3x-Leverage Kelly Playbook & Matchweek Analysis

## Executive Summary
**Worm (`worm.wtf`)** brings continuous, real-time sports prediction markets to Solana where outcome shares trade from **1¢ to 99¢** (`$1.00 USDC` payout on settlement), move live as the Premier League match unfolds, and support **up to 3× leverage** alongside a **$1,500 USDC weekly leaderboard prize pool** and **up to 30% referral fee share**.

---

## 1. Quantitative Pricing & 3× Leverage Fractional-Kelly Model
Implemented and verified in [`src/solana_alpha_suite.py`](../src/solana_alpha_suite.py) (`evaluate_worm_leveraged_epl_position`):

- **Share Price & Implied Probability**: A Worm share trading at $c \in [1, 99]$ cents implies a market win probability $p_{\text{mkt}} = c / 100$ and unleveraged net odds $b = \frac{1 - p_{\text{mkt}}}{p_{\text{mkt}}}$.
- **True Edge ($\Delta p$)**: When a trader's expected-goals ($xG$) + lineup model estimates true win probability $p_{\text{true}} > p_{\text{mkt}}$, the raw edge in basis points is:
  $$\text{Edge (bps)} = (p_{\text{true}} - p_{\text{mkt}}) \times 10,000$$
- **Optimal Leverage Selection ($1\times$ to $3\times$)**:
  Because in-play football goal events create discontinuous jumps in share price (a single goal shifts win probability by $+28\%$ to $+45\%$), applying $3\times$ leverage indiscriminately risks premature liquidation during normal variance. Our engine gates leverage by edge and match state:
  - **Pre-Match Value Entry ($\text{Edge} \ge +800\text{ bps}$, low early-goal variance)**: Up to **2.5×–3.0× leverage** with quarter-Kelly sizing ($f = 0.25 \cdot f^*$).
  - **Live In-Play Mean Reversion (60'–75' dominant favorite trailing 0-1 with $xG > 2.1$)**: **1.5×–2.0× leverage** capturing the steep convexity of `18¢ → 55¢` equalizer repricing.

---

## 2. Premier League Matchweek Quantitative Trade Setups

| Fixture Archetype | Worm Share Price | Implied Prob ($p_{\text{mkt}}$) | xG Model Prob ($p_{\text{true}}$) | Edge (bps) | Optimal Worm Leverage | Quarter-Kelly Allocation | Expected Leveraged ROI |
|---|---|---|---|---|---|---|---|
| **Home Title Contender vs High-Line Visitor** | `46¢` | `46.0%` | `56.0%` | **+1,000 bps** | **3.0×** | `4.63%` | **+65.22%** |
| **Underpriced Draw in Low-Tempo Derby** | `24¢` | `24.0%` | `31.0%` | **+700 bps** | **2.4×** | `2.30%` | **+70.00%** |
| **Public Overbet Away Favorite (Avoid/Fade)** | `65¢` | `65.0%` | `55.0%` | `-1,000 bps` | **1.0× (No Bet / Fade)** | `0.00%` | `-15.38%` |

---

## 3. Ready-to-Publish Content Thread (`worm.wtf` Premier League)
1. **1/8** `gworm!` The Premier League is back on @worm_wtf and the weekly **$1,500 USDC leaderboard** is live. Most traders treat 3× leveraged prediction markets like a casino—here is the quantitative Kelly framework to trade EPL shares (1¢–99¢) like a sharp desk:
2. **2/8** On Worm (`worm.wtf/sports?league=eng.1`), every outcome share trades between **1¢ and 99¢** and settles at **$1.00 USDC** if correct. A share at `46¢` = `46%` implied probability. If your xG + lineup model puts true probability at `56%`, you have **+1,000 bps of raw edge**.
3. **3/8** When should you turn on **3× leverage** on Worm? Never on coin-flip noise. Use 2.5×–3.0× leverage ONLY when pre-match edge exceeds +800 bps AND early downside liquidation buffer covers a first-half counter-attack goal.
4. **4/8** **The Live In-Play Alpha (Minute 55'–70')**: When a dominant home side trails 0-1 against the run of play (>65% box touches, >1.8 non-penalty xG), their Worm share frequently over-corrects into the `18¢–25¢` zone. A single equalizer reprices the share to `50¢+` instantly—you do not even need to hold to full time!
5. **5/8** **Leaderboard Strategy ($1,500 USDC weekly pool)**: Consistent realized PnL beats single all-in punts. Sizing at Quarter-Kelly (`f = 0.25 * (p_true - p_mkt) / (1 - p_mkt)`) compounds top-10 leaderboard rank while surviving EPL upsets.
6. **6/8** Plus, Worm pays **up to 30% referral fee share**—meaning publishing data-driven matchweek previews turns your football analytics directly into recurring USDC yield.
7. **7/8** We open-sourced our Python **Worm 3× Leveraged EPL Kelly Calculator** (`evaluate_worm_leveraged_epl_position` + unit tests) here: https://github.com/huangji6693-max/raptorx-solana-alpha-research
8. **8/8** Trade Premier League live on Solana: https://www.worm.wtf/sports?league=eng.1&view=leaderboard #gworm #Solana #PremierLeague #PredictionMarkets
