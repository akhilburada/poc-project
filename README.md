# Provider Data Reconciliation & Recommendation Agent

## 1. Purpose
Deliver a three-layer, business-ready workflow that reconciles provider records between SIMPLYR PDM data and LAKE data, enriches detected gaps with agentic insights, and exposes the full story through a consumable analytics surface (Power BI). The demo must prove we can:
- Deterministically reconcile two large provider datasets ahead of any LLM/agent execution.
- Run an intelligent layer that classifies gaps, recommends next actions, and assigns operational ownership.
- Present the enriched recon table so business stakeholders can filter, slice, and act without wading through raw files.

## 2. Layered Architecture
| Layer | Responsibility | Tech Notes |
| --- | --- | --- |
| **Task / Reconciliation** | Compare SIMPLYR vs LAKE files across ~120 provider attributes; log every mismatch into `recon_table.csv`. | Spark or Python batch job runs prior to agent. Outputs deterministic facts: `provider_id`, `field`, `simplyr_value`, `lake_value`, plus metadata (timestamps, source batch IDs). |
| **Intelligence / Agent** | Read recon table, interpret each gap, label domains (Credentialing, Network Ops, Provider Directory, Claims), recommend remediation, assign owner group, severity, workflow, and priority. | Agent can start as scripted reasoning with curated prompts. Future state: autonomous agent triggered post-batch, writing enriched columns back to recon table (JSON or wide columns). |
| **Visualization / Business Consumption** | Provide rapid insight into gaps, recommendations, and next steps. Power BI dashboard is primary vehicle; shows counts, severities, owner work queues, geo filters, etc. | Consumes enriched recon table. Enables drill-through to provider-level detail, evidence (SIMPLYR vs LAKE), and agent commentary. |

## 3. Data Assets
- `simplyr_data`: Source-of-truth snapshot from SIMPLYR/PDM. Includes provider demographics, contract information, credentialing flags, location metadata, 60+ custom attributes, geocodes, and IDs (TIN, CAQH, NPI, etc.).
- `data_late.csv`: Parallel snapshot from the LAKE domain, representing downstream or lagged data. Schema mirrors `simplyr_data` so field-by-field comparison is feasible.
- `recon_table.csv` (schema defined): Stores reconciliation output plus enrichment placeholders:
  - `provider_id`, `field`, `simplyr_value`, `lake_value`
  - `gap_type` (Missing, Mismatch, Stale, etc.)
  - `root_cause` hypothesis (e.g., late credentialing feed, partial contract load)
  - `recommendation`, `Next Steps`
  - `owner_group` (TEAM-XYZ), `domain_group` (Credentialing/Network Ops/Provider Directory/Claims)
  - `severity_score`, `suggested_workflow`, `priority_bucket`

## 4. Reconciliation Flow (Layer 1)
1. **Ingest Files:** Scheduled Spark/Python job pulls daily/weekly SIMPLYR & LAKE extracts.
2. **Normalize:** Standardize casing, trim whitespace, harmonize date formats, map enumerations (plan codes, flag values).
3. **Compare:** For each provider + column, evaluate equality. Emit a recon row when values differ or when one side lacks data.
4. **Persist:** Write recon results to `recon_table.csv` (or lakehouse table) with batch IDs so runs are auditable.
5. **Quality Checks:** Count mismatches per column, detect spike anomalies, ensure coverage ratios.

## 5. Intelligence Flow (Layer 2)
1. **Gap Intake:** Agent loads fresh recon rows.
2. **Context Build:** Augment with provider metadata (specialty, status, plan participation) to improve reasoning.
3. **Prompt/Rule Evaluation:** Apply domain heuristics + LLM reasoning to categorize gaps, suggest root causes, and recommend actions. Example—credentialing status mismatch → assign to Credentialing, severity high if provider Active in SIMPLYR but Terminated in LAKE.
4. **Ownership & Workflow:** Map gaps to owner groups (e.g., `Credentialing Ops`, `Network Operations`, `Provider Directory`, `Claims Data Mgmt`). Suggest JIRA/ServiceNow queue or automation playbook.
5. **Write-Back:** Update recon table columns (`gap_type`, `recommendation`, etc.) so downstream consumers see enriched context.

## 6. Visualization Flow (Layer 3)
- **Dataset:** Power BI dataset refreshes from enriched recon table.
- **Dashboards:**
  - Overview KPIs (total gaps, by severity/domain/owner).
  - Provider drill-through cards with SIMPLYR vs LAKE values and agent notes.
  - Geo filters (state/county) leveraging latitude/longitude.
  - Trend visuals by ingestion batch.
- **Future Automation:** From dashboard selections, trigger workflows (e.g., service tickets) once client approves integration.

## 7. Demo Strategy (Dec Week 2)
- **Narrative:** Lead with Business layer (Power BI mock), then peel back to agent reasoning (UI mock), finally show deterministic recon foundation.
- **Mock UI:** Use prebuilt UI simulation (file upload → AI analysis → reviewer overrides) to illustrate agent experience without standing up full infra.
- **Sample Data:** Provide curated SIMPLYR/LAKE CSVs plus initial recon table so demo is grounded yet repeatable.
- **Talking Points:** Emphasize deterministic compute, agentic enrichment, and ability to operationalize insights.

## 8. Future Enhancements
- Full agent orchestration (event-driven triggers post-batch).
- Embedding-based fuzzy matching for reconciliation step (semantic comparisons, historical learning).
- Feedback loops so business overrides reinforce agent prompts.
- Workflow automation (ServiceNow/JIRA) fed directly from recon insights.
- Expanded chatbot scenario once provider gap agent proves value.

## 9. Roles & Responsibilities
- **Venu / Core Data Team:** Prepare sample datasets, define recon schema, ensure deterministic pipeline narrative.
- **Zuber / UI & Demo Lead:** Build/refine UI mock, integrate sample data, craft agent reasoning story, drive demo.
- **Sandeep / Engagement Lead:** Coordinate client scheduling, ensure messaging aligns with HCSC needs, manage follow-ups.

## 10. Key Dates
- **Now – Nov End:** Finalize sample data + recon schema, align narrative.
- **Early Dec:** Hand over assets to Zuber, build/refine UI mock & Power BI views.
- **Second Week of Dec:** Remote demo (~30 mins) focusing on business outcomes, backed by recon + agent story.

---
This README is the living reference for anyone joining the effort—update as the architecture or deliverables evolve.
