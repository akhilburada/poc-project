# FIGMA AI PROMPT: HCSC Provider Data Reconciliation Platform
## Enterprise Workflow Application - Complete Frontend Specification

---

## 🎯 PROJECT OVERVIEW

Create a **professional enterprise-grade web application** for HCSC (Health Care Service Corporation) Provider Data Reconciliation. This is a **workflow-based application** that allows users to:

1. Upload provider data files (Simplyr and Data Lake)
2. Execute reconciliation to identify data gaps
3. View AI-powered analysis and recommendations
4. Review and approve/reject recommendations
5. Export results for downstream processing

**IMPORTANT:** This is a **100% frontend application** with NO backend. All data is pre-loaded and hardcoded. All calculations, AI reasoning, and recommendations are pre-computed and embedded in the application.

---

## 🔐 AUTHENTICATION

### Login Page Credentials (Hardcoded)

```javascript
const VALID_USERS = [
  {
    username: "sarah.mitchell",
    password: "HCSC2025!",
    name: "Sarah Mitchell",
    role: "Data Quality Manager",
    department: "Provider Data Operations",
    avatar: "SM"
  },
  {
    username: "james.chen",
    password: "Provider123!",
    name: "James Chen",
    role: "Claims Operations Lead",
    department: "Claims Processing",
    avatar: "JC"
  },
  {
    username: "admin",
    password: "admin123",
    name: "System Administrator",
    role: "Administrator",
    department: "IT Operations",
    avatar: "AD"
  }
];
```

---

## 🎨 DESIGN SYSTEM

### Brand Colors
```css
:root {
  /* Primary - HCSC Blue */
  --primary-900: #0D1F4B;
  --primary-800: #1A3A6E;
  --primary-700: #1E4D8C;
  --primary-600: #2563EB;
  --primary-500: #3B82F6;
  --primary-100: #DBEAFE;
  
  /* Status Colors */
  --critical: #DC2626;
  --critical-bg: #FEE2E2;
  --high: #EA580C;
  --high-bg: #FFEDD5;
  --medium: #CA8A04;
  --medium-bg: #FEF9C3;
  --low: #16A34A;
  --low-bg: #DCFCE7;
  --resolved: #6B7280;
  --resolved-bg: #F3F4F6;
  
  /* Neutrals */
  --gray-900: #111827;
  --gray-700: #374151;
  --gray-500: #6B7280;
  --gray-300: #D1D5DB;
  --gray-100: #F3F4F6;
  --white: #FFFFFF;
  
  /* Domain Colors */
  --claims-color: #7C3AED;
  --credentialing-color: #0891B2;
  --network-color: #059669;
  --directory-color: #D97706;
}
```

### Typography
```css
/* Font Family: Inter */
--font-heading: 'Inter', -apple-system, sans-serif;
--font-body: 'Inter', -apple-system, sans-serif;
--font-mono: 'JetBrains Mono', monospace;

/* Sizes */
--text-xs: 12px;
--text-sm: 14px;
--text-base: 16px;
--text-lg: 18px;
--text-xl: 20px;
--text-2xl: 24px;
--text-3xl: 30px;
```

### Spacing & Radius
```css
--spacing-1: 4px;
--spacing-2: 8px;
--spacing-3: 12px;
--spacing-4: 16px;
--spacing-6: 24px;
--spacing-8: 32px;

--radius-sm: 6px;
--radius-md: 8px;
--radius-lg: 12px;
--radius-xl: 16px;
```

---

## 📱 APPLICATION SCREENS

---

### SCREEN 1: LOGIN PAGE

**Layout:** Centered card on gradient background

**Background:** Linear gradient from `--primary-900` to `--primary-700`

**Card Contents:**
- HCSC Logo (placeholder: "HCSC" in bold white text with blue underline)
- Title: "Provider Data Reconciliation Platform"
- Subtitle: "Sign in to continue"
- Username input field with user icon
- Password input field with lock icon (show/hide toggle)
- "Remember me" checkbox
- Primary button: "Sign In"
- Footer text: "© 2025 Health Care Service Corporation. All rights reserved."

**Validation:**
- Show error message "Invalid credentials. Please try again." for wrong login
- Redirect to Dashboard on successful login

**Design Notes:**
- Card has subtle shadow and rounded corners (16px)
- Inputs have focus state with blue border
- Button has hover state (darker blue)

---

### SCREEN 2: MAIN DASHBOARD

**Layout:** Sidebar navigation + Main content area

#### Sidebar (Fixed, 260px width, dark background)
```
┌─────────────────────────────┐
│ [HCSC Logo]                 │
│ Provider Reconciliation     │
├─────────────────────────────┤
│ ○ Dashboard          [active]│
│ ○ Reconciliation             │
│ ○ Gap Analysis               │
│ ○ Recommendations            │
│ ○ Reports                    │
│ ○ Settings                   │
├─────────────────────────────┤
│ [User Avatar: SM]           │
│ Sarah Mitchell              │
│ Data Quality Manager        │
│ [Logout]                    │
└─────────────────────────────┘
```

#### Main Content Area

**Header Bar:**
```
┌─────────────────────────────────────────────────────────────────────────┐
│ Dashboard                                        🔔 Notifications (3)   │
│ Last sync: December 5, 2025 09:30:45 AM                    [?] Help    │
└─────────────────────────────────────────────────────────────────────────┘
```

**KPI Cards Row (4 cards):**
```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│ 🔴 CRITICAL     │ 🟠 HIGH         │ 🟡 MEDIUM       │ 🟢 LOW          │
│     47          │    156          │    312          │    89           │
│ +12 from last   │ +34 from last   │ -8 from last    │ +5 from last    │
│ run             │ run             │ run             │ run             │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

**Summary Stats Row:**
```
┌─────────────────────────────────────────────────────────────────────────┐
│ RECONCILIATION SUMMARY                                                  │
├─────────────────┬─────────────────┬─────────────────┬─────────────────┤
│ Total Providers │ Total Gaps      │ Resolution Rate │ Avg. Resolution │
│      99         │     604         │     67.2%       │    2.3 days     │
│ Compared        │ Identified      │ Last 30 days    │ Time            │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

**Charts Section (2 columns):**

**Left Chart: Gaps by Domain (Donut Chart)**
```
Data:
- Claims: 211 gaps (35%)
- Credentialing: 169 gaps (28%)
- Network Ops: 133 gaps (22%)
- Provider Directory: 91 gaps (15%)
```

**Right Chart: Gaps by Root Cause (Horizontal Bar Chart)**
```
Data:
- Data Sync Failure: 254 (42%)
- Source System Delay: 169 (28%)
- Data Entry Error: 91 (15%)
- Format Mismatch: 60 (10%)
- Unknown: 30 (5%)
```

**Recent Critical Gaps Table:**
```
┌─────────────┬───────────────────┬──────────────┬─────────────┬──────────┐
│ Provider ID │ Field             │ Domain       │ Gap Type    │ Age      │
├─────────────┼───────────────────┼──────────────┼─────────────┼──────────┤
│ P100000     │ npi               │ Claims       │ Mismatch    │ 3 days   │
│ P100000     │ tin               │ Claims       │ Mismatch    │ 3 days   │
│ P100002     │ npi               │ Claims       │ Mismatch    │ 2 days   │
│ P100001     │ credentialing_    │ Credentialing│ Mismatch    │ 5 days   │
│             │ status            │              │             │          │
│ P100003     │ contract_status   │ Network Ops  │ Mismatch    │ 1 day    │
└─────────────┴───────────────────┴──────────────┴─────────────┴──────────┘
                                                        [View All Gaps →]
```

---

### SCREEN 3: RECONCILIATION (File Upload & Process)

**Page Title:** "New Reconciliation"

