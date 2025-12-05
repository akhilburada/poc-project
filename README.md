# HCSC Provider Data Reconciliation Opportunity — Architectural Analysis

## 1. Client Ask & Business Context
- HCSC wants a production-feasible reconciliation solution inspired by the prior Healthfirst demo but anchored in a clearer three-layer architecture (Task → Intelligence → Visualization).
- Primary objective: compare provider data between SimplyR (presumably Provider Data Management source) and the enterprise Data Lake, flag gaps, and turn those gaps into business-ready insights.
- Expectation: demonstrate an agentic/intelligent layer that can interpret deterministic reconciliation output, enrich it with recommendations, and signal ownership domains (Credentialing, Network Operations, Provider Directory, Claims).
- Engagement is pre-sales/demo oriented with expectations of a near-term remote demo (target: first or second week of December) using realistic mock data if necessary but explaining the agentic path to production.

## 2. Underlying Problem Statement
- Provider records across systems (SimplyR vs Data Lake) drift, causing inaccurate directories, credentialing delays, claim denials, and network management issues.
- Existing teams may already run isolated chatbot or data initiatives, but there is no cohesive reconciliation workflow with automated interpretation and remediation guidance.
- HCSC needs a deterministic baseline to build trust (task layer) and an AI-driven interpretation layer to translate technical gaps into actionable business narratives and next steps.
- Longer term, they anticipate workflow automation/orchestration triggered off the enriched gap data, but immediate need is analytic clarity and storytelling that resonates with business stakeholders.

## 3. Expected Outcomes (Near-Term Demo)
- **Recon Table Output**: A structured dataset showing each provider/entity gap, the discrepancy type, severity, and source references.
- **Agentic Enrichment**: For every gap, AI-generated recommendations, ownership cues, and domain grouping that business teams immediately understand.
- **Business Visualization**: Power BI dashboard consuming the enriched recon table, enabling slicing/filtering by domain, severity, geography, provider type, etc.
- **Demo Narrative**: Start from Visualization (what business sees), drill into Intelligence Layer behavior (how the agent reasons over recon rows), and ground everything on the Task Layer’s deterministic pipeline to prove trustworthiness.
- **Future-State Teaser**: Show how the same enriched dataset can trigger automated workflows once orchestration is prioritized.

## 4. Architectural Approach

### 4.1 Three-Layer Stack
1. **Task / Reconciliation Layer (Non-AI)**
   - Spark or Python-based jobs run before any agent execution.
   - Responsibilities: ingest parallel snapshots from SimplyR & Data Lake, standardize schemas, perform record-level and attribute-level comparisons, and publish a normalized “Recon Table”.
   - Deterministic outputs provide confidence and isolate heavy compute from the agentic layer.

2. **Intelligence / Agentic Layer (AI Enrichment)**
   - Reads recon table rows as the base context.
   - Applies domain-specific logic (rules + LLM-based reasoning) to:
     - Bucketize gap types (missing credential data, directory inconsistency, contract mismatch, etc.).
     - Assign ownership domain (Credentialing, Network Ops, Provider Directory, Claims) based on impact signals and metadata.
     - Generate remediation recommendations (e.g., “Initiate re-credentialing workflow”, “Sync taxonomy codes from source X”).
     - Provide next-step cues (who approves, data needed, suggested SLAs).
   - Writes enriched insights back to the recon table (additional columns or JSON payload), enabling downstream consumption.

3. **Visualization / Business Consumption Layer**
   - Power BI (or equivalent) connects to the enriched recon table.
   - Purpose: display heatmaps of gaps, drilldowns per domain, status tracking, and ability to export action lists.
   - Serves as the storytelling surface for business stakeholders; sets the stage for later integration with orchestration/workflow tools.

