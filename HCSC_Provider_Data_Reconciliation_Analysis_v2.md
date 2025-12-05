# HCSC Provider Data Reconciliation Solution
## Deep Analysis & Architectural Understanding - Version 2.0
### (Incorporating Actual Data Structure Analysis)

**Document Version:** 2.0  
**Date:** December 5, 2025  
**Author:** AI Architect  
**Status:** Analysis Phase - Data-Informed

---

## Executive Summary

This updated analysis incorporates a deep review of the actual **Simplyr**, **Data Lake**, and **Recon Table** datasets provided. The analysis reveals a complex provider data structure with 120+ fields per record, spanning multiple business domains. The reconciliation challenge is significant due to the breadth of data and the need for intelligent interpretation of discrepancies.

---

## 1. Data Structure Deep Analysis

### 1.1 Schema Overview

Both Simplyr and Data Lake share an identical schema structure with **120 columns**:

| Category | Field Count | Description |
|----------|-------------|-------------|
| Core Identity | 7 | provider_id, npi, first_name, last_name, middle_name, suffix, gender |
| Demographics | 2 | dob, tin, tin_type |
| Organization | 2 | group_id, facility_id |
| Contract/Network | 7 | contract_status, contract_effective_date, contract_end_date, network_flag, network_tier, plan_participation_list, panel_status |
| Credentialing | 2 | credentialing_status, credentialing_last_verified_date |
| Taxonomy/Specialty | 4 | taxonomy_code_primary, taxonomy_code_secondary, specialty_primary, specialty_secondary |
| Practice Info | 4 | accepting_new_patients_flag, languages_spoken, telehealth_flag, email |
| Contact | 2 | phone, fax |
| Practice Address | 6 | practice_address_line1/2, practice_city, practice_state, practice_zip, practice_county |
| Billing Address | 6 | billing_address_line1/2, billing_city, billing_state, billing_zip, billing_county |
| Geolocation | 2 | latitude, longitude |
| Regulatory IDs | 5 | dea_number, medicaid_id, medicare_id, upin, caqh_id |
| License | 3 | license_number, license_state, license_expiration_date |
| Classification | 3 | provider_type, provider_category, time_zone |
| Metadata | 3 | last_update_ts, ingestion_batch_id, source_system |
| Custom Attributes | 60 | custom_attribute_61 through custom_attribute_120 |

### 1.2 Sample Data Comparison (P100000)

