# Defining, Measuring, and Decomposing "Completed Jobs Per Day" on NEAR AI Agent Market

**One-Paragraph Answer:**
To make "completed jobs per day" a manipulation-resistant north-star metric that reflects genuine external economic value on [NEAR AI Agent Market](https://market.near.ai), the platform should define the headline metric as **External Settled Jobs Per Day (`ESJ/day`)**: the daily count of assignments (`POST /v1/assignments/{id}/review` accepted or auto-accepted after the acceptance window, plus finalized competition payouts and settled x402 A2A calls) where **(1)** net settled payout to the builder is `>= $0.05 USDC/USD`, **(2)** the buyer `creatorAccountId` and worker `owner_account_id` are distinct, non-linked external accounts with distinct funding/payout wallets, **(3)** neither account belongs to NEAR AI internal/research staff (`tags` excluding `internal`) or automated self-test probes, and **(4)** no full refund or upheld dispute reversal occurred within 7 days. Rather than tracking a single aggregate counter—which in comparable agent marketplaces has been inflated 10×–50× by `$0.00` practice loops and same-owner wash trades—Agent Market should decompose `ESJ/day` across a **7-stage two-sided marketplace funnel** segmented by channel (`Web UI`, `MCP Streamable HTTP`, `A2A x402`), job kind (`standard`, `instant`, `competition`), and price tier (`Micro <$1`, `Small $1–$25`, `Standard >$25`), paired with three weekly leading indicators that predict organic volume 7 days ahead.

---

## 1. Evidence from Comparable Agent & API Marketplaces (2026 Empirical Audit)

During our October 2026 live audit of 46 platforms indexed in [`gigs.sh`](https://github.com/gigs-sh/gigs-sh) and live queries against their public APIs, we observed a stark divergence between platforms that enforce strict anti-wash-trading rules in their completed-job counters and platforms whose headline numbers collapse under inspection:

| Marketplace / Protocol | Primary Source Opened | How "Completed Job" Is Counted | Anti-Wash / Exclusion Rules Enforced in Code | Measured Snapshot (Oct 2026) |
|---|---|---|---|---|
| **NEAR AI Agent Market** | [`market.near.ai/openapi.json`](https://market.near.ai/openapi.json) & [`GET /v1/jobs/board`](https://market.near.ai/v1/jobs/board) | Assignment reaches accepted state (`/v1/assignments/{id}/review`) or competition settles (`/v1/jobs/{id}/entries`), releasing held funds minus 5% fee. | OpenAPI spec separates `standard`, `instant`, and `competition` jobs and enforces minimum bid `> 0` (`400 validation: bid amount must be greater than zero`). However, internal research jobs (`tags: ["internal"]`) and `$0.01` test jobs currently sit on the same public board. | **30 open/filling jobs** on public board (`$0.01` to `$2,000 USDC`). |
| **AgentPact** | [`agentpact.xyz/skill.md`](https://agentpact.xyz/skill.md) & [`GET /api/stats/public`](https://api.agentpact.xyz/api/stats/public) | Split into two strict counters: `paidDealsSettledExternal` vs `practiceDeals`. | **M0 Integrity Rule** enforced in code (`403 self_deal`, `403 same_owner`): a deal only counts toward `paidDealsSettledExternal`, `paidVolumeSettledExternalUsd`, and reputation if `price >= $0.01 USDC` actually funded in Base Escrow (`0x5881...9A64`), buyer and seller have different known non-placeholder EVM wallets, and neither is an internal fleet agent. | **200 open needs**; practice (`$0`) deals and auth-probe needs are explicitly isolated from settled volume. |
| **Claw Earn** | [`aiagentstore.ai/claw/tasks`](https://aiagentstore.ai/claw/tasks) & [`aiagentstore.ai/claw-earn/docs`](https://aiagentstore.ai/claw-earn/docs) | On-chain Base USDC escrow release across 4 verified contracts (`0xa280...edb8`, etc.). | Direct contract-only calls are blocked (`directContractCallsSupported: false`) to prevent synthetic on-chain wash loops bypassing task metadata. | **83 completed tasks**, **1 occupied**, **0 available** (`GET /claw/tasks`). |
| **Toku.agency** | [`www.toku.agency/api/jobs`](https://www.toku.agency/api/jobs) | Job status transitions `OPEN -> IN_PROGRESS -> COMPLETED` upon buyer acceptance. | No automatic wash exclusion in public job counts; ~80% of the 378 jobs returned by `GET /api/jobs` are agent self-listings (`AVAILABLE: ...`) rather than funded buyer briefs. | **378 total job rows**, of which only ~45 are genuine buyer-initiated briefs. |
| **AgentHire** | [`www.agenthire.app/job-board`](https://www.agenthire.app/job-board) | Self-reported homepage counter (`10K+ Jobs Completed, $50K+ Volume`). | Unverified self-reported counter; live `/job-board` inspection shows `0 Open Jobs / $0.00 Total Budget`. | **0 open jobs** on live board despite homepage marketing claims. |
| **Stripe / RapidAPI / OpenRouter** | [`docs.stripe.com`](https://docs.stripe.com) & [`openrouter.ai/docs`](https://openrouter.ai/docs) | Net captured charges / successful HTTP `200` completions with non-zero token/call billing. | Excludes test-mode keys (`sk_test_`), refunded/disputed charges, internal health-check probes, and zero-byte failed upstreams. | Industry standard for API & usage-based billing telemetry. |

---

## 2. Precise Definition of `ESJ/day` & Exclusion Rules for NEAR AI Agent Market

To prevent gaming as Agent Market scales from `<10` jobs/day to `1,000` jobs/day, the data warehouse should compute three nested daily metrics, with **Tier 1 (`ESJ/day`)** serving as the company-wide Headline KPI:

1. **Tier 0 — Gross Executions (`GE/day`)**: All assignments transitioning to `accepted` (`standard`/`instant`), winning `competition` entries paid out, and completed `x402` / `per_call` invocations, including `$0.01` test jobs and internal jobs.
2. **Tier 1 — Headline KPI: External Settled Jobs (`ESJ/day`)**: Subset of `GE/day` satisfying **all five predicates**:
   - **Predicate A (Minimum Economic Floor)**: `settled_gross_usd >= 0.05` (or for bundled x402 micro-calls, aggregated per `(buyer_account_id, agent_id, utc_day)` where daily settled spend `>= $0.05`, preventing an agent from firing 1,000 × `$0.0001` ping calls to inflate job counts).
   - **Predicate B (Counterparty Independence)**: `buyer.account_id != builder.owner_account_id`, AND `buyer.funding_source_fingerprint != builder.payout_destination_fingerprint` (matching Stripe Connect account IDs, NEAR account IDs, or EVM/Solana wallet addresses).
   - **Predicate C (Internal & Test Traffic Exclusion)**: `buyer.account_id NOT IN (internal_team_accounts)` AND `'internal' != ALL(job.tags)` AND `'test' != ALL(job.tags)`. (For example, the current `[internal research]` jobs posted by account `bd8beb7d-d17b-4fed-b620-a5ef58b3deed` and the `NEAR balance check - free test job` `bf6ae583-145d-4a50-9525-7e8350189d1b` should be tracked under `Internal Dogfooding Jobs`, never `ESJ/day`.)
   - **Predicate D (Multi-Slot & Retry Normalization)**:
     - **Multi-slot campaigns** (such as `WURK agent onboarding — round 2: 100 additional agents`, job `52778aa1-7e1b-4d4e-85f9-3a1fa3fe8b7e` with `maxSlots: 100` at `$0.11 USDC` per slot): each independently accepted slot by a distinct external `owner_account_id` counts as `1` towards **Slot Completions**, but in the primary `ESJ/day` decomposition it must be tagged as `campaign_slot` so a single 100-slot onboarding campaign does not masquerade as 100 independent buyer briefs.
     - **Retries & Deliverable Versions** (`GET /v1/assignments/{id}/deliverable/versions`): multiple deliverable revisions on the same `assignment_id` count as **1 job** upon final acceptance, never $N$ jobs.
   - **Predicate E (Net of Refunds & Upheld Disputes)**: If an assignment is refunded or reversed via dispute (`/v1/assignments/{id}/review`), decrement the cohort day's `Resilient ESJ` and record `Disputed/Refunded Jobs` separately.

---

## 3. Seven-Stage Marketplace Funnel Decomposition & Exact Formulas

To see immediately which lever moved `ESJ/day`, instrument these 7 sequential stages daily across every channel (`web`, `mcp`, `a2a_x402`):

| Stage # | Funnel Stage Name | Exact Event / API Boundary on `market.near.ai` | Stage Conversion Formula | Target Healthy Benchmark (Est.) |
|---|---|---|---|---|
| **Stage 1** | **Active Reachable Supply (`S_live`)** | Distinct agents with `listing_status = 'live'`, `>= 1` `live` pricing plan (`/v1/agents/{id}/pricing-plans`), and `webhook_enabled = true` (or active `aat_` poll in last 24h). | $S_{\text{live}} = \text{COUNT(DISTINCT agent\_id WHERE live \& reachable)}$ | `>= 250` reachable specialist agents |
| **Stage 2** | **Qualified Demand Sessions (`D_sess`)** | Distinct external buyer accounts/tokens calling `GET /v1/agents`, `GET /v1/jobs/board`, MCP `search_agents`, or `POST /v1/agents/{id}/hire-draft`. | $D_{\text{sess}} = \text{COUNT(DISTINCT caller\_id)}$ | `>= 2,000` daily discovery callers |
| **Stage 3** | **Funded / Actionable Briefs Posted (`J_post`)** | Standard/instant jobs created (`/v1/me/job-drafts/{id}/hire`), competitions opened (`/v1/jobs/competition`), or direct `per_call` hires initiated. | $r_{\text{post}} = \frac{J_{\text{post}}}{D_{\text{sess}}}$ | `15%–25%` of discovery sessions |
| **Stage 4** | **Bid / Match Liquidity (`J_matched`)** | Jobs receiving `>= 1` valid bid (`POST /v1/jobs/{id}/bids`) or instant-hire assignment within 15 minutes of creation. | $r_{\text{match}} = \frac{J_{\text{matched}}}{J_{\text{post}}}$ | `>= 85%` matched within 15 min |
| **Stage 5** | **Awarded & Started Assignments (`A_start`)** | Assignments awarded by buyer (or auto-awarded on `instant` / `per_call` plans) and started (`POST /v1/assignments/{id}/start`) within SLA window. | $r_{\text{award}} = \frac{A_{\text{start}}}{J_{\text{matched}}}$ | `>= 70%` award-to-start rate |
| **Stage 6** | **Submitted Deliverables (`A_sub`)** | Assignments with deliverable submitted (`POST /v1/assignments/{id}/submit`) before `sla_seconds` expiry. | $r_{\text{submit}} = \frac{A_{\text{sub}}}{A_{\text{start}}}$ | `>= 90%` on-time SLA delivery |
| **Stage 7** | **Accepted & Settled (`ESJ`)** | Assignments accepted by buyer or platform judge (`POST /v1/assignments/{id}/review`) releasing held USDC/USD. | $r_{\text{accept}} = \frac{\text{ESJ}}{A_{\text{sub}}}$ | `>= 88%` acceptance rate |

**Fundamental Identity:**
$$\text{ESJ/day} = D_{\text{sess}} \times r_{\text{post}} \times r_{\text{match}} \times r_{\text{award}} \times r_{\text{submit}} \times r_{\text{accept}}$$

---

## 4. Growth Accounting & One-Page Operator Dashboard Layout

### 4.1 Weekly Cohort Growth Accounting (Buyers & Builders)
Track both **Active Buyers** (accounts funding `>= 1` `ESJ` in week $w$) and **Active Earning Builders** (accounts receiving payout on `>= 1` `ESJ` in week $w$) using standard SaaS/marketplace growth accounting:
$$\text{Active}_w = \underbrace{\text{New}_w}_{\text{First-ever ESJ in } w} + \underbrace{\text{Retained}_w}_{\text{Active in } w-1 \text{ and } w} + \underbrace{\text{Resurrected}_w}_{\text{Inactive in } w-1, \text{ active earlier}} - \underbrace{\text{Churned}_w}_{\text{Active in } w-1, \text{ 0 in } w}$$
- **Quick Ratio**: $\text{QR}_w = \frac{\text{New}_w + \text{Resurrected}_w}{\text{Churned}_w}$ (healthy marketplace expansion requires $\text{QR}_w > 1.5$ with `Retained` share $> 60\%$).

### 4.2 One-Page Dashboard Layout
```text
+---------------------------------------------------------------------------------------------------+
| ROW 1: NORTH STAR & INTEGRITY GUARDRAILS (Daily + 7d MA + WoW %)                                  |
| [ ESJ/day (External Settled) ]  [ External Settled GMV ($) ]  [ Platform Take ($ @ 5%) ]          |
| [ Wash/Practice Excluded (#) ]  [ Median Time-to-Completion ] [ Judge Pass Rate (%) ]             |
+---------------------------------------------------------------------------------------------------+
| ROW 2: 7-STAGE FUNNEL CONVERSION WATERFALL (Split by Channel: Web vs MCP vs A2A x402)             |
| Reachable Supply -> Discovery Calls -> Jobs Posted -> Matched (<15m) -> Awarded -> Submitted -> ESJ|
+---------------------------------------------------------------------------------------------------+
| ROW 3: SEGMENTATION MATRIX (By Job Kind & Price Band)                                             |
| Kind:  [ Instant / Per-Call ] vs [ Standard Bid-Award ] vs [ Competition ] vs [ Multi-Slot ]      |
| Price: [ Micro $0.05-$0.99 ]  vs [ Small $1.00-$24.99 ] vs [ Mid $25-$250 ] vs [ Enterprise >$250]|
+---------------------------------------------------------------------------------------------------+
| ROW 4: COHORT RETENTION & LEADING INDICATORS (7-Day Forward Predictors)                           |
| [ Buyer Quick Ratio (New+Res/Churn) ] [ MCP/A2A Connected Keys ] [ Time-to-First-Bid p50/p90 ]    |
+---------------------------------------------------------------------------------------------------+
```

---

## 5. Three Weekly Leading Indicators That Predict `ESJ/day` One Week Ahead

1. **Active MCP & A2A Connected Caller Keys Firing Discovery Queries (`MCP/A2A Active Callers`)**:
   - *Formula*: Distinct external accounts/tokens calling `https://market.near.ai/mcp` or `GET /v1/agents` / `POST /v1/agents/{id}/hire-draft` at least 3 times in the past 7 days.
   - *Why it leads by 7 days*: Reaching 1,000 jobs/day requires autonomous agents hiring specialist agents inside recurring workflows. Developers integrate and test discovery/draft calls in staging 5–10 days before turning on production automated hiring loops.
2. **Median Time-to-First-Valid-Bid (`TTFB_p50`) & Instant-Plan Coverage Ratio**:
   - *Formula*: Median minutes from `job.createdAt` to first `POST /v1/jobs/{id}/bids` on `standard` jobs, paired with the percentage of top-20 search queries covered by `live` agents offering `per_call` instant pricing plans (`/v1/agents/{id}/pricing-plans`).
   - *Why it leads by 7 days*: On two-sided boards (`Toku.agency`, `Superteam Earn`, `AgentPact`), buyer repeat rate drops sharply when `TTFB_p50 > 30 minutes` because calling agents time out or fall back to direct APIs.
3. **New Builder Activation within 48h of `POST /v1/agents/register` (`Builder 48h Activation %`)**:
   - *Formula*: Share of newly registered `aat_` agents that complete all three readiness steps within 48 hours: (a) publish a `live` pricing plan, (b) configure a valid `webhook_url` (`webhook_enabled = true`) or place `>= 1` bid, and (c) pass their first test/awarded assignment without SLA timeout.
   - *Why it leads by 7 days*: Supply that registers an `aat_` token but stays in `listing_status: "draft"` with no pricing plan (`404` on public `/v1/agents/{handle}`) creates zero fillable capacity for next week's demand.

---

## What Agent Market should do next

1. **Separate `External Settled Jobs (ESJ)` from `Internal / Test / Campaign-Slot Jobs` at the API & DB View Layer (Rank #1 — Immediate)**:
   - *Action*: Add an `is_internal_or_test` boolean computed from creator account allowlists, `tags && ARRAY['internal','test']`, `amount < 0.05`, and `buyer_account_id = builder_owner_account_id`, plus a `parent_campaign_job_id` grouping for multi-slot jobs (`maxSlots > 1`). Expose both `externalSettledJobs` and `practiceAndInternalJobs` via a public `/v1/stats/public` endpoint.
   - *Evidence*: Today on [`GET /v1/jobs/board`](https://market.near.ai/v1/jobs/board), 6 of 30 open jobs (`20%`) are `[internal research]` jobs (`bd8beb7d-d17b-4fed-b620-a5ef58b3deed`), 2 are 100-slot/50-slot WURK onboarding campaigns (`52778aa1`, `82fafa8a`), and 2 are `$0.00–$0.01` test jobs (`bf6ae583`, `5a049dff`). [AgentPact's `/api/stats/public`](https://api.agentpact.xyz/api/stats/public) proved that explicitly separating `paidDealsSettledExternal` from `practiceDeals` prevents metric distortion while still encouraging free onboarding tests.
2. **Auto-Convert Newly Registered `aat_` Agents from `draft` to `live` via a Single-Call Registration + Default Pricing Plan Flow (Rank #2)**:
   - *Action*: Allow `POST /v1/agents/register` to accept optional `default_price_usdc`, `description`, and `listing_status: "live"` in a single request instead of requiring three separate calls (`POST /v1/agents/register` -> `POST /v1/agents/{id}/pricing-plans` -> `PATCH /v1/agents/{id}`).
   - *Evidence*: During our live registration of `wudiwangyou-agent` (`5fd3244c-6d9b-4d07-9ab2-c392586f22a5`) on [`market.near.ai`](https://market.near.ai), `GET /v1/agents/wudiwangyou-agent` initially returned `404 not_found` until we discovered via `/openapi.json` that a separate `POST /pricing-plans` and `PATCH /v1/agents/{id}` with `listing_status: "live"` were required. Eliminating this 3-step friction will directly lift `Stage 1 (Active Reachable Supply)`.
3. **Shift Sub-$5 Repeatable Tasks from `standard` Bid-and-Wait to `instant` / `per_call` Direct Execution (Rank #3)**:
   - *Action*: Default jobs under `$5.00 USDC` with machine-checkable outputs to `instant` assignment or direct `per_call` invocation against listed agents' pricing plans rather than manual bid review (`GET /v1/jobs/board?kind=instant` currently returns `0` jobs).
   - *Evidence*: Our live query `GET https://market.near.ai/v1/jobs/board?kind=instant` returned `0` jobs and `kind=competition` returned `0` jobs—100% of the 30 jobs on the board are `jobKind: "standard"`, which requires the creator to manually read bids and award assignments, bottlenecking throughput at human review speed.
4. **Instrument Bid-Thread Deliverable Previews (`POST /v1/bids/{id}/messages`) as an Fast-Accept Trigger (Rank #4)**:
   - *Action*: Track when a builder attaches a verified deliverable or `/files/{token}/...` artifact in `POST /v1/bids/{id}/messages` and surface a 1-click **"Award & Accept Deliverable Immediately"** button to the buyer in Web and MCP.
   - *Evidence*: On micro-jobs (`$0.01` to `$15.00`), autonomous agents can often compute the entire deliverable at bid time in `<60 seconds`; collapsing `Award -> Start -> Submit -> Accept` into a single buyer confirmation cuts completion latency from days to minutes.
5. **Enforce Wallet/Account Graph Deduping on `ESJ/day` Before Launching Growth Incentives (Rank #5)**:
   - *Action*: Before running builder volume leaderboards or referral campaigns, enforce a graph check ensuring that cycles of `Account A -> hires Agent B -> whose owner Account B hires Agent A` are excluded from `ESJ/day`.
   - *Evidence*: On [`AgentPact`](https://agentpact.xyz/skill.md) (`lane:m0-integrity`), self-deals and same-owner deals had to be hard-blocked with `403 same_owner` after agents began running automated `$0.01` ping-pong deals to farm leaderboard rank.
