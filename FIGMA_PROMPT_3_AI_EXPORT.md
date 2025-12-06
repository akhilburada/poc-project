# HCSC Reconciliation - Step 3: AI Analysis + Step 4: Export

Dark glassmorphism. AI-enriched gaps. Background: #0A0F1C→#1A1F3C.

## STEP 3 HEADER
[1 ✓]━━[2 ✓]━━[3 AI ANALYSIS]━━[4] - Step 3 cyan active

## LOADING (4 sec)
🧠 Running AI Analysis... 65%
✅ Analyzing patterns ✅ Root causes ⏳ Recommendations...

## ALERT BANNER (pulsing, clickable)
⚠️ SYSTEMIC ISSUE: Provider ID Collision - 98 gaps (39.7%) [View Details →]

## DOMAIN TABS (clickable)
[All 247] [Claims 89] [Credentialing 62] [Network 54] [Directory 42]

## VIEW TOGGLE: [📋 Table] [📊 Buckets]

## AI-ENRICHED TABLE

| Provider | Field | Simplyr | Lake | Root Cause | Recommendation | Owner | Score |
|----------|-------|---------|------|------------|----------------|-------|-------|
| P100000 | npi | 1065939459 | 1014581341 | ID collision. 27 mismatches=different providers | DO NOT sync. Validate NPPES. Escalate | Claims | 🔴10 |
| P100000 | tin | 534360412 | 260622691 | Different legal entities | Hold payments. Verify W-9 | Claims | 🔴10 |
| P100000 | cred_status | Verified | Expired | Status conflict | Verify CAQH. Update Lake | Cred | 🔴9 |
| P100000 | specialty | Family Med | Orthopedics | Confirms collision | Do not update | Directory | 🟠8 |
| P100000 | dob | 1/1/1962 | 1/1/1994 | 32-year diff | Document as evidence | Directory | 🟠7 |
| P100001 | npi | 1502778451 | 1600215021 | Systemic collision. Priya≠John | Audit ID generation | Claims | 🔴10 |
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

## BUCKETS VIEW (tabs)

**By Provider:** P100000: 27 gaps | P100001: 24 | P100002: 26

**By Domain:** Claims 89 (36%) | Cred 62 (25%) | Network 54 (22%) | Directory 42 (17%)

**By Root Cause:** ID Collision 98 (40%) | Sync Failure 67 (27%) | Delay 42 (17%)

**By Priority:** 🔴23 (24h) | 🟠64 (72h) | 🟡112 (1wk) | 🟢48 (2wk)

[Continue to Export →]

---

## STEP 4: EXPORT

**Summary:** ✅ 247 gaps | Dec 5, 2025

**4 Cards (clickable downloads):**
```
┌─────────────────┐ ┌─────────────────┐
│📊 Full Report   │ │📄 Exec Summary  │
│ Excel - All 247 │ │ PDF - Metrics   │
│ [⬇ Download]    │ │ [⬇ Download]    │
└─────────────────┘ └─────────────────┘
┌─────────────────┐ ┌─────────────────┐
│🔴 Critical Only │ │📁 Raw Data      │
│ CSV - 23 items  │ │ JSON - API      │
│ [⬇ Download]    │ │ [⬇ Download]    │
└─────────────────┘ └─────────────────┘
```

[🔄 New Reconciliation] [📧 Email] [🖨 Print]
