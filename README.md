# Provider Data Reconciliation & Recommendation Agent

## 1. Executive Summary
Blue Cross HCSC asked for a pragmatic demonstration that proves we can (a) reconcile provider records between their operational PDM domain (SIMPLYR) and analytic LAKE domain, (b) add intelligent recommendations that speak the language of Credentialing/Network Ops/Provider Directory/Claims, and (c) surface the enriched story through a business-facing experience (Power BI now, workflow later). The success signal is a deterministic, reviewable recon dataset that an AI agent enhances with root-cause hypotheses, owner cues, and actionable next steps.

## 2. Target Outcomes
- **Deterministic truth set** – Spark/Python job produces `recon_table` rows for every provider-field discrepancy before any agent executes.
- **Explainable intelligence** – Agent reads recon facts, reasons over provider context, and writes back structured recommendations plus severity/ownership metadata.
- **Business-ready storytelling** – Power BI (or equivalent) consumes the enriched table so stakeholders can filter, slice, assign, and eventually trigger workflows.
- **Demo readiness** – Remote demo in second week of December showing all three layers, with emphasis on the business/agent experience.

## 3. System-at-a-Glance
```
SIMPLYR (PDM)  --->
                   \     (Spark/Python Reconciliation) -->  recon_table core columns
LAKE (Analytic)  --->                                         |
                                                           Agent enrichment (LLM + rules) --> recon_table enriched columns
                                                                                               |
                                                                                           Power BI / future workflow
```
All compute before the agent is deterministic, logged, and repeatable. The agent sits downstream, never mutating raw source files—only appending insights to the recon facts.

## 4. Data Contracts
| Asset | Format | Refresh | Notes |
| --- | --- | --- | --- |
| `simplyr_data` | CSV (120 cols) | Weekly snapshot | Authoritative provider master from SIMPLYR/PDM. Includes demographics, contracts, credentialing flags, geocodes, 60 custom attributes, etc. |
| `data_late.csv` | CSV (same schema) | Weekly | Represents LAKE / downstream systems that may lag or drift. |
| `recon_table.csv` | CSV / Delta table | Per run | Stores field-level discrepancies and enrichment metadata. Schema snippet below. |

### Recon Table Schema (initial + enrichment columns)
- `provider_id`
- `field`
- `simplyr_value`
- `lake_value`
- `gap_type` (Missing/Mismatch/Stale/Formatting)
- `root_cause`
- `recommendation`
- `next_steps`
- `owner_group` (Team or queue)
- `domain_group` (Credentialing, Network Ops, Provider Directory, Claims)
- `severity_score` (1–5)
- `suggested_workflow`
- `priority_bucket` (P0/P1/P2)
- `ingestion_batch_id`, `source_system`, `last_update_ts`

## 5. Layer 1 – Reconciliation (Task Layer)
1. **Ingestion** – Spark/Python pulls SIMPLYR & LAKE files (support SFTP or blob). Each run tagged with batch ID + timestamp.
2. **Normalization** – Standardize data types, date formats, trimming, enumerations, case sensitivity, zip formatting. Build config-driven mapping file so change management is easy.
3. **Comparison Logic**
   - Row alignment by `provider_id` (and fallback composite keys if duplicates).
   - Column-level diff with tolerance rules (e.g., +/- for latitude/longitude, case-insensitive for emails).
   - Emit recon row when: values differ, value missing on either side, stale effective dates, conflicting flags.
4. **Quality Checks** – Validate row counts, field coverage %, unusual spikes (control chart), and produce summary metrics for the agent’s context.
5. **Persist & Audit** – Write deterministic recon table plus run metadata. Store raw inputs + outputs in immutable storage for replay. Trigger success/failure notification.

## 6. Layer 2 – Intelligence (Agent Layer)
**Mission**: read recon rows, add context that helps business teams prioritize and resolve gaps.

### Reasoning Inputs
- Recon row (field, values, gap type).
- Provider metadata (status, specialty, language, plan participation, credential dates).
- Historical behavior (has this provider tripped same gap before?).
- Domain heuristics (lookup tables: which fields map to Credentialing vs Network Ops, severity rules, etc.).