**Stepper Navigation:**
```
Step 1: Upload Files  →  Step 2: Configure  →  Step 3: Process  →  Step 4: Review
     [●]                    [○]                  [○]                 [○]
```

#### Step 1: Upload Files

**Two Upload Zones (side by side):**

```
┌─────────────────────────────────┐  ┌─────────────────────────────────┐
│                                 │  │                                 │
│     📁 SIMPLYR DATA             │  │     📁 DATA LAKE                │
│                                 │  │                                 │
│  Drag & drop your Simplyr CSV   │  │  Drag & drop your Data Lake    │
│  file here, or click to browse  │  │  CSV file here, or click       │
│                                 │  │  to browse                      │
│  Supported: .csv, .xlsx         │  │  Supported: .csv, .xlsx         │
│  Max size: 50MB                 │  │  Max size: 50MB                 │
│                                 │  │                                 │
│  [Browse Files]                 │  │  [Browse Files]                 │
│                                 │  │                                 │
└─────────────────────────────────┘  └─────────────────────────────────┘
```

**After "Upload" (Simulated - instant load of pre-loaded data):**
```
┌─────────────────────────────────┐  ┌─────────────────────────────────┐
│ ✅ simplyr_providers.csv        │  │ ✅ datalake_providers.csv       │
│                                 │  │                                 │
│ 99 provider records             │  │ 99 provider records             │
│ 120 fields per record           │  │ 120 fields per record           │
│ File size: 245 KB               │  │ File size: 248 KB               │
│ Uploaded: Just now              │  │ Uploaded: Just now              │
│                                 │  │                                 │
│ [Preview Data] [Remove]         │  │ [Preview Data] [Remove]         │
└─────────────────────────────────┘  └─────────────────────────────────┘
```

**Button:** [Continue to Configuration →]

#### Step 2: Configure Reconciliation

**Configuration Options:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│ RECONCILIATION SETTINGS                                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│ Match Key:                                                              │
│ ┌─────────────────────────────────────────────────────────────────────┐│
│ │ ○ Provider ID (Recommended)                                         ││
│ │ ○ NPI                                                               ││
│ │ ○ Provider ID + NPI (Composite)                                     ││
│ └─────────────────────────────────────────────────────────────────────┘│
│                                                                         │
│ Fields to Compare:                                                      │
│ ┌─────────────────────────────────────────────────────────────────────┐│
│ │ ☑ All Fields (120 fields)                                          ││
│ │ ☐ Critical Fields Only (12 fields)                                  ││
│ │ ☐ Custom Selection                                                  ││
│ └─────────────────────────────────────────────────────────────────────┘│
│                                                                         │
│ AI Analysis:                                                            │
│ ┌─────────────────────────────────────────────────────────────────────┐│
│ │ ☑ Enable AI-powered root cause analysis                            ││
│ │ ☑ Enable AI-powered recommendations                                ││
│ │ ☑ Enable domain classification                                     ││
│ │ ☑ Enable severity scoring                                          ││
│ └─────────────────────────────────────────────────────────────────────┘│
│                                                                         │
│ Notification:                                                           │
│ ┌─────────────────────────────────────────────────────────────────────┐│
│ │ ☑ Email notification when complete                                 ││
│ │   Email: sarah.mitchell@hcsc.com                                    ││
│ └─────────────────────────────────────────────────────────────────────┘│
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Buttons:** [← Back] [Start Reconciliation →]

#### Step 3: Processing (Animated)

**Processing Animation Screen:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│                    ⚙️ RECONCILIATION IN PROGRESS                        │
│                                                                         │
│     ┌─────────────────────────────────────────────────────────────┐    │
│     │ ████████████████████████████░░░░░░░░░░░  68%                │    │
│     └─────────────────────────────────────────────────────────────┘    │
│                                                                         │
│                                                                         │
│     ┌─────────────────────────────────────────────────────────────┐    │
│     │ LAYER 1: TASK (Reconciliation)                              │    │
│     │ ✅ Loading Simplyr data... Complete                         │    │
│     │ ✅ Loading Data Lake data... Complete                       │    │
│     │ ✅ Matching records by Provider ID... Complete              │    │
│     │ ✅ Comparing 11,880 field pairs... Complete                 │    │
│     │ ✅ Identified 604 gaps... Complete                          │    │
│     └─────────────────────────────────────────────────────────────┘    │
│                                                                         │
│     ┌─────────────────────────────────────────────────────────────┐    │
│     │ LAYER 2: INTELLIGENCE (AI Analysis)                         │    │
│     │ ✅ Analyzing root causes... Complete                        │    │
│     │ ✅ Classifying domains... Complete                          │    │
│     │ ⏳ Generating recommendations... 68%                        │    │
│     │ ○ Calculating severity scores... Pending                    │    │
│     │ ○ Assigning owners... Pending                               │    │
│     └─────────────────────────────────────────────────────────────┘    │
│                                                                         │
│     Elapsed time: 00:00:47                                              │
│     Estimated remaining: 00:00:22                                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**After completion (auto-advance):**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│                    ✅ RECONCILIATION COMPLETE                           │
│                                                                         │
│     ┌─────────────────────────────────────────────────────────────┐    │
│     │ ████████████████████████████████████████  100%              │    │
│     └─────────────────────────────────────────────────────────────┘    │
│                                                                         │
│     ┌─────────────────────────────────────────────────────────────┐    │
│     │                                                             │    │
│     │   📊 SUMMARY                                                │    │
│     │                                                             │    │
│     │   Providers Compared:          99                           │    │
│     │   Total Fields Analyzed:       11,880                       │    │
│     │   Gaps Identified:             604                          │    │
│     │   AI Recommendations Generated: 604                         │    │
│     │                                                             │    │
│     │   ┌─────────────────────────────────────────────────────┐  │    │
│     │   │ Critical: 47  │ High: 156  │ Medium: 312 │ Low: 89  │  │    │
│     │   └─────────────────────────────────────────────────────┘  │    │
│     │                                                             │    │
│     │   Processing Time: 00:01:09                                 │    │
│     │   Completed: December 5, 2025 09:31:54 AM                   │    │
│     │                                                             │    │
│     └─────────────────────────────────────────────────────────────┘    │
│                                                                         │
│                      [View Results →]                                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### SCREEN 4: GAP ANALYSIS (Main Working Screen)

**Layout:** Header + Filters + Data Table + Side Panel

#### Header Section
```
┌─────────────────────────────────────────────────────────────────────────┐
│ Gap Analysis                                          Run: Dec 5, 2025  │
│ 604 gaps identified across 99 providers                                │
│                                                                         │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────┐│
│ │🔴 47     │ │🟠 156    │ │🟡 312    │ │🟢 89     │ │ ⬜ All: 604     ││
│ │Critical  │ │High      │ │Medium    │ │Low       │ │ [Selected]      ││
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────────────┘│
└─────────────────────────────────────────────────────────────────────────┘
```

#### Filter Bar
```
┌─────────────────────────────────────────────────────────────────────────┐
│ Filters:                                                                │
│ ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌─────────┐│
│ │Domain    ▼ │ │Gap Type  ▼ │ │Owner     ▼ │ │Status    ▼ │ │🔍 Search││
│ └────────────┘ └────────────┘ └────────────┘ └────────────┘ └─────────┘│
│                                                                         │
│ Active Filters: [Domain: Claims ×] [Priority: Critical ×]  [Clear All] │
└─────────────────────────────────────────────────────────────────────────┘
```

