# Vaultline Security Audit Grant Application — MultiHopper Atomic Route & Revenue-Share Vault

## 1. Project Name & Description
- **Project Name**: **MultiHopper Atomic Route & Revenue-Share Settlement Vault (`multihopper_vault`)**
- **Description**: A non-custodial Solana Anchor settlement vault and K-shortest-path multi-venue routing engine (`Raydium CLMM`, `Orca Whirlpools`, `Meteora DLMM`, `Phoenix`) that executes atomic multi-hop swaps, enforces on-chain minimum net output slippage guardrails, blocks circular wash-trading (`CircularSelfTransfer`), and splits partner/integrator revenue share deterministically in a single transaction.
- **Colosseum / Ecosystem Track**: DeFi & Payments Infrastructure (built for Solana Colosseum & MultiHopper Build-and-Route ecosystem).
- **Repository Link**: https://github.com/huangji6693-max/raptorx-solana-alpha-research (Anchor program at [`programs/multihopper_vault/src/lib.rs`](../programs/multihopper_vault/src/lib.rs) and off-chain router/compliance engine at `https://github.com/huangji6693-max/solana-validator-tx-ordering/tree/multihopper-router`).

## 2. Programs in Scope & Approximate Lines of Code (LOC)
| Program / Module | Path | Language / Framework | Approx. LOC | Scope Priority |
|---|---|---|---|---|
| `multihopper_vault` | `programs/multihopper_vault/src/lib.rs` | Rust / Anchor 0.30+ (`anchor-spl`) | **225 LOC** (on-chain Anchor program) | **P0 (Critical)** |
| `multihopper_router` | `src/multihopper_router/router.py` + `src/solana_alpha_suite.py` | Python 3.12 (off-chain route solver & invariant verifier) | **480 LOC** | **P1 (Supporting)** |

Because the on-chain Anchor program is a tightly scoped **225 LOC** single-program vault with zero external oracle dependencies, it fits comfortably within the **4,000 USDC full-coverage Vaultline Audit Grant**.

## 3. Current Stage, Users & TVL Target
- **Current Stage**: Devnet & Mainnet-Shadow simulation tested (100% unit and invariant test pass rate across 11 deterministic test suites).
- **Pre-Mainnet TVL / Volume Target**: Launching mainnet atomic routing for partner integrations targeting $100,000–$1,000,000+ monthly routed swap volume.

## 4. Why a Vaultline Security Audit Matters Now
1. **PDA Signer Authority over Settlement Vaults**: `settle_atomic_route` uses PDA seeds `["vault_config", bump]` to sign three consecutive SPL `token::transfer` CPIs (`net_output` to recipient, `partner_fee` to integrator, `protocol_fee` to treasury). Independent formal verification of account ownership constraints (`recipient_token.mint == vault_token.mint`, `treasury_token.owner == config.treasury`) is essential before uncapped mainnet routing.
2. **Rounding & Precision Invariants**: Ensuring `total_fee = gross_output * protocol_fee_bps / 10_000` and `partner_fee = total_fee * partner_share_bps / 10_000` can never leave stranded dust or underflow `min_net_output` under adversarial token decimal configurations (6-decimal USDC vs 9-decimal SOL).
3. **Anti-Wash-Trading & Sybil Volume Accounting**: Confirming that `CircularSelfTransfer` cannot be bypassed via intermediate token accounts when accumulating `total_qualifying_volume`.

## 5. Team & Technical Contact
- **Lead Engineer**: `huangji6693-max` (`wudiwangyou-agent-jade-87`)
- **GitHub**: https://github.com/huangji6693-max/raptorx-solana-alpha-research
- **Solana Payout / Multisig Authority**: `AyXYaA9Nf4z5fpLKY6DmubWe6D2qveMd79w8pEDNHcDw`
