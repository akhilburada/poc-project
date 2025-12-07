# HCSC Provider Data Reconciliation - Enterprise UI

Design a futuristic, enterprise-grade 4-step workflow app. 100% frontend with ALL data pre-loaded. Dark glassmorphism theme with neon accents.

---

## DESIGN SYSTEM

**Theme:** Dark futuristic glassmorphism
**Background:** Deep gradient #0A0F1C → #1A1F3C with subtle grid pattern
**Cards:** Semi-transparent glass (rgba(255,255,255,0.05)) with blur backdrop, glowing borders
**Primary:** Electric blue #3B82F6, Cyan accent #06B6D4
**Status:** Critical #EF4444, High #F97316, Medium #EAB308, Low #22C55E
**Text:** White #FFFFFF, Muted #94A3B8
**Font:** Inter/SF Pro, monospace for data
**Effects:** Subtle glow, smooth 300ms transitions, hover lift animations

---

## LOGIN PAGE

Full dark gradient background with animated mesh/particles. Centered glass card (480px):

```
┌─────────────────────────────────────────────────┐
│                                                 │
│           🏥 HCSC                               │
│     Provider Data Reconciliation                │
│     ─────────────────────────                   │
│                                                 │
│     ┌─────────────────────────────────┐         │
│     │ 👤  Username                    │         │
│     └─────────────────────────────────┘         │
│                                                 │
│     ┌─────────────────────────────────┐         │
│     │ 🔒  Password               👁   │         │
│     └─────────────────────────────────┘         │
│                                                 │
│     ☑ Remember me                               │
│                                                 │
│     ┌─────────────────────────────────┐         │
│     │         SIGN IN →               │ (glow)  │
│     └─────────────────────────────────┘         │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Credentials:** admin / admin123

---

## MAIN LAYOUT (All Steps)

**Header (70px, glass):**
- Left: 🏥 HCSC logo with cyan glow
- Center: Step progress with glowing active step
- Right: "Admin" avatar dropdown, notification bell

**Step Progress Indicator:**
```
[1 UPLOAD]━━━━[2 RECONCILE]━━━━[3 AI ANALYSIS]━━━━[4 EXPORT]
   ●              ●                 ○                 ○
```
Active = pulsing cyan, Completed = solid green ✓, Pending = dim outline

---

## STEP 1: DATA UPLOAD

**Header:** "📤 Upload Provider Data Files"
**Subtext:** "Upload Simplyr and Data Lake CSV files to begin reconciliation"

**Two glass cards side by side:**

```
┌─────────────────────────────┐   ┌─────────────────────────────┐
│  SIMPLYR SOURCE             │   │  DATA LAKE SOURCE           │
│  ┌───────────────────────┐  │   │  ┌───────────────────────┐  │
│  │                       │  │   │  │                       │  │
│  │     ☁️ DROP FILE      │  │   │  │     ☁️ DROP FILE      │  │
│  │   or click to browse  │  │   │  │   or click to browse  │  │
│  │                       │  │   │  │                       │  │
│  │   CSV • XLSX • 50MB   │  │   │  │   CSV • XLSX • 50MB   │  │
│  └───────────────────────┘  │   │  └───────────────────────┘  │
│                             │   │                             │
│  [Browse Files]             │   │  [Browse Files]             │
└─────────────────────────────┘   └─────────────────────────────┘
```

**After upload - Show REAL file info:**

```
┌─────────────────────────────┐   ┌─────────────────────────────┐
│  ✅ SIMPLYR SOURCE          │   │  ✅ DATA LAKE SOURCE        │
│  ─────────────────────────  │   │  ─────────────────────────  │
│  📄 simplyr_sample.csv      │   │  📄 datalake_sample.csv     │
│                             │   │                             │
│  Providers:     99          │   │  Providers:     99          │
│  Fields:        58          │   │  Fields:        58          │
│  Size:          127 KB      │   │  Size:          124 KB      │
│                             │   │                             │
│  Sample Records:            │   │  Sample Records:            │
│  • P100000 - Ana Garcia     │   │  • P100000 - Ana Garcia     │
│  • P100001 - Priya Smith    │   │  • P100001 - John Johnson   │
│  • P100002 - Luis Johnson   │   │  • P100002 - David Kim      │
│                             │   │                             │
│  [Preview Data] [✕ Remove]  │   │  [Preview Data] [✕ Remove]  │
└─────────────────────────────┘   └─────────────────────────────┘
```

**Button:** "Start Reconciliation →" (cyan glow, enabled when both uploaded)

---

## STEP 2: RECONCILIATION (Task Layer - NO AI Yet)

**Processing Animation (3 seconds):**
```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                    🔄 Running Reconciliation                    │
│                                                                 │
│     ████████████████████████░░░░░░░░░░  67%                    │
│                                                                 │
│     ✅ Loading Simplyr data (99 records)                       │
│     ✅ Loading Data Lake data (99 records)                     │
│     ✅ Matching by Provider ID                                 │
│     ⏳ Comparing 5,742 field pairs...                          │
│     ○  Calculating gap statistics                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Results Dashboard:**

