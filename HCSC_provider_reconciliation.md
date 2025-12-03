# HCSC Provider Data Reconciliation – Deep-Dive Blueprint

## 1. Context & Objectives
- **Client need**: HCSC wants an agentic workflow that reconciles Simplyr PDM data against the enterprise Data Lake, interprets mismatches, and surfaces business-ready recommendations via Power BI. Timeline requires a compelling demo focusing on business language rather than backend orchestration.
- **Three-layer framing**:
  1. **Task / Reconciliation Layer** – deterministic Spark/Python jobs compare Simplyr vs Lake, producing a recon table.
  2. **Intelligence / Agentic Layer** – LLM-powered agent consumes recon rows, assigns ownership, proposes remediation, and packages workflow payloads.
  3. **Visualization / Consumption Layer** – Power BI dashboards present enriched gaps for business users, enable slicing, and showcase readiness for future orchestration.
- **Data scope**: Provided `simplyr_data` and `data_late.csv` contain ~100 providers with 110+ attributes each (identity, credentialing, contracting, addresses, network, custom fields). Sample mismatches include NPI, contract status, credentialing dates, network tiers, plan participation, and demographic info.

## 2. Task / Reconciliation Layer
### 2.1 Ingestion & Validation
- **Pipelines**: Two independent ingestion jobs (Simplyr, Lake) with schema enforcement, dtype normalization (ISO dates, enumerated statuses), and canonical ID formatting (NPI zero padding, uppercased IDs). Each batch tagged with `run_id`, `ingestion_batch_id`, `source_system` (`SIMPLYR` vs `LAKE`).
- **Data quality guards**: Null thresholds on critical identifiers, UDFs for date parsing, referential validation for `group_id`, `facility_id`, and plan codes. Quarantine zone captures rows failing schema checks.
- **Normalization**: Standardize addresses (USPS rules), flatten multi-plan fields (split `PlanA,PlanC`), convert booleans (`Yes/No` → true/false), and geocode lat/long into consistent precision.

### 2.2 Recon Rule Design
- **Rule pack** mapped to dimensions:
  - **Identity**: `npi`, `first_name`, `last_name`, `gender`, `dob`.
  - **Contracting**: `contract_status`, effective/end dates, `network_flag`, `network_tier`, `plan_participation_list`.
  - **Credentialing**: `credentialing_status`, `credentialing_last_verified_date`, license info.
  - **Access & Experience**: `accepting_new_patients_flag`, `panel_status`, `telehealth_flag`, languages.
  - **Location & Contact**: practice/billing addresses, `phone`, `email`, lat/long, counties.
- **Recon table schema** (current working design):
  - `provider_id`, `field`, `simplyr_value`, `lake_value`, `gap_type`, `root_cause`, `recommendation`, `next_steps`, `owner_group`, `domain_group`, `severity_score`, `suggested_workflow`, `priority_bucket`, plus audit metadata (`rule_id`, `first_detected_ts`, `last_seen_ts`, `is_current_gap`, `evidence_json`). Partition by `business_date` (and optionally geography or owner group).
- **Sample snapshot (latest run)**:

  | provider_id | field     | simplyr_value | lake_value  | gap_type  | root_cause | recommendation | Next Steps | owner_group | domain_group | severity_score | suggested_workflow | priority_bucket |
  |-------------|-----------|---------------|-------------|-----------|------------|----------------|------------|-------------|---------------|----------------|--------------------|-----------------|
  | P100000     | npi       | 1685061829    | 1873963800  | Mismatch  | _TBD_      | _TBD_          | _TBD_      | _TBD_       | _TBD_         | _TBD_          | _TBD_              | _TBD_           |
  | P100000     | last_name | Smith         | Wong        | Mismatch  | _TBD_      | _TBD_          | _TBD_      | _TBD_       | _TBD_         | _TBD_          | _TBD_              | _TBD_           |
  | P100000     | gender    | M             | F           | Mismatch  | _TBD_      | _TBD_          | _TBD_      | _TBD_       | _TBD_         | _TBD_          | _TBD_              | _TBD_           |

  > **Note**: Root cause / recommendation columns are intentionally blank in the raw recon table. They will be populated by the agentic layer, preserving deterministic facts separately from AI enrichment.
- **Examples from data**:
  - `P100000` – NPI mismatch (`1065939459` vs `1014581341`), gender mismatch (`M` vs `U`), contract status drift (Pending vs Inactive), address differences. Severity high due to identity conflict.
  - `P100001` – Simplyr pending but Lake active; network tier and credentialing expiry out of sync; languages and telehealth flags differ.
  - `P100005` – Simplyr shows pending contract/closed panel vs Lake indicates active participation; addresses across IL/TX differ; multiple custom attributes misaligned.
- **Evidence capture**: include hashed addresses, coordinate distance, credential age in days, plan overlap analysis, etc., to support explainability downstream.

### 2.3 Deterministic Outputs
- **Metrics** captured per run: total providers processed, columns compared, gaps by type/severity, top 10 rule violations, ingestion latency.
- **Lineage**: register recon datasets in metadata catalog (e.g., Unity Catalog or Purview) to provide audit path for Power BI and future orchestration.

## 3. Intelligence / Agentic Layer
### 3.1 Inputs & Retrieval
- Agent consumes recon table + contextual slices (full provider profile, historical resolutions, policy documents). Retrieval APIs keyed by `provider_id` expose structured attributes and document embeddings (contracts, credentialing policies).
- Provide guardrails: agent must reference deterministic values; cannot override raw recon output; must cite fields (`simplyr.contract_status`, `lake.credentialing_last_verified_date`).

