# Provider Data Reconciliation & Recommendation Agent

> **Mission:** Deliver an explainable, multi-layer system that reconciles provider data between SIMPLYR (PDM) and the LAKE domain, enriches gaps with AI-driven recommendations, and exposes the intelligence through a business-ready experience for HCSC stakeholders.

---

## 1. Executive Summary
HCSC needs proof that we can quickly surface actionable provider data gaps without sacrificing determinism. Our approach separates concerns into three tightly-coupled layers:
1. **Task / Reconciliation Layer** – Spark/Python job compares SIMPLYR vs LAKE files field-by-field and logs mismatches into a recon table.
2. **Intelligence / Agent Layer** – Agent reads recon rows, applies heuristics + LLM reasoning to explain gaps, assign ownership, and recommend remediation.
3. **Visualization / Business Layer** – Power BI (initially) consumes enriched recon data so Credentialing, Network Ops, Provider Directory, and Claims teams can triage and act.

Success looks like a deterministic recon dataset proven before demo day, an agent that speaks business language, and a walkthrough that shows actionable insights within ~30 minutes.

---

## 2. Target Outcomes
| Outcome | Description | Verification |
| --- | --- | --- |
| Deterministic truth set | Every provider-field mismatch logged with batch metadata before any AI runs. | Reproducible recon_table extracts, row counts, CDC logs. |
| Explainable intelligence | Agent recommendations traceable to prompts/rules with owner + severity metadata. | Recon table enriched columns populated with agent version, timestamp, rationale. |
| Business storytelling | Dashboard enabling slicing by domain, severity, geography, and direct drill to provider detail. | Power BI mock wired to sample enriched recon table. |
| Demo readiness | Remote session (second week of Dec) showing all three layers with a focus on business value. | Dry run with internal team, recorded script. |

---

## 3. Architecture Overview
```
SIMPLYR (PDM) ─┐
                ├─► Spark/Python Recon Job ─► recon_table core facts ─┐
LAKE (Analytics) ┘                                                   │
                                                                     ▼
                                                         Agent Enrichment Service
                                                                     │
                                                                     ▼
                                                Power BI / Workflow / Future Chatbot
```
- **Isolation:** Reconciliation compute is deterministic and auditable. Agent only enriches recon facts, never mutating original sources.
- **Extensibility:** Enriched recon table can power workflow orchestration, chatbot experiences, and closed-loop learning.

---

## 4. Data Contracts
| Asset | Columns | Source | Refresh | Notes |
| --- | --- | --- | --- | --- |
| `simplyr_data` | ~120 | SIMPLYR/PDM | Weekly snapshot | Authoritative roster (demographics, contracts, credentialing, TIN/NPI, geocodes, 60+ custom attrs). |
| `data_late.csv` | ~120 | LAKE | Weekly | Mirrors SIMPLYR schema; represents downstream lag/drift. |
| `recon_table` | flexible | Recon job | Per run | Field-level discrepancies + agent metadata. Stored as CSV during demo, Delta later. |

### Recon Table Required Columns
- Keys: `provider_id`, `field`, `ingestion_batch_id`, `source_system`, `last_update_ts`.
- Values: `simplyr_value`, `lake_value`, `gap_type` (Missing, Mismatch, Stale, Format), `confidence`.
- Agent metadata: `root_cause`, `recommendation`, `next_steps`, `domain_group`, `owner_group`, `severity_score` (1–5), `priority_bucket` (P0/P1/P2), `suggested_workflow`, `agent_version`, `prompt_id`.

---

## 5. Layer 1 – Reconciliation Workflow
1. **Ingest** – Pull SIMPLYR/LAKE files via SFTP or blob. Tag run with batch ID and timestamp.
2. **Normalize** – Apply config-driven transforms (trim, casing, date formats, enumeration mapping). Track anomalies.
3. **Compare** – Align rows by provider_id (with composite fallback). Evaluate every column with tolerance rules (e.g., lat/long +/- 0.0001, case-insensitive emails). Emit recon row for differences, missing values, stale effective dates, or conflicting booleans.
4. **Quality Checks** – Validate row counts, unmatched providers, field coverage %, and issue summary metrics.
5. **Persist & Audit** – Write recon_table, store inputs/outputs, log metrics. Failure path notifies team.

**KPIs for Layer 1**
- % of providers matched.
- # of gaps per domain-critical field (credentialing_status, contract_status, practice_address).
- Average time to reconcile dataset.

---

## 6. Layer 2 – Intelligence Workflow
**Objective:** Convert raw gaps into business-ready recommendations.

### Inputs
- Recon rows awaiting enrichment.
- Provider metadata (status, specialty, languages, plan participation, contract dates).
- Domain mapping table (field → domain_group, baseline severity).
- Historical overrides to avoid repeated false positives.

### Steps
1. **Batch Selection:** Pull recon rows lacking recommendations (using status flag).
2. **Context Build:** Join metadata to form prompt payload (JSON or structured template).
3. **Reasoning:** Apply deterministic rules first, then LLM prompt for narrative (root cause, recommendation, next steps). Example prompt snippet:
   - _"Given provider status ACTIVE in SIMPLYR but INACTIVE in LAKE with credentialing verified on 2025-06-06, classify domain, severity, and recommend next action."_