#### Main Data Table

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ ☐ │ Provider    │ Field              │ Simplyr Value    │ Lake Value       │ Gap Type  │ Domain       │ Severity │ Status    │
├────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ ☐ │ P100000     │ npi                │ 1065939459       │ 1014581341       │ Mismatch  │ Claims       │ 🔴 10    │ Pending   │
│ ☐ │ P100000     │ tin                │ 534360412        │ 260622691        │ Mismatch  │ Claims       │ 🔴 10    │ Pending   │
│ ☐ │ P100000     │ credentialing_     │ Verified         │ Expired          │ Mismatch  │ Credentialing│ 🔴 9     │ Pending   │
│   │             │ status             │                  │                  │           │              │          │           │
│ ☐ │ P100000     │ specialty_primary  │ Family Medicine  │ Orthopedics      │ Mismatch  │ Directory    │ 🟠 8     │ Pending   │
│ ☐ │ P100000     │ contract_status    │ Pending          │ Inactive         │ Mismatch  │ Network Ops  │ 🟠 8     │ Pending   │
│ ☐ │ P100000     │ dob                │ 1/1/1962         │ 1/1/1994         │ Mismatch  │ Directory    │ 🟠 7     │ Pending   │
│ ☐ │ P100000     │ license_state      │ IL               │ TX               │ Mismatch  │ Credentialing│ 🟠 7     │ Pending   │
│ ☐ │ P100000     │ practice_state     │ IL               │ NY               │ Mismatch  │ Directory    │ 🟡 6     │ Pending   │
│ ☐ │ P100000     │ gender             │ M                │ U                │ Mismatch  │ Directory    │ 🟡 4     │ Pending   │
│ ☐ │ P100000     │ phone              │ (empty)          │ 2125551212       │ Missing   │ Directory    │ 🟢 3     │ Pending   │
├────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Showing 1-10 of 604 gaps                                          [← Previous] Page 1 of 61 [Next →]                         │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

#### Side Panel (Opens when row is clicked)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ GAP DETAILS                                                    [×]     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐│
│ │ PROVIDER: P100000                                                   ││
│ │ Name: Ana Garcia, DO (Simplyr) | Ana Garcia (Lake)                  ││
│ │ Specialty: Family Medicine | Orthopedics                            ││
│ └─────────────────────────────────────────────────────────────────────┘│
│                                                                         │
│ FIELD COMPARISON                                                        │
│ ┌──────────────────────────────┬──────────────────────────────────────┐│
│ │ SIMPLYR                      │ DATA LAKE                            ││
│ ├──────────────────────────────┼──────────────────────────────────────┤│
│ │ NPI: 1065939459              │ NPI: 1014581341                      ││
│ │ Last Updated: 1/16/2025      │ Last Updated: 3/18/2025              ││
│ │ Source: SIMPLYR              │ Source: LAKE                         ││
│ └──────────────────────────────┴──────────────────────────────────────┘│
│                                                                         │
│ 🔴 SEVERITY: 10/10 (Critical)                                          │
│ 📁 DOMAIN: Claims                                                       │
│ 👤 OWNER: Claims Operations Team                                       │
│                                                                         │
│ ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│ 🤖 AI ANALYSIS                                                         │
│                                                                         │
│ ROOT CAUSE:                                                             │
│ ┌─────────────────────────────────────────────────────────────────────┐│
│ │ Data sync failure detected. Analysis of provider P100000 reveals   ││
│ │ 27 field mismatches out of 120 fields (22.5% discrepancy rate).    ││
│ │ The Lake record appears to contain data from a different provider  ││
│ │ that was incorrectly mapped to the same Provider ID.               ││
│ │                                                                     ││
│ │ Key indicators:                                                     ││
│ │ • NPI values are completely different (not a typo)                 ││
│ │ • TIN values differ (suggests different legal entity)              ││
│ │ • DOB differs by 32 years (1962 vs 1994)                           ││
│ │ • Specialties are unrelated (Family Medicine vs Orthopedics)       ││
│ │                                                                     ││
│ │ This pattern suggests either a data merge error or duplicate       ││
│ │ Provider ID assignment in the source systems.                       ││
│ └─────────────────────────────────────────────────────────────────────┘│
│                                                                         │
│ RECOMMENDATION:                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐│
│ │ ⚠️ CRITICAL ACTION REQUIRED                                        ││
│ │                                                                     ││
│ │ Do NOT automatically sync this record. Manual investigation        ││
│ │ required to determine:                                              ││
│ │                                                                     ││
│ │ 1. Validate Simplyr NPI (1065939459) against NPPES registry        ││
│ │ 2. Validate Lake NPI (1014581341) against NPPES registry           ││
│ │ 3. Determine if these are two different providers                  ││
│ │ 4. If different providers: Correct Provider ID mapping in Lake     ││
│ │ 5. If same provider: Determine authoritative source and update     ││
│ │                                                                     ││
│ │ Escalate to Data Governance team if NPIs map to different          ││
│ │ providers in NPPES.                                                 ││
│ └─────────────────────────────────────────────────────────────────────┘│
│                                                                         │
│ NEXT STEPS:                                                             │
│ ┌─────────────────────────────────────────────────────────────────────┐│
│ │ □ Step 1: Query NPPES API for both NPI values                      ││
│ │ □ Step 2: Compare NPPES results with internal records              ││
│ │ □ Step 3: Identify root cause of Provider ID collision             ││
│ │ □ Step 4: Create data correction ticket in ServiceNow              ││
│ │ □ Step 5: Notify Claims Operations of potential payment impact     ││
│ │ □ Step 6: Monitor for claims using incorrect NPI                   ││
│ └─────────────────────────────────────────────────────────────────────┘│
│                                                                         │
│ SUGGESTED WORKFLOW: WF_PROVIDER_ID_COLLISION_CRITICAL                  │
│                                                                         │
│ ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│ ACTIONS                                                                 │
│ ┌─────────────────────────────────────────────────────────────────────┐│
│ │ [✓ Approve Recommendation]  [✗ Reject]  [📝 Add Note]              ││
│ │                                                                     ││
│ │ [Assign to Different Owner ▼]  [Change Priority ▼]                 ││
│ │                                                                     ││
│ │ [Create ServiceNow Ticket]  [Export Details]                       ││
│ └─────────────────────────────────────────────────────────────────────┘│
│                                                                         │
│ ACTIVITY LOG                                                            │
│ ┌─────────────────────────────────────────────────────────────────────┐│
│ │ Dec 5, 2025 09:31 AM - Gap identified by reconciliation process    ││
│ │ Dec 5, 2025 09:32 AM - AI analysis completed                       ││
│ │ Dec 5, 2025 09:45 AM - Viewed by Sarah Mitchell                    ││
│ └─────────────────────────────────────────────────────────────────────┘│
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### SCREEN 5: RECOMMENDATIONS VIEW

**Layout:** Card-based view of recommendations grouped by priority

#### Header
```
┌─────────────────────────────────────────────────────────────────────────┐
│ AI Recommendations                                                      │
│ Review and approve AI-generated recommendations for gap resolution      │
│                                                                         │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐│
│ │ Pending: 547 │ │ Approved: 42 │ │ Rejected: 15 │ │ [Bulk Actions ▼] ││
│ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────────┘│
└─────────────────────────────────────────────────────────────────────────┘
```

