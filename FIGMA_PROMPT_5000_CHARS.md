# HCSC Provider Reconciliation - Futuristic Enterprise App

Dark glassmorphism UI. 4-step workflow. 100% frontend, all data pre-loaded.

## THEME
Background: #0A0F1C→#1A1F3C gradient with grid. Cards: glass blur rgba(255,255,255,0.05). Accent: cyan #06B6D4, blue #3B82F6. Critical #EF4444, High #F97316, Medium #EAB308, Low #22C55E. Glow effects, 300ms transitions.

## LOGIN
Dark bg with particles. Glass card center. Logo "🏥 HCSC Provider Reconciliation". Username/password inputs. Cyan "SIGN IN" button with glow. Creds: admin/admin123

## HEADER
Glass bar 70px. Logo left, step progress center (●━●━○━○), avatar right. Active=cyan pulse, done=green✓

---

## STEP 1: UPLOAD
Two glass drag-drop cards: "SIMPLYR SOURCE" + "DATA LAKE SOURCE"

After upload shows:
```
✅ simplyr_sample.csv        ✅ datalake_sample.csv
Providers: 99                Providers: 99
Fields: 58                   Fields: 58
• P100000 - Ana Garcia       • P100000 - Ana Garcia
• P100001 - Priya Smith      • P100001 - John Johnson
• P100002 - Luis Johnson     • P100002 - David Kim
```
Button: "Start Reconciliation →"

---

## STEP 2: RECONCILIATION
Loading: "🔄 Running..." progress bar, animated checklist

Summary cards: [99 Providers] [5,742 Fields] [247 Gaps] [72.7% Affected]
Priority pills: 🔴23 Critical | 🟠64 High | 🟡112 Medium | 🟢48 Low

**RAW GAPS TABLE (no AI columns):**
| Provider | Field | Simplyr | Lake | Type |
|----------|-------|---------|------|------|
| P100000 | npi | 1065939459 | 1014581341 | Mismatch |
| P100000 | tin | 534360412 | 260622691 | Mismatch |
| P100000 | dob | 1/1/1962 | 1/1/1994 | Mismatch |
| P100000 | specialty | Family Medicine | Orthopedics | Mismatch |
| P100000 | cred_status | Verified | Expired | Mismatch |
| P100001 | npi | 1502778451 | 1600215021 | Mismatch |
| P100001 | first_name | Priya | John | Mismatch |
| P100001 | last_name | Smith | Johnson | Mismatch |
| P100001 | tin | 607697301 | 122193804 | Mismatch |
| P100002 | npi | 1010168041 | 1510441276 | Mismatch |
| P100002 | first_name | Luis | David | Mismatch |
| P100002 | suffix | DO | PA | Mismatch |
| P100003 | contract | Active | Terminated | Mismatch |
| P100005 | phone | 2125551212 | (empty) | Missing |

Pagination: 1-15 of 247. Button: "🧠 Run AI Analysis →"

---

## STEP 3: AI ANALYSIS
Loading: "🧠 Analyzing..." with stages

⚠️ Alert banner: "SYSTEMIC ISSUE: Provider ID Collision affecting 6+ providers (98 gaps, 39.7%)"

Domain tabs: [Claims 89] [Credentialing 62] [Network 54] [Directory 42]

**AI-ENRICHED TABLE:**
| Provider | Field | Type | Root Cause | Recommendation | Owner | Domain | Score |
|----------|-------|------|------------|----------------|-------|--------|-------|
| P100000 | npi | Mismatch | ID collision. 27 mismatches=different providers | DO NOT sync. Validate NPPES. Escalate | Claims Ops | Claims | 🔴10 |
| P100000 | tin | Mismatch | TIN confirms different entities | Hold payments. Verify W-9 | Claims Ops | Claims | 🔴10 |
| P100000 | cred_status | Mismatch | Status conflict causes denials | Verify CAQH. Update Lake | Cred Team | Cred | 🔴9 |
| P100001 | npi | Mismatch | Systemic collision. Priya≠John | Audit ID generation process | Claims Ops | Claims | 🔴10 |
| P100001 | first_name | Mismatch | Different individuals confirmed | Do not reconcile. Investigate | Directory | Directory | 🔴9 |
| P100002 | npi | Mismatch | 3rd collision. DO vs PA credentials | Escalate to IT. Systemic issue | Claims Ops | Claims | 🔴10 |
| P100003 | contract | Mismatch | Payment eligibility affected | Verify contract system | Network | Network | 🟠8 |
| P100005 | phone | Missing | Contact incomplete | Sync from Simplyr | Directory | Directory | 🟡5 |

**Row click → slide panel:** Score, value comparison, AI root cause analysis, recommendation, next steps checkboxes, [Approve][Reject][Note] buttons

**Bucketization tabs:**
By Provider: P100000(27), P100001(24), P100002(26)...
By Domain: Claims 89(36%), Cred 62(25%), Network 54(22%), Directory 42(17%)
By Root Cause: ID Collision 98(40%), Sync Failure 67(27%), Delay 42(17%)
By Priority: Critical 23(9%), High 64(26%), Medium 112(45%), Low 48(19%)

Button: "Export Results →"

---

## STEP 4: EXPORT
Summary: ✅ 247 gaps | 247 recommendations | Dec 5, 2025

4 download cards: 📊Full Report(Excel) | 📄Executive Summary(PDF) | 🔴Critical Gaps(CSV) | 📁Raw Data(JSON)

Button: "🔄 Start New Reconciliation"
