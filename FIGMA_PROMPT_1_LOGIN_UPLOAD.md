# HCSC Reconciliation - Login & Upload

Dark glassmorphism UI. Interactive prototype. Background: #0A0F1C→#1A1F3C with particles. Cards: glass blur, cyan #06B6D4 glow.

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
- Wrong creds: red shake + "Invalid credentials" toast

## UPLOAD SCREEN (Step 1)

**Header:** Logo left, step progress [●━○━○━○], avatar dropdown right

**Title:** "📤 Upload Provider Data Files"

**Two glass drop-zone cards:**
```
┌─────────────────────────┐  ┌─────────────────────────┐
│  SIMPLYR SOURCE         │  │  DATA LAKE SOURCE       │
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
│ ✅ SIMPLYR              │  │ ✅ DATA LAKE            │
│ simplyr_sample.csv      │  │ datalake_sample.csv     │
│ Providers: 99           │  │ Providers: 99           │
│ Fields: 58              │  │ Fields: 58              │
│ Size: 127 KB            │  │ Size: 124 KB            │
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

**Preview Modal:**
| provider_id | npi | first_name | last_name | specialty |
|-------------|-----|------------|-----------|-----------|
| P100000 | 1065939459 | Ana | Garcia | Family Medicine |
| P100001 | 1502778451 | Priya | Smith | Pediatrics |
| P100002 | 1010168041 | Luis | Johnson | Dermatology |
[Close] button

**Bottom Button:**
"Start Reconciliation →" (disabled gray → enabled cyan glow when both uploaded)
Click → navigates to Step 2