#### Recommendation Cards

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 🔴 CRITICAL RECOMMENDATIONS (47)                          [Expand All] │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐│
│ │ P100000 - NPI Mismatch                                    🔴 10/10  ││
│ │ Domain: Claims | Owner: Claims Operations                           ││
│ │ ──────────────────────────────────────────────────────────────────  ││
│ │ Simplyr: 1065939459 → Lake: 1014581341                              ││
│ │ ──────────────────────────────────────────────────────────────────  ││
│ │ 💡 RECOMMENDATION:                                                  ││
│ │ Manual investigation required. Do NOT auto-sync. Validate both     ││
│ │ NPIs against NPPES registry. Likely Provider ID collision.         ││
│ │ ──────────────────────────────────────────────────────────────────  ││
│ │ [✓ Approve] [✗ Reject] [📝 Note] [→ Assign] [📋 View Details]      ││
│ └─────────────────────────────────────────────────────────────────────┘│
│                                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐│
│ │ P100000 - TIN Mismatch                                    🔴 10/10  ││
│ │ Domain: Claims | Owner: Claims Operations                           ││
│ │ ──────────────────────────────────────────────────────────────────  ││
│ │ Simplyr: 534360412 → Lake: 260622691                                ││
│ │ ──────────────────────────────────────────────────────────────────  ││
│ │ 💡 RECOMMENDATION:                                                  ││
│ │ CRITICAL: TIN mismatch affects payment routing. Verify with W-9    ││
│ │ on file. Do NOT process payments until resolved. Related to NPI    ││
│ │ collision issue - same root cause suspected.                        ││
│ │ ──────────────────────────────────────────────────────────────────  ││
│ │ [✓ Approve] [✗ Reject] [📝 Note] [→ Assign] [📋 View Details]      ││
│ └─────────────────────────────────────────────────────────────────────┘│
│                                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐│
│ │ P100002 - NPI Mismatch                                    🔴 10/10  ││
│ │ Domain: Claims | Owner: Claims Operations                           ││
│ │ ──────────────────────────────────────────────────────────────────  ││
│ │ Simplyr: 1010168041 → Lake: 1510441276                              ││
│ │ ──────────────────────────────────────────────────────────────────  ││
│ │ 💡 RECOMMENDATION:                                                  ││
│ │ NPI mismatch detected. Pattern consistent with P100000. Validate   ││
│ │ Simplyr NPI against NPPES. If valid, initiate Data Lake sync.      ││
│ │ ──────────────────────────────────────────────────────────────────  ││
│ │ [✓ Approve] [✗ Reject] [📝 Note] [→ Assign] [📋 View Details]      ││
│ └─────────────────────────────────────────────────────────────────────┘│
│                                                                         │
│                        [Load More Critical Recommendations]             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ 🟠 HIGH PRIORITY RECOMMENDATIONS (156)                    [Expand All] │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐│
│ │ P100000 - Credentialing Status Mismatch                   🟠 9/10   ││
│ │ Domain: Credentialing | Owner: Credentialing Team                   ││
│ │ ──────────────────────────────────────────────────────────────────  ││
│ │ Simplyr: Verified → Lake: Expired                                   ││
│ │ ──────────────────────────────────────────────────────────────────  ││
│ │ 💡 RECOMMENDATION:                                                  ││
│ │ Status mismatch may cause incorrect claims denials. Verify current ││
│ │ credentialing status with primary source. If Verified in Simplyr,  ││
│ │ update Lake immediately to prevent member access issues.           ││
│ │ ──────────────────────────────────────────────────────────────────  ││
│ │ [✓ Approve] [✗ Reject] [📝 Note] [→ Assign] [📋 View Details]      ││
│ └─────────────────────────────────────────────────────────────────────┘│
│                                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐│
│ │ P100000 - Contract Status Mismatch                        🟠 8/10   ││
│ │ Domain: Network Ops | Owner: Network Management                     ││
│ │ ──────────────────────────────────────────────────────────────────  ││
│ │ Simplyr: Pending → Lake: Inactive                                   ││
│ │ ──────────────────────────────────────────────────────────────────  ││
│ │ 💡 RECOMMENDATION:                                                  ││
│ │ Contract status affects claims payment eligibility. Pending status ││
│ │ in Simplyr suggests onboarding in progress. Verify with contract   ││
│ │ management. If Pending, provider should not appear as in-network.  ││
│ │ ──────────────────────────────────────────────────────────────────  ││
│ │ [✓ Approve] [✗ Reject] [📝 Note] [→ Assign] [📋 View Details]      ││
│ └─────────────────────────────────────────────────────────────────────┘│
│                                                                         │
│                        [Load More High Priority Recommendations]        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### SCREEN 6: REPORTS

**Layout:** Report selection cards + Generated report view

#### Report Selection
```
┌─────────────────────────────────────────────────────────────────────────┐
│ Reports & Analytics                                                     │
│ Generate and export reconciliation reports                              │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
│ 📊 Executive Summary│ │ 📋 Gap Details      │ │ 📈 Trend Analysis   │
│                     │ │                     │ │                     │
│ High-level overview │ │ Complete list of    │ │ Historical trends   │
│ for leadership      │ │ all identified gaps │ │ over time           │
│                     │ │                     │ │                     │
│ [Generate Report]   │ │ [Generate Report]   │ │ [Generate Report]   │
└─────────────────────┘ └─────────────────────┘ └─────────────────────┘

┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
│ 👥 Owner Assignment │ │ 📁 Domain Summary   │ │ ⚡ Action Items     │
│                     │ │                     │ │                     │
│ Gaps assigned to    │ │ Breakdown by        │ │ Pending actions     │
│ each team/owner     │ │ business domain     │ │ requiring attention │
│                     │ │                     │ │                     │
│ [Generate Report]   │ │ [Generate Report]   │ │ [Generate Report]   │
└─────────────────────┘ └─────────────────────┘ └─────────────────────┘
```

