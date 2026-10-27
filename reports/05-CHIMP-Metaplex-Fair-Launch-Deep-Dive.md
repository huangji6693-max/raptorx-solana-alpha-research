# $CHIMP on Metaplex: Quantitative Analysis of Fair-Launch Pro-Rata Mechanics & Mojo AI SuperApp Economics

## Executive Summary
After 3 years of building **Mojo AI** (Solana personal AI money superapp used by **56,000+ wallets**, **1,000,000+ AI requests**, and **$3.9M+ routed trading volume**), ChimpX is launching **$CHIMP** via a fair public raise on **Metaplex** migrating to **Raydium**. Unlike standard bonding curves that reward latency snipers and penalize later buyers, the `$CHIMP` sale uses a **Soft-Cap Pro-Rata Refund & Uniform Clearing Price** mechanism with **100% public TGE unlock**.

---

## 1. Quantitative Comparison: Metaplex Fair Launch vs. Standard Bonding Curves

| Mechanism Dimension | Standard Meme Bonding Curve (e.g. Sequential AMM) | $CHIMP on Metaplex Fair Launch | Economic Winner |
|---|---|---|---|
| **Entry Price Fairness** | Exponential price curve; block-0 sniper bots buy 5–20x cheaper than retail | **Uniform clearing price** across all participants in the window | **100% Retail / Community Parity** |
| **Oversubscription Handling** | First-come-first-served gas wars or extreme slippage | **Automatic Pro-Rata USDC Refund** (nobody overpays) | **Zero Gas War / Zero Overpayment** |
| **Token Unlock at Launch** | Often gated by insider cliffs or hidden presale dumps | **100% Unlocked at Launch** for all public sale buyers | **Full Immediate Liquidity** |
| **Total Supply** | Variable | **1,000,000,000 `$CHIMP`** | Fixed, non-inflationary supply |

---

## 2. Mathematical Proof of the Pro-Rata Refund & Guaranteed Rate Invariant
Implemented and unit-tested in [`src/solana_alpha_suite.py`](../src/solana_alpha_suite.py) (`simulate_chimp_metaplex_launch`):

Let:
- $S_{\text{total}} = 1,000,000,000$ `$CHIMP`
- $A_{\text{pub}} = 500,000,000$ `$CHIMP` allocated to the public raise
- $C_{\text{soft}}$ be the soft cap in USDC, and $C_{\text{total}} = \sum_{i=1}^n c_i$ be total committed USDC across all participants.

When oversubscribed ($C_{\text{total}} > C_{\text{soft}}$):
1. **Fill Ratio**: $\alpha = \frac{C_{\text{soft}}}{C_{\text{total}}} \in (0, 1)$
2. **Effective Capital Accepted**: $c_i^{\text{eff}} = \alpha \cdot c_i$
3. **Automatic Pro-Rata Refund**: $R_i = (1 - \alpha) \cdot c_i$
4. **Unlocked Token Allocation**: $T_i = \frac{c_i}{C_{\text{total}}} \cdot A_{\text{pub}} = \frac{c_i^{\text{eff}}}{P_{\text{clear}}}$ where $P_{\text{clear}} = \frac{C_{\text{soft}}}{A_{\text{pub}}}$.

**Verified Numerical Example** (`tests/test_solana_alpha_suite.py`):
- At $C_{\text{soft}} = \$250,000$ USDC and $C_{\text{total}} = \$1,000,000$ USDC ($4\times$ oversubscribed), a participant committing $\$4,000$ USDC has $\$1,000$ USDC accepted at the guaranteed clearing price ($\$0.0005 / \text{CHIMP}$), receives **2,000,000 `$CHIMP` (100% unlocked at TGE)**, and is automatically refunded **$\$3,000$ USDC**.

---

## 3. Ready-to-Publish 10-Post X / Twitter Thread (`$CHIMP` on Metaplex)
1. **1/10** Most Solana token launches are broken: block-0 MEV snipers buy 80% of the curve in slot 1 and dump on retail 30 seconds later. After 3 years of building @ChimpX_AI, **$CHIMP** is doing the exact opposite on @metaplex + @RaydiumProtocol. Here is the full quantitative breakdown:
2. **2/10** First, traction before token: ChimpX built **Mojo AI**, a natural-language Solana SuperApp where you type what you want and AI executes the DeFi route. Measured footprint prior to TGE: **56,000+ wallets**, **1,000,000+ requests**, and **$3.9M+ traded volume**.
3. **3/10** How does the **$CHIMP** Metaplex sale eliminate sniping? Instead of a sequential price curve where bots frontrun human transactions via Jito bundles, every participant enters on equal footing during the public raise window.
4. **4/10** **Rule #1: Soft Cap Unlocks a Guaranteed Rate or Better.** Total supply is fixed at **1,000,000,000 $CHIMP**. Once the soft cap is met, the clearing rate is locked—meaning early second-1 bots get zero price edge over a human joining hours later.
5. **5/10** **Rule #2: Pro-Rata Refunds (Nobody Overpays).** If the pool is 4x oversubscribed, you do not pay 4x higher price per token. Instead, 25% of your commitment fills at the guaranteed rate and **75% of your excess funds are refunded pro-rata**.
6. **6/10** **Rule #3: 100% Unlocked at Launch.** Public sale buyers receive 100% of their $CHIMP tokens unlocked at Raydium launch—no complicated vesting traps for public participants while liquidity seeds directly into Raydium.
7. **7/10** Why does this matter for Solana AI agents? Mojo AI abstracts multi-hop swaps, yield routing, and portfolio management behind conversational intent—converting the 56K+ wallet userbase into organic utility demand for $CHIMP.
8. **8/10** We open-sourced a runnable Python simulator verifying the $CHIMP pro-rata refund math and Raydium launch clearing mechanics here: https://github.com/huangji6693-max/raptorx-solana-alpha-research
9. **9/10** Key takeaway: Real product first (3 years, 56K wallets, 1M+ requests, $3.9M volume), fair distribution second (pro-rata refund, zero bot sniping, 100% public unlock).
10. **10/10** Explore the $CHIMP fair launch on Metaplex and test our open-source allocation calculator in the repo above! #Solana #CHIMP #Metaplex #MojoAI #Raydium
