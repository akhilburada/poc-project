# HCSC Reconciliation - Login & Upload

Dark glassmorphism UI. Background: #0A0F1C→#1A1F3C. Cards: glass blur, cyan #06B6D4.

## LOGIN SCREEN
Centered glass card (480px) on dark particle background:
```
┌───────────────────────────────────────┐
│           🏥 HCSC                     │
│   Provider Data Reconciliation        │
│   ─────────────────────────           │
│   ┌─────────────────────────────┐     │
│   │ 👤  admin                   │     │
│   └─────────────────────────────┘     │
│   ┌─────────────────────────────┐     │
│   │ 🔒  ••••••••            👁  │     │
│   └─────────────────────────────┘     │
│   ☑ Remember me    Forgot password?  │
│   ┌─────────────────────────────┐     │
│   │      SIGN IN →              │glow │
│   └─────────────────────────────┘     │
└───────────────────────────────────────┘
```
- Inputs typeable, eye toggles password
- SIGN IN → navigates to Upload
- Creds: admin / admin123
- Wrong creds: red shake + error toast

## UPLOAD SCREEN (Step 1)

**Header:** Logo left, step progress [●━○━○━○], avatar dropdown right

**Title:** "📤 Upload Provider Data Files"

**Two glass drop-zone cards:**
```
┌─────────────────────────┐  ┌─────────────────────────┐
│  SIMPLYR DATA           │  │  DATA LAKE              │
│  ┌───────────────────┐  │  │  ┌───────────────────┐  │
│  │   ☁️ DROP FILE    │  │  │  │   ☁️ DROP FILE    │  │
│  │  or click browse  │  │  │  │  or click browse  │  │
│  │  CSV, XLSX, 50MB  │  │  │  │  CSV, XLSX, 50MB  │  │
│  └───────────────────┘  │  │  └───────────────────┘  │
│  [Browse Files]         │  │  [Browse Files]         │
└─────────────────────────┘  └─────────────────────────┘
```

**After upload - cards show real data:**
```
┌─────────────────────────┐  ┌─────────────────────────┐
│ ✅ SIMPLYR DATA         │  │ ✅ DATA LAKE            │
│ simplyr_200.csv         │  │ datalake_200.csv        │
│ Providers: 200          │  │ Providers: 200          │
│ Fields: 120             │  │ Fields: 120             │
│ Size: 312 KB            │  │ Size: 308 KB            │
│                         │  │                         │
│ • P100000 Ana Garcia    │  │ • P100000 Ana Garcia    │
│ • P100001 Priya Smith   │  │ • P100001 John Johnson  │
│ • P100002 Luis Johnson  │  │ • P100002 David Kim     │
│                         │  │                         │
│ [Preview] [✕ Remove]    │  │ [Preview] [✕ Remove]    │
└─────────────────────────┘  └─────────────────────────┘
```

**Interactions:**
- Drop zones clickable → file picker
- Preview → modal with data table (provider_id, npi, first_name, last_name, specialty)
- Remove → clears file
- Note different names: Simplyr has Priya Smith, Lake has John Johnson (collision!)

**Preview Modal (5 rows × 120 cols, horizontal scroll):**
| provider_id | npi | first_name | last_name | dob | specialty | contract | ... |
|-------------|-----|------------|-----------|-----|-----------|----------|-----|
| P100000 | 1065939459 | Ana | Garcia | 1/1/1962 | Family Med | Pending | ... |
| P100001 | 1502778451 | Priya | Smith | 1/1/1974 | Pediatrics | Pending | ... |
| P100002 | 1010168041 | Luis | Johnson | 1/1/1974 | Dermatology | Inactive | ... |
| P100003 | 1592491251 | Priya | Smith | 1/1/1961 | Cardiology | Active | ... |
| P100004 | 1154519413 | Mike | Johnson | 1/1/1996 | Family Med | Active | ... |
[Close]

**Bottom Button:**
"Start Reconciliation →" (disabled gray → enabled cyan glow when both uploaded)
Click → navigates to Step 2
