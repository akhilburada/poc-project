# HCSC Provider Data Reconciliation - Enterprise Web App

Build a polished 4-step workflow app for healthcare data reconciliation. 100% frontend with hardcoded data. Professional enterprise design.

## LOGIN PAGE
- Full-screen dark blue gradient (#0F172A → #1E3A5F)
- Centered white card (480px), rounded-xl, large shadow
- Logo: "🏥 HCSC Provider Reconciliation"
- Username input (user icon), Password input (lock icon, show/hide toggle)
- Remember me checkbox
- Blue "Sign In →" button (#2563EB)
- Credentials: username="admin", password="admin123"
- Show error toast for wrong credentials

## MAIN LAYOUT (after login)
- Fixed header (64px): "HCSC Reconciliation" left, step indicator center, "👤 Admin" right
- Step progress: ●━━●━━○━━○ (4 steps)
- States: Completed=green✓, Current=blue pulse, Pending=gray

## STEP 1: DATA UPLOAD
Title: "Upload Provider Data Files"
Subtitle: "Upload Simplyr and Data Lake CSV files"

Two cards side-by-side:
- Left: "📁 SIMPLYR SOURCE" - dashed border drop zone, "Drag & drop or browse"
- Right: "📁 DATA LAKE" - same layout
After upload show: ✅ filename.csv | 99 records | 58 fields | 127KB
Button: "Continue to Step 2 →" (disabled until both uploaded, then blue)

## STEP 2: RECONCILIATION
**Processing (3 seconds):**
"🔄 Running Reconciliation..." with progress bar 0→100%
Checklist: ✅Loading Simplyr ✅Loading Lake ✅Matching records ⏳Comparing fields...

**Results:**
Summary box: Providers: 99 | Fields Compared: 5,742 | Total Gaps: 247 | Providers with Gaps: 72 (72.7%)
Priority row: [🔴 CRITICAL 23] [🟠 HIGH 64] [🟡 MEDIUM 112] [🟢 LOW 48]
Domain bar chart: Claims 89 (36%), Credentialing 62 (25%), Network 54 (22%), Directory 42 (17%)
Button: "Continue to AI Analysis →"

## STEP 3: AI ANALYSIS
**Processing (4 sec):** "🧠 AI Analysis..." with progress bar

**Results - Data Table:**
Filter pills: [🔴23] [🟠64] [🟡112] [🟢48] [All: 247]
Search box, sortable columns

| Provider | Field | Simplyr Value | Lake Value | Type | Severity | Domain |
|----------|-------|---------------|------------|------|----------|--------|
| P100000 | npi | 1065939459 | 1014581341 | Mismatch | 🔴 10 | Claims |
| P100000 | tin | 534360412 | 260622691 | Mismatch | 🔴 10 | Claims |
| P100000 | credentialing_status | Verified | Expired | Mismatch | 🔴 9 | Credentialing |
| P100001 | npi | 1502778451 | 1600215021 | Mismatch | 🔴 10 | Claims |
| P100001 | first_name | Priya | John | Mismatch | 🔴 9 | Directory |
| P100002 | npi | 1010168041 | 1510441276 | Mismatch | 🔴 10 | Claims |
| P100002 | specialty | Dermatology | Cardiology | Mismatch | 🟠 8 | Directory |
| P100003 | contract_status | Active | Terminated | Mismatch | 🟠 8 | Network |
| P100004 | license_state | NY | CA | Mismatch | 🟠 7 | Credentialing |
| P100005 | phone | 2125551212 | (empty) | Missing | 🟡 5 | Directory |

Pagination: "Showing 1-10 of 247"

**Side Panel (slides from right on row click):**
Header: "🔴 CRITICAL • Severity 10/10" with X close
Content:
- Provider: P100000 | Field: npi | Domain: Claims
- Comparison box: SIMPLYR: 1065939459 | LAKE: 1014581341
- "🤖 AI ROOT CAUSE": "Provider ID collision detected. 27 field mismatches (22.5%) including NPI, TIN, DOB, specialty. Two different providers mapped to same Provider ID."
- "💡 RECOMMENDATION": "CRITICAL - DO NOT AUTO-SYNC. 1) Validate both NPIs against NPPES registry 2) If different providers, correct mapping in Lake 3) Escalate to Data Governance team"
- "📋 NEXT STEPS": □ Query NPPES for validation □ Create ServiceNow ticket □ Notify Claims Operations
- "👤 OWNER": Claims Operations Team
- Buttons: [✓ Approve] [✗ Reject] [📝 Add Note]

## STEP 4: EXPORT
Title: "📥 Export Results"
Summary: ✅ Reconciliation Complete | 247 gaps | 247 recommendations | Dec 5, 2025

Four export cards (2x2):
1. "📊 Full Report (Excel)" - All gaps with AI analysis → [Download]
2. "📄 Executive Summary (PDF)" - Key metrics for leadership → [Download]
3. "📋 Critical Gaps (CSV)" - 23 critical items only → [Download]
4. "📁 Raw Data (JSON)" - For system integration → [Download]
Button: "🔄 Start New Reconciliation"

## DESIGN SPECS
Colors: Primary #2563EB, Critical #DC2626, High #EA580C, Medium #CA8A04, Low #22C55E
Background: #F8FAFC, Cards: white, Border: #E2E8F0, Text: #0F172A / #64748B
Font: Inter (400/600 weights)
Cards: rounded-xl, shadow-sm, 24px padding
Animations: 200ms step transitions, 300ms side panel slide, progress bar fills smoothly
Table: hover rows #F1F5F9, clickable for detail panel
