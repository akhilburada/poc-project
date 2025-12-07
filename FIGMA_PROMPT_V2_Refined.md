# FIGMA PROMPT: HCSC Provider Data Reconciliation Platform

## Create an enterprise-grade, polished React web application with these exact specifications:

---

# 🎯 APPLICATION OVERVIEW

Build a **4-step workflow application** for healthcare provider data reconciliation. The application must be:
- **100% Frontend** - No backend, no API calls
- **All data is hardcoded** - Use the exact data provided below
- **Enterprise-grade design** - Clean, professional, modern
- **Highly interactive** - Smooth transitions, animations, progress indicators

---

# 🔐 SCREEN 1: LOGIN PAGE

## Design Requirements:
- Full-screen gradient background (dark blue #0F172A to #1E3A5F)
- Centered white card (480px width, rounded-xl, shadow-2xl)
- Company branding at top

## Layout:
```
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│                    ┌──────────────────────┐                    │
│                    │                      │                    │
│                    │      🏥 HCSC         │                    │
│                    │  Provider Data       │                    │
│                    │  Reconciliation      │                    │
│                    │                      │                    │
│                    │  ┌────────────────┐  │                    │
│                    │  │ 👤 Username    │  │                    │
│                    │  └────────────────┘  │                    │
│                    │                      │                    │
│                    │  ┌────────────────┐  │                    │
│                    │  │ 🔒 Password    │  │                    │
│                    │  └────────────────┘  │                    │
│                    │                      │                    │
│                    │  ☐ Remember me       │                    │
│                    │                      │                    │
│                    │  ┌────────────────┐  │                    │
│                    │  │   Sign In  →   │  │                    │
│                    │  └────────────────┘  │                    │
│                    │                      │                    │
│                    │  Forgot password?    │                    │
│                    │                      │                    │
│                    └──────────────────────┘                    │
│                                                                │
│               © 2025 Health Care Service Corporation           │
└────────────────────────────────────────────────────────────────┘
```

## Hardcoded Credentials (validate on frontend):
```javascript
const USERS = [
  { username: "sarah.mitchell", password: "HCSC2025!", name: "Sarah Mitchell", role: "Data Quality Manager" },
  { username: "admin", password: "admin123", name: "Administrator", role: "System Admin" }
];
```

## Interactions:
- Show error toast "Invalid credentials" for wrong login
- Show loading spinner on button during validation (1 second delay)
- Redirect to main app on success
- Input fields have focus states (blue border glow)

---

# 🏠 MAIN APPLICATION LAYOUT

After login, show a layout with:

## Header Bar (Fixed, 64px height):
```
┌────────────────────────────────────────────────────────────────────────────┐
│ 🏥 HCSC Reconciliation          Step 2 of 4: Reconciliation    👤 Sarah ▼  │
└────────────────────────────────────────────────────────────────────────────┘
```

## Step Progress Indicator (Below header):
```
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│   ●━━━━━━━━━━━━━●━━━━━━━━━━━━━○━━━━━━━━━━━━━○                              │
│   1. Upload     2. Reconcile   3. AI Analysis  4. Export                  │
│   ✓ Complete    ● In Progress  ○ Pending       ○ Pending                  │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

## Step Indicator Colors:
- Completed: Green (#22C55E) with checkmark
- Current: Blue (#3B82F6) with pulse animation
- Pending: Gray (#9CA3AF)

---

# 📤 STEP 1: DATA UPLOAD

## Page Title:
"Upload Provider Data Files"
"Upload your Simplyr and Data Lake CSV files to begin reconciliation"

## Layout - Two Upload Cards Side by Side:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  Upload Provider Data Files                                                 │
│  Upload your Simplyr and Data Lake CSV files to begin reconciliation       │
│                                                                             │
│  ┌─────────────────────────────────┐  ┌─────────────────────────────────┐  │
│  │                                 │  │                                 │  │
│  │    📁 SIMPLYR SOURCE            │  │    📁 DATA LAKE                 │  │
│  │                                 │  │                                 │  │
│  │    ┌─────────────────────────┐  │  │    ┌─────────────────────────┐  │  │
│  │    │                         │  │  │    │                         │  │  │
│  │    │   📄                    │  │  │    │   📄                    │  │  │
│  │    │                         │  │  │    │                         │  │  │
│  │    │  Drag & drop your file  │  │  │    │  Drag & drop your file  │  │  │
│  │    │  or click to browse     │  │  │    │  or click to browse     │  │  │
│  │    │                         │  │  │    │                         │  │  │
│  │    │  CSV, XLSX up to 50MB   │  │  │    │  CSV, XLSX up to 50MB   │  │  │
│  │    │                         │  │  │    │                         │  │  │
│  │    └─────────────────────────┘  │  │    └─────────────────────────┘  │  │
│  │                                 │  │                                 │  │
│  │    [Browse Files]               │  │    [Browse Files]               │  │
│  │                                 │  │                                 │  │
│  └─────────────────────────────────┘  └─────────────────────────────────┘  │
│                                                                             │
│                                                                             │
│                         ┌─────────────────────────┐                         │
│                         │   Continue to Step 2 →  │  (disabled until both)  │
│                         └─────────────────────────┘                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## After File "Upload" (simulated - instant load):

```
┌─────────────────────────────────────┐  ┌─────────────────────────────────┐
│  ✅ SIMPLYR SOURCE                  │  │  ✅ DATA LAKE                   │
│                                     │  │                                 │
│  ┌─────────────────────────────────┐│  │┌─────────────────────────────────┐
│  │ 📄 simplyr_providers.csv        ││  ││ 📄 datalake_providers.csv      │
│  │                                 ││  ││                                 │
│  │ ✓ 99 provider records           ││  ││ ✓ 99 provider records           │
│  │ ✓ 58 fields detected            ││  ││ ✓ 58 fields detected            │
│  │ ✓ File validated successfully   ││  ││ ✓ File validated successfully   │
│  │                                 ││  ││                                 │
│  │ Size: 127 KB                    ││  ││ Size: 131 KB                    │
│  │ Uploaded: Just now              ││  ││ Uploaded: Just now              │
│  └─────────────────────────────────┘│  │└─────────────────────────────────┘
│                                     │  │                                 │
│  [Preview Data] [✕ Remove]          │  │  [Preview Data] [✕ Remove]      │
│                                     │  │                                 │
└─────────────────────────────────────┘  └─────────────────────────────────┘
```

## Button States:
- "Continue to Step 2" - Disabled (gray) until BOTH files uploaded
- "Continue to Step 2" - Enabled (blue) when both uploaded, with arrow animation

---

# 🔍 STEP 2: RECONCILIATION

## When user arrives at this step, show processing animation:

### Processing State (3 seconds animation):
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                      🔄 Running Reconciliation...                           │
│                                                                             │
│     ┌─────────────────────────────────────────────────────────────────┐    │
│     │ ████████████████████████████░░░░░░░░░░░░░░░░░░░  58%            │    │
│     └─────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│     ┌─────────────────────────────────────────────────────────────────┐    │
│     │  ✅ Loading Simplyr data (99 records)                           │    │
│     │  ✅ Loading Data Lake data (99 records)                         │    │
│     │  ✅ Matching records by Provider ID                             │    │
│     │  ⏳ Comparing 5,742 field pairs...                              │    │
│     │  ○ Identifying gaps                                             │    │
│     │  ○ Calculating statistics                                       │    │
│     └─────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│                      Elapsed: 00:00:02                                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Completion State (auto-transition after processing):
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                      ✅ Reconciliation Complete                             │
│                                                                             │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                                                                        │ │
│  │   SUMMARY                                                              │ │
│  │   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │ │
│  │                                                                        │ │
│  │   Providers Compared        99                                         │ │
│  │   Fields Analyzed           5,742                                      │ │
│  │   Total Gaps Found          247                                        │ │
│  │   Providers with Gaps       72 (72.7%)                                 │ │
│  │                                                                        │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │ 🔴 CRITICAL │ │ 🟠 HIGH     │ │ 🟡 MEDIUM   │ │ 🟢 LOW      │           │
│  │     23      │ │     64      │ │     112     │ │     48      │           │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘           │
│                                                                             │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ GAPS BY DOMAIN                                                         │ │
│  │                                                                        │ │
│  │ Claims           ████████████████████░░░░░░  89 (36%)                  │ │
│  │ Credentialing    ██████████████░░░░░░░░░░░░  62 (25%)                  │ │
│  │ Network Ops      ████████████░░░░░░░░░░░░░░  54 (22%)                  │ │
│  │ Directory        ████████░░░░░░░░░░░░░░░░░░  42 (17%)                  │ │
│  │                                                                        │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│                    ┌─────────────────────────────────┐                      │
│                    │   Continue to AI Analysis →     │                      │
│                    └─────────────────────────────────┘                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# 🤖 STEP 3: AI ANALYSIS

## Processing State First (4 seconds):
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                   🧠 AI Analysis in Progress...                             │
│                                                                             │
│     ┌─────────────────────────────────────────────────────────────────┐    │
│     │ ████████████████████████████████░░░░░░░░░  75%                  │    │
│     └─────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│     ┌─────────────────────────────────────────────────────────────────┐    │
│     │  ✅ Analyzing gap patterns                                      │    │
│     │  ✅ Identifying root causes                                     │    │
│     │  ✅ Classifying by domain                                       │    │
│     │  ⏳ Generating recommendations...                               │    │
│     │  ○ Calculating severity scores                                  │    │
│     │  ○ Assigning ownership                                          │    │
│     └─────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│     🤖 "Analyzing NPI mismatch patterns across 23 critical gaps..."        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## After AI Analysis Complete - Show Interactive Results Table:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  AI Analysis Results                                    [Filter ▼] [Search] │
│  247 gaps analyzed • 247 recommendations generated                         │
│                                                                             │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────────────┐                      │
│  │🔴 23 │ │🟠 64 │ │🟡 112│ │🟢 48 │ │ All: 247     │ ← Clickable filters  │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────────────┘                      │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ Provider  │ Field           │ Gap Type │ Severity │ Domain      │ Action   │
├───────────┼─────────────────┼──────────┼──────────┼─────────────┼──────────┤
│ P100000   │ npi             │ Mismatch │ 🔴 10    │ Claims      │ [View]   │
│ P100000   │ tin             │ Mismatch │ 🔴 10    │ Claims      │ [View]   │
│ P100000   │ credential_stat │ Mismatch │ 🔴 9     │ Credential  │ [View]   │
│ P100001   │ npi             │ Mismatch │ 🔴 10    │ Claims      │ [View]   │
│ P100001   │ first_name      │ Mismatch │ 🔴 9     │ Directory   │ [View]   │
│ P100002   │ npi             │ Mismatch │ 🔴 10    │ Claims      │ [View]   │
│ P100002   │ specialty       │ Mismatch │ 🟠 8     │ Directory   │ [View]   │
│ P100003   │ contract_status │ Mismatch │ 🟠 8     │ Network     │ [View]   │
│ P100004   │ license_state   │ Mismatch │ 🟠 7     │ Credential  │ [View]   │
│ P100005   │ phone           │ Missing  │ 🟡 5     │ Directory   │ [View]   │
├───────────┴─────────────────┴──────────┴──────────┴─────────────┴──────────┤
│                      Showing 1-10 of 247     [←] [1] [2] [3] ... [25] [→]   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## When User Clicks [View] - Show Slide-in Detail Panel:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Main Table (dimmed)              │ DETAIL PANEL (slide from right)          │
│                                  │─────────────────────────────────────────│
│                                  │ Gap Details                        [✕]  │
│                                  │─────────────────────────────────────────│
│                                  │                                         │
│                                  │ 🔴 CRITICAL • Severity 10/10            │
│                                  │                                         │
│                                  │ ┌─────────────────────────────────────┐ │
│                                  │ │ PROVIDER: P100000                   │ │
│                                  │ │ Field: npi                          │ │
│                                  │ │ Domain: Claims                      │ │
│                                  │ └─────────────────────────────────────┘ │
│                                  │                                         │
│                                  │ VALUE COMPARISON                        │
│                                  │ ┌────────────────┬────────────────────┐ │
│                                  │ │ SIMPLYR        │ DATA LAKE          │ │
│                                  │ ├────────────────┼────────────────────┤ │
│                                  │ │ 1065939459     │ 1014581341         │ │
│                                  │ │ Updated:       │ Updated:           │ │
│                                  │ │ Jan 16, 2025   │ Mar 18, 2025       │ │
│                                  │ └────────────────┴────────────────────┘ │
│                                  │                                         │
│                                  │ 🤖 AI ROOT CAUSE ANALYSIS               │
│                                  │ ┌─────────────────────────────────────┐ │
│                                  │ │ Provider ID collision detected.     │ │
│                                  │ │ Analysis shows 27 field mismatches  │ │
│                                  │ │ (22.5% discrepancy rate) including  │ │
│                                  │ │ NPI, TIN, DOB, and specialty.       │ │
│                                  │ │                                     │ │
│                                  │ │ This suggests two different         │ │
│                                  │ │ providers are mapped to the same    │ │
│                                  │ │ Provider ID in the systems.         │ │
│                                  │ └─────────────────────────────────────┘ │
│                                  │                                         │
│                                  │ 💡 RECOMMENDATION                       │
│                                  │ ┌─────────────────────────────────────┐ │
│                                  │ │ ⚠️ CRITICAL - DO NOT AUTO-SYNC      │ │
│                                  │ │                                     │ │
│                                  │ │ 1. Validate Simplyr NPI against     │ │
│                                  │ │    NPPES registry                   │ │
│                                  │ │ 2. Validate Lake NPI against NPPES  │ │
│                                  │ │ 3. If different providers, correct  │ │
│                                  │ │    Provider ID mapping in Lake      │ │
│                                  │ │ 4. Escalate to Data Governance      │ │
│                                  │ └─────────────────────────────────────┘ │
│                                  │                                         │
│                                  │ 📋 NEXT STEPS                           │
│                                  │ □ Query NPPES for both NPIs             │
│                                  │ □ Compare NPPES results                 │
│                                  │ □ Create ServiceNow ticket              │
│                                  │ □ Notify Claims Operations              │
│                                  │                                         │
│                                  │ 👤 OWNER: Claims Operations Team        │
│                                  │                                         │
│                                  │ ┌─────────────────────────────────────┐ │
│                                  │ │ [✓ Approve] [✕ Reject] [📝 Note]   │ │
│                                  │ └─────────────────────────────────────┘ │
│                                  │                                         │
└──────────────────────────────────┴─────────────────────────────────────────┘
```

## Continue Button at Bottom:
```
                    ┌─────────────────────────────────┐
                    │   Continue to Export →          │
                    └─────────────────────────────────┘
```

---

# 📥 STEP 4: EXPORT

## Export Screen Layout:
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  📥 Export Results                                                          │
│  Download your reconciliation analysis and recommendations                  │
│                                                                             │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                                                                        │ │
│  │   ✅ RECONCILIATION COMPLETE                                           │ │
│  │                                                                        │ │
│  │   ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐         │ │
│  │   │ Providers  │ │ Total Gaps │ │ Critical   │ │ AI Recs    │         │ │
│  │   │    99      │ │    247     │ │    23      │ │    247     │         │ │
│  │   └────────────┘ └────────────┘ └────────────┘ └────────────┘         │ │
│  │                                                                        │ │
│  │   Completed: December 5, 2025 at 10:45:23 AM                           │ │
│  │   Duration: 00:00:12                                                   │ │
│  │                                                                        │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  EXPORT OPTIONS                                                             │
│                                                                             │
│  ┌─────────────────────────────────┐  ┌─────────────────────────────────┐  │
│  │                                 │  │                                 │  │
│  │  📊 FULL REPORT (Excel)         │  │  📄 EXECUTIVE SUMMARY (PDF)     │  │
│  │                                 │  │                                 │  │
│  │  Complete gap analysis with     │  │  High-level summary for         │  │
│  │  all 247 gaps, AI analysis,     │  │  leadership with key metrics    │  │
│  │  and recommendations            │  │  and critical findings          │  │
│  │                                 │  │                                 │  │
│  │  Includes:                      │  │  Includes:                      │  │
│  │  • All provider gaps            │  │  • Summary statistics           │  │
│  │  • AI root cause analysis       │  │  • Domain breakdown             │  │
│  │  • Recommendations              │  │  • Top 10 critical gaps         │  │
│  │  • Severity scores              │  │  • Recommended actions          │  │
│  │  • Owner assignments            │  │                                 │  │
│  │                                 │  │                                 │  │
│  │  ┌─────────────────────────┐   │  │  ┌─────────────────────────┐   │  │
│  │  │   📥 Download Excel     │   │  │  │   📥 Download PDF       │   │  │
│  │  └─────────────────────────┘   │  │  └─────────────────────────┘   │  │
│  │                                 │  │                                 │  │
│  └─────────────────────────────────┘  └─────────────────────────────────┘  │
│                                                                             │
│  ┌─────────────────────────────────┐  ┌─────────────────────────────────┐  │
│  │                                 │  │                                 │  │
│  │  📋 CRITICAL GAPS ONLY (CSV)    │  │  📁 RAW DATA (JSON)             │  │
│  │                                 │  │                                 │  │
│  │  Export only the 23 critical    │  │  Raw reconciliation data in     │  │
│  │  gaps requiring immediate       │  │  JSON format for system         │  │
│  │  attention                      │  │  integration                    │  │
│  │                                 │  │                                 │  │
│  │  ┌─────────────────────────┐   │  │  ┌─────────────────────────┐   │  │
│  │  │   📥 Download CSV       │   │  │  │   📥 Download JSON      │   │  │
│  │  └─────────────────────────┘   │  │  └─────────────────────────┘   │  │
│  │                                 │  │                                 │  │
│  └─────────────────────────────────┘  └─────────────────────────────────┘  │
│                                                                             │
│                                                                             │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │              ┌─────────────────────────────────┐                       │ │
│  │              │   🔄 Start New Reconciliation   │                       │ │
│  │              └─────────────────────────────────┘                       │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# 📊 COMPLETE HARDCODED DATA

## Use this exact data in the application:

### Provider Gaps Data (All 247 gaps):

```javascript
const GAPS_DATA = [
  // ============ CRITICAL (23 gaps) ============
  {
    id: 1,
    provider_id: "P100000",
    provider_name: "Ana Garcia, DO",
    field: "npi",
    simplyr_value: "1065939459",
    lake_value: "1014581341",
    gap_type: "Mismatch",
    severity: 10,
    priority: "Critical",
    domain: "Claims",
    owner: "Claims Operations",
    root_cause: "Provider ID collision detected. Analysis shows 27 field mismatches (22.5% discrepancy rate) including NPI, TIN, DOB, and specialty. This suggests two different providers are mapped to the same Provider ID.",
    recommendation: "CRITICAL - DO NOT AUTO-SYNC. 1) Validate Simplyr NPI (1065939459) against NPPES registry. 2) Validate Lake NPI (1014581341) against NPPES. 3) If different providers confirmed, correct Provider ID mapping in Lake. 4) Escalate to Data Governance team.",
    next_steps: ["Query NPPES for both NPIs", "Compare NPPES results", "Identify root cause of ID collision", "Create ServiceNow ticket", "Notify Claims Operations"],
    workflow: "WF_PROVIDER_ID_COLLISION"
  },
  {
    id: 2,
    provider_id: "P100000",
    provider_name: "Ana Garcia, DO",
    field: "tin",
    simplyr_value: "534360412",
    lake_value: "260622691",
    gap_type: "Mismatch",
    severity: 10,
    priority: "Critical",
    domain: "Claims",
    owner: "Claims Operations",
    root_cause: "TIN mismatch is part of the Provider ID collision affecting P100000. Different TINs (534360412 vs 260622691) confirm these are different legal entities incorrectly sharing the same Provider ID.",
    recommendation: "CRITICAL - Related to NPI collision issue. TIN mismatch confirms different legal entities. Do NOT process payments until resolved. Verify W-9 on file matches Simplyr TIN.",
    next_steps: ["Review W-9 documentation", "Cross-reference with NPI investigation", "Hold payment processing for P100000"],
    workflow: "WF_TIN_VERIFICATION"
  },
  {
    id: 3,
    provider_id: "P100000",
    provider_name: "Ana Garcia, DO",
    field: "credentialing_status",
    simplyr_value: "Verified",
    lake_value: "Expired",
    gap_type: "Mismatch",
    severity: 9,
    priority: "Critical",
    domain: "Credentialing",
    owner: "Credentialing Team",
    root_cause: "Credentialing status mismatch. Simplyr shows Verified (active) while Lake shows Expired. If Lake is used for claims adjudication, this could cause incorrect denials for a credentialed provider.",
    recommendation: "HIGH PRIORITY: Verify actual credentialing status from primary source documents. If provider is truly Verified, Lake must be updated immediately to prevent member access issues.",
    next_steps: ["Pull credentialing file for P100000", "Verify current status with CAQH", "Update Lake if Simplyr confirmed correct"],
    workflow: "WF_CREDENTIALING_UPDATE"
  },
  {
    id: 4,
    provider_id: "P100001",
    provider_name: "Priya Smith, PA",
    field: "npi",
    simplyr_value: "1502778451",
    lake_value: "1600215021",
    gap_type: "Mismatch",
    severity: 10,
    priority: "Critical",
    domain: "Claims",
    owner: "Claims Operations",
    root_cause: "Complete provider mismatch. Names are entirely different (Priya Smith vs John Johnson in Lake) indicating Provider ID collision. This is a systemic issue - same pattern as P100000.",
    recommendation: "CRITICAL: Provider ID P100001 maps to completely different individuals. Same pattern as P100000 - suggests systemic Provider ID assignment issue. Escalate to Data Governance.",
    next_steps: ["Validate both NPIs in NPPES", "Document as systemic issue", "Add to pattern analysis", "Create incident report"],
    workflow: "WF_SYSTEMIC_DATA_ISSUE"
  },
  {
    id: 5,
    provider_id: "P100001",
    provider_name: "Priya Smith, PA",
    field: "first_name",
    simplyr_value: "Priya",
    lake_value: "John",
    gap_type: "Mismatch",
    severity: 9,
    priority: "Critical",
    domain: "Directory",
    owner: "Directory Management",
    root_cause: "First name completely different - Priya vs John. This is not a spelling variation but entirely different names, confirming Provider ID collision for P100001.",
    recommendation: "Name mismatch confirms Provider ID collision. Do NOT update either system. Requires source data investigation to determine correct Provider ID assignment.",
    next_steps: ["Document as Provider ID collision evidence", "Bundle with NPI investigation for P100001"],
    workflow: "WF_IDENTITY_VERIFICATION"
  },
  {
    id: 6,
    provider_id: "P100002",
    provider_name: "Luis Johnson, DO",
    field: "npi",
    simplyr_value: "1010168041",
    lake_value: "1510441276",
    gap_type: "Mismatch",
    severity: 10,
    priority: "Critical",
    domain: "Claims",
    owner: "Claims Operations",
    root_cause: "Third Provider ID collision case. Simplyr shows Luis Johnson, DO while Lake shows David Kim, PA. Completely different individuals with different credentials (DO vs PA).",
    recommendation: "CRITICAL: Same pattern as P100000 and P100001. Three Provider ID collisions indicate systemic issue with ID generation or data integration process.",
    next_steps: ["Add to systemic pattern analysis", "Escalate to Data Governance", "Audit Provider ID generation process"],
    workflow: "WF_SYSTEMIC_DATA_ISSUE"
  },
  {
    id: 7,
    provider_id: "P100002",
    provider_name: "Luis Johnson, DO",
    field: "tin",
    simplyr_value: "809296119",
    lake_value: "569288394",
    gap_type: "Mismatch",
    severity: 10,
    priority: "Critical",
    domain: "Claims",
    owner: "Claims Operations",
    root_cause: "TIN mismatch consistent with Provider ID collision pattern for P100002.",
    recommendation: "Part of P100002 collision issue. Different TINs confirm different legal entities. Bundle with NPI investigation.",
    next_steps: ["Bundle with NPI investigation", "Verify W-9 records"],
    workflow: "WF_TIN_VERIFICATION"
  },
  {
    id: 8,
    provider_id: "P100003",
    provider_name: "Priya Smith, DO",
    field: "contract_status",
    simplyr_value: "Active",
    lake_value: "Terminated",
    gap_type: "Mismatch",
    severity: 9,
    priority: "Critical",
    domain: "Network Ops",
    owner: "Network Management",
    root_cause: "Critical contract status discrepancy. Active vs Terminated has major claims payment implications. If Lake is used for claims, active provider may be incorrectly denied.",
    recommendation: "URGENT: Verify current contract status immediately. If Active in contract system, Lake must be corrected. Active providers shown as Terminated cause claims denials.",
    next_steps: ["Query contract management system", "Verify effective/term dates", "Correct Lake if Active confirmed", "Monitor for affected claims"],
    workflow: "WF_CONTRACT_STATUS_CRITICAL"
  },
  {
    id: 9,
    provider_id: "P100003",
    provider_name: "Priya Smith, DO",
    field: "npi",
    simplyr_value: "1592491251",
    lake_value: "1050474560",
    gap_type: "Mismatch",
    severity: 10,
    priority: "Critical",
    domain: "Claims",
    owner: "Claims Operations",
    root_cause: "Fourth Provider ID collision. Different NPIs and names (Priya Smith vs David Patel in Lake).",
    recommendation: "CRITICAL: Another Provider ID collision case. Add to systemic investigation.",
    next_steps: ["NPPES validation", "Add to systemic investigation"],
    workflow: "WF_PROVIDER_ID_COLLISION"
  },
  {
    id: 10,
    provider_id: "P100004",
    provider_name: "Mike Johnson, MD",
    field: "npi",
    simplyr_value: "1154519413",
    lake_value: "1306713563",
    gap_type: "Mismatch",
    severity: 10,
    priority: "Critical",
    domain: "Claims",
    owner: "Claims Operations",
    root_cause: "NPI mismatch - fifth Provider ID collision case identified.",
    recommendation: "Continue systemic investigation. Pattern indicates data integration failure.",
    next_steps: ["Add to pattern analysis", "Document for root cause analysis"],
    workflow: "WF_PROVIDER_ID_COLLISION"
  },
  {
    id: 11,
    provider_id: "P100005",
    provider_name: "Ana Smith, NP",
    field: "npi",
    simplyr_value: "1306205845",
    lake_value: "1961352854",
    gap_type: "Mismatch",
    severity: 10,
    priority: "Critical",
    domain: "Claims",
    owner: "Claims Operations",
    root_cause: "Sixth Provider ID collision. Systemic issue confirmed.",
    recommendation: "Document as part of systemic issue. NPI mismatch pattern consistent.",
    next_steps: ["Add to master investigation list"],
    workflow: "WF_PROVIDER_ID_COLLISION"
  },
  {
    id: 12,
    provider_id: "P100006",
    provider_name: "David Wong, DO",
    field: "tin",
    simplyr_value: "144406205",
    lake_value: "425798786",
    gap_type: "Mismatch",
    severity: 10,
    priority: "Critical",
    domain: "Claims",
    owner: "Claims Operations",
    root_cause: "TIN mismatch affects payment routing. Different TINs indicate different legal entities.",
    recommendation: "Verify W-9 documentation. Determine correct TIN for payment routing.",
    next_steps: ["Review W-9 on file", "Verify with provider", "Update correct system"],
    workflow: "WF_TIN_VERIFICATION"
  },
  {
    id: 13,
    provider_id: "P100007",
    provider_name: "Luis Smith",
    field: "npi",
    simplyr_value: "1186352988",
    lake_value: "1159763070",
    gap_type: "Mismatch",
    severity: 10,
    priority: "Critical",
    domain: "Claims",
    owner: "Claims Operations",
    root_cause: "NPI mismatch - Provider ID collision pattern continues.",
    recommendation: "Add to systemic investigation. Validate both NPIs.",
    next_steps: ["NPPES validation", "Add to pattern list"],
    workflow: "WF_PROVIDER_ID_COLLISION"
  },
  {
    id: 14,
    provider_id: "P100008",
    provider_name: "Ana Wong, MD",
    field: "credentialing_status",
    simplyr_value: "Expired",
    lake_value: "Verified",
    gap_type: "Mismatch",
    severity: 9,
    priority: "Critical",
    domain: "Credentialing",
    owner: "Credentialing Team",
    root_cause: "Inverse of typical pattern - Simplyr shows Expired but Lake shows Verified. May indicate recent recredentialing not synced to Simplyr.",
    recommendation: "Verify with CAQH for current status. If Verified, update Simplyr. Provider may be correctly credentialed but Simplyr outdated.",
    next_steps: ["Check CAQH status", "Verify recredentialing date", "Update Simplyr if needed"],
    workflow: "WF_CREDENTIALING_UPDATE"
  },
  {
    id: 15,
    provider_id: "P100009",
    provider_name: "Chen Wong",
    field: "npi",
    simplyr_value: "1235133629",
    lake_value: "1833148373",
    gap_type: "Mismatch",
    severity: 10,
    priority: "Critical",
    domain: "Claims",
    owner: "Claims Operations",
    root_cause: "NPI mismatch continues systemic pattern.",
    recommendation: "Add to systemic investigation.",
    next_steps: ["Bundle with other NPI mismatches"],
    workflow: "WF_PROVIDER_ID_COLLISION"
  },
  {
    id: 16,
    provider_id: "P100010",
    provider_name: "Sarah Garcia, MD",
    field: "tin",
    simplyr_value: "401608181",
    lake_value: "537012851",
    gap_type: "Mismatch",
    severity: 10,
    priority: "Critical",
    domain: "Claims",
    owner: "Claims Operations",
    root_cause: "TIN mismatch affects payment processing.",
    recommendation: "Verify correct TIN for claims payment.",
    next_steps: ["Review W-9", "Verify with provider"],
    workflow: "WF_TIN_VERIFICATION"
  },
  {
    id: 17,
    provider_id: "P100011",
    provider_name: "David Wong, PA",
    field: "npi",
    simplyr_value: "1082023700",
    lake_value: "1506818229",
    gap_type: "Mismatch",
    severity: 10,
    priority: "Critical",
    domain: "Claims",
    owner: "Claims Operations",
    root_cause: "NPI mismatch - systemic issue.",
    recommendation: "Part of systemic investigation.",
    next_steps: ["Add to pattern list"],
    workflow: "WF_PROVIDER_ID_COLLISION"
  },
  {
    id: 18,
    provider_id: "P100012",
    provider_name: "Chen Garcia, NP",
    field: "npi",
    simplyr_value: "1977657793",
    lake_value: "1445874783",
    gap_type: "Mismatch",
    severity: 10,
    priority: "Critical",
    domain: "Claims",
    owner: "Claims Operations",
    root_cause: "NPI mismatch continues pattern.",
    recommendation: "Bundle with systemic investigation.",
    next_steps: ["NPPES validation"],
    workflow: "WF_PROVIDER_ID_COLLISION"
  },
  {
    id: 19,
    provider_id: "P100013",
    provider_name: "Sarah Wong, PA",
    field: "tin",
    simplyr_value: "359396108",
    lake_value: "351053423",
    gap_type: "Mismatch",
    severity: 10,
    priority: "Critical",
    domain: "Claims",
    owner: "Claims Operations",
    root_cause: "TIN values are similar but different. May be transposition error.",
    recommendation: "Compare digit-by-digit. Likely data entry error. Verify with W-9.",
    next_steps: ["Review W-9 carefully", "Check for transposition"],
    workflow: "WF_TIN_VERIFICATION"
  },
  {
    id: 20,
    provider_id: "P100014",
    provider_name: "Luis Garcia, PA",
    field: "npi",
    simplyr_value: "1777288199",
    lake_value: "1766895725",
    gap_type: "Mismatch",
    severity: 10,
    priority: "Critical",
    domain: "Claims",
    owner: "Claims Operations",
    root_cause: "NPI mismatch - similar prefix suggests possible data entry error.",
    recommendation: "Validate both NPIs in NPPES. Check for transposition errors.",
    next_steps: ["NPPES lookup", "Compare provider details"],
    workflow: "WF_PROVIDER_ID_COLLISION"
  },
  {
    id: 21,
    provider_id: "P100015",
    provider_name: "David Smith",
    field: "npi",
    simplyr_value: "1092854975",
    lake_value: "1085096675",
    gap_type: "Mismatch",
    severity: 10,
    priority: "Critical",
    domain: "Claims",
    owner: "Claims Operations",
    root_cause: "NPI mismatch.",
    recommendation: "Validate in NPPES.",
    next_steps: ["NPPES validation"],
    workflow: "WF_PROVIDER_ID_COLLISION"
  },
  {
    id: 22,
    provider_id: "P100016",
    provider_name: "Ana Kim, PA",
    field: "tin",
    simplyr_value: "210325077",
    lake_value: "539282482",
    gap_type: "Mismatch",
    severity: 10,
    priority: "Critical",
    domain: "Claims",
    owner: "Claims Operations",
    root_cause: "TIN completely different - confirms different entities.",
    recommendation: "Verify correct TIN for this provider.",
    next_steps: ["W-9 review", "Provider verification"],
    workflow: "WF_TIN_VERIFICATION"
  },
  {
    id: 23,
    provider_id: "P100017",
    provider_name: "Luis Johnson, PA",
    field: "npi",
    simplyr_value: "1267237267",
    lake_value: "1955205493",
    gap_type: "Mismatch",
    severity: 10,
    priority: "Critical",
    domain: "Claims",
    owner: "Claims Operations",
    root_cause: "NPI mismatch - part of systemic issue.",
    recommendation: "Add to investigation.",
    next_steps: ["Bundle with systemic analysis"],
    workflow: "WF_PROVIDER_ID_COLLISION"
  },

  // ============ HIGH PRIORITY (64 gaps) ============
  {
    id: 24,
    provider_id: "P100000",
    provider_name: "Ana Garcia, DO",
    field: "specialty_primary",
    simplyr_value: "Family Medicine",
    lake_value: "Orthopedics",
    gap_type: "Mismatch",
    severity: 8,
    priority: "High",
    domain: "Directory",
    owner: "Directory Management",
    root_cause: "Major specialty discrepancy. Family Medicine and Orthopedics are unrelated. Further confirms Provider ID collision - different providers with different specialties.",
    recommendation: "Specialty mismatch supports Provider ID collision theory. Verify board certification records. Do not update until NPI investigation resolved.",
    next_steps: ["Wait for NPI investigation", "Verify board certifications", "Check taxonomy alignment"],
    workflow: "WF_SPECIALTY_VERIFICATION"
  },
  {
    id: 25,
    provider_id: "P100000",
    provider_name: "Ana Garcia, DO",
    field: "contract_status",
    simplyr_value: "Pending",
    lake_value: "Inactive",
    gap_type: "Mismatch",
    severity: 8,
    priority: "High",
    domain: "Network Ops",
    owner: "Network Management",
    root_cause: "Contract status discrepancy. Pending suggests onboarding, Inactive suggests terminated. Different statuses have payment implications.",
    recommendation: "Verify current contract status with contracting team. Critical for claims accuracy.",
    next_steps: ["Review contract system", "Verify effective dates", "Align status across systems"],
    workflow: "WF_CONTRACT_VERIFICATION"
  },
  {
    id: 26,
    provider_id: "P100000",
    provider_name: "Ana Garcia, DO",
    field: "dob",
    simplyr_value: "1/1/1962",
    lake_value: "1/1/1994",
    gap_type: "Mismatch",
    severity: 7,
    priority: "High",
    domain: "Directory",
    owner: "Directory Management",
    root_cause: "32-year difference in DOB. Definitive evidence of Provider ID collision - cannot be data entry error.",
    recommendation: "DOB discrepancy confirms different individuals. Document for investigation.",
    next_steps: ["Document as evidence", "No direct action until NPI resolved"],
    workflow: "WF_IDENTITY_VERIFICATION"
  },
  {
    id: 27,
    provider_id: "P100000",
    provider_name: "Ana Garcia, DO",
    field: "license_state",
    simplyr_value: "IL",
    lake_value: "TX",
    gap_type: "Mismatch",
    severity: 7,
    priority: "High",
    domain: "Credentialing",
    owner: "Credentialing Team",
    root_cause: "License state mismatch affects regulatory compliance. Provider cannot practice in both IL and TX without separate licenses.",
    recommendation: "Verify state licensure records. Cross-reference with practice address.",
    next_steps: ["Query IL medical board", "Query TX medical board", "Document all active licenses"],
    workflow: "WF_LICENSE_VERIFICATION"
  },
  {
    id: 28,
    provider_id: "P100001",
    provider_name: "Priya Smith, PA",
    field: "last_name",
    simplyr_value: "Smith",
    lake_value: "Johnson",
    gap_type: "Mismatch",
    severity: 8,
    priority: "High",
    domain: "Directory",
    owner: "Directory Management",
    root_cause: "Last name different - Smith vs Johnson. Confirms Provider ID collision for P100001.",
    recommendation: "Part of P100001 collision investigation. Last name difference adds to evidence.",
    next_steps: ["Document as evidence", "Bundle with NPI investigation"],
    workflow: "WF_IDENTITY_VERIFICATION"
  },
  {
    id: 29,
    provider_id: "P100002",
    provider_name: "Luis Johnson, DO",
    field: "specialty_primary",
    simplyr_value: "Dermatology",
    lake_value: "Cardiology",
    gap_type: "Mismatch",
    severity: 8,
    priority: "High",
    domain: "Directory",
    owner: "Directory Management",
    root_cause: "Specialty mismatch. Dermatology vs Cardiology are completely unrelated.",
    recommendation: "Evidence of Provider ID collision. Different specialties cannot be reconciled.",
    next_steps: ["Document for investigation"],
    workflow: "WF_SPECIALTY_VERIFICATION"
  },
  // ... Continue with remaining HIGH priority gaps (30-87)
  // Adding representative samples...
  
  {
    id: 30,
    provider_id: "P100004",
    provider_name: "Mike Johnson, MD",
    field: "license_state",
    simplyr_value: "NY",
    lake_value: "CA",
    gap_type: "Mismatch",
    severity: 7,
    priority: "High",
    domain: "Credentialing",
    owner: "Credentialing Team",
    root_cause: "License state discrepancy between NY and CA.",
    recommendation: "Verify all active state licenses for this provider.",
    next_steps: ["Query state medical boards", "Update license records"],
    workflow: "WF_LICENSE_VERIFICATION"
  },
  
  // ============ MEDIUM PRIORITY (112 gaps) ============
  {
    id: 88,
    provider_id: "P100000",
    provider_name: "Ana Garcia, DO",
    field: "practice_state",
    simplyr_value: "IL",
    lake_value: "NY",
    gap_type: "Mismatch",
    severity: 6,
    priority: "Medium",
    domain: "Directory",
    owner: "Directory Management",
    root_cause: "Practice state mismatch affects member search and network adequacy reporting.",
    recommendation: "Verify current practice location. Update directory for accurate search results.",
    next_steps: ["Verify practice address", "Update directory", "Check network adequacy impact"],
    workflow: "WF_ADDRESS_UPDATE"
  },
  {
    id: 89,
    provider_id: "P100000",
    provider_name: "Ana Garcia, DO",
    field: "suffix",
    simplyr_value: "DO",
    lake_value: "",
    gap_type: "Missing_In_Lake",
    severity: 5,
    priority: "Medium",
    domain: "Directory",
    owner: "Directory Management",
    root_cause: "Provider suffix (DO) missing in Lake. Affects title display.",
    recommendation: "Update Lake with suffix 'DO' from Simplyr. Low risk update.",
    next_steps: ["Queue for batch update"],
    workflow: "WF_DIRECTORY_UPDATE"
  },
  {
    id: 90,
    provider_id: "P100000",
    provider_name: "Ana Garcia, DO",
    field: "gender",
    simplyr_value: "M",
    lake_value: "U",
    gap_type: "Mismatch",
    severity: 4,
    priority: "Medium",
    domain: "Directory",
    owner: "Directory Management",
    root_cause: "Gender shows Male in Simplyr, Unknown in Lake. Lake may have defaulted during ingestion.",
    recommendation: "Update Lake with Simplyr value after verification.",
    next_steps: ["Verify gender", "Update Lake"],
    workflow: "WF_DEMOGRAPHIC_UPDATE"
  },
  {
    id: 91,
    provider_id: "P100005",
    provider_name: "Ana Smith, NP",
    field: "phone",
    simplyr_value: "2125551212",
    lake_value: "",
    gap_type: "Missing_In_Lake",
    severity: 5,
    priority: "Medium",
    domain: "Directory",
    owner: "Directory Management",
    root_cause: "Phone number exists in Simplyr but missing in Lake. Members cannot contact provider via Lake-powered directory.",
    recommendation: "Sync phone number from Simplyr to Lake. Standard directory update.",
    next_steps: ["Verify phone current", "Add to batch update"],
    workflow: "WF_CONTACT_UPDATE"
  },
  {
    id: 92,
    provider_id: "P100010",
    provider_name: "Sarah Garcia, MD",
    field: "languages_spoken",
    simplyr_value: "Mandarin",
    lake_value: "Spanish",
    gap_type: "Mismatch",
    severity: 4,
    priority: "Medium",
    domain: "Directory",
    owner: "Directory Management",
    root_cause: "Language mismatch affects member search for language-specific providers.",
    recommendation: "Verify languages spoken with provider. May be multi-lingual.",
    next_steps: ["Contact provider office", "Update language list"],
    workflow: "WF_PROVIDER_OUTREACH"
  },
  {
    id: 93,
    provider_id: "P100015",
    provider_name: "David Smith",
    field: "accepting_new_patients_flag",
    simplyr_value: "Yes",
    lake_value: "No",
    gap_type: "Mismatch",
    severity: 6,
    priority: "Medium",
    domain: "Directory",
    owner: "Directory Management",
    root_cause: "Panel status affects member experience. If accepting but shown as not, members cannot book.",
    recommendation: "Verify current panel status with practice. Update immediately if accepting.",
    next_steps: ["Call provider office", "Update Lake if accepting"],
    workflow: "WF_PANEL_STATUS_UPDATE"
  },
  // ... Continue with remaining MEDIUM gaps (94-199)
  
  // ============ LOW PRIORITY (48 gaps) ============
  {
    id: 200,
    provider_id: "P100000",
    provider_name: "Ana Garcia, DO",
    field: "phone",
    simplyr_value: "",
    lake_value: "2125551212",
    gap_type: "Missing_In_Simplyr",
    severity: 3,
    priority: "Low",
    domain: "Directory",
    owner: "Directory Management",
    root_cause: "Phone exists in Lake but missing in Simplyr. Lake may have more recent contact info.",
    recommendation: "Consider backfilling Simplyr with Lake phone after verification.",
    next_steps: ["Verify phone current", "Update Simplyr if valid"],
    workflow: "WF_CONTACT_UPDATE"
  },
  {
    id: 201,
    provider_id: "P100020",
    provider_name: "Ana Johnson, DO",
    field: "practice_zip",
    simplyr_value: "73657",
    lake_value: "62980",
    gap_type: "Mismatch",
    severity: 4,
    priority: "Low",
    domain: "Directory",
    owner: "Directory Management",
    root_cause: "ZIP code mismatch affects distance calculations for member search.",
    recommendation: "Verify current practice address. Update both systems if change verified.",
    next_steps: ["Confirm address with provider", "Update systems"],
    workflow: "WF_ADDRESS_UPDATE"
  },
  {
    id: 202,
    provider_id: "P100025",
    provider_name: "Chen Kim, PA",
    field: "fax",
    simplyr_value: "2125551213",
    lake_value: "",
    gap_type: "Missing_In_Lake",
    severity: 2,
    priority: "Low",
    domain: "Directory",
    owner: "Directory Management",
    root_cause: "Fax number missing in Lake. Minor directory completeness issue.",
    recommendation: "Add fax to Lake during next sync. Low priority.",
    next_steps: ["Add to batch update list"],
    workflow: "WF_DIRECTORY_UPDATE"
  },
  {
    id: 203,
    provider_id: "P100030",
    provider_name: "John Patel",
    field: "time_zone",
    simplyr_value: "PST",
    lake_value: "CST",
    gap_type: "Mismatch",
    severity: 2,
    priority: "Low",
    domain: "Directory",
    owner: "Directory Management",
    root_cause: "Time zone mismatch. Minor operational impact.",
    recommendation: "Update based on practice address. Low priority.",
    next_steps: ["Derive from practice ZIP", "Update both systems"],
    workflow: "WF_DIRECTORY_UPDATE"
  }
  // ... Continue with remaining LOW gaps (204-247)
];

// Summary Statistics
const SUMMARY_STATS = {
  total_providers: 99,
  total_fields_compared: 5742,
  total_gaps: 247,
  providers_with_gaps: 72,
  providers_clean: 27,
  
  by_priority: {
    critical: { count: 23, percentage: 9.3 },
    high: { count: 64, percentage: 25.9 },
    medium: { count: 112, percentage: 45.3 },
    low: { count: 48, percentage: 19.4 }
  },
  
  by_domain: {
    claims: { count: 89, percentage: 36.0, color: "#7C3AED" },
    credentialing: { count: 62, percentage: 25.1, color: "#0891B2" },
    network_ops: { count: 54, percentage: 21.9, color: "#059669" },
    directory: { count: 42, percentage: 17.0, color: "#D97706" }
  },
  
  by_gap_type: {
    mismatch: { count: 198, percentage: 80.2 },
    missing_in_lake: { count: 35, percentage: 14.2 },
    missing_in_simplyr: { count: 14, percentage: 5.7 }
  }
};
```

---

# 🎨 VISUAL DESIGN REQUIREMENTS

## Colors:
```css
/* Primary */
--primary: #2563EB;
--primary-hover: #1D4ED8;
--primary-light: #DBEAFE;

/* Status */
--critical: #DC2626;
--critical-bg: #FEE2E2;
--high: #EA580C;
--high-bg: #FFEDD5;
--medium: #CA8A04;
--medium-bg: #FEF9C3;
--low: #22C55E;
--low-bg: #DCFCE7;

/* Neutrals */
--bg: #F8FAFC;
--card-bg: #FFFFFF;
--border: #E2E8F0;
--text-primary: #0F172A;
--text-secondary: #64748B;
```

## Typography:
- Font: Inter (or system font stack)
- Headings: 600-700 weight
- Body: 400 weight
- Monospace for data: JetBrains Mono

## Spacing:
- Card padding: 24px
- Section gaps: 32px
- Element gaps: 16px
- Border radius: 12px for cards, 8px for buttons

## Shadows:
- Cards: `0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06)`
- Modals: `0 25px 50px -12px rgba(0,0,0,0.25)`

---

# ⚡ INTERACTIONS & ANIMATIONS

## Step Transitions:
- Fade out current step (200ms)
- Fade in new step (200ms)
- Progress bar animates smoothly

## Processing Animations:
- Progress bar fills smoothly
- Checklist items appear one by one (300ms delay each)
- Pulse animation on current step indicator

## Table Interactions:
- Row hover: Background #F1F5F9
- Row click: Opens side panel with slide animation (300ms)
- Sorting: Column headers clickable with sort icon

## Buttons:
- Hover: Slightly darker, lift shadow
- Click: Scale down slightly (98%)
- Disabled: 50% opacity, no hover effect

## Side Panel:
- Slides in from right (300ms ease-out)
- Background overlay with fade (200ms)
- Click outside to close

---

# 📱 RESPONSIVE NOTES

- Desktop-first design (1280px+)
- Tables should be horizontally scrollable on smaller screens
- Side panel becomes full-screen modal on mobile
- Step indicator stacks vertically on mobile

---

# ✅ FINAL CHECKLIST FOR FIGMA

1. ☐ Login page with gradient background and centered card
2. ☐ 4-step progress indicator in header
3. ☐ Step 1: Two file upload zones side by side
4. ☐ Step 2: Processing animation → Summary results
5. ☐ Step 3: Data table with filters + Slide-in detail panel
6. ☐ Step 4: Four export option cards
7. ☐ All data is hardcoded from the provided JavaScript
8. ☐ Smooth transitions between steps
9. ☐ Professional enterprise look
10. ☐ No backend - 100% frontend

---

**END OF PROMPT**
