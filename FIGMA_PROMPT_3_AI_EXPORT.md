# HCSC Reconciliation - Step 3: AI Analysis + Step 4: Export

Dark glassmorphism. AI-enriched gaps. Background: #0A0F1C→#1A1F3C.

## STEP 3 HEADER
[1 ✓]━━[2 ✓]━━[3 AI ANALYSIS]━━[4] - Step 3 cyan active

## LOADING (4 sec)
🧠 Running AI Analysis... 65%
✅ Analyzing patterns ✅ Root causes ⏳ Recommendations...

## ALERT BANNER (pulsing, clickable)
⚠️ SYSTEMIC ISSUE: Provider ID Collision - 196 gaps (39.6%) [View Details →]

## DOMAIN TABS (clickable - filters table)
[All 495] [Claims 178] [Cred 124] [Network 108] [Directory 85]

Click each tab → filters table to that domain only

## VIEW TOGGLE: [📋 Table] [📊 Buckets]

## AI-ENRICHED TABLE

| Provider | Field | Simplyr | Lake | Root Cause | Recommendation | Owner | Score |
|----------|-------|---------|------|------------|----------------|-------|-------|
| P100000 | npi | 1065939459 | 1014581341 | ID collision. Different providers | DO NOT sync. Escalate | Claims | 🔴10 |
| P100000 | tin | 534360412 | 260622691 | Different legal entities | Hold payments. Verify W-9 | Claims | 🔴10 |
| P100000 | cred_status | Verified | Expired | Status conflict | Verify CAQH. Update Lake | Cred | 🔴9 |
| P100000 | specialty | Family Med | Orthopedics | Confirms collision | Do not update | Directory | 🟠8 |
| P100000 | dob | 1/1/1962 | 1/1/1994 | 32-year diff | Document as evidence | Directory | 🟠7 |
| P100001 | npi | 1502778451 | 1600215021 | Priya≠John collision | Audit ID system | Claims | 🔴10 |
| P100001 | first_name | Priya | John | Different individuals | Investigate source | Directory | 🔴9 |
| P100001 | tin | 607697301 | 122193804 | Different entities | Hold payments | Claims | 🔴10 |
| P100002 | npi | 1010168041 | 1510441276 | 3rd collision. DO≠PA | Escalate to IT | Claims | 🔴10 |
| P100003 | contract | Active | Terminated | Payment affected | Verify contract | Network | 🟠8 |
| P100005 | phone | 2125551212 | (empty) | Contact incomplete | Sync from Simplyr | Directory | 🟡5 |

## ROW CLICK → SLIDE PANEL
```
┌────────────────────────────────────────┐
│ 🔴 CRITICAL  Score: 10  SLA: 24h  [✕] │
│ P100000 / npi  │  Claims Operations   │
├────────────────────────────────────────┤
│ SIMPLYR: 1065939459 │ LAKE: 1014581341│
├────────────────────────────────────────┤
│ 🤖 ROOT CAUSE                          │
│ Provider ID collision. 27 mismatches   │
│ Two different providers same ID.       │
├────────────────────────────────────────┤
│ 💡 RECOMMENDATION                      │
│ Do NOT sync. Validate NPPES. Escalate. │
├────────────────────────────────────────┤
│ 📋 NEXT STEPS (checkboxes)             │
│ ☐ Query NPPES ☐ Create ticket         │
├────────────────────────────────────────┤
│ [✓ Approve] [✕ Reject] [📝 Note]      │
└────────────────────────────────────────┘
```

## BUCKETS VIEW (tabs - clickable)

**By Provider:** P100000: 27 gaps | P100001: 24 | P100002: 26 | ... (200 providers)

**By Domain:** Claims 178 (36%) | Cred 124 (25%) | Network 108 (22%) | Directory 85 (17%)

**By Root Cause:** ID Collision 196 (40%) | Sync Failure 134 (27%) | Delay 84 (17%)

**By Priority:** 🔴47 (24h) | 🟠128 (72h) | 🟡224 (1wk) | 🟢96 (2wk)

[Continue to Export →]

---

## STEP 4: EXPORT

**Summary:** ✅ 495 gaps across 200 providers | Dec 5, 2025

**4 Cards (clickable downloads):**
```
┌─────────────────┐ ┌─────────────────┐
│📊 Full Report   │ │📄 Exec Summary  │
│ Excel - All 495 │ │ PDF - Metrics   │
│ [⬇ Download]    │ │ [⬇ Download]    │
└─────────────────┘ └─────────────────┘
┌─────────────────┐ ┌─────────────────┐
│🔴 Critical Only │ │📁 Raw Data      │
│ CSV - 47 items  │ │ JSON - API      │
│ [⬇ Download]    │ │ [⬇ Download]    │
└─────────────────┘ └─────────────────┘
```

[🔄 New Reconciliation] [📧 Email] [🖨 Print]
