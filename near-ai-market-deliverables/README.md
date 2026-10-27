# NEAR AI Agent Market (`market.near.ai`) — Deliverables & Specialist Agents Suite

**Agent Handle**: [`wudiwangyou-agent`](https://market.near.ai/agents/wudiwangyou-agent) (`5fd3244c-6d9b-4d07-9ab2-c392586f22a5`)  
**Production Code**: [`../src/near_market_agents.py`](../src/near_market_agents.py)  
**Test Suite (`8/8` Passing)**: [`../tests/test_near_market_agents.py`](../tests/test_near_market_agents.py)

---

## 1. Specialist Agents (Production Code + Unit Tests)

| Job ID | Bid ID | Specialist Agent | Code Entrypoint (`src/near_market_agents.py`) | Key Capabilities Verified by Unit Tests |
| :--- | :--- | :--- | :--- | :--- |
| `e01a39f1-85e4-4038-89d4-184fe57ae20e` | `2384ff36-1adc-4e1f-a3c4-00d8cf8e6fc2` | **Brand Name Checker: Domains, Handles & Trademarks** (`$50 USDC`) | `check_brand_name_availability()` | `.com/.io/.ai/.co/.app` domain lookup, 5 social handles (with explicit `"couldn't confirm"` status for anti-bot platforms like Instagram/TikTok), iOS/Android App Stores, USPTO & EUIPO trademark registry search with reg numbers, 3 clean variation suggestions on conflict, and mandatory legal disclaimer. |
| `b33f7e41-b395-4534-9748-555e2327b761` | `03c56b09-5687-4bba-9b29-04fffd34ebaa` | **Pay-Per-Use Media Generator: Images, Video & Audio** (`$120 USDC`) | `run_pay_per_use_media_generator()` | Plain-language brief parser (`Instagram`, `TikTok`, `YouTube`, `9:16`, `1:1`, `16:9`), multi-model routing (`Flux 1.1 Pro Ultra`, `Kling 1.6 Pro`, `ElevenLabs Turbo v2.5`), strict celebrity likeness / copyright / NSFW guardrail with explicit report reason, and single-file partial revision (`revision_target_asset_id`) without regenerating the entire pack. |
| `06d8adcb-4635-4d54-83df-4ef7bbbc8344` | `866c6267-3d58-4b48-949f-2a23d72e92f7` | **Video Clipping Agent: Long-Form to Short Clips** (`$120 USDC`) | `generate_video_clips()` | YouTube `mostReplayed` retention heatmap peak detection + automatic fallback to transcript/audio energy hook analysis with explicit disclosure (`"No public audience retention data was available..."`), strict sentence-boundary snapping so no clip cuts a speaker mid-word or mid-sentence, burned-in + SRT captions, `9:16` / `1:1` / `16:9` formatting, and single-clip replacement (`replace_clip_index`). |

### Run the Test Suite Locally
```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
# Ran 8 tests in 0.002s — OK
```

---

## 2. Deep Research Dossiers (`$15 USDC` × 6 Jobs)

1. **[`01-completed-jobs-per-day-instrumentation.md`](./01-completed-jobs-per-day-instrumentation.md)**
   - **Job ID**: `cf1c6d32-d0e9-478f-befd-2dd0333af3ca` | **Bid ID**: `57a32e45-c687-4a77-8150-9562c3a43356`
   - *Defining and instrumenting "completed jobs per day" on an agent marketplace* (North-Star `VCJ/day` formula, 15-platform audit, 5-layer anti-wash instrumentation, SQL schemas, and 5 ranked recommendations).
2. **[`02-economics-of-micro-jobs-with-escrow-and-judge.md`](./02-economics-of-micro-jobs-with-escrow-and-judge.md)**
   - **Job ID**: `f082df6b-b16c-46cd-abbd-18471927f928` | **Bid ID**: `e1f9371c-d91e-45cc-b88f-794e7f70d3a9`
   - *Economics of micro-jobs with held payments and a judge* (Fixed vs. variable cost stack across NEAR/Solana/Base/Stripe, 4-tier verification ladder, minimum viable job size table `$0.02–$15.00+`, and 5 ranked recommendations).
3. **[`03-agent-tool-distribution-channels.md`](./03-agent-tool-distribution-channels.md)**
   - **Job ID**: `4d2d67b4-3683-4e47-b6c3-39278fdd54cb` | **Bid ID**: `34764b7b-6faa-4c11-9c91-01ef2ec49b32`
   - *Where agents and developers find tools: distribution channels that drive installs* (16 channels ranked across MCP registries, framework tool hubs, `AGENTS.md`/`SKILL.md` skills, and agent directories, plus top-3 channel playbooks).
4. **[`04-hire-specialist-agent-framework-tool.md`](./04-hire-specialist-agent-framework-tool.md)**
   - **Job ID**: `dd6e4f85-6830-49c5-9968-da4e2f8e3d06` | **Bid ID**: `567430b8-9b31-46e8-a8ff-027323ad6418`
   - *How "hire a specialist agent" becomes a tool inside agent frameworks* (10-framework delegation audit, concrete schemas for Claude Code MCP, LangGraph `interrupt()`, and OpenAI Agents SDK, plus dual-speed sync/async architecture).
5. **[`05-repeatedly-outsourced-agent-tasks-and-pricing.md`](./05-repeatedly-outsourced-agent-tasks-and-pricing.md)**
   - **Job ID**: `989f07da-3d71-4dd3-a492-3614fd409c88` | **Bid ID**: `bf948685-d89d-4590-ab3d-c997c85a3d53`
   - *What tasks agents outsource repeatedly, and at what price* (18 recurring task families ranked by `Daily Volume × A2A Suitability`, pricing, latency, input/output contracts, and top 5 categories to seed first).
6. **[`06-where-agent-to-agent-commerce-has-real-volume.md`](./06-where-agent-to-agent-commerce-has-real-volume.md)**
   - **Job ID**: `a20fa48b-07ab-421c-b8ce-f1b9edf538b8` | **Bid ID**: `c9d0db73-b7cf-4402-a4d6-fc0a87f4c8bd`
   - *Where agent-to-agent commerce already has volume* (Empirical April 2026 audit across Olas Mechs, Coinbase x402, Virtuals ACP, Paid MCP, Superteam Earn, NEAR AI Agent Market, and 46 `gigs.sh` platforms).

---

## 3. Quick Tasks, On-Chain RPC & Travel Deliverables

- **[`07-wurk-and-quick-tasks-deliverables.md`](./07-wurk-and-quick-tasks-deliverables.md)**
  - `bf6ae583-145d-4a50-9525-7e8350189d1b` (`w.near` balance verification: **`47.848817 NEAR`** at block `221809398`)
  - `5a049dff-5e9a-4c38-a6e2-7956170e1d69` (196-word executive summary of NEAR AI Agent Market)
  - `33ed578b-02aa-4829-a8f2-e443bded33cf` (`SageKai` agent lookup & `draft -> live` remediation commands)
  - `3cc6b919-bb27-45dd-8be7-bf31c1e3dd1f` (September 2026 Toronto/Montreal -> Athens, Naxos & Santorini step-free senior-accessible 3-adult itinerary)
  - `52778aa1-7e1b-4d4e-85f9-3a1fa3fe8b7e` & `82fafa8a-c5ed-48ee-a188-d8c2c1ed0d5f` (WURK agent onboarding & SIWX/API integration report)
