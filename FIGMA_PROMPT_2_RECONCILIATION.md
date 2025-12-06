# HCSC Reconciliation - Step 2: Gaps Table

Dark glassmorphism. Raw gaps comparison (NO AI columns). Background: #0A0F1C→#1A1F3C. Cyan accents.

## HEADER
[1 ✓]━━[2 RECONCILE]━━[3]━━[4] - Step 2 active cyan, Step 1 green check

## LOADING (3 sec animation)
```
🔄 Running Reconciliation...
████████████████░░░░░░░░  72%
✅ Loading Simplyr (99 records)
✅ Loading Data Lake (99 records)
⏳ Comparing 5,742 field pairs...
```

## RESULTS

**Summary Cards (glass, clickable):**
[99 Providers] [5,742 Fields] [247 Gaps] [72.7% Affected]

**Priority Pills (clickable filters):**
[🔴 23 Critical] [🟠 64 High] [🟡 112 Medium] [🟢 48 Low]

**Filters:** Provider dropdown, Field dropdown, Search box

## RAW GAPS TABLE

| Provider | Field | Simplyr Value | Lake Value | Type |
|----------|-------|---------------|------------|------|
| P100000 | npi | 1065939459 | 1014581341 | 🔴 Mismatch |
| P100000 | tin | 534360412 | 260622691 | 🔴 Mismatch |
| P100000 | suffix | DO | (empty) | 🟡 Missing |
| P100000 | gender | M | U | 🟡 Mismatch |
| P100000 | dob | 1/1/1962 | 1/1/1994 | 🔴 Mismatch |
| P100000 | contract_status | Pending | Inactive | 🟠 Mismatch |
| P100000 | credentialing_status | Verified | Expired | 🔴 Mismatch |
| P100000 | specialty_primary | Family Medicine | Orthopedics | 🟠 Mismatch |
| P100000 | practice_state | IL | NY | 🟠 Mismatch |
| P100000 | license_state | IL | TX | 🟠 Mismatch |
| P100001 | npi | 1502778451 | 1600215021 | 🔴 Mismatch |
| P100001 | first_name | Priya | John | 🔴 Mismatch |
| P100001 | last_name | Smith | Johnson | 🔴 Mismatch |
| P100001 | gender | M | F | 🟠 Mismatch |
| P100001 | dob | 1/1/1974 | 1/1/1957 | 🟠 Mismatch |
| P100001 | tin | 607697301 | 122193804 | 🔴 Mismatch |
| P100001 | specialty_primary | Pediatrics | Orthopedics | 🟠 Mismatch |
| P100002 | npi | 1010168041 | 1510441276 | 🔴 Mismatch |
| P100002 | first_name | Luis | David | 🔴 Mismatch |
| P100002 | last_name | Johnson | Kim | 🔴 Mismatch |
| P100002 | suffix | DO | PA | 🟠 Mismatch |
| P100003 | npi | 1592491251 | 1050474560 | 🔴 Mismatch |
| P100003 | contract_status | Active | Terminated | 🔴 Mismatch |
| P100005 | phone | 2125551212 | (empty) | 🟡 Missing |

**Interactions:**
- Column headers: click to sort
- Rows: hover highlight, click opens detail popup
- Pagination: "1-25 of 247" with arrows

**Row Click Popup:**
```
┌─────────────────────────────────────┐
│ Gap: P100000 / npi         [✕]     │
├─────────────────────────────────────┤
│ SIMPLYR      │  DATA LAKE          │
│ 1065939459   │  1014581341         │
├─────────────────────────────────────┤
│ Run AI Analysis for recommendations │
│         [Close] [🧠 Analyze]        │
└─────────────────────────────────────┘
```

**Bottom Actions:**
[📥 Export Raw CSV] [🧠 Run AI Analysis →]

AI Analysis button → navigates to Step 3
