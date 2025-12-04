# Provider Data Reconciliation & Recommendation Agent

> **Mission:** Provide HCSC with an explainable, auditable, three-layer solution that reconciles provider data between SIMPLYR (PDM) and the LAKE domain, enriches the gaps with AI-assisted intelligence, and exposes the full story as a business-ready experience.

---

## Table of Contents
1. [Executive Context](#executive-context)
2. [Target Outcomes](#target-outcomes)
3. [Stakeholders & Responsibilities](#stakeholders--responsibilities)
4. [Architecture Overview](#architecture-overview)
5. [Data Contracts & Schemas](#data-contracts--schemas)
6. [Layer-1: Reconciliation Pipeline](#layer-1-reconciliation-pipeline)
7. [Layer-2: Intelligence / Agent Workflow](#layer-2-intelligence--agent-workflow)
8. [Layer-3: Business Consumption & Visualization](#layer-3-business-consumption--visualization)
9. [Demo Blueprint](#demo-blueprint)
10. [Delivery Timeline](#delivery-timeline)
11. [Success Metrics & Acceptance Criteria](#success-metrics--acceptance-criteria)
12. [Risks & Mitigations](#risks--mitigations)
13. [Roadmap Beyond Demo](#roadmap-beyond-demo)
14. [Glossary](#glossary)
15. [Call to Action](#call-to-action)

---

## Executive Context
- **Client Pain:** SIMPLYR (upstream provider master) drifts from LAKE (downstream analytics). HCSC teams must manually cross-check ~120 attributes per provider to understand discrepancies.
- **Expectation:** Within a 30‑minute remote session, we must demonstrate a deterministic reconciliation foundation, an agent that speaks the language of Credentialing/Network Ops/Provider Directory/Claims, and a business-friendly visualization layer.
- **Constraint:** Limited runway before second week of December; no time to build full orchestration, so we simulate agent UX via a robust UI mock while ensuring the recon data is real and auditable.

Success hinges on three principles:
1. **Recon First:** Produce a trustworthy gap dataset before any LLM touches the data.
2. **Agentic Insight:** Transform raw gaps into recommendations, ownership cues, and severity labels that business users understand.
3. **Business Consumption:** Present enriched gaps through Power BI and interactive UI views so stakeholders can filter, slice, and drill without touching CSVs.

---

## Target Outcomes
| Outcome | Definition of "Good" | Demo Evidence |
| --- | --- | --- |
| Deterministic Reconciliation | Every provider/field mismatch recorded with batch metadata, quality stats, and reproducible logic. | `recon_table.csv` populated from Spark/Python job; coverage metrics slide. |
| Explainable Intelligence | Each gap annotated with domain, owner, severity, recommendation, rationale, and agent version. | UI mock showing reasoning panel, overrides, acceptance workflow. |
| Business Storytelling | Enables slicing by domain/severity/state, viewing provider drill-through, and exporting evidence. | Power BI mock wired to enriched recon sample. |
| Demo Readiness | 30‑minute remote walkthrough with no data surprises or broken flows. | Dry-run checklist + backup assets (screenshots, CSVs). |

---

## Stakeholders & Responsibilities
| Workstream | Primary Owner | Support | Deliverables |
| --- | --- | --- | --- |
| Data prep & recon schema | **Venu** | Core Data Engineering | SIMPLYR + LAKE sample files, recon configuration, KPI snapshots. |
| Agent prompts & UI mock | **Zuber** | Practice Design, GenAI CoE | Clickable UI prototype, prompt templates, reasoning narratives, audit logs. |
| Visualization (Power BI) | **Venu** (data) / BI partner | TBD | Dashboard pages, dataset, drill-through views, export templates. |
| Engagement & messaging | **Sandeep** | Venu | Client scheduling, story alignment, feedback capture, follow-up notes. |
| QA & rehearsal | All | — | Dry-run recordings, risk log, Q&A cheat sheet, demo script. |

---

## Architecture Overview
```
SIMPLYR (PDM) ─┐
                ├─► Spark/Python Recon Job ─► recon_table (core facts)
LAKE (Analytics) ┘                                  │
                                                    ▼
                                   Agent Enrichment Service (rules + LLM)
                                                    │
                                                    ▼
                             Power BI + Interactive UI + Future Workflow Hooks
```
- **Layer Isolation:** Deterministic reconciliation and AI reasoning stay decoupled; recon table acts as contract between layers.
- **Auditability:** Each layer writes batch metadata, prompts IDs, and agent versions for traceability.
- **Extensibility:** Same pattern can power future workflows (ServiceNow/JIRA) or provider chatbots once validated.

---

## Data Contracts & Schemas
| Asset | Source | Contents | Refresh Cadence | Notes |
| --- | --- | --- | --- | --- |
| `simplyr_data` | SIMPLYR/PDM | Provider demographics, contract statuses, credentialing info, locations, custom attributes, geo, IDs (TIN/NPI/CAQH). | Weekly for demo | Treated as gold source. |
| `data_late.csv` | LAKE | Same schema; represents downstream/lagged view for reconciliation. | Weekly | Highlights drift due to processing lag or transformation errors. |
| `recon_table.csv` | Recon job output | Field-level gaps + enrichment placeholders + audit metadata. | Per batch | Stored as CSV for demo; Delta table later. |

### Recon Table Schema (Baseline Columns)
- **Keys:** `provider_id`, `field`, `ingestion_batch_id`, `source_system`, `last_update_ts`.
- **Raw Facts:** `simplyr_value`, `lake_value`, `gap_type` (Mismatch, Missing, Stale, Format), `confidence`.
- **Enrichment Columns:** `root_cause`, `recommendation`, `next_steps`, `domain_group`, `owner_group`, `severity_score (1–5)`, `priority_bucket (P0–P2)`, `suggested_workflow`, `agent_version`, `prompt_id`, `recommendation_status (Pending/Accepted/Overridden)`.

---

## Layer 1: Reconciliation Pipeline
1. **Ingest:** Pull SIMPLYR & LAKE files (SFTP/blob). Stamp `ingestion_batch_id`, timestamps, row counts.
2. **Normalize:** Trim strings, standardize casing, harmonize date formats, map enumerations, de-duplicate addresses, apply tolerance rules (lat/long rounding, phone formatting).
3. **Match Providers:** Default join on `provider_id`. If missing, fall back to composite key (NPI + TIN + name). Log unmatched entities in diagnostic table.
4. **Compare Fields:** Evaluate ~120 columns. Emit recon row when values differ, missing vs populated, or violate freshness thresholds (e.g., contract_end_date earlier upstream).
5. **Quality Checks:**
   - Provider coverage (matched vs total per source).
   - Field coverage (# fields reconciled, # gaps per field).
   - Spike detection vs prior batch (alert if >x% increase).
6. **Persist & Audit:** Write to `recon_table.csv`; capture summary metrics JSON for dashboard ingest; retain logs for reproducibility.

**Layer‑1 KPIs**
- `% providers matched` (target >95% curated sample).
- `# gaps` per critical attributes (credentialing_status, contract_status, addresses, plan flags).
- `Runtime` (<5 min on sample) to highlight efficiency.

---

## Layer 2: Intelligence / Agent Workflow
**Objective:** Turn raw gap facts into business-ready actions with traceable reasoning.

### Inputs
- Recon rows with `recommendation_status = Pending`.
- Provider context: status, specialty, plan participation, credentialing recency, languages, network tier, geography.
- Mapping tables: `field → domain_group`, default severity, default owner.
- Historical overrides to avoid repeat false positives.

### Processing Steps
1. **Selection:** Fetch latest-batch recon rows requiring enrichment.
2. **Context Build:** Assemble JSON payload combining recon facts, provider metadata, historical notes, and heuristics.
3. **Reasoning:**
   - Deterministic heuristics (e.g., `credentialing_status` mismatch with recent verification = severity High, domain Credentialing).
   - LLM prompt to draft narrative explanation, root cause hypothesis, and next steps; log `prompt_id` + `agent_version`.
4. **Ownership & Workflow:** Map to owner queues (e.g., `Credentialing Ops Squad A`, `Network Ops Region Central`). Suggest workflow (ServiceNow ticket, JIRA board, manual outreach).
5. **Write-Back:** Update recon table columns with recommendations, severity, owner, workflow, status.
6. **Feedback Hooks:** UI mock allows reviewers to accept or override; capture overrides for future prompt tuning and heuristics adjustments.

**Layer‑2 KPIs**
- `% gaps enriched` (goal 100% in demo dataset).
- Distribution across domain groups/severity buckets.
- Mocked override rate (discussion point to show feedback loop concept).

---

## Layer 3: Business Consumption & Visualization
### Dataset
- Power BI dataset references enriched recon table (static CSV for demo; Delta/DirectQuery later).
- Supports filters on batch, severity, domain, owner, geography, plan participation.

### Dashboard Components
- **Overview KPIs:** Total gaps, P0 gaps, batches awaiting review, acceptance rate.
- **Domain Stack Chart:** Credentialing vs Network Ops vs Provider Directory vs Claims.
- **Severity Donut:** P0/P1/P2 breakdown.
- **Trend Line:** Gaps per batch to illustrate stabilization potential.
- **Interactive Table:** Columns `Provider ID`, `Domain`, `Field`, `Gap Type`, `Severity`, `Owner`, `Status`. Sorting, filtering, pagination, export button.
- **Detail Pane:** Side-by-side SIMPLYR vs LAKE values, agent narrative, next steps checklist (toggleable), buttons for `Accept`, `Escalate`, `Download Evidence`.
- **Filters:** Domain, owner group, severity, state, ingestion batch, plan type.

**Future Enhancements**
- Trigger workflow automation (ServiceNow/JIRA) directly from dashboard.
- Integrate provider chatbot to answer questions using enriched recon data.
- Embed SLO monitoring (time to resolve gaps, reoccurrence rate).

---

## Demo Blueprint
| Segment | Duration | Content |
| --- | --- | --- |
| Scene Setting | 5 min | Recap pain, show 3-layer diagram, clarify deterministic vs agentic roles. |
| Visualization Walkthrough | 10 min | Power BI mock with filtering by domain/geography, drill into provider detail, show export capability. |
| Agent Experience | 10 min | UI mock: file upload, AI analysis, confidence scores, reviewer overrides, acceptance flow, toast notifications. |
| Recon Proof | 3 min | Display pipeline diagram, recon table sample, quality metrics to reinforce deterministic foundation. |
| Wrap & Next Steps | 2 min | Outline roadmap (workflow automation, chatbot), confirm actions, collect feedback. |

### Demo Asset Checklist
- Curated SIMPLYR & LAKE CSVs with engineered gaps.
- Precomputed enriched recon table for BI + UI consumption.
- Clickable UI mock (Figma/React) with reasoning panes, acceptance buttons, progress indicators.
- Power BI mock connected to static dataset; backup screenshots.
- Demo script, Q&A cheat sheet, dry-run recording.

---

## Delivery Timeline
| Week | Activities |
| --- | --- |
| **Nov 18–24** | Finalize sample data, recon schema, architecture README. Validate key attributes (credentialing_status, contract dates, addresses). |
| **Nov 25–Dec 1** | Build recon prototype, produce enriched sample, lock UI mock scope, draft prompt templates, define domain mappings. |
| **Dec 2–6** | Wire UI mock + Power BI to sample data, run internal dry runs, capture feedback, finalize script, prep backup assets. |
| **Dec 8–12 (Target Demo)** | Execute remote demo, record session (with permission), capture client questions, discuss next steps. |

---

## Success Metrics & Acceptance Criteria
- **Data Accuracy:** 100% of curated provider gaps appear correctly in recon table and BI views.
- **Agent Coverage:** 100% of recon rows in demo show populated domain, owner, severity, recommendation, and rationale fields.
- **Demo Flow:** Run-through completed within 30 minutes; contingency assets available for any connectivity issues.
- **Client Feedback:** Positive confirmation that approach meets immediate needs, plus verbal alignment on roadmapping next phase.

---

## Risks & Mitigations
| Risk | Impact | Mitigation |
| --- | --- | --- |
| Limited time for true agent orchestration | Demo could appear theoretical | Use high-fidelity UI mock with real data; clearly articulate path to automation. |
| Data inconsistencies in sample | Demo credibility suffers | Manually curate & double-check sample records; maintain checklist per field. |
| Power BI refresh or connectivity issues | Demo stall | Use static dataset with offline screenshots as backup. |
| Prompt variability | Confusing recommendations | Freeze prompt templates, include deterministic guardrails, capture override flow. |
| Stakeholder availability | Scheduling slips | Secure calendar slot early; share pre-read with recorded dry run if necessary. |

---

## Roadmap Beyond Demo
1. **Automated Orchestration:** Event-driven recon + agent pipeline on Delta Lake/Databricks or similar platform.
2. **Semantic Matching:** Add embeddings/fuzzy logic for addresses, specialties, taxonomy codes.
3. **Feedback Learning:** Feed reviewer overrides into model/rule weighting; monitor precision/recall.
4. **Workflow Integration:** Push accepted recommendations into ServiceNow/JIRA, track resolution SLAs.
5. **Provider Chatbot:** Use enriched recon insights to power conversational interfaces for provider support teams.

---

## Glossary
- **SIMPLYR/PDM:** Upstream provider master data platform.
- **LAKE:** Downstream analytics repository (may lag or transform data).
- **Recon Table:** Field-level gap log with enrichment metadata; contract between deterministic and agentic layers.
- **Domain Group:** Business function (Credentialing, Network Ops, Provider Directory, Claims) accountable for remediation.
- **Owner Group:** Specific queue/team (e.g., `Credentialing Ops Squad A`).
- **Ingestion Batch ID:** Identifier for each recon run; used for auditing and incremental refresh.
- **Agent Version / Prompt ID:** Metadata capturing which prompt/LLM version generated the recommendation.

---

## Call to Action
- Treat this README as the living source of truth; update whenever data contracts, prompts, or timeline change.
- Coordinate schema changes to the recon table across all layers before implementation.
- Log dry-run outcomes, risks, and mitigation actions so the second-week-of-December demo lands smoothly.