4. **Ownership Mapping:** Determine `owner_group` (e.g., Credentialing Ops) and `suggested_workflow` (JIRA queue, ServiceNow assignment).
5. **Write-back:** Update recon table columns, include `agent_version` + `prompt_id` for lineage.
6. **Feedback Hooks:** Capture user overrides (from UI mock). Store in separate table for future reinforcement.

**KPIs for Layer 2**
- % of gaps with agent recommendations.
- Distribution of domain groups and severities.
- User acceptance rate of recommendations (mocked now, real later).

---

## 7. Layer 3 – Visualization & Business Consumption
### Dataset
- Power BI dataset referencing enriched recon table.
- Incremental refresh by `ingestion_batch_id` once in production.

### Dashboard Elements
- **Top KPIs** – Total gaps, critical gaps, batches awaiting review, acceptance rate.
- **Domain Stack** – Stacked bar showing gaps by domain (Credentialing, Network Ops, Provider Directory, Claims).
- **Severity Donut** – Proportional severity view.
- **Trend Chart** – Gaps over ingestion batches.
- **Interactive Table** – Columns: Provider ID, Domain, Field, Gap Type, Severity, Owner Group, Recommendation status. Row click opens detail overlay.
- **Detail Pane** – Side-by-side values (SIMPLYR vs LAKE), agent narrative, next steps checklist, acceptance toggle.
- **Filters** – Domain, owner, severity, state, plan participation, batch.

**Future Enhancements** – Workflow triggers (ServiceNow/JIRA), export to Excel, integration with provider chatbot once matured.

---

## 8. Demo Blueprint (Remote, ~30 min)
1. **Set the Stage (5 min)** – Context of HCSC pains, three-layer structure slide.
2. **Visualization First (10 min)** – Walk through Power BI mock highlighting insights, filtering, provider drill-down.
3. **Agent Experience (10 min)** – Show UI mock (file upload → AI mapping → recommendation panel). Emphasize clickable buttons, confidence scores, reviewer overrides.
4. **Deterministic Proof (3 min)** – Flash recon table output + pipeline diagram to reinforce credibility.
5. **Close (2 min)** – Next steps, timeline to production, potential chatbot tie-in.

### Demo Assets Checklist
- Sample SIMPLYR & LAKE CSVs (consistent provider IDs, curated gaps).
- Precomputed recon_table sample with agent columns.
- UI mock (Figma/React) wired for interactions.
- Power BI mock connected to static dataset.
- Script + Q&A prep.

---

## 9. Roles & Responsibilities
| Stream | Lead | Backup | Deliverables |
| --- | --- | --- | --- |
| Data prep & recon schema | Venu + Core Data Eng | Analytics support | Sample data, recon configs, metrics. |
| UI mock & agent storyline | Zuber | Practice design | Interactive UI demo, prompt design. |
| Power BI mock | Venu (data) / BI partner | TBD | KPI view, table, drill-through. |
| Client engagement | Sandeep | Venu | Scheduling, narrative alignment, feedback. |
| Agent prompt governance | Zuber (LLM) | GenAI CoE | Prompt templates, rules, override capture. |

---

## 10. Timeline (Compressed)
| Week | Focus |
| --- | --- |
| Nov 18–24 | Finalize sample datasets, recon schema, architecture doc (this file). |
| Nov 25–Dec 1 | Build recon job prototype, deliver enriched recon sample, lock UI scope. |
| Dec 2–6 | Wire UI mock + Power BI to sample data, rehearse demo. |
| Dec 8–12 (target) | Remote demo with HCSC. |

---

## 11. Roadmap Beyond Demo
1. **Automated Orchestration** – Event-driven recon + agent pipeline with Delta Lake storage.
2. **Semantic Matching** – Use embeddings or fuzzy logic for addresses, names, taxonomy codes.
3. **Closed-loop Learning** – Feed reviewer overrides back into rule weights/prompt tuning.
4. **Workflow Integration** – Push accepted recommendations into ServiceNow/JIRA; capture completion status.
5. **Provider Chatbot** – Use enriched recon data to seed contextual Q&A for provider teams.

---

## 12. Glossary
- **SIMPLYR/PDM:** Source-of-truth provider master domain.
- **LAKE:** Downstream analytic store that lags or transforms provider data.
- **Recon Table:** Field-level gap log plus agent enrichment. Single source for storytelling.
- **Domain Group:** Business function accountable for remediation (Credentialing, Network Ops, Provider Directory, Claims).
- **Owner Group:** Specific team or queue for action (e.g., Credentialing Ops Squad A).
- **Batch ID:** Identifier for each reconciliation run; drives lineage and BI incremental refresh.
- **Agent:** Combination of deterministic rules and LLM reasoning that annotates recon rows.

---

## 13. Call to Action
- Keep this README updated as data, prompts, or demo scope evolves.
- Use it to onboard new contributors quickly.
- Treat the recon table as the contract between layers—if it changes, all downstream components must realign.