### 3.2 Reasoning Workflow
1. **Prefilter**: select active gaps, aggregate by provider/field, compute feature vectors (severity, gap age, impacted plans).
2. **Prompts/LLM**: craft template emphasizing business tone (“Explain what’s wrong, why it matters, next steps”). Provide domain lexicon (Credentialing, Network Ops, Provider Directory, Claims).
3. **Assignments**: heuristics + LLM classify `owner_group` and `domain_group`. Example mapping:
   - Credentialing issues → `Credentialing` owner.
   - Contract/network conflicts → `Network Ops`.
   - Demographic/address mismatches → `Provider Directory`.
   - Taxonomy/specialty mismatches affecting claims adjudication → `Claims`.
4. **Recommendations**: LLM outputs `recommended_action`, `next_steps`, `priority_bucket`, `suggested_workflow` (auto-ticket vs manual review), `confidence`, `explanation_markdown`.
5. **Feedback loop**: UI captures “accept/override” with reason, storing `human_review_status` and `feedback_text` for prompt refinement.

### 3.3 Guardrails & MLOps
- Validate recommendation references actual data; reject hallucinations or missing citations.
- Confidence adjustments: degrade if `credentialing_last_verified_date` > 365 days or conflicting data is incomplete.
- Logging: store prompt, completion, latency, cost metrics; monitor toxicity/compliance filters.
- Versioning: maintain prompt registry & evaluation harness using synthetic recon data (Healthfirst analog) to ensure consistent reasoning.
- Workflow payloads: JSON structure with provider metadata, gap summaries, recommended owner, SLA, supporting evidence. Ready for ServiceNow/Jira integration once approved.

## 4. Visualization / Business Consumption Layer
### 4.1 Data Model
- Power BI dataset built on enriched recon table (fact) + dimensions:
  - `dim_provider` (taxonomy, location, plan participation, plan status).
  - `dim_owner_group`, `dim_domain`, `dim_severity`, `dim_priority`.
  - `dim_run` (ingestion batch, timestamps, source lineage).
- Incremental refresh keyed on `run_id`/`business_date` to keep demo performant.

### 4.2 Core Experiences
1. **Executive KPIs**: cards for total gaps, critical count, avg AI confidence, workflows triggered. Trend visuals showing gap volume over time and by domain.
2. **Operations Queue**: table with provider, gap field, owner group, severity, AI recommendation, status. Filters for plan, network tier, accepting new patients, geography.
3. **Drill-through**: provider detail page with side-by-side Simplyr vs Lake values, agent explanation, workflow history, SLA countdown.
4. **Quality Insights**: charts for recurring rules, credentialing aging, plan participation mismatches, language/telehealth inconsistencies.
5. **Storytelling**: bookmarks illustrating flow (raw gaps → agent enrichment → workflow buttons). Include buttons “Export CSV”, “Push to ServiceNow”, “Acknowledge Recommendation”.

### 4.3 Future Hooks
- Reserve space for chatbot entry point (once provider chatbot ready) and workflow timeline showing automation readiness.
- Provide data export API for downstream orchestration once agentic backend is implemented.

## 5. Sample Recon & Agent Outputs (Illustrative)
| Provider | Gap | Simplyr | Lake | Severity | Owner | Recommendation |
|---------|-----|---------|------|----------|-------|----------------|
| P100000 Ana Garcia | NPI | 1065939459 | 1014581341 | Critical | Credentialing | Re-credential using Lake record; lock Simplyr updates until confirmed |
| P100000 Ana Garcia | Contract Status | Pending | Inactive | High | Network Ops | Align contract records, notify provider directory to pause updates |
| P100001 Priya Smith | Credentialing Last Verified | 1/30/2024 Expired | 4/25/2024 Expired | Medium | Credentialing | Expedite re-verification to restore network status |
| P100005 Ana Smith | Accepting Patients | Yes/Closed | No/Open | Medium | Provider Directory | Confirm panel status with facility lead; update both systems for consistency |

## 6. Operational Considerations
- **Security & Governance**: mask PII/PHI for demos; restrict Power BI access via RLS; log agent interactions for audit.
- **Runbook**: daily ingestion (Task layer) → agent enrichment job → Power BI refresh. Provide manual override procedure and escalation paths.
- **Testing**: synthetic dataset replicating sample mismatches; unit tests for rules, contract tests for schema, LLM eval set with expected outputs.
- **Scalability**: design pipelines to handle 100k+ providers via partitioning (region, group). Batch agent prompts (per provider or gap cluster) to control cost/latency.

## 7. Demo Narrative Checklist
1. **Task layer**: show recon dashboard with sample mismatches (P100000 etc.). Emphasize deterministic foundation.
2. **Agent layer**: highlight reasoning UI with recommendations, owner assignments, guardrails, and workflow suggestions.
3. **Visualization layer**: walk through Power BI screens (KPIs, queue, drill-through). Demonstrate filtering and readiness for workflow integration.
4. **Next steps**: explain roadmap to full orchestration (chatbot integration, automated workflow triggers) once client validates concept.

## 8. Recommended Next Actions
- Finalize recon schema and rule pack; generate sample recon table from provided CSVs.
- Draft prompt templates + retrieval logic using real gap examples; set up feedback capture in UI mock.
- Build Power BI prototype wired to enriched dataset; prep bookmarks telling “Input → AI → Output” story.
- Prepare Figma screens (Task, Intelligence, Visualization) to align design with narrative.
- Define evaluation metrics (precision/recall of owner classification, accuracy of recommendations) for future automation.

---
This markdown captures the full end-to-end design, data insights, and storytelling plan necessary for the HCSC demo, while leaving room for future agentic orchestration and chatbot integration once timelines allow.