Examining the first record reveals significant discrepancies between Simplyr and Data Lake:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ PROVIDER P100000 - SIDE-BY-SIDE COMPARISON                                  │
├─────────────────────┬──────────────────────┬────────────────────────────────┤
│ FIELD               │ SIMPLYR              │ DATA LAKE                      │
├─────────────────────┼──────────────────────┼────────────────────────────────┤
│ npi                 │ 1065939459           │ 1014581341          ⚠️ MISMATCH│
│ first_name          │ Ana                  │ Ana                  ✓ MATCH   │
│ last_name           │ Garcia               │ Garcia               ✓ MATCH   │
│ suffix              │ DO                   │ (empty)              ⚠️ MISSING │
│ gender              │ M                    │ U                    ⚠️ MISMATCH│
│ dob                 │ 1/1/1962             │ 1/1/1994             ⚠️ MISMATCH│
│ tin                 │ 534360412            │ 260622691            ⚠️ MISMATCH│
│ group_id            │ G1010                │ G1082                ⚠️ MISMATCH│
│ facility_id         │ F2037                │ F2013                ⚠️ MISMATCH│
│ contract_status     │ Pending              │ Inactive             ⚠️ MISMATCH│
│ contract_eff_date   │ 4/8/2022             │ 9/4/2021             ⚠️ MISMATCH│
│ credentialing_status│ Verified             │ Expired              ⚠️ MISMATCH│
│ network_tier        │ Standard             │ Tier1                ⚠️ MISMATCH│
│ taxonomy_primary    │ 1223S0112X           │ 1223S0112X           ✓ MATCH   │
│ specialty_primary   │ Family Medicine      │ Orthopedics          ⚠️ MISMATCH│
│ plan_participation  │ PlanA                │ PlanC                ⚠️ MISMATCH│
│ accepting_new_pts   │ No                   │ Yes                  ⚠️ MISMATCH│
│ languages_spoken    │ Mandarin             │ English              ⚠️ MISMATCH│
│ telehealth_flag     │ Yes                  │ Yes                  ✓ MATCH   │
│ phone               │ (empty)              │ 2125551212           ⚠️ MISSING │
│ practice_city       │ Dallas               │ Dallas               ✓ MATCH   │
│ practice_state      │ IL                   │ NY                   ⚠️ MISMATCH│
│ practice_zip        │ 10400                │ 76000                ⚠️ MISMATCH│
│ license_state       │ IL                   │ TX                   ⚠️ MISMATCH│
│ provider_type       │ Facility             │ Ancillary            ⚠️ MISMATCH│
│ provider_category   │ Specialist           │ Facility             ⚠️ MISMATCH│
│ source_system       │ SIMPLYR              │ LAKE                 ✓ EXPECTED│
└─────────────────────┴──────────────────────┴────────────────────────────────┘
```

### 1.3 Critical Observation: Data Quality Issue

**⚠️ IMPORTANT FINDING:** The sample data appears to be **synthetic/test data** with randomized values, as evidenced by:
- Same `provider_id` (P100000) has completely different NPIs, TINs, and DOBs
- Specialties don't align with taxonomy codes
- Geographic inconsistencies (Dallas, IL doesn't exist)

**Implication for Solution Design:**
- The reconciliation logic must handle scenarios where records have the same `provider_id` but vastly different data
- The Intelligence Layer must determine **which source is authoritative** for each field type
- Root cause analysis becomes critical (is this a data sync issue or two different providers?)

---

## 2. Recon Table Structure Analysis

### 2.1 Current Recon Table Schema

The provided recon table shows a **two-phase structure**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         RECON TABLE STRUCTURE                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ PHASE 1: TASK LAYER OUTPUT (Populated by Reconciliation Job)       │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │ provider_id    │ Unique provider identifier                        │   │
│  │ field          │ Name of the field with discrepancy                │   │
│  │ simplyr_value  │ Value from Simplyr source system                  │   │
│  │ lake_value     │ Value from Data Lake                              │   │
│  │ gap_type       │ Type of gap (Mismatch, Missing, etc.)             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ PHASE 2: INTELLIGENCE LAYER AUGMENTATION (Populated by AI Agent)   │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │ root_cause         │ AI-identified reason for the discrepancy      │   │
│  │ recommendation     │ Specific action to resolve the gap            │   │
│  │ next_steps         │ Detailed steps for resolution                 │   │
│  │ owner_group        │ Team/role responsible for resolution          │   │
│  │ domain_group       │ Business domain classification                │   │
│  │ severity_score     │ Numeric severity (1-10 or similar)            │   │
│  │ suggested_workflow │ Workflow to trigger for resolution            │   │
│  │ priority_bucket    │ Priority classification (Critical/High/Med/Low)│   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Gap Types Identified

Based on the data structure, the following gap types should be detected:

| Gap Type | Description | Example |
|----------|-------------|---------|
| **Mismatch** | Both values exist but differ | NPI: 1065939459 vs 1014581341 |
| **Missing_In_Lake** | Value in Simplyr, NULL/empty in Lake | Simplyr has DEA, Lake is empty |
| **Missing_In_Simplyr** | Value in Lake, NULL/empty in Simplyr | Simplyr phone empty, Lake has value |
| **Format_Difference** | Same data, different format | Phone: 212-555-1212 vs 2125551212 |
| **Case_Difference** | Same data, different case | "Family Medicine" vs "FAMILY MEDICINE" |
| **Stale_Data** | Value in Lake older than threshold | Lake last_update older than 90 days |

---

## 3. Field-to-Domain Mapping (Refined Based on Actual Schema)

### 3.1 Domain Classification Matrix

Based on the actual fields in the dataset:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FIELD-TO-DOMAIN CLASSIFICATION MATRIX                    │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ DOMAIN: CREDENTIALING                                                       │
│ Owner: Credentialing Team                                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ Fields:                                                                     │
│   • credentialing_status          • license_number                          │
│   • credentialing_last_verified   • license_state                           │
│   • dea_number                    • license_expiration_date                 │
│   • caqh_id                       • taxonomy_code_primary                   │
│   • medicaid_id                   • taxonomy_code_secondary                 │
│   • medicare_id                   • upin                                    │
│                                                                             │
│ Business Impact: Compliance, Regulatory, Provider Enrollment                │
│ Severity Multiplier: HIGH (regulatory implications)                         │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ DOMAIN: NETWORK OPERATIONS                                                  │
│ Owner: Network Management Team                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ Fields:                                                                     │
│   • contract_status               • network_flag                            │
│   • contract_effective_date       • network_tier                            │
│   • contract_end_date             • plan_participation_list                 │
│   • group_id                      • panel_status                            │
│   • facility_id                   • accepting_new_patients_flag             │
│                                                                             │
│ Business Impact: Network Adequacy, Contract Compliance, Member Access      │
│ Severity Multiplier: HIGH (affects member access to care)                   │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ DOMAIN: PROVIDER DIRECTORY                                                  │
│ Owner: Directory Management Team                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ Fields:                                                                     │
│   • first_name, last_name         • practice_address_line1/2                │
│   • middle_name, suffix           • practice_city, practice_state           │
│   • gender                        • practice_zip, practice_county           │
│   • specialty_primary/secondary   • phone, fax, email                       │
│   • languages_spoken              • latitude, longitude                     │
│   • telehealth_flag               • provider_type, provider_category        │
│   • time_zone                                                               │
│                                                                             │
│ Business Impact: Member Experience, Directory Accuracy, CMS Compliance     │
│ Severity Multiplier: MEDIUM-HIGH (member-facing, regulatory)               │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ DOMAIN: CLAIMS                                                              │
│ Owner: Claims Operations Team                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│ Fields:                                                                     │
│   • npi                           • billing_city, billing_state             │
│   • tin, tin_type                 • billing_zip, billing_county             │
│   • billing_address_line1/2       • dob (for provider validation)           │
│                                                                             │
│ Business Impact: Claims Processing, Payment Accuracy, Fraud Prevention     │
│ Severity Multiplier: CRITICAL (financial implications)                      │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ DOMAIN: METADATA / SYSTEM                                                   │
│ Owner: Data Operations Team                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ Fields:                                                                     │
│   • provider_id                   • source_system                           │
│   • last_update_ts                • custom_attribute_61 through 120         │
│   • ingestion_batch_id                                                      │
│                                                                             │
│ Business Impact: Data Lineage, Audit Trail, System Health                  │
│ Severity Multiplier: LOW (operational, not business-critical)              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Multi-Domain Fields

Some fields impact multiple domains:

| Field | Primary Domain | Secondary Domain(s) | Notes |
|-------|---------------|---------------------|-------|
| npi | Claims | Credentialing, Directory | Universal provider identifier |
| tin | Claims | Network Ops | Tax/financial identity |
| specialty_primary | Directory | Credentialing, Network | Affects directory display AND network adequacy |
| practice_address | Directory | Claims, Credentialing | Location impacts all domains |
| license_state | Credentialing | Network Ops | Determines practice authorization |
| contract_status | Network Ops | Claims | Affects payment eligibility |

---

## 4. Intelligence Layer Design (Detailed)

### 4.1 Agent Processing Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    INTELLIGENCE LAYER PROCESSING FLOW                       │
└─────────────────────────────────────────────────────────────────────────────┘

INPUT: Single gap record from Recon Table
┌─────────────────────────────────────────────────────────────────────────────┐
│ {                                                                           │
│   "provider_id": "P100000",                                                 │
│   "field": "npi",                                                           │
│   "simplyr_value": "1065939459",                                            │
│   "lake_value": "1014581341",                                               │
│   "gap_type": "Mismatch"                                                    │
│ }                                                                           │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 1: CONTEXT ENRICHMENT                                                  │
│ ────────────────────────────────────────────────────────────────────────── │
│ Fetch full provider record from both sources:                               │
│   • Simplyr full record for P100000                                         │
│   • Data Lake full record for P100000                                       │
│   • Other gaps for same provider (if any)                                   │
│   • Historical data (if available)                                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 2: ROOT CAUSE ANALYSIS AGENT                                           │
│ ────────────────────────────────────────────────────────────────────────── │
│ Prompt:                                                                     │
│ "Analyze this data discrepancy for provider P100000:                        │
│  Field: npi                                                                 │
│  Simplyr Value: 1065939459                                                  │
│  Lake Value: 1014581341                                                     │
│  Gap Type: Mismatch                                                         │
│                                                                             │
│  Additional Context:                                                        │
│  - Simplyr last updated: 1/16/2025                                          │
│  - Lake last updated: 3/18/2025                                             │
│  - Other mismatches for this provider: 15 fields                            │
│                                                                             │
│  Determine the most likely root cause:                                      │
│  - Data sync failure                                                        │
│  - Source system update not propagated                                      │
│  - Data entry error                                                         │
│  - Merge/split of provider records                                          │
│  - Historical data overwrite                                                │
│  - Different data collection sources"                                       │
│                                                                             │
│ Output: root_cause = "Data sync failure - Simplyr record updated after      │
│         Lake ingestion; 15+ field mismatches suggest full record sync issue"│
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 3: DOMAIN CLASSIFICATION AGENT                                         │
│ ────────────────────────────────────────────────────────────────────────── │
│ Prompt:                                                                     │
│ "Classify this gap into business domains:                                   │
│  Field: npi                                                                 │
│  Gap Type: Mismatch                                                         │
│                                                                             │
│  Available Domains:                                                         │
│  - Credentialing (licenses, certifications, regulatory IDs)                 │
│  - Network Operations (contracts, network status, participation)            │
│  - Provider Directory (name, address, contact, specialties)                 │
│  - Claims (NPI, TIN, billing address, payment info)                         │
│                                                                             │
│  Determine:                                                                 │
│  1. Primary domain                                                          │
│  2. Secondary domains (if applicable)                                       │
│  3. Owner team/group"                                                       │
│                                                                             │
│ Output:                                                                     │
│   domain_group = "Claims"                                                   │
│   secondary_domains = ["Credentialing", "Provider Directory"]               │
│   owner_group = "Claims Operations"                                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 4: SEVERITY SCORING AGENT                                              │
│ ────────────────────────────────────────────────────────────────────────── │
│ Scoring Factors:                                                            │
│   • Field criticality (NPI = Critical, custom_attr = Low)                   │
│   • Domain multiplier (Claims = 1.5x, Directory = 1.2x)                     │
│   • Gap type severity (Mismatch = High, Format = Low)                       │
│   • Provider type impact (Active contract = High)                           │
│   • Downstream dependencies (Claims processing = Critical)                  │
│                                                                             │
│ Calculation:                                                                │
│   base_score = 8 (NPI is critical identifier)                               │
│   domain_multiplier = 1.5 (Claims domain)                                   │
│   gap_type_factor = 1.2 (Mismatch)                                          │
│   severity_score = min(10, 8 * 1.5 * 1.2) = 10                              │
│                                                                             │
│ Output:                                                                     │
│   severity_score = 10                                                       │
│   priority_bucket = "Critical"                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 5: RECOMMENDATION AGENT                                                │
│ ────────────────────────────────────────────────────────────────────────── │
│ Prompt:                                                                     │
│ "Generate a specific, actionable recommendation for this gap:               │
│  Field: npi                                                                 │
│  Gap Type: Mismatch                                                         │
│  Root Cause: Data sync failure                                              │
│  Domain: Claims                                                             │
│  Severity: Critical                                                         │
│                                                                             │
│  Context:                                                                   │
│  - Simplyr is the source of truth for provider data                         │
│  - NPI is a critical identifier for claims processing                       │
│  - Mismatch could cause claims rejections                                   │
│                                                                             │
│  Provide:                                                                   │
│  1. Clear recommendation (what to do)                                       │
│  2. Next steps (how to do it)                                               │
│  3. Suggested workflow (if applicable)"                                     │
│                                                                             │
│ Output:                                                                     │
│   recommendation = "Update Data Lake NPI to match Simplyr value.            │
│                     Simplyr (1065939459) is authoritative. Verify NPI       │
│                     against NPPES registry before update."                  │
│                                                                             │
│   next_steps = "1. Validate Simplyr NPI against NPPES database              │
│                 2. If valid, trigger Data Lake sync for P100000             │
│                 3. Verify downstream systems (Claims, Credentialing)        │
│                 4. Document root cause for future prevention"               │
│                                                                             │
│   suggested_workflow = "WF_NPI_CORRECTION_CRITICAL"                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
OUTPUT: Enriched gap record
┌─────────────────────────────────────────────────────────────────────────────┐
│ {                                                                           │
│   "provider_id": "P100000",                                                 │
│   "field": "npi",                                                           │
│   "simplyr_value": "1065939459",                                            │
│   "lake_value": "1014581341",                                               │
│   "gap_type": "Mismatch",                                                   │
│   "root_cause": "Data sync failure - Simplyr updated after Lake ingestion", │
│   "recommendation": "Update Data Lake NPI to match Simplyr. Verify NPPES.", │
│   "next_steps": "1. Validate NPPES, 2. Trigger sync, 3. Verify downstream", │
│   "owner_group": "Claims Operations",                                       │
│   "domain_group": "Claims",                                                 │
│   "severity_score": 10,                                                     │
│   "suggested_workflow": "WF_NPI_CORRECTION_CRITICAL",                       │
│   "priority_bucket": "Critical"                                             │
│ }                                                                           │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Recommendation Templates by Domain

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    RECOMMENDATION TEMPLATES BY DOMAIN                       │
└─────────────────────────────────────────────────────────────────────────────┘

CREDENTIALING DOMAIN:
├── License Mismatch
│   └── "Verify license status with state board. If Simplyr is current,
│        update Lake. Flag for credentialing review if discrepancy is >30 days."
├── DEA Number Missing
│   └── "DEA number present in Simplyr but missing in Lake. Required for
│        controlled substance prescribing. Priority update to Lake."
└── Credentialing Status Conflict
    └── "Credentialing status differs: Simplyr={val1}, Lake={val2}. Contact
         credentialing team to confirm current status. Do not update until
         verified with primary source documentation."

NETWORK OPERATIONS DOMAIN:
├── Contract Status Mismatch
│   └── "Contract status discrepancy may affect claims payment. Simplyr shows
│        {val1}, Lake shows {val2}. Verify with contract management system
│        before updating. If active in Simplyr, expedite Lake sync."
├── Network Tier Difference
│   └── "Network tier affects member cost-sharing. Verify current contract
│        terms and update Lake to match Simplyr. Notify member services of
│        potential impact."
└── Panel Status Conflict
    └── "Panel status determines new patient acceptance. Discrepancy may
         cause member dissatisfaction. Verify with practice and update."

PROVIDER DIRECTORY DOMAIN:
├── Address Mismatch
│   └── "Practice address differs between systems. Verify current address
│        with provider. Update both systems if outdated. Consider geocoding
│        validation."
├── Phone/Contact Missing
│   └── "Contact information missing in {system}. Members cannot reach
│        provider. Priority outreach to provider for current contact info."
└── Specialty Mismatch
    └── "Specialty classification differs. Affects member search results.
         Verify with credentialing records and update directory."

CLAIMS DOMAIN:
├── NPI Mismatch [CRITICAL]
│   └── "NPI mismatch will cause claims rejections. Validate against NPPES.
│        Update Lake immediately if Simplyr is correct. Monitor for claims
│        impact."
├── TIN Mismatch [CRITICAL]
│   └── "Tax ID mismatch affects payment routing. Verify with W-9 on file.
│        Update Lake after validation. Alert finance team."
└── Billing Address Mismatch
    └── "Billing address affects remittance delivery. Verify with provider
         and update. Lower priority than NPI/TIN but should be resolved."
```

