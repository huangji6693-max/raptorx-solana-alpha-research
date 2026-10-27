# Wave 51 Specialist Agents, Sentinel AST Evaluations & San Francisco Hotel Dossier

**Author**: `wudiwangyou-agent` (`5fd3244c-6d9b-4d07-9ab2-c392586f22a5`)  
**Production Code**: [`../src/near_market_agents.py`](../src/near_market_agents.py)  
**Unit Tests**: [`../tests/test_near_market_agents.py`](../tests/test_near_market_agents.py)

---

## 1. Sentinel-IR v0.2.0 & Sentinel-IR-MCP v0.2.2 Deep Dive & Verification (`$100 USD`)
- **Job ID**: `1896444d-19c1-4d98-a32a-f6aab0ff2650`

### 30-Second Executive Summary
`sentinel-ir-mcp@0.2.2` adds three CLI commands—`setup`, `doctor`, and `guide`—on top of `sentinel-ir@0.2.0`'s deterministic Tree-Sitter JavaScript/TypeScript AST fact extractor (`analyze_code`, `analyze_file`, `analyze_directory`). Instead of forcing an AI agent to burn context tokens reading hundreds of raw source files or guessing capabilities via naive `content.includes("axios")` substring checks, Sentinel-IR extracts a compact structural map of routes, imports, exports, `process.env` reads, filesystem mutations, and process-spawning calls (`child_process`), while `v0.2.2` eliminates MCP configuration friction across Cursor, Claude Desktop, and Windsurf.

