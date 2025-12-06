# HCSC Provider Data Reconciliation - Enterprise Workflow App

Create polished 4-step workflow. 100% frontend, hardcoded data. Modern enterprise design.

## LOGIN
Dark blue gradient bg. White centered card (450px). Logo "🏥 HCSC Provider Reconciliation". Username/password inputs. Blue "Sign In" button. Creds: admin/admin123

## HEADER (all pages)
Fixed 60px bar. Logo left, step progress center (●━●━○━○), user avatar right. Steps: Upload→Reconcile→AI Analysis→Export

---

## STEP 1: DATA UPLOAD
Two side-by-side cards with drag-drop zones. "SIMPLYR" and "DATA LAKE" labels.

After upload shows: ✅ filename, 99 records, 58 fields, 127KB, Remove button.

Button: "Continue to Reconciliation →" (enabled when both uploaded)

---

## STEP 2: RECONCILIATION
Loading: Progress bar "🔄 Running Reconciliation..." 3 sec animation

Results Summary: [99 Providers] [5,742 Fields] [247 Gaps] [72% Affected]
Priority pills: 🔴23 Critical | 🟠64 High | 🟡112 Medium | 🟢48 Low

**Raw Gaps Table (NO AI columns):**
| Provider | Field | Simplyr | Lake | Type |
|----------|-------|---------|------|------|
| P100000 | npi | 1065939459 | 1014581341 | Mismatch |
| P100000 | tin | 534360412 | 260622691 | Mismatch |
| P100000 | specialty | Family Medicine | Orthopedics | Mismatch |
| P100001 | npi | 1502778451 | 1600215021 | Mismatch |
| P100001 | first_name | Priya | John | Mismatch |
| P100002 | npi | 1010168041 | 1510441276 | Mismatch |
| P100003 | contract_status | Active | Terminated | Mismatch |
| P100005 | phone | 2125551212 | (empty) | Missing |

Pagination: 1-15 of 247. Button: "Run AI Analysis →"

---

## STEP 3: AI ANALYSIS
Loading: "🧠 Analyzing..." 4 sec animation (Patterns→Root causes→Recommendations→Severity)

Domain filters: [Claims 89] [Credentialing 62] [Network 54] [Directory 42]

**Enriched Table (adds AI columns):**
| Provider | Field | Gap | Root Cause | Recommendation | Owner | Domain | Score |
|----------|-------|-----|------------|----------------|-------|--------|-------|
| P100000 | npi | Mismatch | ID collision. Different providers same ID | DO NOT sync. Validate NPPES. Escalate | Claims Ops | Claims | 🔴10 |
| P100000 | tin | Mismatch | TIN confirms different entities | Hold payments. Verify W-9 | Claims Ops | Claims | 🔴10 |
| P100001 | npi | Mismatch | Systemic collision. Names differ | Audit ID generation | Claims Ops | Claims | 🔴10 |
| P100001 | first_name | Mismatch | Different individuals | Do not reconcile | Directory | Directory | 🔴9 |
| P100003 | contract | Mismatch | Payment eligibility affected | Verify contract system | Network | Network | 🟠8 |
| P100005 | phone | Missing | Contact incomplete | Sync from Simplyr | Directory | Directory | 🟡5 |

**Row click → Right slide panel:**
- Score/Domain/Owner header
- Side-by-side value comparison
- 🤖 ROOT CAUSE: "Provider ID collision detected. 27 field mismatches..."
- 💡 RECOMMENDATION: "CRITICAL - Do NOT auto-sync. Validate NPIs..."
- 📋 NEXT STEPS: Checkboxes (Query NPPES, Create ticket, Notify Claims)
- [Approve] [Reject] [Note] buttons

Button: "Continue to Export →"

---

## STEP 4: EXPORT
Summary: ✅ 247 gaps analyzed | Dec 5, 2025

Four download cards (2x2):
📊 Full Report (Excel) | 📄 Executive Summary (PDF)
📋 Critical Gaps (CSV) | 📁 Raw Data (JSON)

Button: "🔄 Start New Reconciliation"

---

## DESIGN
Primary #2563EB, Critical #DC2626, High #EA580C, Medium #CA8A04, Low #22C55E
Background #F8FAFC, Cards white rounded-xl shadow-sm
Font: Inter, monospace for data. Smooth 200ms transitions.