---

## 5. Severity Scoring Model

### 5.1 Field Criticality Weights

| Field Category | Weight | Rationale |
|----------------|--------|-----------|
| NPI | 10 | Universal identifier, claims rejection risk |
| TIN | 10 | Payment routing, fraud risk |
| License Number/State | 9 | Regulatory compliance |
| DEA Number | 9 | Controlled substance compliance |
| Contract Status | 8 | Network participation, claims payment |
| Credentialing Status | 8 | Provider eligibility |
| Specialty | 7 | Directory accuracy, network adequacy |
| Practice Address | 6 | Member experience, directory accuracy |
| Phone/Email | 5 | Member communication |
| Name Fields | 4 | Identity, but less operational impact |
| Custom Attributes | 2 | Typically operational metadata |

### 5.2 Severity Calculation Formula

```
severity_score = min(10, 
    field_weight 
    × gap_type_multiplier 
    × domain_priority_factor 
    × recency_factor
)

Where:
  gap_type_multiplier:
    - Mismatch (critical field): 1.3
    - Mismatch (non-critical): 1.0
    - Missing_In_Lake: 1.2
    - Missing_In_Simplyr: 1.1
    - Format_Difference: 0.5
    
  domain_priority_factor:
    - Claims: 1.3
    - Credentialing: 1.2
    - Network Ops: 1.1
    - Directory: 1.0
    
  recency_factor:
    - Gap detected in last 7 days: 1.0
    - Gap older than 7 days: 1.1
    - Gap older than 30 days: 1.3
```