**Summary Cards (glass, glowing borders):**
```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  PROVIDERS   │  │   FIELDS     │  │    GAPS      │  │  AFFECTED    │
│      99      │  │    5,742     │  │     247      │  │   72.7%      │
│  Matched     │  │  Compared    │  │  Identified  │  │  (72 of 99)  │
└──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
```

**Priority Filter Pills (clickable):**
```
[🔴 23 Critical]  [🟠 64 High]  [🟡 112 Medium]  [🟢 48 Low]
```

**RAW GAPS TABLE (No AI columns - just comparison):**

| Provider ID | Field | Simplyr Value | Lake Value | Gap Type |
|-------------|-------|---------------|------------|----------|
| P100000 | npi | 1065939459 | 1014581341 | Mismatch |
| P100000 | tin | 534360412 | 260622691 | Mismatch |
| P100000 | suffix | DO | (empty) | Missing_In_Lake |
| P100000 | gender | M | U | Mismatch |
| P100000 | dob | 1/1/1962 | 1/1/1994 | Mismatch |
| P100000 | contract_status | Pending | Inactive | Mismatch |
| P100000 | credentialing_status | Verified | Expired | Mismatch |
| P100000 | specialty_primary | Family Medicine | Orthopedics | Mismatch |
| P100000 | practice_state | IL | NY | Mismatch |
| P100000 | license_state | IL | TX | Mismatch |
| P100001 | npi | 1502778451 | 1600215021 | Mismatch |
| P100001 | first_name | Priya | John | Mismatch |
| P100001 | last_name | Smith | Johnson | Mismatch |
| P100001 | gender | M | F | Mismatch |
| P100001 | dob | 1/1/1974 | 1/1/1957 | Mismatch |
| P100001 | tin | 607697301 | 122193804 | Mismatch |
| P100001 | specialty_primary | Pediatrics | Orthopedics | Mismatch |
| P100002 | npi | 1010168041 | 1510441276 | Mismatch |
| P100002 | first_name | Luis | David | Mismatch |
| P100002 | last_name | Johnson | Kim | Mismatch |
| P100002 | suffix | DO | PA | Mismatch |
| P100002 | specialty_primary | Dermatology | Cardiology | Mismatch |
| P100003 | npi | 1592491251 | 1050474560 | Mismatch |
| P100003 | first_name | Priya | David | Mismatch |
| P100003 | contract_status | Active | Terminated | Mismatch |
| P100005 | phone | 2125551212 | (empty) | Missing_In_Lake |

*Pagination: "Showing 1-25 of 247 gaps" [← 1 2 3 ... 10 →]*

**Provider Dropdown Filter:** [All Providers ▾] - List P100000 through P100098

**Button:** "🧠 Run AI Analysis →" (prominent cyan glow)

---

## STEP 3: AI ANALYSIS (Intelligence Layer)