#### Generated Report View (Executive Summary)
```
┌─────────────────────────────────────────────────────────────────────────┐
│ EXECUTIVE SUMMARY REPORT                                                │
│ Generated: December 5, 2025 10:15:23 AM                                 │
│                                                    [📥 Export PDF]      │
│                                                    [📥 Export Excel]    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│ RECONCILIATION RUN: December 5, 2025                                    │
│ ═══════════════════════════════════════════════════════════════════════ │
│                                                                         │
│ OVERVIEW                                                                │
│ ┌─────────────────────────────────────────────────────────────────────┐│
│ │ Total Providers Analyzed:        99                                 ││
│ │ Total Fields Compared:           11,880                             ││
│ │ Gaps Identified:                 604 (5.1% discrepancy rate)        ││
│ │ Providers with Gaps:             87 (87.9% of providers)            ││
│ │ Providers without Gaps:          12 (12.1% of providers)            ││
│ └─────────────────────────────────────────────────────────────────────┘│
│                                                                         │
│ SEVERITY BREAKDOWN                                                      │
│ ┌─────────────────────────────────────────────────────────────────────┐│
│ │ Priority     │ Count  │ Percentage │ SLA                           ││
│ │──────────────┼────────┼────────────┼───────────────────────────────││
│ │ 🔴 Critical  │   47   │    7.8%    │ 24 hours                      ││
│ │ 🟠 High      │  156   │   25.8%    │ 72 hours                      ││
│ │ 🟡 Medium    │  312   │   51.7%    │ 1 week                        ││
│ │ 🟢 Low       │   89   │   14.7%    │ 2 weeks                       ││
│ └─────────────────────────────────────────────────────────────────────┘│
│                                                                         │
│ DOMAIN DISTRIBUTION                                                     │
│ ┌─────────────────────────────────────────────────────────────────────┐│
│ │ Domain              │ Gaps   │ Critical │ Owner                    ││
│ │─────────────────────┼────────┼──────────┼──────────────────────────││
│ │ Claims              │  211   │    32    │ Claims Operations        ││
│ │ Credentialing       │  169   │     8    │ Credentialing Team       ││
│ │ Network Operations  │  133   │     5    │ Network Management       ││
│ │ Provider Directory  │   91   │     2    │ Directory Management     ││
│ └─────────────────────────────────────────────────────────────────────┘│
│                                                                         │
│ ROOT CAUSE ANALYSIS                                                     │
│ ┌─────────────────────────────────────────────────────────────────────┐│
│ │ Root Cause                    │ Count  │ Recommended Action        ││
│ │───────────────────────────────┼────────┼───────────────────────────││
│ │ Data Sync Failure             │  254   │ Review ETL pipeline       ││
│ │ Source System Delay           │  169   │ Reduce sync interval      ││
│ │ Data Entry Error              │   91   │ Implement validation      ││
│ │ Format Mismatch               │   60   │ Standardize formats       ││
│ │ Unknown/Requires Investigation│   30   │ Manual review             ││
│ └─────────────────────────────────────────────────────────────────────┘│
│                                                                         │
│ TOP 10 IMPACTED PROVIDERS                                               │
│ ┌─────────────────────────────────────────────────────────────────────┐│
│ │ Rank │ Provider ID │ Gap Count │ Critical │ Primary Domain         ││
│ │──────┼─────────────┼───────────┼──────────┼────────────────────────││
│ │   1  │ P100000     │    27     │     4    │ Claims                 ││
│ │   2  │ P100002     │    24     │     3    │ Claims                 ││
│ │   3  │ P100001     │    22     │     2    │ Credentialing          ││
│ │   4  │ P100003     │    19     │     2    │ Network Ops            ││
│ │   5  │ P100005     │    18     │     1    │ Directory              ││
│ │   6  │ P100007     │    16     │     1    │ Claims                 ││
│ │   7  │ P100004     │    15     │     1    │ Credentialing          ││
│ │   8  │ P100009     │    14     │     0    │ Directory              ││
│ │   9  │ P100006     │    13     │     0    │ Network Ops            ││
│ │  10  │ P100008     │    12     │     0    │ Directory              ││
│ └─────────────────────────────────────────────────────────────────────┘│
│                                                                         │
│ RECOMMENDATIONS SUMMARY                                                 │
│ ┌─────────────────────────────────────────────────────────────────────┐│
│ │ • 47 gaps require immediate attention (within 24 hours)            ││
│ │ • 32 NPI/TIN mismatches need NPPES validation                      ││
│ │ • 8 credentialing status conflicts need verification               ││
│ │ • Data sync pipeline review recommended for systemic fix           ││
│ │ • Consider implementing real-time sync for critical fields         ││
│ └─────────────────────────────────────────────────────────────────────┘│
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 COMPLETE MOCK DATA (Pre-computed)

### Reconciliation Gaps Data (All 604 gaps - showing first 50)

```javascript
const RECONCILIATION_GAPS = [
  // ===== PROVIDER P100000 (27 gaps) =====
  {
    id: "GAP-001",
    provider_id: "P100000",
    provider_name_simplyr: "Ana Garcia, DO",
    provider_name_lake: "Ana Garcia",
    field: "npi",
    simplyr_value: "1065939459",
    lake_value: "1014581341",
    gap_type: "Mismatch",
    domain: "Claims",
    severity_score: 10,
    priority: "Critical",
    owner: "Claims Operations",
    status: "Pending",
    root_cause: "Provider ID collision detected. Lake record appears to contain data from a different provider incorrectly mapped to same Provider ID. 27 field mismatches (22.5% discrepancy rate) including NPI, TIN, DOB suggests completely different individuals.",
    recommendation: "CRITICAL: Do NOT auto-sync. Manual investigation required. Step 1: Validate Simplyr NPI (1065939459) against NPPES. Step 2: Validate Lake NPI (1014581341) against NPPES. Step 3: If different providers confirmed, correct Provider ID mapping in Lake. Escalate to Data Governance.",
    next_steps: ["Query NPPES API for both NPIs", "Compare NPPES results", "Identify root cause of ID collision", "Create ServiceNow ticket", "Notify Claims of potential impact"],
    suggested_workflow: "WF_PROVIDER_ID_COLLISION_CRITICAL",
    created_at: "2025-12-05T09:31:54Z",
    age_days: 0
  },
  {
    id: "GAP-002",
    provider_id: "P100000",
    provider_name_simplyr: "Ana Garcia, DO",
    provider_name_lake: "Ana Garcia",
    field: "tin",
    simplyr_value: "534360412",
    lake_value: "260622691",
    gap_type: "Mismatch",
    domain: "Claims",
    severity_score: 10,
    priority: "Critical",
    owner: "Claims Operations",
    status: "Pending",
    root_cause: "TIN mismatch is part of the same Provider ID collision issue affecting P100000. Different TINs confirm these are likely different legal entities incorrectly sharing the same Provider ID.",
    recommendation: "CRITICAL: Related to NPI collision issue (GAP-001). TIN mismatch confirms different legal entities. Do NOT process payments until resolved. Verify W-9 on file matches Simplyr TIN. If validated, this supports Simplyr as authoritative source.",
    next_steps: ["Review W-9 documentation", "Cross-reference with NPI investigation", "Hold payment processing for P100000", "Document findings"],
    suggested_workflow: "WF_TIN_VERIFICATION_CRITICAL",
    created_at: "2025-12-05T09:31:54Z",
    age_days: 0
  },
  {
    id: "GAP-003",
    provider_id: "P100000",
    provider_name_simplyr: "Ana Garcia, DO",
    provider_name_lake: "Ana Garcia",
    field: "credentialing_status",
    simplyr_value: "Verified",
    lake_value: "Expired",
    gap_type: "Mismatch",
    domain: "Credentialing",
    severity_score: 9,
    priority: "Critical",
    owner: "Credentialing Team",
    status: "Pending",
    root_cause: "Credentialing status mismatch. Simplyr shows Verified (active) while Lake shows Expired. If Lake is used for claims adjudication, this could cause incorrect denials for a credentialed provider.",
    recommendation: "HIGH PRIORITY: Verify actual credentialing status from primary source documents. If provider is truly Verified, Lake must be updated immediately to prevent member access issues and incorrect claims denials.",
    next_steps: ["Pull credentialing file for P100000", "Verify current status with CAQH", "Update Lake if Simplyr confirmed correct", "Audit recent claims for incorrect denials"],
    suggested_workflow: "WF_CREDENTIALING_STATUS_UPDATE",
    created_at: "2025-12-05T09:31:54Z",
    age_days: 0
  },
  {
    id: "GAP-004",
    provider_id: "P100000",
    provider_name_simplyr: "Ana Garcia, DO",
    provider_name_lake: "Ana Garcia",
    field: "specialty_primary",
    simplyr_value: "Family Medicine",
    lake_value: "Orthopedics",
    gap_type: "Mismatch",
    domain: "Provider Directory",
    severity_score: 8,
    priority: "High",
    owner: "Directory Management",
    status: "Pending",
    root_cause: "Major specialty discrepancy. Family Medicine and Orthopedics are completely unrelated specialties. This further confirms Provider ID collision hypothesis - these appear to be different providers.",
    recommendation: "Specialty mismatch supports Provider ID collision theory. Verify board certification records. Cross-reference with taxonomy codes. Do not update until NPI/TIN investigation (GAP-001, GAP-002) is resolved.",
    next_steps: ["Wait for NPI investigation results", "Verify board certifications", "Check taxonomy code alignment", "Update directory after root cause resolved"],
    suggested_workflow: "WF_SPECIALTY_VERIFICATION",
    created_at: "2025-12-05T09:31:54Z",
    age_days: 0
  },
  {
    id: "GAP-005",
    provider_id: "P100000",
    provider_name_simplyr: "Ana Garcia, DO",
    provider_name_lake: "Ana Garcia",
    field: "contract_status",
    simplyr_value: "Pending",
    lake_value: "Inactive",
    gap_type: "Mismatch",
    domain: "Network Ops",
    severity_score: 8,
    priority: "High",
    owner: "Network Management",
    status: "Pending",
    root_cause: "Contract status discrepancy affects network participation and claims payment. Pending in Simplyr suggests onboarding in progress. Inactive in Lake suggests terminated. Different statuses have significant payment implications.",
    recommendation: "Verify current contract status with contracting team. If Pending (onboarding), provider should NOT appear as in-network in Lake. If truly Inactive, Simplyr needs update. Critical for claims accuracy.",
    next_steps: ["Review contract management system", "Verify effective dates", "Align status across systems", "Notify claims of correct status"],
    suggested_workflow: "WF_CONTRACT_STATUS_VERIFICATION",
    created_at: "2025-12-05T09:31:54Z",
    age_days: 0
  },
  {
    id: "GAP-006",
    provider_id: "P100000",
    provider_name_simplyr: "Ana Garcia, DO",
    provider_name_lake: "Ana Garcia",
    field: "dob",
    simplyr_value: "1/1/1962",
    lake_value: "1/1/1994",
    gap_type: "Mismatch",
    domain: "Provider Directory",
    severity_score: 7,
    priority: "High",
    owner: "Directory Management",
    status: "Pending",
    root_cause: "32-year difference in date of birth. This is not a data entry error - confirms different individuals. Strong evidence of Provider ID collision.",
    recommendation: "DOB discrepancy confirms different individuals. This is definitive evidence of Provider ID collision. Do not attempt to reconcile - requires source data investigation.",
    next_steps: ["Document as evidence for Provider ID collision", "Include in investigation report", "No direct action - dependent on NPI resolution"],
    suggested_workflow: "WF_IDENTITY_VERIFICATION",
    created_at: "2025-12-05T09:31:54Z",
    age_days: 0
  },
  {
    id: "GAP-007",
    provider_id: "P100000",
    provider_name_simplyr: "Ana Garcia, DO",
    provider_name_lake: "Ana Garcia",
    field: "license_state",
    simplyr_value: "IL",
    lake_value: "TX",
    gap_type: "Mismatch",
    domain: "Credentialing",
    severity_score: 7,
    priority: "High",
    owner: "Credentialing Team",
    status: "Pending",
    root_cause: "License state mismatch. Provider cannot practice in both IL and TX without separate licenses. This affects network adequacy and regulatory compliance.",
    recommendation: "Verify state licensure records. Cross-reference with practice address. If multi-state provider, both licenses should be on file. Part of larger Provider ID investigation.",
    next_steps: ["Query state medical board for IL license", "Query state medical board for TX license", "Document all active licenses", "Update both systems with complete license list"],
    suggested_workflow: "WF_LICENSE_VERIFICATION",
    created_at: "2025-12-05T09:31:54Z",
    age_days: 0
  },
  {
    id: "GAP-008",
    provider_id: "P100000",
    provider_name_simplyr: "Ana Garcia, DO",
    provider_name_lake: "Ana Garcia",
    field: "practice_state",
    simplyr_value: "IL",
    lake_value: "NY",
    gap_type: "Mismatch",
    domain: "Provider Directory",
    severity_score: 6,
    priority: "Medium",
    owner: "Directory Management",
    status: "Pending",
    root_cause: "Practice state mismatch affects member search and network adequacy reporting. IL vs NY are different service areas.",
    recommendation: "Verify current practice location. Member-facing impact - incorrect state will cause members to not find provider or see incorrect provider in search results.",
    next_steps: ["Verify practice address with provider", "Update directory accordingly", "Check impact on network adequacy metrics"],
    suggested_workflow: "WF_ADDRESS_UPDATE",
    created_at: "2025-12-05T09:31:54Z",
    age_days: 0
  },
  {
    id: "GAP-009",
    provider_id: "P100000",
    provider_name_simplyr: "Ana Garcia, DO",
    provider_name_lake: "Ana Garcia",
    field: "suffix",
    simplyr_value: "DO",
    lake_value: "",
    gap_type: "Missing_In_Lake",
    domain: "Provider Directory",
    severity_score: 5,
    priority: "Medium",
    owner: "Directory Management",
    status: "Pending",
    root_cause: "Provider suffix (DO - Doctor of Osteopathy) missing in Lake. Affects provider title display in directory.",
    recommendation: "Update Lake with suffix 'DO' from Simplyr. Low risk update - can be auto-synced after Provider ID issue resolved.",
    next_steps: ["Queue for update after main investigation", "Add to batch update list"],
    suggested_workflow: "WF_DIRECTORY_UPDATE_BATCH",
    created_at: "2025-12-05T09:31:54Z",
    age_days: 0
  },
  {
    id: "GAP-010",
    provider_id: "P100000",
    provider_name_simplyr: "Ana Garcia, DO",
    provider_name_lake: "Ana Garcia",
    field: "gender",
    simplyr_value: "M",
    lake_value: "U",
    gap_type: "Mismatch",
    domain: "Provider Directory",
    severity_score: 4,
    priority: "Medium",
    owner: "Directory Management",
    status: "Pending",
    root_cause: "Gender shows Male in Simplyr, Unknown in Lake. Lake may have defaulted to Unknown due to missing data during ingestion.",
    recommendation: "Update Lake with Simplyr value (M) after confirming with provider records. Low priority but affects demographic reporting.",
    next_steps: ["Verify gender from credentialing file", "Update Lake", "Low priority - batch update eligible"],
    suggested_workflow: "WF_DEMOGRAPHIC_UPDATE",
    created_at: "2025-12-05T09:31:54Z",
    age_days: 0
  },
  {
    id: "GAP-011",
    provider_id: "P100000",
    provider_name_simplyr: "Ana Garcia, DO",
    provider_name_lake: "Ana Garcia",
    field: "phone",
    simplyr_value: "",
    lake_value: "2125551212",
    gap_type: "Missing_In_Simplyr",
    domain: "Provider Directory",
    severity_score: 3,
    priority: "Low",
    owner: "Directory Management",
    status: "Pending",
    root_cause: "Phone number exists in Lake but missing in Simplyr. Lake may have more recent contact information from different source.",
    recommendation: "Consider backfilling Simplyr with Lake phone number after verification. Verify number is current before update. Lower priority.",
    next_steps: ["Verify phone number is current", "Update Simplyr if valid", "Low priority - batch eligible"],
    suggested_workflow: "WF_CONTACT_UPDATE",
    created_at: "2025-12-05T09:31:54Z",
    age_days: 0
  },
  
  // ===== PROVIDER P100001 (22 gaps) =====
  {
    id: "GAP-012",
    provider_id: "P100001",
    provider_name_simplyr: "Priya Smith, PA",
    provider_name_lake: "John Johnson, PA",
    field: "npi",
    simplyr_value: "1502778451",
    lake_value: "1600215021",
    gap_type: "Mismatch",
    domain: "Claims",
    severity_score: 10,
    priority: "Critical",
    owner: "Claims Operations",
    status: "Pending",
    root_cause: "Complete provider mismatch. Names are entirely different (Priya Smith vs John Johnson) indicating Provider ID collision. NPI, name, and multiple demographics all differ.",
    recommendation: "CRITICAL: Provider ID P100001 maps to completely different individuals in each system. Immediate investigation required. Do NOT sync - will corrupt data in both directions.",
    next_steps: ["Validate both NPIs in NPPES", "Determine correct Provider ID assignment", "Correct source system mapping", "Create incident report"],
    suggested_workflow: "WF_PROVIDER_ID_COLLISION_CRITICAL",
    created_at: "2025-12-05T09:31:54Z",
    age_days: 0
  },
  {
    id: "GAP-013",
    provider_id: "P100001",
    provider_name_simplyr: "Priya Smith, PA",
    provider_name_lake: "John Johnson, PA",
    field: "first_name",
    simplyr_value: "Priya",
    lake_value: "John",
    gap_type: "Mismatch",
    domain: "Provider Directory",
    severity_score: 9,
    priority: "Critical",
    owner: "Directory Management",
    status: "Pending",
    root_cause: "First name completely different. Not a spelling variation - entirely different names confirming Provider ID collision.",
    recommendation: "Name mismatch confirms Provider ID collision. Do NOT update either system. Requires source data investigation to determine correct assignment.",
    next_steps: ["Document as Provider ID collision evidence", "Include in investigation ticket"],
    suggested_workflow: "WF_IDENTITY_VERIFICATION",
    created_at: "2025-12-05T09:31:54Z",
    age_days: 0
  },
  {
    id: "GAP-014",
    provider_id: "P100001",
    provider_name_simplyr: "Priya Smith, PA",
    provider_name_lake: "John Johnson, PA",
    field: "last_name",
    simplyr_value: "Smith",
    lake_value: "Johnson",
    gap_type: "Mismatch",
    domain: "Provider Directory",
    severity_score: 9,
    priority: "Critical",
    owner: "Directory Management",
    status: "Pending",
    root_cause: "Last name completely different. Smith vs Johnson - confirms different providers under same ID.",
    recommendation: "Part of Provider ID collision for P100001. Last name difference adds to evidence of separate providers.",
    next_steps: ["Document as evidence", "Bundle with other P100001 gaps"],
    suggested_workflow: "WF_IDENTITY_VERIFICATION",
    created_at: "2025-12-05T09:31:54Z",
    age_days: 0
  },
  {
    id: "GAP-015",
    provider_id: "P100001",
    provider_name_simplyr: "Priya Smith, PA",
    provider_name_lake: "John Johnson, PA",
    field: "credentialing_status",
    simplyr_value: "Expired",
    lake_value: "Expired",
    gap_type: "Match",
    domain: "Credentialing",
    severity_score: 0,
    priority: "None",
    owner: "Credentialing Team",
    status: "Matched",
    root_cause: "N/A - Values match",
    recommendation: "No action required - field values are consistent across systems.",
    next_steps: [],
    suggested_workflow: null,
    created_at: "2025-12-05T09:31:54Z",
    age_days: 0
  },
  
  // ===== PROVIDER P100002 (24 gaps) =====
  {
    id: "GAP-016",
    provider_id: "P100002",
    provider_name_simplyr: "Luis Johnson, DO",
    provider_name_lake: "David Kim, PA",
    field: "npi",
    simplyr_value: "1010168041",
    lake_value: "1510441276",
    gap_type: "Mismatch",
    domain: "Claims",
    severity_score: 10,
    priority: "Critical",
    owner: "Claims Operations",
    status: "Pending",
    root_cause: "Another Provider ID collision. Simplyr shows Luis Johnson, DO while Lake shows David Kim, PA. Completely different individuals with different credentials.",
    recommendation: "CRITICAL: Same pattern as P100000 and P100001. Systemic Provider ID mapping issue suspected. Escalate to Data Governance for pattern analysis.",
    next_steps: ["Add to pattern analysis", "Check Provider ID generation process", "Audit all Provider IDs for collisions"],
    suggested_workflow: "WF_SYSTEMIC_DATA_ISSUE",
    created_at: "2025-12-05T09:31:54Z",
    age_days: 0
  },
  {
    id: "GAP-017",
    provider_id: "P100002",
    provider_name_simplyr: "Luis Johnson, DO",
    provider_name_lake: "David Kim, PA",
    field: "tin",
    simplyr_value: "809296119",
    lake_value: "569288394",
    gap_type: "Mismatch",
    domain: "Claims",
    severity_score: 10,
    priority: "Critical",
    owner: "Claims Operations",
    status: "Pending",
    root_cause: "TIN mismatch consistent with Provider ID collision pattern.",
    recommendation: "Part of P100002 collision issue. Different TINs confirm different legal entities.",
    next_steps: ["Bundle with NPI investigation", "Verify W-9 records"],
    suggested_workflow: "WF_TIN_VERIFICATION_CRITICAL",
    created_at: "2025-12-05T09:31:54Z",
    age_days: 0
  },
  {
    id: "GAP-018",
    provider_id: "P100002",
    provider_name_simplyr: "Luis Johnson, DO",
    provider_name_lake: "David Kim, PA",
    field: "specialty_primary",
    simplyr_value: "Dermatology",
    lake_value: "Cardiology",
    gap_type: "Mismatch",
    domain: "Provider Directory",
    severity_score: 8,
    priority: "High",
    owner: "Directory Management",
    status: "Pending",
    root_cause: "Specialty mismatch. Dermatology vs Cardiology are unrelated specialties.",
    recommendation: "Further evidence of Provider ID collision. Different specialties cannot be reconciled without determining correct provider.",
    next_steps: ["Document for investigation", "Do not auto-update"],
    suggested_workflow: "WF_SPECIALTY_VERIFICATION",
    created_at: "2025-12-05T09:31:54Z",
    age_days: 0
  },

  // ===== PROVIDER P100003 (19 gaps) =====
  {
    id: "GAP-019",
    provider_id: "P100003",
    provider_name_simplyr: "Priya Smith, DO",
    provider_name_lake: "David Patel, DO",
    field: "contract_status",
    simplyr_value: "Active",
    lake_value: "Terminated",
    gap_type: "Mismatch",
    domain: "Network Ops",
    severity_score: 9,
    priority: "Critical",
    owner: "Network Management",
    status: "Pending",
    root_cause: "Critical contract status discrepancy. Active vs Terminated has major claims payment implications. If Lake is used for claims, active provider may be incorrectly denied.",
    recommendation: "URGENT: Verify current contract status immediately. If Active in contract system, Lake must be corrected. Active providers being shown as Terminated will cause claims denials.",
    next_steps: ["Query contract management system", "Verify effective/term dates", "Correct Lake if Active confirmed", "Monitor for affected claims"],
    suggested_workflow: "WF_CONTRACT_STATUS_CRITICAL",
    created_at: "2025-12-05T09:31:54Z",
    age_days: 1
  },
  {
    id: "GAP-020",
    provider_id: "P100003",
    provider_name_simplyr: "Priya Smith, DO",
    provider_name_lake: "David Patel, DO",
    field: "npi",
    simplyr_value: "1592491251",
    lake_value: "1050474560",
    gap_type: "Mismatch",
    domain: "Claims",
    severity_score: 10,
    priority: "Critical",
    owner: "Claims Operations",
    status: "Pending",
    root_cause: "NPI mismatch with different names. Another Provider ID collision case.",
    recommendation: "CRITICAL: Same Provider ID collision pattern. Different NPIs and different names (Priya Smith vs David Patel).",
    next_steps: ["NPPES validation", "Add to systemic investigation"],
    suggested_workflow: "WF_PROVIDER_ID_COLLISION_CRITICAL",
    created_at: "2025-12-05T09:31:54Z",
    age_days: 1
  },

  // ===== ADDITIONAL GAPS (Medium/Low Priority Examples) =====
  {
    id: "GAP-021",
    provider_id: "P100005",
    provider_name_simplyr: "Ana Smith, NP",
    provider_name_lake: "Chen Garcia, MD",
    field: "phone",
    simplyr_value: "2125551212",
    lake_value: "",
    gap_type: "Missing_In_Lake",
    domain: "Provider Directory",
    severity_score: 5,
    priority: "Medium",
    owner: "Directory Management",
    status: "Pending",
    root_cause: "Phone number exists in Simplyr but missing in Lake. Members searching Lake-powered directory cannot contact provider.",
    recommendation: "Sync phone number from Simplyr to Lake. Standard directory update - can be batched with other contact updates.",
    next_steps: ["Verify phone number is current", "Add to Lake update batch", "Confirm after sync"],
    suggested_workflow: "WF_DIRECTORY_UPDATE_BATCH",
    created_at: "2025-12-05T09:31:54Z",
    age_days: 2
  },
  {
    id: "GAP-022",
    provider_id: "P100007",
    provider_name_simplyr: "Luis Smith",
    provider_name_lake: "Luis Johnson, MD",
    field: "telehealth_flag",
    simplyr_value: "Yes",
    lake_value: "Yes",
    gap_type: "Match",
    domain: "Provider Directory",
    severity_score: 0,
    priority: "None",
    owner: "Directory Management",
    status: "Matched",
    root_cause: "N/A - Values match",
    recommendation: "No action required.",
    next_steps: [],
    suggested_workflow: null,
    created_at: "2025-12-05T09:31:54Z",
    age_days: 0
  },
  {
    id: "GAP-023",
    provider_id: "P100010",
    provider_name_simplyr: "Sarah Garcia, MD",
    provider_name_lake: "Sarah Singh, PA",
    field: "languages_spoken",
    simplyr_value: "Mandarin",
    lake_value: "Spanish",
    gap_type: "Mismatch",
    domain: "Provider Directory",
    severity_score: 4,
    priority: "Medium",
    owner: "Directory Management",
    status: "Pending",
    root_cause: "Language mismatch. May affect member search for language-specific providers.",
    recommendation: "Verify languages spoken with provider. Update directory for accurate member search. May be multi-lingual - consider adding both.",
    next_steps: ["Contact provider office", "Update language list", "May need to support multiple languages"],
    suggested_workflow: "WF_PROVIDER_OUTREACH",
    created_at: "2025-12-05T09:31:54Z",
    age_days: 3
  },
  {
    id: "GAP-024",
    provider_id: "P100015",
    provider_name_simplyr: "David Smith",
    provider_name_lake: "Luis Patel",
    field: "accepting_new_patients_flag",
    simplyr_value: "Yes",
    lake_value: "No",
    gap_type: "Mismatch",
    domain: "Provider Directory",
    severity_score: 6,
    priority: "Medium",
    owner: "Directory Management",
    status: "Pending",
    root_cause: "Panel status affects member experience. If provider is accepting but shown as not accepting, members cannot book.",
    recommendation: "Verify current panel status with practice. Update immediately if accepting - affects member access to care.",
    next_steps: ["Call provider office", "Confirm panel status", "Update Lake if accepting"],
    suggested_workflow: "WF_PANEL_STATUS_UPDATE",
    created_at: "2025-12-05T09:31:54Z",
    age_days: 5
  },
  {
    id: "GAP-025",
    provider_id: "P100020",
    provider_name_simplyr: "Ana Johnson, DO",
    provider_name_lake: "Ana Wong, DO",
    field: "practice_zip",
    simplyr_value: "73657",
    lake_value: "62980",
    gap_type: "Mismatch",
    domain: "Provider Directory",
    severity_score: 5,
    priority: "Medium",
    owner: "Directory Management",
    status: "Pending",
    root_cause: "ZIP code mismatch affects member search by location. May indicate address change not synced.",
    recommendation: "Verify current practice address. ZIP code affects distance calculations for member search.",
    next_steps: ["Confirm current address with provider", "Update both systems if change verified", "Recalculate geocode"],
    suggested_workflow: "WF_ADDRESS_UPDATE",
    created_at: "2025-12-05T09:31:54Z",
    age_days: 4
  },
  
  // Continue with more gaps...
  // (In the actual implementation, all 604 gaps would be defined)
];

