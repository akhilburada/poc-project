# HCSC Provider Reconciliation - LOGIN PAGE

Design a futuristic enterprise login page. Dark glassmorphism theme.

## DESIGN
- **Background:** Deep gradient #0A0F1C → #1A1F3C with animated mesh/particle effect
- **Theme:** Dark glassmorphism with cyan neon accents
- **Primary:** Electric blue #3B82F6, Cyan #06B6D4
- **Font:** Inter/SF Pro, clean modern

## LAYOUT

Full-screen dark background with subtle animated grid pattern. Centered glass card.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                              (animated particles)                           │
│                                                                             │
│                    ┌─────────────────────────────────────┐                  │
│                    │                                     │                  │
│                    │         🏥 HCSC                     │                  │
│                    │   Provider Data Reconciliation      │                  │
│                    │   ─────────────────────────────     │                  │
│                    │                                     │                  │
│                    │   Welcome back                      │                  │
│                    │   Sign in to your account           │                  │
│                    │                                     │                  │
│                    │   ┌─────────────────────────────┐   │                  │
│                    │   │ 👤  Username                │   │                  │
│                    │   └─────────────────────────────┘   │                  │
│                    │                                     │                  │
│                    │   ┌─────────────────────────────┐   │                  │
│                    │   │ 🔒  Password            👁  │   │                  │
│                    │   └─────────────────────────────┘   │                  │
│                    │                                     │                  │
│                    │   ☑ Remember me    Forgot password? │                  │
│                    │                                     │                  │
│                    │   ┌─────────────────────────────┐   │                  │
│                    │   │        SIGN IN →            │   │ (cyan glow)     │
│                    │   └─────────────────────────────┘   │                  │
│                    │                                     │                  │
│                    │   ─────────────────────────────     │                  │
│                    │   🔒 Secure Enterprise Login        │                  │
│                    │                                     │                  │
│                    └─────────────────────────────────────┘                  │
│                                                                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## LOGIN CARD SPECS
- Width: 480px, centered
- Background: rgba(255,255,255,0.05) with backdrop blur
- Border: 1px rgba(255,255,255,0.1) with subtle cyan glow
- Border-radius: 24px
- Padding: 48px

## ELEMENTS

**Logo Section:**
- 🏥 icon with cyan glow effect
- "HCSC" in bold white 32px
- "Provider Data Reconciliation" in muted #94A3B8 18px
- Divider line with gradient

**Form Fields:**
- Input height: 56px
- Background: rgba(255,255,255,0.05)
- Border: 1px rgba(255,255,255,0.1)
- Border-radius: 12px
- Icon left, placeholder text muted
- Focus: cyan border glow

**Password Field:**
- Eye icon toggle (👁/👁‍🗨) for show/hide

**Sign In Button:**
- Full width, height: 56px
- Background: gradient #3B82F6 → #06B6D4
- Text: White, bold, 16px
- Border-radius: 12px
- Glow effect on hover
- Arrow icon →

**Footer:**
- Lock icon 🔒 with "Secure Enterprise Login"
- Muted text #64748B

## CREDENTIALS
- Username: `admin`
- Password: `admin123`

## STATES

**Default:** Empty fields, button enabled

**Error State:**
- Red border on invalid field
- Toast notification: "Invalid credentials" with ✕ icon
- Shake animation on card

**Loading:**
- Button shows spinner
- "Signing in..." text

**Success:**
- Brief checkmark animation
- Fade transition to main app

## INTERACTIONS
- Hover: Button glows brighter
- Focus: Cyan outline on inputs
- Click: Ripple effect
- Transition: 300ms smooth