**Processing Animation (4 seconds):**
```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                    🧠 Running AI Analysis                       │
│                                                                 │
│     ████████████████████████████░░░░░  78%                     │
│                                                                 │
│     ✅ Analyzing gap patterns                                  │
│     ✅ Detecting root causes                                   │
│     ⏳ Generating recommendations...                           │
│     ○  Calculating severity scores                             │
│     ○  Assigning ownership                                     │
│     ○  Creating workflow suggestions                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**AI Results Dashboard:**

**Domain Filter Tabs:**
```
[All Domains]  [Claims 89]  [Credentialing 62]  [Network 54]  [Directory 42]
```

**AI-ENRICHED TABLE (adds Root Cause, Recommendation, Owner, Domain, Score):**

| Provider | Field | Simplyr | Lake | Type | Root Cause | Recommendation | Owner | Domain | Score |
|----------|-------|---------|------|------|------------|----------------|-------|--------|-------|
| P100000 | npi | 1065939459 | 1014581341 | Mismatch | Provider ID collision. 27 mismatches including NPI, TIN, DOB = different providers | CRITICAL: Do NOT sync. Validate NPPES. Escalate to Data Governance | Claims Ops | Claims | 🔴 10 |
| P100000 | tin | 534360412 | 260622691 | Mismatch | TIN confirms different legal entities. Related to NPI collision | CRITICAL: Hold payments. Verify W-9 on file | Claims Ops | Claims | 🔴 10 |
| P100000 | credentialing_status | Verified | Expired | Mismatch | Status conflict causes claims denials | HIGH: Verify CAQH. Update Lake if Verified | Cred Team | Credentialing | 🔴 9 |
| P100000 | specialty_primary | Family Medicine | Orthopedics | Mismatch | Unrelated specialties confirm collision | Part of collision investigation | Directory | Directory | 🟠 8 |
| P100000 | dob | 1/1/1962 | 1/1/1994 | Mismatch | 32-year difference. Definitive collision evidence | Document as collision evidence | Directory | Directory | 🟠 7 |
| P100001 | npi | 1502778451 | 1600215021 | Mismatch | Systemic collision. Priya Smith vs John Johnson = different people | CRITICAL: Systemic issue. Escalate to Data Gov | Claims Ops | Claims | 🔴 10 |
| P100001 | first_name | Priya | John | Mismatch | Names completely different - confirms collision | Do NOT update. Requires source investigation | Directory | Directory | 🔴 9 |
| P100001 | tin | 607697301 | 122193804 | Mismatch | Different TIN = different entities | Hold payments. Verify correct TIN | Claims Ops | Claims | 🔴 10 |
| P100002 | npi | 1010168041 | 1510441276 | Mismatch | 3rd collision. Luis Johnson DO vs David Kim PA | CRITICAL: Audit Provider ID generation | Claims Ops | Claims | 🔴 10 |
| P100002 | suffix | DO | PA | Mismatch | Different credentials (DO vs PA) | Cannot reconcile - different provider types | Cred Team | Credentialing | 🟠 8 |
| P100003 | contract_status | Active | Terminated | Mismatch | Payment eligibility affected | Verify contract system. Align status | Network | Network | 🟠 8 |
| P100005 | phone | 2125551212 | (empty) | Missing | Contact info incomplete in Lake | Sync phone from Simplyr | Directory | Directory | 🟡 5 |

**Row Click → Slide-in Detail Panel (from right, glass effect):**

```
┌─────────────────────────────────────────────────────────┐
│ GAP DETAILS                                        [✕]  │
├─────────────────────────────────────────────────────────┤
│ 🔴 CRITICAL  •  Score: 10/10  •  24hr SLA              │
│ Provider: P100000  •  Field: npi                        │
│ Domain: Claims  •  Owner: Claims Operations             │
├─────────────────────────────────────────────────────────┤
│ VALUE COMPARISON                                        │
│ ┌─────────────────────┬─────────────────────┐          │
│ │     SIMPLYR         │     DATA LAKE       │          │
│ │    1065939459       │    1014581341       │          │
│ │  Ana Garcia, DO     │  Different Person   │          │
│ │  Family Medicine    │  Orthopedics        │          │
│ │  DOB: 1/1/1962      │  DOB: 1/1/1994      │          │
│ └─────────────────────┴─────────────────────┘          │
├─────────────────────────────────────────────────────────┤
│ 🤖 AI ROOT CAUSE ANALYSIS                               │
│ ─────────────────────────────────────────────────────   │
│ Provider ID collision detected. Analysis of 58 fields   │
│ shows 27 mismatches (46.5%) including critical identity │
│ fields: NPI, TIN, DOB, Name, Specialty.                 │
│                                                         │
│ This pattern indicates two completely different         │
│ providers are mapped to the same Provider ID (P100000)  │
│ in the two systems.                                     │
├─────────────────────────────────────────────────────────┤
│ 💡 RECOMMENDATION                                       │
│ ─────────────────────────────────────────────────────   │
│ CRITICAL - Do NOT auto-sync these records.              │
│                                                         │
│ 1. Validate both NPIs in NPPES database                 │
│ 2. Confirm these are different providers                │
│ 3. Correct Provider ID mapping in Data Lake             │
│ 4. Escalate to Data Governance immediately              │
├─────────────────────────────────────────────────────────┤
│ 📋 NEXT STEPS                                           │
│ ☐ Query NPPES for NPI 1065939459                       │
│ ☐ Query NPPES for NPI 1014581341                       │
│ ☐ Create ServiceNow incident ticket                    │
│ ☐ Notify Claims Operations team                        │
│ ☐ Document in audit log                                │
├─────────────────────────────────────────────────────────┤
│ SUGGESTED WORKFLOW: WF_PROVIDER_ID_COLLISION            │
├─────────────────────────────────────────────────────────┤
│  [✓ Approve]   [✕ Reject]   [📝 Add Note]              │
└─────────────────────────────────────────────────────────┘
```

**BUCKETIZATION VIEWS (Toggle tabs above table):**

**Tab 1: By Provider**
| Provider ID | Total Gaps | Critical | High | Medium | Low | Primary Issue |
|-------------|------------|----------|------|--------|-----|---------------|
| P100000 | 27 | 4 | 8 | 10 | 5 | Provider ID Collision |
| P100001 | 24 | 4 | 7 | 9 | 4 | Provider ID Collision |
| P100002 | 26 | 4 | 8 | 10 | 4 | Provider ID Collision |
| P100003 | 22 | 3 | 7 | 8 | 4 | Contract + Collision |
| P100004 | 23 | 3 | 6 | 9 | 5 | Network + Collision |
| P100005 | 21 | 3 | 6 | 8 | 4 | Missing Contact |

**Tab 2: By Domain**
| Domain | Count | % | Key Fields |
|--------|-------|---|------------|
| Claims | 89 | 36.0% | npi, tin, billing |
| Credentialing | 62 | 25.1% | license, dea, caqh |
| Network Ops | 54 | 21.9% | contract, network_tier |
| Directory | 42 | 17.0% | name, address, phone |

**Tab 3: By Root Cause**
| Root Cause | Count | % | Action |
|------------|-------|---|--------|
| Provider ID Collision | 98 | 39.7% | Escalate to Data Gov |
| Data Sync Failure | 67 | 27.1% | Review ETL pipeline |
| Source Delay | 42 | 17.0% | Reduce sync interval |
| Data Entry Error | 25 | 10.1% | Implement validation |
| Format Mismatch | 15 | 6.1% | Standardize formats |

**Tab 4: By Priority**
| Priority | Count | % | SLA | Action |
|----------|-------|---|-----|--------|
| 🔴 Critical | 23 | 9.3% | 24 hrs | Immediate escalation |
| 🟠 High | 64 | 25.9% | 72 hrs | Prioritized resolution |
| 🟡 Medium | 112 | 45.3% | 1 week | Standard queue |
| 🟢 Low | 48 | 19.4% | 2 weeks | Batch processing |

**ALERT BANNER (top of page, pulsing):**
```
⚠️ SYSTEMIC ISSUE DETECTED: Provider ID Collision affecting 6+ providers. 
   98 gaps (39.7%) stem from this root cause. [View Details]
