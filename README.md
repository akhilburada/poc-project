# Provider Data Reconciliation & Recommendation Agent

> **Mission:** Deliver an explainable, auditable, three-layer solution that reconciles provider data between SIMPLYR (PDM) and the LAKE domain, enriches the resulting gaps with AI-assisted intelligence, and exposes the full story as a business-ready experience for HCSC stakeholders.

---

## 1. Executive Context
- **Client Pain:** Provider data drifts between upstream PDM (SIMPLYR) and downstream analytics (LAKE), forcing manual investigations across dozens of fields.
- **Expectations:** HCSC wants proof—within ~30 minutes—that we can deterministically detect gaps, explain them in business language, and show how teams would triage them.
- **Constraints:** Remote demo in the *second week of December*. Limited time to build net-new infra, so we will simulate agent orchestration via a robust UI mock while keeping the recon logic fully deterministic.

Success requires:
1. A **recon truth set** produced before any agent/LLM touches the data.
2. An **agent layer** that speaks the language of Credentialing, Network Ops, Provider Directory, and Claims.
3. A **business consumption layer** (Power BI) that lets HCSC slice, filter, and drill into gaps instantly.

---

## 2. Target Outcomes
| Outcome | What “Good” Looks Like | Evidence for Demo |
| --- | --- | --- |
| Deterministic Reconciliation | Every provider-field mismatch recorded with batch metadata; reproducible runs. | `recon_table.csv` with batch IDs, source timestamps, row counts. |
| Explainable Intelligence | Gap rows annotated with domain, severity, owner, recommendation, rationale, and agent version. | Enriched recon sample plus UI mock showing reasoning & overrides. |
| Business Storytelling | Dashboard and UI mock allow filtering by domain/severity/state and viewing provider-level context. | Power BI mock wired to sample data; scripted walkthrough. |
| Demo Readiness | 30-min remote session covering visualization → agent → recon pipeline without technical hiccups. | Dry run + checklist completed week prior to demo. |

---

## 3. Stakeholders & Roles
| Stream | Primary Owner | Support | Deliverables |
| --- | --- | --- | --- |
| Data prep & recon schema | **Venu** | Core Data Eng | SIMPLYR/LAKE samples, recon configs, metrics. |
| Agent prompts & UI mock | **Zuber** | Practice Design, GenAI CoE | Interactive UI, prompt templates, reasoning narratives. |
| Visualization (Power BI) | **Venu** (data) / BI partner | TBD | KPI view, interactive table, provider drill-through. |
| Engagement & messaging | **Sandeep** | Venu | Client scheduling, story alignment, feedback loop. |
| QA & rehearsal | All | — | Dry run assets, risk log, demo script. |

---

## 4. Architecture Overview
```
SIMPLYR (PDM) ─┐
                ├─► Spark/Python Reconciliation Job ─► recon_table (core facts)
LAKE (Analytics) ┘                                  │
                                                    ▼
                                      Agent Enrichment Service (rules + LLM)
                                                    │
                                                    ▼
                                Power BI + UI Mock + Future Workflow/Chatbot
```
- **Layer Separation:** Deterministic compute (Layer 1) is isolated from generative reasoning (Layer 2), which feeds consumption (Layer 3).
- **Single Contract:** The recon table is the contract between layers—changing its schema requires downstream alignment.
- **Extensibility:** Same architecture can power workflow automation or provider chatbots once validated.

---

## 5. Data Contracts
| Asset | Source | Contents | Refresh Cadence | Notes |
| --- | --- | --- | --- | --- |
| `simplyr_data` | SIMPLYR/PDM snapshot | ~120 columns: demographics, contracts, credentialing, TIN/NPI, geo, 60+ custom attrs. | Weekly for demo | Authoritative provider master. |
| `data_late.csv` | LAKE snapshot | Same schema as SIMPLYR to simplify comparison. | Weekly | Represents downstream/lagged state. |
| `recon_table.csv` | Recon job output | Field-level discrepancies + enrichment placeholders. | Per recon run | Stored as CSV for demo; Delta table later. |

