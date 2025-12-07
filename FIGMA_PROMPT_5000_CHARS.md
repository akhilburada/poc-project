# HCSC Provider Reconciliation - Interactive Prototype

Dark glassmorphism UI. 4-step workflow. All buttons/tabs/rows clickable.

## THEME
Background: #0A0F1C→#1A1F3C. Cards: glass blur. Accent: cyan #06B6D4. Critical #EF4444, High #F97316, Medium #EAB308, Low #22C55E.

## LOGIN
Glass card. Username/password inputs. "SIGN IN" → Step 1. Creds: admin/admin123

## HEADER
Step progress [●━○━○━○] clickable. Avatar dropdown: Profile, Settings, Logout.

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
Loading 3sec → Results. Summary: 🔴47 Critical | 🟠128 High | 🟡224 Medium | 🟢96 Low (495 total gaps across 200 providers)

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

Domain tabs: [All] [Claims 178] [Credentialing 124] [Network 108] [Directory 85]

**AI DECISION TABLE (Agent analyzes each gap):**
| Gap | Domain | Owner Group | Severity | Recommendation | Why |
|-----|--------|-------------|----------|----------------|-----|
| P100000.npi | Claims | Claims Operations | 🔴10 Critical | DO NOT sync. Validate NPPES. Escalate | 27 mismatches=different providers mapped to same ID |
| P100000.tin | Claims | Claims Operations | 🔴10 Critical | Hold payments. Verify W-9 | TIN confirms different legal entities |
| P100000.cred_status | Credentialing | Cred Team | 🔴9 Critical | Verify CAQH. Update Lake | Verified vs Expired causes claim denials |
| P100001.npi | Claims | Claims Operations | 🔴10 Critical | Audit ID generation | Systemic collision: Priya Smith ≠ John Johnson |
| P100001.first_name | Provider Directory | Directory Team | 🔴9 Critical | Do not reconcile | Different individuals confirmed by name mismatch |
| P100002.npi | Claims | Claims Operations | 🔴10 Critical | Escalate to IT | 3rd collision: Luis DO ≠ David PA |
| P100003.contract | Network Ops | Network Team | 🟠8 High | Verify contract system | Active vs Terminated affects payment eligibility |
| P100005.phone | Provider Directory | Directory Team | 🟡5 Medium | Sync from Simplyr | Contact info incomplete in Lake |

**Row click → slide panel:** Values, Root Cause, Recommendation, Next Steps checkboxes, [Approve][Reject][Note]

Bucketization tabs: [By Provider] [By Domain] [By Root Cause] [By Priority]

"Export →" → Step 4

---

## STEP 4: EXPORT
4 download cards: 📊Full Report(Excel) | 📄Summary(PDF) | 🔴Critical(CSV) | 📁Raw(JSON)
[New Reconciliation] [Email] [Print]
