# HCSC Provider Reconciliation - Interactive Prototype

Dark glassmorphism UI. 4-step workflow. All buttons/tabs/rows clickable.

## THEME (toggle 🌙/☀️ in header)
**Dark:** BG #0A0F1C→#1A1F3C, glass cards, text #FFF
**Light:** BG #F8FAFC, white cards, text #1E293B
Accent: #06B6D4. Severity: 🔴#EF4444 🟠#F97316 🟡#EAB308 🟢#22C55E

## LOGIN
Glass card. Inputs: admin/admin123. "SIGN IN" → Step 1

## HEADER
[●━○━○━○] steps | [🌙/☀️] theme toggle | Avatar: Profile, Logout

---

## STEP 1: UPLOAD
Two drag-drop cards: "Simplyr Data" and "Data Lake"

After upload, [Preview] button → modal shows 5 rows × 120 columns:

**Simplyr Data Preview (horizontal scroll):**
| provider_id | npi | first_name | last_name | suffix | gender | dob | tin | specialty_primary | contract_status | ... |
|-------------|-----|------------|-----------|--------|--------|-----|-----|-------------------|-----------------|-----|
| P100000 | 1065939459 | Ana | Garcia | DO | M | 1/1/1962 | 534360412 | Family Medicine | Pending | ... |
| P100001 | 1502778451 | Priya | Smith | PA | M | 1/1/1974 | 607697301 | Pediatrics | Pending | ... |
| P100002 | 1010168041 | Luis | Johnson | DO | U | 1/1/1974 | 809296119 | Dermatology | Inactive | ... |
| P100003 | 1592491251 | Priya | Smith | DO | M | 1/1/1961 | 379378356 | Cardiology | Active | ... |
| P100004 | 1154519413 | Mike | Johnson | MD | M | 1/1/1996 | 514610493 | Family Medicine | Active | ... |

**Data Lake Preview:**
| provider_id | npi | first_name | last_name | suffix | gender | dob | tin | specialty_primary | contract_status | ... |
|-------------|-----|------------|-----------|--------|--------|-----|-----|-------------------|-----------------|-----|
| P100000 | 1014581341 | Ana | Garcia | | U | 1/1/1994 | 260622691 | Orthopedics | Inactive | ... |
| P100001 | 1600215021 | John | Johnson | PA | F | 1/1/1957 | 122193804 | Orthopedics | Active | ... |
| P100002 | 1510441276 | David | Kim | PA | U | 1/1/1988 | 569288394 | Cardiology | Active | ... |
| P100003 | 1050474560 | David | Patel | DO | U | 1/1/1993 | 150649038 | Family Medicine | Terminated | ... |
| P100004 | 1306713563 | Luis | Johnson | PA | F | 1/1/1997 | 439634360 | Orthopedics | Pending | ... |

[Remove] clears file. "Start Reconciliation →" → Step 2

---

## STEP 2: RECONCILIATION
Loading 3sec → Results.

**Summary Cards:**
🔴47 Critical | 🟠128 High | 🟡224 Medium | 🟢96 Low (495 gaps, 200 providers)

**GAPS TABLE:**
| Provider | Field | Simplyr | Lake | Type |
|----------|-------|---------|------|------|
| P100000 | npi | 1065939459 | 1014581341 | Mismatch |
| P100000 | dob | 1/1/1962 | 1/1/1994 | Mismatch |
| P100000 | specialty | Family Medicine | Orthopedics | Mismatch |
| P100001 | first_name | Priya | John | Mismatch |
| P100001 | last_name | Smith | Johnson | Mismatch |
| P100002 | first_name | Luis | David | Mismatch |
| P100003 | contract | Active | Terminated | Mismatch |

Sortable columns, row click highlights, pagination. "🧠 Run AI Analysis →" → Step 3

---

## STEP 3: AI ANALYSIS
Loading 4sec → Results. ⚠️ Alert: "Provider ID Collision - 196 gaps (39.6%)"

**SLA Timers:** 🔴47 Critical ⏱️18h left | 🟠128 High ⏱️48h left

**Bulk Actions Bar:** ☑️ Select All | [Approve Selected] [Assign To ▼] [Tag ▼]

**Domain Tabs (click to filter):**
[All 495] [Claims 178] [Cred 124] [Network 108] [Directory 85]
Each tab filters table: Claims=npi/tin, Cred=license/CAQH, Network=contract, Dir=name/address

🔍 Search: [provider, field, keyword...]

**AI DECISION TABLE (updates based on tab):**
| Gap | Domain | Severity | Action | Confidence | Status |
|-----|--------|----------|--------|------------|--------|
| P100000.npi | Claims | 🔴10 | Escalate | 🟢98% | ⏳ Pending |
| P100000.tin | Claims | 🔴10 | Hold | 🟢95% | ✅ Approved |
| P100000.cred | Cred | 🔴9 | Verify CAQH | 🟡78% | ⏳ Pending |
| P100001.npi | Claims | 🔴10 | Audit | 🟢96% | ❌ Rejected |
| P100001.name | Directory | 🔴9 | No sync | 🟢92% | 👁️ Reviewed |
| P100002.npi | Claims | 🔴10 | Escalate | 🟢97% | ⏳ Pending |
| P100003.contract | Network | 🟠8 | Verify | 🟡72% | ⏳ Pending |
| P100005.phone | Directory | 🟡5 | Sync | 🟢88% | ⏳ Pending |

Status: ✅Approved ⏳Pending ❌Rejected 👁️Reviewed

**Row click → slide panel:** Root Cause, Recommendation, [Approve][Reject][Note]

Bucketization tabs: [By Provider] [By Domain] [By Root Cause] [By Priority]

"Export →" → Step 4

---

## STEP 4: EXPORT
4 download cards: 📊Full Report(Excel) | 📄Summary(PDF) | 🔴Critical(CSV) | 📁Raw(JSON)
[New Reconciliation] [Email] [Print]