### Processing Steps
1. **Load recon batch** filtered to rows without recommendations yet.
2. **Context build** – enrich with provider attributes and heuristics so prompt covers business context.
3. **Prompt/RULE evaluation** – combination of deterministic rules (e.g., `credentialing_status` mismatch -> Credentialing) plus LLM reasoning to craft root cause + actionable recommendation in business tone.
4. **Ownership & Workflow mapping** – map to `owner_group`, `domain_group`, severity, and recommended workflow (JIRA queue, ServiceNow, email runbook).
5. **Write-back** – update recon table columns. Maintain lineage of agent version + prompt ID.
6. **Feedback hooks** – capture user overrides (from UI mock) so prompts improve later.

### Example Output
> Provider P100006 shows SIMPLYR credentialing status “Verified” vs LAKE “Pending”. This is a Credentialing issue (owner Credentialing Ops). Severity high because provider is Out-of-Network in LAKE but In-Network in SIMPLYR. Recommendation: trigger expedited credentialing refresh, verify CAQH ID, update LAKE feed.

## 7. Layer 3 – Visualization (Business Layer)
- **Dataset** – Power BI dataset pointing to enriched recon table. Supports incremental refresh per batch.
- **Core visuals**
  - KPI cards for total gaps, critical gaps, batches awaiting review.
  - Domain split (stacked bar), severity donut, timeline per ingestion batch.
  - Interactive table (provider ID, domain, specialty, gap type, owner, severity, recommendation status). Row click opens detail.
  - Detail pane: SIMPLYR vs LAKE values, agent recommendation, next steps checklist, acceptance status.
- **Filters** – domain group, owner group, severity, geography (state/county), plan participation, ingestion batch.
- **Future workflow** – once client ready, hooking accepted recommendations to ServiceNow/JIRA automation.

## 8. Demo Blueprint (Remote – 30 min)
1. **Hook (Layer 3 first)** – Show Power BI view summarizing critical issues, highlight ability to filter by Credentialing, drill to provider detail.
2. **Agent Walkthrough (Layer 2)** – Transition to UI mock (built in React/Figma). Upload SIMPLYR/LAKE files, run recon, show AI reasoning panel with confidence, editable recommendations, acceptance buttons—all clickable.
3. **Foundational Proof (Layer 1)** – Briefly show recon table output (CSV/Delta) to prove deterministic facts exist before agent.
4. **Close** – Outline path to production: automate recon, integrate real agent, extend to workflow.

## 9. Delivery Owner Matrix
| Workstream | Primary | Secondary |
| --- | --- | --- |
| Sample data & recon schema | Venu + Core Data Eng | Analytics support |
| UI mock & demo orchestration | Zuber | Practice design team |
| Power BI mock | Venu (initial dataset) / BI partner | TBD |
| Client engagement & scheduling | Sandeep | Venu |
| Agent prompt design | Zuber (prompt), Venu (rules) | GenAI CoE |

## 10. Timeline (compressed)
- **Week of Nov 24** – Finalize sample SIMPLYR/LAKE files, recon schema, storyteller notes.
- **Week of Dec 1** – Hand assets to Zuber, finalize UI mock + prompts; craft Power BI visuals.
- **Week of Dec 8 (target)** – Remote demo (30 min). Use same assets for follow-up.

## 11. Future Enhancements
1. **Full agent orchestration** – trigger agent automatically after each recon batch, store outputs in Delta Lakehouse.
2. **Vector-assisted reconciliation** – leverage embeddings to catch semantic similarities (e.g., “St.” vs “Street”).
3. **Closed-loop learning** – capture reviewer overrides to retrain prompts or adjust rule weights.
4. **Workflow integration** – push accepted recommendations to ServiceNow/JIRA; feed status back into recon table.
5. **Provider chatbot** – reuse enriched recon data to power conversational assistant (HCSC’s additional ask).

## 12. Glossary
- **SIMPLYR/PDM** – Provider Data Management source system (authoritative roster).
- **LAKE** – Downstream data lake / warehouse copy of provider data.
- **Recon Table** – Field-level mismatch log with enrichment; single source for gaps.
- **Domain Group** – Business function responsible for remediation (Credentialing, Network Ops, Provider Directory, Claims).
- **Agent** – LLM + rule-based reasoning service that annotates recon rows with next-best actions.
- **Batch ID** – Unique identifier for each reconciliation run, used for lineage and BI refresh.

---
Update this document as architecture, prompts, or demo scope evolves. It should give any newcomer enough depth to contribute after one read-through.