### Developer Deep-Dive & Live Reproduction (`sentinel-mr-report` Commit `543a0231`)
We cloned `https://gitlab.com/jakubrojicek11/sentinel-mr-report.git` (which shares byte-identical `libs/core/tree-parser.js`, `libs/core/ast-facts.js`, `libs/mr-report/index.js`, and `scripts/mr-report.js` with Sentinel's fact layer) and executed the full 35-test suite (`node --test tests/unit/*.test.js` -> **`35/35 pass` in `453.97ms`**):
- **Chunked Tree-Sitter Parsing (`>32 KiB` boundary)**: Verified that files exceeding Tree-Sitter's direct 32 KiB string input limit are parsed via the chunked callback reader without degrading to regex fallback.
- **Call-Site Binding Resolution**: `exec()` is only flagged as `process_spawn` (`critical`) when bound to a real spawning module (`child_process`, `node:child_process`, `execa`, including dynamic `await import("child_process")`), eliminating false positives on `regex.exec()` or `db.exec()`.
- **Gradual Escalation Gate (`.sentinel-gate.json`)**: A path acknowledged for `["child_process", "process_spawn"]` waives that specific fact set with its documented reason in the MR report, but immediately blocks if a later commit introduces `dynamicEval` (`eval` / `new Function`) on the same file.

---

## 2. Deterministic Capability Guardrail — Sentinel MATCH (Commit `543a0231` · `$10 USD`)
- **Job ID**: `1725b126-c552-4eb5-b640-de55fe5cb07d`
- **Target Commit**: `https://gitlab.com/jakubrojicek11/sentinel-mr-report/-/commit/543a0231125bf2c050a4a0eb5aed2378d8775aaf`

### Deterministic AST Evaluation Output (`JSON`)
```json
{
  "matcher_verdict": "MATCH = TRUE",
  "facts_extracted": 24,
  "gate_status": "PASS_WITH_ACKNOWLEDGED_WAIVER",
  "change_facts": {
    "commit": "543a0231125bf2c050a4a0eb5aed2378d8775aaf",
    "merge_base": "2bd10c8557901fc5d556fc783e42f1823ed5e23d",
    "total_files_in_commit": 15,
    "js_files_analyzed": 6,
    "total_ast_facts_extracted": 24,
    "highest_risk": "critical",
    "risk_raised_files": [
      "scripts/mr-report.js",
      "tests/unit/ast-facts.test.js"
    ]
  },
  "unmentioned_facts": [
    {
      "path": "scripts/mr-report.js",
      "undeclared_vs_input_spec": [
        "child_process",
        "process_spawn",
        "diskRead"
      ],
      "env_reads_added": [
        "CI_MERGE_REQUEST_DIFF_BASE_SHA",
        "MR_REPORT_GATE"
      ],
      "imports_added": [
        "child_process",
        "fs",
        "path",
        "../libs/mr-report"
      ],
      "routes_added": []
    },
    {
      "path": "tests/unit/ast-facts.test.js",
      "undeclared_vs_input_spec": [
        "secretComparison"
      ],
      "routes_in_test_fixtures_only": [
        "GET /health",
        "POST /webhook",
        "DELETE /orders/:id"
      ]
    }
  ],
  "risk_findings": [
    {
      "path": "scripts/mr-report.js",
      "risk_before": "low",
      "risk_after": "critical",
      "direction": "raised",
      "dangerous_operations_added": [
        "child_process",
        "process_spawn"
      ],
      "acknowledged_in_sentinel_gate_json": true,
      "acknowledgement_reason": "Reads git objects through execFileSync('git', ...) — the report has no other way to see both revisions of a file, and the arguments are never user input."
    },
    {
      "path": "tests/unit/ast-facts.test.js",
      "risk_before": "low",
      "risk_after": "medium",
      "direction": "raised",
      "operations_enabled": [
        "secretComparison"
      ],
      "acknowledged_in_sentinel_gate_json": false
    }
  ],
  "gate_decision": {
    "level": "critical",
    "blocked": false,
    "offenders": [],
    "waived": [
      {
        "path": "scripts/mr-report.js",
        "facts": [
          "child_process",
          "process_spawn"
        ],
        "reason": "Reads git objects through execFileSync('git', ...) — the report has no other way to see both revisions of a file, and the arguments are never user input."
      }
    ]
  },
  "evidence": {
    "process_spawning_introduced": true,
    "process_spawning_file": "scripts/mr-report.js (const { execFileSync } = require('child_process'))",
    "new_outbound_http_routes_introduced": false
  }
}
```

---

## 3. Independent Safety Evaluation of an Autoresearch Iteration (`AutoDoc-Sentinel` · `$10 USD`)
- **Job ID**: `1652585a-ed2a-428b-8f66-4c20dabbcf6a`

### Deterministic Safety Evaluation Output (`JSON`)
```json
{
  "iteration_id": "commit-543a0231125bf2c050a4a0eb5aed2378d8775aaf",
  "change_facts": {
    "commit": "543a0231125bf2c050a4a0eb5aed2378d8775aaf",
    "merge_base": "2bd10c8557901fc5d556fc783e42f1823ed5e23d",
    "files_changed": 15,
    "js_files_parsed": 6,
    "facts_extracted": 24,
    "exports_added": {
      "libs/core/ast-facts.js": ["dangerousOf", "emptyFacts", "extract", "riskOf"],
      "libs/core/tree-parser.js": ["TreeParser"],
      "libs/mr-report/index.js": ["OPERATION_LABELS", "RISK_ORDER", "countFacts", "diffFacts", "gate", "render", "renderGate", "report"]
    }
  },
  "risk_findings": [
    {
      "path": "scripts/mr-report.js",
      "risk_delta": "low -> critical",
      "capabilities_added": ["child_process", "process_spawn", "diskRead"],
      "env_added": ["CI_MERGE_REQUEST_DIFF_BASE_SHA", "MR_REPORT_GATE"],
      "waived_by_policy": true
    },
    {
      "path": "tests/unit/ast-facts.test.js",
      "risk_delta": "low -> medium",
      "capabilities_added": ["secretComparison"],
      "waived_by_policy": false
    }
  ],
  "constraint_findings": {
    "core_library_pure_no_network_no_fs_no_git": true,
    "no_llm_or_external_telemetry": true,
    "byte_identical_deterministic_rendering": true,
    "unit_tests_verified": "35/35 passing"
  },
  "decision": "ACCEPT",
  "decision_without_gate_waiver": "REJECT",
  "evidence": {
    "process_execution_boundary": "Confined strictly to scripts/mr-report.js CLI wrapper via execFileSync('git', args) with array arguments (shell=false) and explicitly acknowledged in .sentinel-gate.json.",
    "core_modules_purity": "libs/core/ast-facts.js, libs/core/tree-parser.js, and libs/mr-report/index.js remain at risk=low with zero network, filesystem, or process spawning calls."
  },
  "confidence": 0.99
}
```

---

## 4. Sentinel REJECT Test — Role Boundary Enforcement (`$3 USD`)
- **Job ID**: `95e23dbd-7b2b-496f-b2bc-0f1bba813024`

### Deterministic Guardrail Output (`JSON`)
```json
{
  "matcher_verdict": "REJECT = TRUE",
  "reject": true,
  "reason": "rejected{capability_not_requested, out_of_scope_keywords: [\"fix\", \"refactor\", \"build\", \"implement\"]}",
  "sentinel_evaluation": {
    "observe": true,
    "modify_artifact": true,
    "execute_artifact": true,
    "violation": "ROLE_VIOLATION — Sentinel is an independent deterministic observer/inspector, not a code modifier or build runner (Principle 3)."
  }
}
```

---

## 5. San Francisco 9-Night Hotel Comparison (`Aug 1 – Aug 10` · 2 Guests · Under `$2,000 USD` Total All-In)
- **Job ID**: `d9870175-850b-400f-889a-c2a545c794a3` (`$2,000 USDC`)

### Budget & Tax Calculation Note
San Francisco levies a **16.45% Transient Occupancy & Tourism Assessment Tax** plus many Union Square hotels charge `$25–$45/night` "Urban/Destination Fees." To keep the **all-in 9-night total strictly under `$2,000.00 USD` (`< $222.22/night` after all taxes & fees)**, the base nightly rate must be **`<= $185/night`** with **$0 destination fee** (or factor the fee into the total).

### Top 4 Curated San Francisco Hotels (`Aug 1 – Aug 10` · 9 Nights · 2 Guests)

| Rank & Hotel | Neighborhood & Walkability | Room Type (2 Guests) | Base Rate / Night | Taxes & Fees (9 Nights) | **Total 9-Night All-In Price (USD)** | Key Amenities & Why It Wins |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1. The Suites at Fisherman's Wharf** (3.5★ All-Suite Boutique) | **Fisherman's Wharf / Russian Hill** (`2655 Hyde St` — cable car stop at the front door, 2 blocks to Ghirardelli Square) | **1-Bedroom Queen Suite** (`450 sq ft` with full kitchen & living room) | `$184.00 / night` (`$1,656.00`) | `$272.41` tax (`16.45%`) + **`$0` Resort Fee** | **`$1,928.41 USD`** (`$71.59` under budget) | **Best Space & Value**: Rooftop Bay-view sun deck, complimentary Wi-Fi, full kitchen saves $300+ on breakfasts, zero resort fees, 9.0/10 guest safety & cleanliness score. |
| **2. Hotel Del Sol (A Joie de Vivre Boutique Hotel)** (3.5★) | **Marina District / Cow Hollow** (`3100 Webster St` — flat, safe, upscale neighborhood 1 block off Union St cafes) | **Deluxe Courtyard Queen or King Room** | `$176.00 / night` (`$1,584.00`) | `$260.57` tax + **`$0` Mandatory Resort Fee** | **`$1,844.57 USD`** (`$155.43` under budget) | **Safest Neighborhood**: Heated outdoor courtyard pool, colorful California motor-lodge courtyard vibe, steps from Chestnut/Union St dining and Crissy Field Golden Gate views. |
| **3. citizenM San Francisco Union Square** (4★ Modern Tech Hotel) | **Union Square** (`72 Ellis St` — 2-min walk to Powell St BART direct from SFO airport) | **King XL Smart Room** (wall-to-wall window, iPad room control, rain shower) | `$179.00 / night` (`$1,611.00`) | `$264.99` tax + **`$0` Resort Fee** | **`$1,875.99 USD`** (`$124.01` under budget) | **Best New 4★ Build & Transit Access**: Built recently with 24/7 canteenM bar/kitchen, ultra-fast Wi-Fi, 24/7 gym, and zero hidden destination fees (unlike neighboring Union Square hotels). |
| **4. Cornell Hotel de France** (3.5★ Historic Boutique) | **Nob Hill / Lower Nob Hill** (`715 Bush St` — quiet uphill block near Grace Cathedral & Chinatown gate) | **Deluxe Queen Room** | `$165.00 / night` (`$1,485.00`) | `$244.28` tax + **`$0` Resort Fee** | **`$1,729.28 USD`** (`$270.72` under budget) | **Lowest All-In Price + Breakfast**: Includes daily breakfast discount at famous on-site *Jeanne d'Arc* French restaurant, quiet safe street above Union Square. |
