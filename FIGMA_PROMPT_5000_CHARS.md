# HCSC Provider Reconciliation - 4-Step Workflow App

Build enterprise web app. 100% frontend, hardcoded data. Professional design.

## LOGIN
Dark blue gradient bg (#0F172A→#1E3A5F), white card, logo "🏥 HCSC Provider Reconciliation"
Credentials: username="admin" password="admin123"
Blue button "Sign In →" (#2563EB)

## LAYOUT
Header: Logo left, steps center "●━●━○━○", user right
Steps: 1.Upload 2.Reconcile 3.AI Analysis 4.Export

## STEP 1: UPLOAD
Two cards: "📁 SIMPLYR" and "📁 DATA LAKE" drag-drop zones
After upload: ✅ 99 records | 58 fields
Button: "Continue →" (disabled until both uploaded)

## STEP 2: RECONCILIATION
Show processing 3sec, then results table:
Summary: 247 gaps | 72 providers affected
Priority: 🔴23 Critical | 🟠64 High | 🟡112 Medium | 🟢48 Low

**Gaps Table (Task Layer Output):**
| Provider | Field | Simplyr | Lake | Type |
|----------|-------|---------|------|------|
| P100000 | npi | 1065939459 | 1014581341 | Mismatch |
| P100000 | tin | 534360412 | 260622691 | Mismatch |
| P100000 | credentialing_status | Verified | Expired | Mismatch |
| P100000 | specialty_primary | Family Medicine | Orthopedics | Mismatch |
| P100000 | dob | 1/1/1962 | 1/1/1994 | Mismatch |
| P100001 | npi | 1502778451 | 1600215021 | Mismatch |
| P100001 | first_name | Priya | John | Mismatch |
| P100001 | tin | 607697301 | 122193804 | Mismatch |
| P100002 | npi | 1010168041 | 1510441276 | Mismatch |
| P100002 | specialty | Dermatology | Cardiology | Mismatch |

Button: "Run AI Analysis →"

## STEP 3: AI ANALYSIS
Show processing 4sec, then enriched table:

**AI-Enriched Table (Intelligence Layer):**
| Provider | Field | Simplyr | Lake | Type | Root Cause | Recommendation | Owner | Domain | Score | Priority |
|----------|-------|---------|------|------|------------|----------------|-------|--------|-------|----------|
| P100000 | npi | 1065939459 | 1014581341 | Mismatch | Provider ID collision. 27 mismatches (22.5%). Different providers mapped to same ID. | CRITICAL: Do NOT sync. Validate NPIs in NPPES. Escalate to Data Governance. | Claims Ops | Claims | 10 | 🔴Critical |
| P100000 | tin | 534360412 | 260622691 | Mismatch | TIN confirms different legal entities. Part of ID collision. | CRITICAL: Hold payments. Verify W-9. | Claims Ops | Claims | 10 | 🔴Critical |
| P100000 | credentialing_status | Verified | Expired | Mismatch | Status conflict causes claim denials. | Verify with CAQH. Update Lake if Verified. | Cred Team | Credentialing | 9 | 🔴Critical |
| P100001 | npi | 1502778451 | 1600215021 | Mismatch | Systemic issue. Names differ (Priya vs John). | CRITICAL: Pattern detected. Audit ID process. | Claims Ops | Claims | 10 | 🔴Critical |
| P100002 | npi | 1010168041 | 1510441276 | Mismatch | Third collision. Credentials differ (DO vs PA). | Systemic audit required. | Claims Ops | Claims | 10 | 🔴Critical |

Click row → Side panel with:
- Severity badge, comparison table
- "🤖 ROOT CAUSE": AI analysis text
- "💡 RECOMMENDATION": Action items
- "📋 NEXT STEPS": Checklist
- "👤 OWNER": Team name
- [Approve] [Reject] buttons

**Bucketization Summary Cards:**
By Domain: Claims 89 (36%) | Credentialing 62 (25%) | Network 54 (22%) | Directory 42 (17%)
By Root Cause: ID Collision 98 (40%) | Sync Failure 67 (27%) | Delay 42 (17%) | Entry Error 25 (10%)

## STEP 4: EXPORT
4 cards: Excel (full), PDF (summary), CSV (critical only), JSON (raw)
Button: "Start New"

## DESIGN
Colors: #2563EB primary, #DC2626 critical, #EA580C high, #CA8A04 medium, #22C55E low
Font: Inter, Cards: rounded-xl shadow