### 5.3 Priority Buckets

| Score Range | Priority Bucket | SLA | Action |
|-------------|-----------------|-----|--------|
| 9-10 | Critical | 24 hours | Immediate escalation |
| 7-8 | High | 72 hours | Prioritized resolution |
| 4-6 | Medium | 1 week | Standard queue |
| 1-3 | Low | 2 weeks | Batch processing |

---

## 6. Sample Enriched Recon Table (Expected Output)

Based on the sample data provided, here's how the enriched recon table should look:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                                        ENRICHED RECON TABLE - SAMPLE OUTPUT                                                                                     │
├─────────────┬───────────────────┬────────────────┬────────────────┬──────────┬─────────────────────────────────────┬─────────────────────────────────────────┬───────────────────┬──────────────┤
│ provider_id │ field             │ simplyr_value  │ lake_value     │ gap_type │ root_cause                          │ recommendation                          │ domain_group      │ severity     │
├─────────────┼───────────────────┼────────────────┼────────────────┼──────────┼─────────────────────────────────────┼─────────────────────────────────────────┼───────────────────┼──────────────┤
│ P100000     │ npi               │ 1065939459     │ 1014581341     │ Mismatch │ Data sync failure. Multiple field   │ CRITICAL: Validate Simplyr NPI against  │ Claims            │ 10 CRITICAL  │
│             │                   │                │                │          │ mismatches suggest full record not  │ NPPES. Update Lake immediately.         │                   │              │
│             │                   │                │                │          │ synced. Lake updated later but with │ Monitor for claims rejections.          │                   │              │
│             │                   │                │                │          │ different source data.              │                                         │                   │              │
├─────────────┼───────────────────┼────────────────┼────────────────┼──────────┼─────────────────────────────────────┼─────────────────────────────────────────┼───────────────────┼──────────────┤
│ P100000     │ tin               │ 534360412      │ 260622691      │ Mismatch │ Tax ID mismatch indicates possible  │ CRITICAL: Verify TIN with W-9 on file.  │ Claims            │ 10 CRITICAL  │
│             │                   │                │                │          │ different legal entities or data    │ Do not process payments until resolved. │                   │              │
│             │                   │                │                │          │ entry error. High fraud risk.       │ Escalate to Finance if no resolution.   │                   │              │
├─────────────┼───────────────────┼────────────────┼────────────────┼──────────┼─────────────────────────────────────┼─────────────────────────────────────────┼───────────────────┼──────────────┤
│ P100000     │ gender            │ M              │ U              │ Mismatch │ Lake has Unknown gender. Simplyr    │ Update Lake with Simplyr value (M).     │ Provider Directory│ 4 MEDIUM     │
│             │                   │                │                │          │ has Male. Likely data quality issue │ Low priority but affects directory.     │                   │              │
│             │                   │                │                │          │ in Lake ingestion.                  │                                         │                   │              │
├─────────────┼───────────────────┼────────────────┼────────────────┼──────────┼─────────────────────────────────────┼─────────────────────────────────────────┼───────────────────┼──────────────┤
│ P100000     │ credentialing_    │ Verified       │ Expired        │ Mismatch │ Critical status mismatch. Simplyr   │ HIGH: Verify current credentialing      │ Credentialing     │ 9 CRITICAL   │
│             │ status            │                │                │          │ shows active/verified but Lake      │ status. If Verified, update Lake        │                   │              │
│             │                   │                │                │          │ shows Expired. Provider may be      │ immediately. Provider may be incorrectly│                   │              │
│             │                   │                │                │          │ incorrectly excluded from network.  │ excluded from claims processing.        │                   │              │
├─────────────┼───────────────────┼────────────────┼────────────────┼──────────┼─────────────────────────────────────┼─────────────────────────────────────────┼───────────────────┼──────────────┤
│ P100000     │ specialty_        │ Family Medicine│ Orthopedics    │ Mismatch │ Major specialty discrepancy. Either │ HIGH: Verify board certification and    │ Provider Directory│ 8 HIGH       │
│             │ primary           │                │                │          │ incorrect classification or data    │ taxonomy code. Update incorrect system. │ + Credentialing   │              │
│             │                   │                │                │          │ from different providers merged.    │ Affects network adequacy reporting.     │                   │              │
├─────────────┼───────────────────┼────────────────┼────────────────┼──────────┼─────────────────────────────────────┼─────────────────────────────────────────┼───────────────────┼──────────────┤
│ P100000     │ contract_status   │ Pending        │ Inactive       │ Mismatch │ Contract status affects claims      │ HIGH: Verify contract status with       │ Network Ops       │ 8 HIGH       │
│             │                   │                │                │          │ payment. Pending vs Inactive have   │ contracting team. If Pending, provider  │                   │              │
│             │                   │                │                │          │ different payment implications.     │ should not be in-network for claims.    │                   │              │
├─────────────┼───────────────────┼────────────────┼────────────────┼──────────┼─────────────────────────────────────┼─────────────────────────────────────────┼───────────────────┼──────────────┤
│ P100000     │ practice_state    │ IL             │ NY             │ Mismatch │ State mismatch affects licensure    │ MEDIUM: Verify practice location.       │ Provider Directory│ 6 MEDIUM     │
│             │                   │                │                │          │ validation and member search.       │ Check license_state alignment.          │ + Credentialing   │              │
│             │                   │                │                │          │ May indicate multi-state practice.  │ Update directory for accurate search.   │                   │              │
├─────────────┼───────────────────┼────────────────┼────────────────┼──────────┼─────────────────────────────────────┼─────────────────────────────────────────┼───────────────────┼──────────────┤
│ P100000     │ phone             │ (empty)        │ 2125551212     │ Missing  │ Phone missing in Simplyr but exists │ LOW: Backfill Simplyr with Lake value.  │ Provider Directory│ 3 LOW        │
│             │                   │                │ _In_Simplyr    │          │ in Lake. Lake may have more recent  │ Verify number is current before update. │                   │              │
│             │                   │                │                │          │ contact information.                │                                         │                   │              │
└─────────────┴───────────────────┴────────────────┴────────────────┴──────────┴─────────────────────────────────────┴─────────────────────────────────────────┴───────────────────┴──────────────┘
```

---

## 7. Power BI Visualization Design

### 7.1 Dashboard Layout

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PROVIDER DATA RECONCILIATION DASHBOARD                   │
│                         Last Refreshed: 12/05/2025 09:30 AM                 │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ EXECUTIVE SUMMARY                                                           │
├───────────────┬───────────────┬───────────────┬───────────────┬─────────────┤
│ ⚠️  CRITICAL   │ 🔴 HIGH       │ 🟡 MEDIUM     │ 🟢 LOW        │ ✅ RESOLVED │
│     127       │     342       │     589       │     201       │    1,247    │
│   (+15 today) │  (+23 today)  │  (-12 today)  │  (+5 today)   │ (+89 today) │
└───────────────┴───────────────┴───────────────┴───────────────┴─────────────┘

┌─────────────────────────────────┬───────────────────────────────────────────┐
│ GAPS BY DOMAIN                  │ GAPS BY ROOT CAUSE                        │
│ ┌─────────────────────────────┐ │ ┌─────────────────────────────────────┐   │
│ │ ████████████████ Claims 35%│ │ │ Data Sync Failure      ████████ 42% │   │
│ │ ████████████░░░ Cred.  28% │ │ │ Source System Delay    █████░░░ 28% │   │
│ │ ██████████░░░░░ Network 22%│ │ │ Data Entry Error       ███░░░░░ 15% │   │
│ │ ██████░░░░░░░░░ Directory15%│ │ │ Format Mismatch        ██░░░░░░ 10% │   │
│ └─────────────────────────────┘ │ │ Unknown                █░░░░░░░  5% │   │
│                                 │ └─────────────────────────────────────┘   │
└─────────────────────────────────┴───────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ CRITICAL GAPS REQUIRING IMMEDIATE ACTION                    [View All →]    │
├─────────────┬─────────────┬───────────────┬─────────────────┬───────────────┤
│ Provider ID │ Field       │ Gap Type      │ Domain          │ Age (Days)    │
├─────────────┼─────────────┼───────────────┼─────────────────┼───────────────┤
│ P100000     │ npi         │ Mismatch      │ Claims          │ 3             │
│ P100023     │ tin         │ Mismatch      │ Claims          │ 5             │
│ P100045     │ license_num │ Missing_Lake  │ Credentialing   │ 1             │
│ P100067     │ contract_   │ Mismatch      │ Network Ops     │ 7             │
│             │ status      │               │                 │               │
└─────────────┴─────────────┴───────────────┴─────────────────┴───────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ FILTERS                                                                     │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│ │ Domain    ▼  │ │ Priority  ▼  │ │ Gap Type  ▼  │ │ Date Range ▼  │        │
│ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘        │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ GAP DETAIL VIEW                                          [Export to Excel]  │
├─────────────────────────────────────────────────────────────────────────────┤
│ Selected: P100000 - npi Mismatch                                            │
│                                                                             │
│ ┌───────────────────────────────────────────────────────────────────────┐   │
│ │ COMPARISON                                                            │   │
│ │ ┌────────────────────────┐    ┌────────────────────────┐              │   │
│ │ │ SIMPLYR                │    │ DATA LAKE              │              │   │
│ │ │ NPI: 1065939459        │ ≠  │ NPI: 1014581341        │              │   │
│ │ │ Updated: 1/16/2025     │    │ Updated: 3/18/2025     │              │   │
│ │ └────────────────────────┘    └────────────────────────┘              │   │
│ └───────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│ ┌───────────────────────────────────────────────────────────────────────┐   │
│ │ AI ANALYSIS                                                           │   │
│ │                                                                       │   │
│ │ ROOT CAUSE:                                                           │   │
│ │ Data sync failure. Multiple field mismatches (15+) suggest complete   │   │
│ │ record synchronization issue. Lake updated after Simplyr but appears  │   │
│ │ to have received data from a different source.                        │   │
│ │                                                                       │   │
│ │ RECOMMENDATION:                                                       │   │
│ │ CRITICAL: Validate Simplyr NPI (1065939459) against NPPES registry.   │   │
│ │ If confirmed valid, trigger immediate Data Lake sync for P100000.     │   │
│ │ Monitor claims system for rejections using incorrect NPI.             │   │
│ │                                                                       │   │
│ │ NEXT STEPS:                                                           │   │
│ │ 1. Query NPPES API for NPI validation                                 │   │
│ │ 2. If valid, initiate WF_NPI_CORRECTION_CRITICAL workflow             │   │
│ │ 3. Notify Claims Operations of potential impact                       │   │
│ │ 4. Document root cause for process improvement                        │   │
│ └───────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ [✓ Approve Recommendation]  [✗ Reject]  [📝 Add Note]  [🔄 Re-analyze] │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 8. Technical Implementation Considerations

### 8.1 Data Volume Estimates

Based on 99 providers in sample data with ~120 fields each:

| Metric | Estimate | Notes |
|--------|----------|-------|
| Total field comparisons per run | ~11,880 | 99 providers × 120 fields |
| Expected gap rate | 5-15% | Based on typical data quality |
| Gaps per run | 594-1,782 | Fields requiring AI analysis |
| LLM calls per run | 594-1,782 | One call per gap (optimized) |

### 8.2 Cost Optimization Strategies

1. **Batch similar gaps:** Group identical field/gap_type combinations for single prompt
2. **Template responses:** For common patterns, use cached recommendations
3. **Field filtering:** Exclude low-impact fields (custom_attributes) from AI processing
4. **Confidence thresholds:** Only escalate to AI when deterministic rules can't resolve

### 8.3 Prompt Engineering Considerations

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ SYSTEM PROMPT FOR INTELLIGENCE LAYER AGENTS                                 │
└─────────────────────────────────────────────────────────────────────────────┘

You are a healthcare provider data specialist analyzing discrepancies between 
Simplyr (source of truth for provider data management) and the Data Lake 
(enterprise analytics repository).

CONTEXT:
- HCSC is a major health insurance company serving multiple states
- Provider data accuracy is critical for claims processing, network adequacy,
  and regulatory compliance
- Simplyr is generally authoritative for provider enrollment data
- Data Lake may have stale data due to sync timing

YOUR ROLE:
1. Analyze each data discrepancy
2. Determine the most likely root cause
3. Classify by business domain (Claims, Credentialing, Network Ops, Directory)
4. Assign severity based on business impact
5. Provide specific, actionable recommendations in business language

OUTPUT FORMAT:
- Use clear, concise language suitable for business stakeholders
- Prioritize patient safety and claims accuracy
- Recommend verification steps before automated updates for critical fields
- Identify when human review is required vs. automated resolution
```