```

**Button:** "Continue to Export →"

---

## STEP 4: EXPORT & REPORTS

**Header:** "📥 Export Reconciliation Results"

**Summary Banner:**
```
✅ Analysis Complete | 247 gaps analyzed | 247 recommendations | Dec 5, 2025 14:32 EST
```

**Export Cards (2x2 grid, glass effect):**

```
┌─────────────────────────────┐  ┌─────────────────────────────┐
│ 📊 FULL REPORT              │  │ 📄 EXECUTIVE SUMMARY        │
│ Excel (.xlsx)               │  │ PDF Document                │
│ ─────────────────────────── │  │ ─────────────────────────── │
│ • All 247 gaps              │  │ • Key metrics               │
│ • AI analysis columns       │  │ • Priority breakdown        │
│ • Recommendations           │  │ • Domain distribution       │
│ • 99 providers              │  │ • Action items              │
│                             │  │                             │
│ [⬇ Download]                │  │ [⬇ Download]                │
└─────────────────────────────┘  └─────────────────────────────┘

┌─────────────────────────────┐  ┌─────────────────────────────┐
│ 🔴 CRITICAL GAPS ONLY       │  │ 📁 RAW DATA                 │
│ CSV File                    │  │ JSON Format                 │
│ ─────────────────────────── │  │ ─────────────────────────── │
│ • 23 critical items         │  │ • Full dataset              │
│ • Immediate action needed   │  │ • For system integration    │
│ • Escalation list           │  │ • API-ready format          │
│                             │  │                             │
│ [⬇ Download]                │  │ [⬇ Download]                │
└─────────────────────────────┘  └─────────────────────────────┘
```

**Action Buttons:**
```
[🔄 Start New Reconciliation]    [📧 Email Report]    [🖨 Print Summary]
```

---

## INTERACTIONS & ANIMATIONS

- **Hover:** Cards lift with increased glow
- **Click:** Ripple effect with cyan color
- **Loading:** Pulsing progress bars, sequential checklist animations
- **Transitions:** 300ms smooth slide/fade
- **Tables:** Row hover highlight, sortable columns
- **Filters:** Instant filter with count updates
- **Panel:** Slide from right with backdrop blur

---

## MOBILE RESPONSIVE

- Cards stack vertically
- Table horizontal scroll
- Collapsible sidebar
- Bottom navigation for steps
