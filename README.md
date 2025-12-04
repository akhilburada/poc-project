# Provider Data Reconciliation & Recommendation Agent

> **Mission:** Deliver an explainable, auditable, three-layer system for HCSC that reconciles provider data between SIMPLYR (PDM) and the LAKE domain, enriches the discovered gaps with AI-assisted intelligence, and exposes the full context as a business-ready experience.

---

## Table of Contents
1. [Executive Context](#executive-context)
2. [Target Outcomes](#target-outcomes)
3. [Stakeholders & Responsibilities](#stakeholders--responsibilities)
4. [Operating Principles](#operating-principles)
5. [Architecture Overview](#architecture-overview)
6. [Data Contracts & Schemas](#data-contracts--schemas)
7. [Layer 1 – Reconciliation Pipeline](#layer-1--reconciliation-pipeline)
8. [Layer 2 – Intelligence / Agent Workflow](#layer-2--intelligence--agent-workflow)
9. [Layer 3 – Business Consumption & Visualization](#layer-3--business-consumption--visualization)
10. [Demo Blueprint & Collateral](#demo-blueprint--collateral)
11. [Delivery Timeline](#delivery-timeline)
12. [Success Metrics & Acceptance Criteria](#success-metrics--acceptance-criteria)
13. [Risks & Mitigations](#risks--mitigations)
14. [Roadmap Beyond Demo](#roadmap-beyond-demo)
15. [Glossary](#glossary)
16. [Call to Action](#call-to-action)

---

## Executive Context
- **Client Pain:** SIMPLYR (upstream provider master) and the LAKE domain (downstream analytics) routinely drift. Teams must manually cross-check ~120 attributes per provider (credentials, contracts, addresses, custom flags) to determine what is wrong and who should fix it.
- **Expectation:** In a 30‑minute remote session, show a deterministic reconciliation backbone, an agent that speaks Credentialing/Network Ops/Provider Directory/Claims language, and a business-friendly visualization layer with drill-through, exports, and recommendations.
- **Constraint:** Limited build runway before the second week of December. No time for full orchestration, so we simulate the agent experience via a high-fidelity UI mock. Recon data remains real and auditable.

**Mantra:**
1. **Recon first:** Produce trustworthy gap facts before any LLM touches the data.
2. **Agentic insight:** Transform gaps into domain-specific recommendations with traceable rationale.
3. **Business consumption:** Present enriched gaps through Power BI + interactive UI so stakeholders never have to parse raw CSVs.

---

## Target Outcomes
| Outcome | Definition of "Good" | Demo Evidence |
| --- | --- | --- |
| Deterministic Reconciliation | Every provider/field mismatch recorded with batch metadata, KPIs, and reproducible logic. | `recon_table.csv`, lineage diagram, QC metrics slide. |
| Explainable Intelligence | Each gap annotated with domain, owner, severity, recommendation, rationale, and agent version. | UI mock reasoning panel, override workflow, audit trail. |
| Business Storytelling | Users can slice by domain/severity/state, drill into provider detail, and export evidence. | Power BI mock wired to enriched recon sample. |
| Demo Reliability | 30‑minute walkthrough with no blockers, plus fallback assets. | Dry-run recording, backup screenshots, contingency plan. |

---

## Stakeholders & Responsibilities
| Workstream | Primary Owner | Support | Deliverables |
| --- | --- | --- | --- |
| Data prep & recon schema | **Venu** | Core Data Engineering | SIMPLYR & LAKE sample files, recon config, QC stats, ingestion scripts. |
| Agent prompts & UI mock | **Zuber** | Design Studio, GenAI CoE | Clickable UI prototype, prompt templates, reasoning narratives, override logging. |
| Visualization (Power BI) | **Venu** (dataset) / BI partner | TBD | Dashboard pages, dataset refresh, detail drill-through, export templates. |
| Engagement & messaging | **Sandeep** | Venu | Client scheduling, script alignment, follow-up notes, risk tracking. |
| QA & rehearsal | All | — | Dry-run checklist, timing notes, demo playbook, Q&A cheat sheet. |

---

## Operating Principles
1. **Determinism before AI:** LLM-based explanations never mask foundational data quality issues.
2. **Separation of concerns:** Recon pipeline, agent enrichment, and visualization communicate through explicit contracts (tables, schemas, metadata).
3. **Explainability:** Each recommendation ties back to underlying facts, prompt IDs, and agent versions for auditing.
4. **Feedback loops:** Reviewer overrides feed future prompt tuning and deterministic heuristics.
5. **Demo honesty:** Clearly state which parts are mocked vs production-ready, and outline path to automation.

---

## Architecture Overview
```
SIMPLYR (PDM) ─┐
                ├─► Spark/Python Reconciliation Job ─► recon_table (core facts)
LAKE (Analytics) ┘                                  │
                                                    ▼
                                   Agent Enrichment Service (rules + LLM)
                                                    │
                                                    ▼
                             Power BI + Interactive UI + Future Workflow Hooks
```
- **Layer isolation:** Recon job populates gap facts; agent reads/writes enrichment fields; visualization only consumes enriched table.
- **Auditability:** Each layer stamps `ingestion_batch_id`, timestamps, prompt IDs, and agent versions.
- **Extensibility:** Same contract can eventually feed workflow systems or provider chatbots.

---

## Data Contracts & Schemas
| Asset | Source | Contents | Cadence | Notes |
| --- | --- | --- | --- | --- |
| `simplyr_data` | SIMPLYR/PDM | Provider demographics, contract & credentialing data, locations, custom attributes, IDs, geo. | Weekly (demo) | Treated as upstream truth. |
| `data_late.csv` | LAKE | Mirror schema; represents downstream or lagged view. | Weekly | Highlights drift due to lag/transformations. |
| `recon_table.csv` | Recon job | Field-level gaps + enrichment placeholders + audit metadata. | Per batch | CSV for demo; Delta table later. |

### Recon Table Columns (Baseline & Enrichment)
- **Keys:** `provider_id`, `field`, `ingestion_batch_id`, `source_system`, `last_update_ts`.
- **Fact Columns:** `simplyr_value`, `lake_value`, `gap_type` (Mismatch, Missing, Stale, Format), `confidence`.
- **Enrichment Columns:** `domain_group`, `owner_group`, `severity_score (1–5)`, `priority_bucket (P0–P2)`, `root_cause`, `recommendation`, `next_steps`, `suggested_workflow`, `agent_version`, `prompt_id`, `recommendation_status (Pending/Accepted/Overridden)`, `reviewer_notes`.

---

## Layer 1 – Reconciliation Pipeline
1. **Ingest:** Pull SIMPLYR & LAKE files (SFTP/blob). Stamp `ingestion_batch_id`, row counts, checksums.
2. **Normalize:** Trim strings, standardize casing, align date formats, map enumerations, normalize addresses, apply rounding tolerance for lat/long.
3. **Match Providers:** Join on `provider_id`; fallback composite key (NPI + TIN + name) with deterministic precedence. Log unmatched rows.
4. **Field Comparison:** Evaluate ~120 attributes. Emit recon row when values differ, when one side is null, or when freshness thresholds violated (e.g., `contract_end_date` earlier upstream).
5. **Quality Controls:**
   - Provider coverage (% matched vs total per source).
   - Field coverage (# fields compared, # gaps per field).
   - Spike detection vs prior batch; flag if >X% increase in critical fields.
6. **Persist & Audit:** Write to `recon_table.csv`, capture summary metrics JSON for dashboards, retain logs for reproduction.

**Layer‑1 KPIs**
- `% providers matched` (target >95% in curated demo dataset).
- `# gaps` per critical attribute (credentialing_status, contract_status, addresses, custom flags).
- `Runtime` (<5 minutes on sample) to highlight efficiency.

---

## Layer 2 – Intelligence / Agent Workflow
**Goal:** Convert raw gaps into prioritized, explainable actions.

### Inputs
- Recon rows with `recommendation_status = Pending`.
- Provider context (status, specialty, plan participation, credentialing recency, languages, network tier, geography).
- Mapping tables: `field → domain_group`, default severity, owner groups.
- Historical overrides for suppression/learning.

### Processing Steps
1. **Selection:** Fetch latest-batch recon rows needing enrichment.
2. **Context Build:** Construct JSON payload with raw facts + provider metadata + heuristics.
3. **Reasoning Engine:**
   - Deterministic heuristics (e.g., credentialing mismatch + recent verification ⇒ high severity, Credentialing domain).
   - LLM prompt to craft narrative explanation, root cause hypothesis, and next steps; log `prompt_id`, `agent_version`, raw prompt and response.
4. **Ownership & Workflow:** Map to owner queues (e.g., `Credentialing Ops Squad A`, `Network Ops West`). Suggest workflow path (ServiceNow ticket, automated reload, manual outreach).
5. **Write-Back:** Update recon table enrichment columns, set `recommendation_status = Pending Review`.
6. **Feedback Loop:** UI mock lets reviewers accept/escalate/override; capture overrides for future prompt tuning and heuristic refinement.

**Layer‑2 KPIs**
- `% gaps enriched` (target 100% of demo rows).
- Distribution across domain groups & severity buckets.
- Mock override rate (illustrates feedback controls).

---

## Layer 3 – Business Consumption & Visualization
### Dataset
- Power BI dataset ingesting enriched recon table (static CSV for demo; Delta/DirectQuery future).
- Supports filters for batch, severity, domain, owner, geography, plan, status.

### Dashboard Composition
1. **Overview KPIs:** Total gaps, P0 gaps, batches awaiting review, acceptance rate.
2. **Domain Stack Chart:** Credentialing vs Network Ops vs Provider Directory vs Claims.
3. **Severity Donut:** P0/P1/P2 share.
4. **Trend Line:** Gaps per batch to illustrate stabilization.
5. **Interactive Table:** Columns `Provider ID`, `Domain`, `Field`, `Gap Type`, `Severity`, `Owner`, `Status`. Sorting, filtering, pagination, export.
6. **Detail Pane:** Side-by-side SIMPLYR vs LAKE values, agent narrative, next steps checklist, toggles for acceptance/escalation, `Download Evidence` button.
7. **Filters:** Domain, owner group, severity, state, ingestion batch, plan type, provider status.

### Future Enhancements
- Trigger ServiceNow/JIRA workflow when recommendation accepted.
- Embed provider chatbot that references enriched recon data for inquiries.
- Add SLA dashboards (time to resolve, recurrence rate).

---

## Demo Blueprint & Collateral
| Segment | Time | Content |
| --- | --- | --- |
| Scene Setting | 5 min | Pain recap, 3-layer diagram, determinism vs agentic roles. |
| Visualization Walkthrough | 10 min | Power BI mock: filters, drill-through, exports, severity heatmap. |
| Agent Experience | 10 min | UI mock: file upload, AI analysis, confidence scores, reviewer overrides, toasts. |
| Recon Proof | 3 min | Pipeline diagram, recon table snippet, QC metrics to prove foundation. |
| Wrap & Next Steps | 2 min | Roadmap (automation, chatbot), feedback capture. |

**Demo Asset Checklist**
- Curated SIMPLYR & LAKE CSVs with engineered gaps.
- Precomputed enriched recon table powering BI + UI mocks.
- Clickable UI prototype (Figma/React) with reasoning panes, acceptance buttons, progress indicators, toasts.
- Power BI mock connected to static dataset; offline screenshots as backup.
- Demo script, Q&A cheat sheet, dry-run recording, fallback narratives.

---

## Delivery Timeline
| Week | Activities |
| --- | --- |
| **Nov 18–24** | Finalize sample data, recon schema, architecture README, QC checklist. |
| **Nov 25–Dec 1** | Build recon prototype, generate enriched sample, lock UI scope, craft prompts, define domain mappings. |
| **Dec 2–6** | Wire UI mock + Power BI to sample data, run dry runs, capture feedback, finalize script, prep backups. |
| **Dec 8–12 (Demo Week)** | Execute remote demo, record session (if permitted), capture questions, outline next steps. |

---

## Success Metrics & Acceptance Criteria
- **Data Accuracy:** 100% of engineered gaps appear correctly in recon table + BI views.
- **Agent Coverage:** 100% of recon rows in demo have populated domain, owner, severity, recommendation, rationale fields.
- **Demo Flow:** Completed within 30 minutes; contingency assets cover offline scenarios.
- **Client Validation:** Verbal alignment that approach meets immediate needs, plus interest in roadmap items.

---

## Risks & Mitigations
| Risk | Impact | Mitigation |
| --- | --- | --- |
| Tight timeline for real agent orchestration | Demo may seem theoretical | Use high-fidelity UI mock with real data; articulate automation path. |
| Sample data inconsistencies | Credibility loss | Curate & double-check sample records with checklist per critical field. |
| Power BI refresh/connectivity issues | Demo stall | Use static dataset + offline screenshots as backup. |
| Prompt variability | Confusing recommendations | Freeze prompt templates, include deterministic guardrails, demonstrate override flow. |
| Stakeholder availability | Scheduling slips | Secure calendar early; share pre-read & recorded dry run if needed. |

---

## Roadmap Beyond Demo
1. **Automated Orchestration:** Event-driven recon + agent pipeline on Delta Lake/Databricks (or equivalent) with CI/CD.
2. **Semantic Matching:** Introduce embeddings/fuzzy matching for addresses, taxonomy codes, custom attributes.
3. **Feedback Learning:** Incorporate reviewer overrides into prompt tuning and heuristic weighting; monitor precision/recall.
4. **Workflow Integration:** Push accepted recommendations into ServiceNow/JIRA; track SLA & resolution metrics.
5. **Provider Chatbot:** Reuse enriched recon context to power conversational support and knowledge retrieval.

---

## Glossary
- **SIMPLYR/PDM:** Upstream provider master system (truth source).
- **LAKE:** Downstream analytics repository (may lag or transform data).
- **Recon Table:** Field-level gap log plus enrichment metadata; contract between deterministic & agentic layers.
- **Domain Group:** Business function responsible for remediation (Credentialing, Network Ops, Provider Directory, Claims).
- **Owner Group:** Specific squad/queue (e.g., `Credentialing Ops Squad A`).
- **Ingestion Batch ID:** Unique identifier per recon run for auditing.
- **Agent Version / Prompt ID:** Metadata tying recommendations to model & prompt used.

---

## Call to Action
- Treat this README as the living source of truth. Update whenever schemas, prompts, or timelines shift.
- Coordinate any schema change to `recon_table` across layers before implementation.
- Log dry-run outcomes, risks, and mitigation actions so the second-week-of-December demo lands smoothly.
