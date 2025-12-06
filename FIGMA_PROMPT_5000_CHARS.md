# HCSC Provider Reconciliation - Interactive Prototype

Fully clickable dark glassmorphism UI. 4-step workflow. All buttons/tabs/rows interactive.

## THEME
Background: #0A0F1C→#1A1F3C gradient. Cards: glass blur. Accent: cyan #06B6D4. Critical #EF4444, High #F97316, Medium #EAB308, Low #22C55E. Glow effects, hover states on everything.

## LOGIN
Glass card center. Username/password inputs (typeable). "SIGN IN" button → navigates to Step 1. Creds: admin/admin123. Wrong login shows error toast.

## HEADER (all pages)
Step indicators clickable to jump between completed steps. Avatar dropdown: Profile, Settings, Logout.

---

## STEP 1: UPLOAD
Two drag-drop zones clickable → shows file picker. After upload:
```
✅ simplyr_sample.csv        ✅ datalake_sample.csv
Providers: 99                Providers: 99
Fields: 58                   Fields: 58
```
[Preview] button → modal with data table. [Remove] button → clears file.
"Start Reconciliation →" button → navigates to Step 2

---

## STEP 2: RECONCILIATION
Loading animation 3sec → Results view

Summary cards clickable → filter table. Priority pills clickable → filter by severity:
🔴23 Critical | 🟠64 High | 🟡112 Medium | 🟢48 Low

**GAPS TABLE:**
| Provider | Field | Simplyr | Lake | Type |
|----------|-------|---------|------|------|
| P100000 | npi | 1065939459 | 1014581341 | Mismatch |
| P100000 | tin | 534360412 | 260622691 | Mismatch |
| P100000 | dob | 1/1/1962 | 1/1/1994 | Mismatch |
| P100000 | specialty | Family Medicine | Orthopedics | Mismatch |
| P100001 | npi | 1502778451 | 1600215021 | Mismatch |
| P100001 | first_name | Priya | John | Mismatch |
| P100001 | last_name | Smith | Johnson | Mismatch |
| P100002 | npi | 1010168041 | 1510441276 | Mismatch |
| P100002 | first_name | Luis | David | Mismatch |
| P100003 | contract | Active | Terminated | Mismatch |
| P100005 | phone | 2125551212 | (empty) | Missing |

Column headers clickable → sort. Rows clickable → highlight. Provider dropdown filter. Pagination arrows work.
"🧠 Run AI Analysis →" → navigates to Step 3

---

## STEP 3: AI ANALYSIS
Loading 4sec → Results

⚠️ Alert banner clickable → expands details about Provider ID Collision (98 gaps)

Domain tabs ALL clickable: [All] [Claims 89] [Credentialing 62] [Network 54] [Directory 42]

**AI TABLE:**
| Provider | Field | Root Cause | Recommendation | Owner | Score |
|----------|-------|------------|----------------|-------|-------|
| P100000 | npi | ID collision. Different providers | DO NOT sync. Escalate | Claims | 🔴10 |
| P100000 | tin | Different entities | Hold payments | Claims | 🔴10 |
| P100001 | npi | Systemic collision | Audit ID process | Claims | 🔴10 |
| P100001 | first_name | Different individuals | Investigate | Directory | 🔴9 |
| P100002 | npi | 3rd collision detected | Escalate to IT | Claims | 🔴10 |
| P100003 | contract | Payment affected | Verify system | Network | 🟠8 |
| P100005 | phone | Contact incomplete | Sync from Simplyr | Directory | 🟡5 |

**Each row clickable → opens slide panel:**
- Value comparison section
- AI root cause text
- Recommendation text  
- Next steps with clickable checkboxes
- [Approve] [Reject] [Note] buttons all clickable
- [✕] closes panel

**Bucketization tabs clickable:**
[By Provider] [By Domain] [By Root Cause] [By Priority] - each shows different summary table

"Export Results →" → navigates to Step 4

---

## STEP 4: EXPORT
4 download cards ALL clickable:
📊 Full Report (Excel) → download
📄 Executive Summary (PDF) → download  
🔴 Critical Gaps (CSV) → download
📁 Raw Data (JSON) → download

[Start New Reconciliation] → returns to Step 1
[Email Report] → modal
[Print] → print dialog

---

## INTERACTIONS
- All buttons: hover glow + cursor pointer
- All tabs: active state highlight
- All rows: hover highlight, click selects
- All inputs: focus state, typeable
- Modals: backdrop click closes
- Tooltips on icons