// Summary statistics (pre-calculated)
const STATS = {
  total_providers: 99,
  total_fields_compared: 11880,
  total_gaps: 604,
  providers_with_gaps: 87,
  providers_clean: 12,
  
  by_priority: {
    critical: 47,
    high: 156,
    medium: 312,
    low: 89
  },
  
  by_domain: {
    claims: { count: 211, percentage: 35 },
    credentialing: { count: 169, percentage: 28 },
    network_ops: { count: 133, percentage: 22 },
    directory: { count: 91, percentage: 15 }
  },
  
  by_root_cause: {
    data_sync_failure: { count: 254, percentage: 42 },
    source_system_delay: { count: 169, percentage: 28 },
    data_entry_error: { count: 91, percentage: 15 },
    format_mismatch: { count: 60, percentage: 10 },
    unknown: { count: 30, percentage: 5 }
  },
  
  by_gap_type: {
    mismatch: 456,
    missing_in_lake: 98,
    missing_in_simplyr: 42,
    format_difference: 8
  },
  
  resolution_rate: 67.2,
  avg_resolution_days: 2.3
};
```

---

## 🔧 INTERACTION BEHAVIORS

### Navigation
- Clicking sidebar items navigates to respective screens
- Active item is highlighted with accent color and left border
- Breadcrumbs show current location in workflow

### Tables
- Rows are clickable to open detail side panel
- Checkbox column for bulk selection
- Sortable columns (click header to sort)
- Pagination with 10/25/50/100 per page options

### Side Panel
- Opens from right side with smooth slide animation
- Overlay dims main content
- Close button and click-outside-to-close
- Scrollable content area

### Forms
- All inputs have focus states (blue border)
- Required fields marked with red asterisk
- Validation messages appear below inputs
- Buttons have hover and active states

### Filters
- Dropdown filters with checkbox multi-select
- Active filters shown as removable chips
- "Clear All" button when filters active
- Filter state persists during session

### Status Updates
- Toast notifications for actions (approve/reject)
- Loading spinners for processing states
- Success/error states for operations

---

## 📱 RESPONSIVE BEHAVIOR

### Desktop (1280px+)
- Full sidebar visible
- Multi-column layouts
- Side panel is 480px wide

### Tablet (768px - 1279px)
- Collapsible sidebar (hamburger menu)
- Two-column layouts stack to single
- Side panel is full width overlay

### Mobile (< 768px)
- Hidden sidebar (hamburger only)
- Single column layouts
- Full screen overlays for details
- Simplified table views (card-based)

---

## ✨ ANIMATIONS

### Transitions
- Page transitions: 200ms ease-in-out
- Sidebar collapse: 300ms ease
- Side panel slide: 250ms ease-out
- Hover states: 150ms

### Loading States
- Skeleton loaders for data tables
- Spinner for processing operations
- Progress bar for multi-step processes

### Micro-interactions
- Button ripple effect on click
- Checkbox animation (checkmark draw)
- Toast slide-in from top-right

---

## 📋 COMPONENT LIBRARY

Create reusable components for:
1. **Button** (Primary, Secondary, Ghost, Danger)
2. **Input** (Text, Password, Search)
3. **Select/Dropdown** (Single, Multi)
4. **Checkbox** (Standard, Indeterminate)
5. **Badge** (Status colors)
6. **Card** (With header, actions)
7. **Table** (Sortable, Selectable, Paginated)
8. **Modal** (Confirmation, Form)
9. **Side Panel** (Detail view)
10. **Toast** (Success, Error, Warning, Info)
11. **Progress** (Bar, Circular)
12. **Tabs** (Horizontal)
13. **Stepper** (Horizontal, Vertical)
14. **Avatar** (Initials, Image)
15. **Charts** (Donut, Bar, Line)

---

## 🎯 FINAL NOTES FOR FIGMA AI

1. **Enterprise Quality**: This is a professional B2B healthcare application. Use clean, corporate design language. Avoid playful elements.

2. **Accessibility**: Ensure WCAG 2.1 AA compliance. Color contrast ratios must meet standards. Include focus indicators.

3. **Data Density**: Healthcare operations need to see lots of data. Optimize for information density while maintaining readability.

4. **Consistency**: Use the design system strictly. All elements should feel cohesive.

5. **White Space**: Use generous padding and margins. Don't crowd elements.

6. **Icons**: Use a professional icon set (Heroicons, Phosphor, or similar). Consistent stroke width.

7. **All Data is Pre-loaded**: Remember, this is 100% frontend. All the data above should be embedded in the application. File "upload" is simulated - it immediately loads the pre-defined data.

8. **No API Calls**: All data comes from the JavaScript objects defined above. Filter, sort, and search operations work on client-side data.

---

**END OF FIGMA PROMPT**
