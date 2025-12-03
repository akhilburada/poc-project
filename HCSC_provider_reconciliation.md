# HCSC Provider Reconciliation Blueprint

## 1. Data Assets

### 1.1 Simplyr Operational Extract (`HCSC_provider_simplyr_data.csv`)
- 50 provider rows in sample with 110 attributes spanning identity, contracting, credentialing, participation, contact, geo, compliance, and 60 custom attributes.
- Mix of individuals, facilities, clinics, and ancillary entities; includes multi-plan participation (PlanA/PlanB/PlanC) and multi-specialty combinations.
- Key business signals:
  - Contract lifecycle (`contract_status`, `contract_effective_date`, `contract_end_date`).
  - Credentialing checkpoints (`credentialing_status`, `credentialing_last_verified_date`, `network_flag/tier`).
  - Access and consumer experience data (`accepting_new_patients_flag`, `telehealth_flag`, `languages_spoken`).
  - Regulatory IDs (DEA, Medicaid, Medicare, UPIN, CAQH, state license) and expirations.
  - Practice vs billing addresses with lat/long for geo validation.

### 1.2 Data Lake Snapshot (`HCSC_provider_data_lake.csv`)
- Mirrors Simplyr schema but sourced from centralized lake; values can drift due to ingestion latency, upstream corrections, or manual overrides.
- Contains mixed system provenance (`source_system = LAKE`, `ingestion_batch_id` series in 1400–1900 range) which is essential for lineage.
- Observed differences vs Simplyr even for the same provider IDs (e.g., `P100000` identity + contract fields).

### 1.3 Recon Table (`HCSC_provider_recon_table.csv`)
- Narrow structure capturing row-per-gap with columns: `provider_id`, `field`, `simplyr_value`, `lake_value`, `gap_type`, `root_cause`, `recommendation`, `Next Steps`, `owner_group`, `domain_group`, `severity_score`, `suggested_workflow`, `priority_bucket`.
- Current sample rows:
  - `P100000` | `npi` | Simplyr `1685061829` vs Lake `1873963800` → `Mismatch`.
  - `P100000` | `last_name` | `Smith` vs `Wong` → `Mismatch`.
  - `P100000` | `gender` | `M` vs `F` → `Mismatch`.
- Remaining enrichment columns are blank, highlighting need for agentic intelligence to populate them.

## 2. Reconciliation Layer (Task)
- **Schema Contracts**: Freeze column definitions for both sources, enforce consistent dtypes (ISO date strings, enumerations for statuses/tier flags) and canonical ID formatting (e.g., zero-padded NPIs).
- **Ingestion Controls**: Idempotent Spark/PySpark jobs per source with `run_id`, `ingestion_ts`, and `source_system`. Include schema drift alarms and quarantine zones for malformed rows.
- **Gap Taxonomy**: Rules classify deltas into categories such as `Mismatch`, `Missing in Simplyr`, `Missing in Lake`, `Stale Credential`, `Location Conflict`. Configurable rule pack stores business logic separately from code.
- **Recon Persistence**: Partition recon table by `business_date` and `provider_segment`; store supporting JSON evidence (hashes, coordinate deltas) plus audit fields (`first_detected_ts`, `last_seen_ts`, `is_current_gap`).
- **Data Quality Metrics**: Capture counts per rule, severity distributions, and compute-level stats to feed monitoring dashboards.
- **Examples**:
  - Identity drift (`npi`, `last_name`, `gender`) for `P100000` flagged as high severity.
  - Contract vs credential status misalignment (e.g., Simplyr `Active` vs Lake `Terminated`).
  - Address variations where practice/billing values diverge; lat/long used for geospatial tolerance checks.

## 3. Agentic Intelligence Layer
- **Inputs**: Recon rows + provider context (historical gaps, policy docs, SLA definitions). Provide retrieval interface keyed by `provider_id`.
- **Reasoning Flow**: Hybrid rules + LLM. Deterministic rules tag gap type/severity; LLM generates recommendation text, assigns `owner_group` (Credentialing, Network Ops, Provider Directory, Claims), and proposes remediation.
- **Outputs**: Populate recon columns `recommendation`, `Next Steps`, `owner_group`, `domain_group`, `severity_score`, `suggested_workflow`, `priority_bucket`, plus `confidence` and `explanation_markdown` fields.
- **Guardrails**: Validate that suggested actions reference actual data values, require citations of source columns, and downgrade confidence for stale verification dates (>365 days) or missing evidence.
- **Feedback Loop**: Business users approve/override recommendations; feedback stored for prompt refinement and potential fine-tuning.
- **Workflow Hooks**: Map owner groups to downstream systems (ServiceNow/Jira/Pega). Agent emits JSON payloads ready for automated ticket creation once human approval thresholds are met.

## 4. Visualization Layer (Business Consumption)
- **Dataset**: Power BI model built on enriched recon table with incremental refresh by `run_id`. Add dimensional tables for domains, severity, owner teams.
- **Core Views**:
  - Executive landing page: KPIs for open gaps, critical severity counts, agent confidence summary.
  - Operations queue: Table by owner group with triage filters (`priority_bucket`, `plan_participation_list`, `credentialing_status`).
  - Provider drill-through: Display Simplyr vs Lake values, agent explanation, workflow status, historical recurrence trend.
- **Storytelling Features**: Bookmarks to compare "pre-agent" vs "post-agent" recon states, highlight overrides, and show downstream workflow triggers.
- **Adoption Tools**: Export options (CSV/Power Automate), SLA timers, and RLS so teams only see relevant providers.

## 5. Cross-Cutting Considerations
- **Data Governance**: Mask PII/PHI for demos, enforce least-privilege access, log all agent decisions for audit.
- **Observability**: Monitor ingestion latency, rule failure spikes, agent inference errors, and Power BI refresh health.
- **Testing**: Maintain synthetic datasets mirroring Simplyr/Lake anomalies for regression and LLM evaluation; implement golden-set assertions for key rule packs.
- **Runbook**: Document batch schedules, manual remediation steps, escalation path for critical gaps, and recovery procedures (re-run recon, replay agent enrichment, refresh BI).

## 6. Demo Preparation Checklist
1. Generate refreshed recon table using provided CSVs and highlight representative gaps (identity, credentialing, address, network tier).
2. Mock agent enrichment for selected rows (fill recommendation/owner/severity/workflow fields) to showcase layer-two intelligence even before full automation.
3. Wire Power BI to enriched table; create bookmarks that narrate the three-layer story (Task → Intelligence → Visualization).
4. Prepare talking points mapping demo screens to eventual agentic automation roadmap, emphasizing how manual UI steps will transition to orchestrated agents post sign-off.