### Recon Table Schema (minimum set)
- **Keys:** `provider_id`, `field`, `ingestion_batch_id`, `source_system`, `last_update_ts`.
- **Raw Facts:** `simplyr_value`, `lake_value`, `gap_type` (Mismatch, Missing, Stale, Format), `confidence`.
- **Enrichment Columns:** `root_cause`, `recommendation`, `next_steps`, `domain_group`, `owner_group`, `severity_score (1–5)`, `priority_bucket (P0–P2)`, `suggested_workflow`, `agent_version`, `prompt_id`, `recommendation_status` (Pending/Accepted/Overridden).

---

## 6. Layer 1 – Reconciliation Pipeline
1. **Ingest:** Pull SIMPLYR & LAKE files via SFTP/blob; assign `ingestion_batch_id` + timestamp.
2. **Normalize:** Apply config-driven transforms (trim, upper/lower, date standardization, enumeration mapping, tolerance rules for lat/long, etc.).
3. **Match:** Join primarily on `provider_id`. If missing, fall back to composite key (NPI + TIN + name). Log unmatched providers as separate diagnostics.
4. **Compare:** Evaluate each column; emit recon rows for mismatches, missing values, stale effective dates, conflicting booleans, or format violations.
5. **Quality Checks:**
   - Provider coverage (% matched vs. total on both sides).
   - Field coverage (# of fields reconciled, # of gaps per field).
   - Spike detection (compare to prior batch).
6. **Persist & Audit:** Write to `recon_table.csv`, store job logs, capture summary metrics for demo narration.

**Layer-1 KPIs**
- `% providers matched` (target >95% for curated sample).
- `# gaps` by critical fields (credentialing_status, contract_status, addresses).
- `Runtime` for job (target <5 min on sample to highlight efficiency).

---

## 7. Layer 2 – Intelligence / Agent Workflow
**Objective:** Turn raw gap facts into business-ready actions.

### Inputs
- New recon rows lacking enrichment.
- Provider context (status, specialty, plan participation, credentialing recency, language, network tier).
- Mapping tables: field → default domain group, severity baseline, owner group.
- Historical overrides (to avoid repeating known false positives).

### Processing Steps
1. **Selection:** Query recon rows with `recommendation_status = Pending` for latest batch.
2. **Context Build:** Assemble structured payload (JSON) combining recon facts + provider metadata + historical signals.
3. **Reasoning:**
   - Apply deterministic heuristics (e.g., if credentialing verified <30 days ago but LAKE expired, severity = High, domain = Credentialing).
   - Use LLM prompt for narrative explanation & recommended action, capturing `prompt_id` and `agent_version`.
4. **Ownership & Workflow:** Map to owner group (e.g., `Credentialing Ops Squad A`) and suggested workflow (ServiceNow queue, JIRA project, escalation path).
5. **Write-back:** Update recon table columns (`root_cause`, `recommendation`, `next_steps`, `severity_score`, etc.).
6. **Feedback Hooks:** In UI mock, allow reviewers to accept/override; capture overrides for future tuning.

**Layer-2 KPIs**
- `% gaps enriched` per batch (goal 100% for demo sample).
- `Distribution of domain groups/severities` to show coverage.
- `Override rate` from reviewers (mocked now, but important talking point).

---

## 8. Layer 3 – Visualization & Business Consumption
### Dataset
- Power BI dataset references enriched recon table (static CSV for demo; Delta/DirectQuery later).
- Filters by ingestion batch, severity, domain, owner, geography.

### Dashboard Components
- **Global KPIs:** Total gaps, P0 gaps, batches awaiting review, acceptance rate.
- **Domain Stack:** Stacked bar chart by Credentialing/Network Ops/Provider Directory/Claims.
- **Severity Donut:** Quick view of P0/P1/P2 distribution.
- **Trend Line:** Gaps by batch to show improvement potential.
- **Interactive Table:** Columns `Provider ID`, `Domain`, `Field`, `Gap Type`, `Severity`, `Owner`, `Recommendation Status`. Row click opens detail pane.
- **Detail Pane:** Side-by-side SIMPLYR vs LAKE values, agent narrative, next steps checklist, buttons (`Accept`, `Escalate`, `Download Evidence`).
- **Filters:** Domain, owner, severity, state, plan participation, ingestion batch.

**Future Enhancements**
- Workflow trigger buttons (ServiceNow/JIRA) once integrated.
- Export to Excel/CSV for offline audit.
- Direct integration with provider chatbot for Q&A about specific gaps.

---

## 9. Demo Blueprint (Remote, ~30 Minutes)
1. **Scene Setting (5 min)** – Recap HCSC challenges, present three-layer diagram, clarify what is deterministic vs. agentic.
2. **Visualization First (10 min)** – Walk through Power BI mock; filter by domain/geography, drill into provider detail.
3. **Agent Experience (10 min)** – Show UI mock with file upload, AI analysis, confidence scores, reviewer overrides, acceptance workflow.
4. **Recon Proof (3 min)** – Display recon table sample + pipeline diagram to reinforce deterministic foundation.
5. **Wrap & Next Steps (2 min)** – Outline path to production, mention chatbot tie-in, answer questions.

### Demo Asset Checklist
- Curated SIMPLYR & LAKE CSVs with interesting gaps.
- Precomputed enriched recon table for ingestion into BI + UI mock.
- UI mock (Figma/React) with clickable interactions and reasoning panels.
- Power BI mock connected to sample dataset.
- Demo script, Q&A cheat sheet, success metrics slide.

---

## 10. Timeline (Compressed)
| Week | Activities |
| --- | --- |
| **Nov 18–24** | Finalize sample datasets, recon schema, architecture README (this doc). |
| **Nov 25–Dec 1** | Build recon prototype, deliver enriched sample, lock UI scope & prompts. |
| **Dec 2–6** | Wire UI mock + Power BI to sample data, run internal dry runs, capture feedback. |
| **Dec 8–12 (Target)** | Execute remote demo with HCSC, capture next steps. |

---

## 11. Success Metrics & Acceptance Criteria
- **Data Accuracy:** 100% of curated provider gaps appear correctly in recon table.
- **Agent Coverage:** 100% of recon rows show domain, owner, severity, recommendation fields populated.
- **Demo Flow:** End-to-end story delivered within 30 minutes, no blocking defects.
- **Client Feedback:** Verbal confirmation that solution meets immediate needs + agreement on next-step planning.

---

## 12. Risks & Mitigations
| Risk | Impact | Mitigation |
| --- | --- | --- |
| Limited time to build true agent orchestration | Demo might look theoretical | Use high-fidelity UI mock with real data; clearly explain path to automation. |
| Data inconsistencies between SIMPLYR/LAKE samples | Demo credibility suffers | Curate sample records manually; validate all key fields before demo. |
| Power BI refresh issues | Demo stall | Use static dataset; export backup screenshots. |
| Prompt behavior inconsistent | Confusing recommendations | Freeze prompt templates; include deterministic guardrails; capture overrides. |

---

## 13. Roadmap Beyond Demo
1. **Automated Orchestration:** Event-driven recon + agent pipeline using Delta Lake and Databricks jobs.
2. **Semantic Matching:** Incorporate embeddings/fuzzy matching for addresses, names, taxonomy codes.
3. **Feedback Learning:** Store reviewer overrides and feed them into rule weighting/prompt tuning.
4. **Workflow Integration:** Push accepted recommendations into ServiceNow/JIRA and track closure status.
5. **Provider Chatbot:** Reuse enriched recon data as context for conversational agent supporting provider teams.

---

## 14. Glossary
- **SIMPLYR/PDM:** Source-of-truth provider master domain.
- **LAKE:** Downstream analytics repository that may lag or transform provider data.
- **Recon Table:** Field-level gap log plus agent enrichment; the contract between layers.
- **Domain Group:** Business function responsible for remediation (Credentialing, Network Ops, Provider Directory, Claims). 
- **Owner Group:** Specific queue/team (e.g., Credentialing Ops Squad A) that executes remediation.
- **Ingestion Batch ID:** Identifier for each recon run; used for auditing and BI incremental refresh.
- **Agent:** Combination of deterministic heuristics and LLM reasoning that annotates recon rows.

---

## 15. Call to Action
- Treat this README as the living reference—update it whenever data contracts, prompts, or demo scope change.
- Keep the recon table schema in sync across all layers; notify downstream owners if you add/remove columns.
- Record dry runs and capture feedback early so we hit the December window confidently.