### 4.2 Data Flow Overview
1. Source extracts from SimplyR and the Data Lake feed the reconciliation batch job.
2. Reconciliation job runs rule-based comparisons (e.g., provider demographic fields, credential status, network participation) and logs discrepancies.
3. Recon table (deterministic output) is stored in a governed location accessible to both agents and BI.
4. Intelligence layer agent pulls batches of unresolved gaps, combines structured fields with relevant provider context (lookup tables, historical actions), and uses AI reasoning + templates/prompts to enrich each record.
5. Enriched recon rows are published back (overwriting or appending columns) and versioned for auditability.
6. Power BI dashboard reads enriched recon data and powers the demo as well as eventual business workflows.

### 4.3 Intelligence Layer Design Considerations
- **Input Schema**: recon_record_id, provider_id, gap_type, attribute_pair (SimplyR vs Lake values), severity, timestamps.
- **Augmented Fields**: domain_bucket, recommended_action, confidence_score, urgency, suggested_owner, rationale_summary.
- **Agent Skills**:
  - Gap interpretation: classify type/severity using deterministic cues first, fall back to LLM classification for nuanced cases.
  - Domain grouping: map impact to Credentialing/Network Ops/Directory/Claims via rules (e.g., credentialing indicators) plus LLM reasoning for ambiguous records.
  - Recommendation generation: combine playbook templates with gap context to produce explainable, business-friendly guidance.
  - Provenance tracking: store prompt/response metadata or reasoning trace for transparency during demo.
- **Guardrails**: enforce deterministic overrides when rules exist, use LLM only where patterns are variable; maintain JSON schemas for enriched payload.

## 5. Demo Storyline & Readiness Plan
- **Step 1 (Visualization-first)**: Begin with the Power BI dashboard to show immediate business value—highlight domain filters and sample gap cards.
- **Step 2 (Intelligence Deep Dive)**: Narrate how the agent ingests recon entries, uses prompts/playbooks, and updates the table. Showcase example records traveling through enrichment.
- **Step 3 (Task Layer Foundation)**: Briefly explain the deterministic reconciliation process (Spark/Python job, schema alignment, gap detection) to reinforce data trust.
- **Data Preparation**: In coming weeks, craft realistic sample datasets for SimplyR and Data Lake, define the recon table schema, and preload sample gaps to drive both the agent demo and Power BI visuals.
- **Delivery Mode**: Remote demo (~30 minutes) with mock/seeded data is acceptable as long as the agentic logic and future automation path are clearly articulated.

## 6. Risks, Assumptions, and Open Questions
- **Time Constraint**: true end-to-end agent automation may exceed the December timeline; demo will likely rely on simulated agent runs with transparent explanation of production path.
- **Environment Access**: No orchestration layer or secured infrastructure is currently available; need clarity on where the recon and agent layers would eventually run (Azure/AWS?).
- **Data Availability**: Access to actual SimplyR/Data Lake extracts is unclear; plan hinges on synthetic yet believable samples.
- **Stakeholder Expectations**: Primary audience has business delivery background; messaging must stay business-oriented while proving technical rigor.
- **Chatbot Scope**: Provider chatbot is a separate need; ensure reconciliation demo remains focused to avoid scope creep.
- **Future Workflow Automation**: Need to articulate integration points (e.g., ServiceNow, PEGA) even if not implemented, since they expect eventual automated workflows.

## 7. Next Steps Before Solutioning
1. Finalize recon table schema and data contracts between Task and Intelligence layers.
2. Define enrichment taxonomy (gap categories, domain mapping rules, recommendation templates).
3. Outline agent prompt/logic flow, including checkpoints for deterministic overrides.
4. Prepare sample recon dataset and Power BI visuals aligning with the narrative.
5. Align stakeholders on demo cadence, artifacts to share (e.g., downloadable enriched file), and post-demo follow-up for orchestration discussions.

This document captures the current understanding of the client’s needs, the core problem they are addressing, the outcomes they expect from the upcoming engagement, and the architectural stance that keeps the deterministic task layer decoupled from the AI-driven intelligence layer while ensuring business-ready visualization.