---

## 9. Key Findings Summary

### 9.1 Data Quality Observations

1. **High Mismatch Rate:** Sample shows extensive mismatches between systems, suggesting either:
   - Test data with randomized values
   - Severe data synchronization issues in production
   - Multiple source feeds creating conflicts

2. **Schema Complexity:** 120+ fields require careful domain mapping
   - 60 custom attributes need business context for classification
   - Core fields (NPI, TIN, License) are critical

3. **Multi-Domain Impact:** Single gaps often affect multiple business domains
   - NPI mismatch: Claims + Credentialing + Directory
   - Address mismatch: Directory + Claims + Credentialing

### 9.2 Architectural Recommendations

1. **Phased Approach:**
   - Phase 1: Focus on critical fields (NPI, TIN, License, Contract Status)
   - Phase 2: Expand to directory fields
   - Phase 3: Custom attributes

2. **Deterministic + AI Hybrid:**
   - Use rules for format standardization (phone numbers, dates)
   - Use AI for root cause analysis and recommendations
   - Human review for critical conflicts

3. **Feedback Loop:**
   - Track recommendation acceptance/rejection
   - Use outcomes to improve future recommendations
   - Build pattern library for common issues

---

## 10. Next Steps

1. **Data Validation:** Confirm if sample data represents production patterns
2. **Domain Mapping Review:** Validate field classifications with business SMEs
3. **Prompt Testing:** Develop and test prompts with representative gaps
4. **UI Mockup:** Create interactive Power BI prototype
5. **Demo Script:** Align demo flow with stakeholder expectations

---

*End of Analysis Document v2.0*
