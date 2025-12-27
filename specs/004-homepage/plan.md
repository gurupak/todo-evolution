# Implementation Plan: Professional Homepage & Developer Portal

**Branch**: `004-homepage` | **Date**: 2025-12-27 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `/specs/004-homepage/spec.md` + User requirements for professional homepage with parallax, dark/light theme, contact form, and comprehensive theme application

---

## Summary

Implement a professional marketing homepage for Todo-Evolution featuring parallax scrolling effects, YouTube video demonstration, 9 feature cards in responsive grid, developer API section, contact form with email integration, and comprehensive dark/light theme system applied across all existing pages (homepage, auth, dashboard, chat).

**Primary Requirements**:
- Hero section with parallax background and dual CTAs
- Auto-scroll + auto-play video demo (YouTube privacy mode)
- 9 feature cards in 3×3/4×2 responsive grid
- Developer section with API/MCP documentation links
- Contact form sending via Resend email API
- Dark/light/system theme toggle with persistence
- Theme application to all routes (auth, dashboard, chat)
- WCAG 2.1 Level AA accessibility compliance
- Navigation active state on scroll (20% viewport offset)

---

## Technical Context

**Language/Version**: TypeScript 5.x with Next.js 15.1.0 (App Router)  
**Primary Dependencies**: 
- **Existing**: React 19, Tailwind CSS 3.4, shadcn/ui (Radix), React Hook Form 7.54, Zod 3.24
- **New**: next-themes (v0.4+), react-intersection-observer, resend, react-email

**Storage**: 
- Theme preference: Client-side localStorage (managed by next-themes)
- Contact submissions: No persistence (email-only for MVP)
- Optional future: PostgreSQL (Neon) for contact form history

**Testing**: Manual testing + Lighthouse accessibility audit  
**Target Platform**: Web (Desktop + Mobile, responsive 320px-1920px)  
**Project Type**: Web application (Next.js frontend)  
**Performance Goals**: 
- First Contentful Paint < 1.5s
- Largest Contentful Paint < 2.0s  
- Lighthouse Performance/Accessibility/SEO 90+

**Constraints**: 
- Parallax must respect `prefers-reduced-motion`
- Email sending must not block UI (async)
- Theme must apply without flash (SSR-compatible)
- Video must lazy load (not above fold)

**Scale/Scope**: 
- Single homepage route
- 1 API endpoint (/api/contact)
- 8-10 new React components
- Theme retrofitting across 4 existing routes

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**GATE 1: Simplicity - Avoid Over-Engineering**
✅ **PASS**: Using native browser APIs (Intersection Observer, scroll-behavior) instead of heavy animation libraries. Chose lightweight next-themes (2-line setup) over custom theme implementation. Email via Resend API instead of SMTP configuration.

**GATE 2: Existing Patterns - Reuse Before Create**
✅ **PASS**: Reusing existing shadcn/ui components, React Hook Form + Zod validation, Tailwind CSS setup. Extending current architecture rather than introducing new patterns.

**GATE 3: Accessibility - Non-Negotiable**
✅ **PASS**: Targeting WCAG 2.1 Level AA (CL-003). Parallax respects `prefers-reduced-motion`. Keyboard navigation for all interactions. Semantic HTML + ARIA labels. Color contrast requirements defined (4.5:1 normal, 3:1 large text).

**GATE 4: Performance - Budget Defined**
✅ **PASS**: Clear performance targets set. Lazy loading for video, parallax limited to CSS transforms, code splitting via Next.js App Router automatic chunking. Bundle size monitored (<300KB target).

**GATE 5: Testing - Verify Before Deploy**
✅ **PASS**: Manual testing checklist defined, Lighthouse audit required, accessibility tools specified (axe DevTools, NVDA/JAWS). Integration tests for contact form email delivery.

---

## Project Structure

### Documentation (this feature)

```text
specs/004-homepage/
├── plan.md                 # This file (/sp.plan command output)
├── research.md             # Phase 0 output (/sp.plan command) ✅
├── data-model.md           # Phase 1 output (/sp.plan command) ✅
├── quickstart.md           # Phase 1 output (/sp.plan command) ✅
├── contracts/              # Phase 1 output (/sp.plan command) ✅
│   └── contact-api.yaml    # OpenAPI spec for contact endpoint
├── spec.md                 # Feature specification (from /sp.specify)
└── checklists/             # Quality validation checklists
    └── requirements.md
```

### Source Code (repository root)

```text
phase-3/frontend/
├── src/
│   ├── app/
│   │   ├── api/
│   │   │   └── contact/
│   │   │       └── route.ts               # NEW: Contact form API handler
│   │   │
│   │   ├── (routes)/                      # Existing authenticated routes
│   │   │   ├── dashboard/                 # MODIFY: Add dark mode styles
│   │   │   └── chat/                      # MODIFY: Add dark mode styles
│   │   │
│   │   ├── auth/                          # Existing auth routes
│   │   │   ├── signin/                    # MODIFY: Add dark mode styles
│   │   │   └── signup/                    # MODIFY: Add dark mode styles
│   │   │
│   │   ├── layout.tsx                     # MODIFY: Wrap with ThemeProvider
│   │   ├── page.tsx                       # MODIFY: Replace with HomePage
│   │   ├── globals.css                    # MODIFY: Add dark mode CSS variables
│   │   └── providers.tsx                  # MODIFY: Include theme provider
│   │
│   ├── components/
│   │   ├── homepage/                      # NEW: Homepage-specific components
│   │   │   ├── homepage.tsx               # Main composition component
│   │   │   ├── hero-section.tsx           # Hero with parallax + CTAs
│   │   │   ├── features-section.tsx       # 9 feature cards (3×3 grid)
│   │   │   ├── video-section.tsx          # YouTube embed with lazy load
│   │   │   ├── developer-section.tsx      # API/MCP documentation links
│   │   │   ├── contact-section.tsx        # Contact form with validation
│   │   │   ├── footer.tsx                 # Footer with links + social
│   │   │   └── navigation.tsx             # Sticky header with active state
│   │   │
│   │   ├── emails/                        # NEW: React Email templates
│   │   │   └── contact-email.tsx          # Email template for contact form
│   │   │
│   │   ├── theme/                         # NEW: Theme management
│   │   │   ├── theme-toggle.tsx           # Light/dark/system toggle
│   │   │   └── theme-script.tsx           # No-flash script (if needed)
│   │   │
│   │   ├── auth/
│   │   │   └── auth-layout.tsx            # MODIFY: Dark mode class names
│   │   │
│   │   ├── layout/
│   │   │   └── header.tsx                 # MODIFY: Add theme toggle button
│   │   │
│   │   ├── tasks/                         # MODIFY: Add dark mode variants
│   │   │   ├── task-list.tsx
│   │   │   └── task-item.tsx
│   │   │
│   │   ├── chat/                          # MODIFY: Add dark mode variants
│   │   │   ├── chat-interface.tsx
│   │   │   └── message-list.tsx
│   │   │
│   │   └── ui/                            # EXISTING: shadcn components (already dark-mode ready)
│   │       ├── button.tsx
│   │       ├── input.tsx
│   │       ├── card.tsx
│   │       └── ...
│   │
│   ├── lib/
│   │   ├── constants/
│   │   │   ├── features.ts                # NEW: Feature cards static data
│   │   │   └── navigation.ts              # NEW: Nav sections config
│   │   │
│   │   ├── validations/
│   │   │   └── contact.ts                 # NEW: Zod contact form schema
│   │   │
│   │   └── utils.ts                       # EXISTING: Utility functions
│   │
│   ├── types/
│   │   └── homepage.ts                    # NEW: Homepage TypeScript types
│   │
│   └── hooks/
│       └── use-section-observer.ts        # NEW: Scroll position hook
│
├── public/
│   └── videos/
│       └── demo-thumbnail.jpg             # NEW: Video fallback image
│
├── .env.local                             # NEW: Environment variables
├── tailwind.config.ts                     # MODIFY: Enable darkMode: 'class'
├── package.json                           # MODIFY: Add new dependencies
└── tsconfig.json                          # EXISTING: No changes needed
```

**Structure Decision**: Web application structure (Option 2) with clear separation:
- `/app` - Next.js App Router pages and API routes
- `/components/homepage` - Homepage-specific UI components
- `/components/theme` - Theme management components
- `/components/ui` - Shared shadcn/ui components
- Existing Phase III components modified to support dark mode via className updates

---

## Complexity Tracking

> **No Constitution violations detected. No justification needed.**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |

---

## Phase 0: Research & Technology Selection

**Status**: ✅ COMPLETE (see `research.md`)

### Key Decisions Made

1. **Dark/Light Theme**: `next-themes` v0.4+ 
   - Zero-flash, SSR-safe, 2-line setup
   - Auto system preference detection
2. **Parallax Scrolling**: CSS `transform: translateZ()` + Intersection Observer
   - Native performance, WCAG compliant
   - No external library needed
3. **Navigation Active State**: `react-intersection-observer`
   - 20% viewport offset (CL-005)
   - High reputation (89.9 score)
4. **Email Sending**: Resend + React Email
   - Official Next.js email API
   - Free tier: 3,000 emails/month
5. **Video Hosting**: YouTube privacy-enhanced mode (CL-002)
   - Free CDN, lazy loading
   - Auto-play muted (CL-001)
6. **Smooth Scrolling**: Native CSS `scroll-behavior: smooth`
   - Zero dependencies
   - Respects prefers-reduced-motion
7. **Form Validation**: React Hook Form + Zod (already installed)
   - Reuse existing dependencies
8. **Component Library**: shadcn/ui (already installed)
   - Accessible by default

### Dependencies to Install

```bash
npm install next-themes react-intersection-observer resend react-email @react-email/components
```

### Environment Variables

```env
RESEND_API_KEY=re_xxxxxxxxxxxx
CONTACT_EMAIL_TO=team@todo-evolution.com
CONTACT_EMAIL_FROM=contact@todo-evolution.com
```

**Full research details**: See [`research.md`](./research.md)

---

## Phase 1: Design & Contracts

**Status**: ✅ COMPLETE (see `data-model.md` and `contracts/`)

### Data Model Overview

**Entities Defined**:
1. `ContactSubmission` - Contact form data structure
2. `ThemePreference` - Theme state (managed by next-themes)
3. `NavigationSection` - Homepage section config
4. `FeatureCard` - Feature highlights data
5. `ContactEmailProps` - Email template props

**Storage Strategy**:
- Contact submissions: Email-only (no DB persistence for MVP)
- Theme preference: Client localStorage (automatic via next-themes)
- Feature cards & navigation: Static TypeScript constants

**API Endpoint**: 
- `POST /api/contact` - Submit contact form, send email via Resend

**Full data model**: See [`data-model.md`](./data-model.md)  
**API contract**: See [`contracts/contact-api.yaml`](./contracts/contact-api.yaml)

### Type Definitions

```typescript
// types/homepage.ts

export interface ContactSubmission {
  id: string;
  submittedAt: Date;
  name: string;
  email: string;
  message: string;
  subject?: string;
  status: 'pending' | 'sent' | 'failed' | 'spam';
  emailId?: string;
}

export interface FeatureCard {
  id: string;
  icon: string;                  // Lucide icon name
  title: string;
  description: string;
  learnMoreUrl?: string;
  order: number;
}

export interface NavigationSection {
  id: string;                    // HTML element ID
  label: string;                 // Display name
  href: string;                  // Scroll anchor
  order: number;
  isActive: boolean;
}
```

### Validation Schemas

```typescript
// lib/validations/contact.ts
import { z } from 'zod';

export const contactSchema = z.object({
  name: z.string()
    .min(2, 'Name must be at least 2 characters')
    .max(100, 'Name too long')
    .regex(/^[a-zA-Z\s'-]+$/, 'Invalid characters'),
  email: z.string()
    .email('Invalid email')
    .max(255, 'Email too long'),
  message: z.string()
    .min(10, 'Message too short')
    .max(1000, 'Message too long'),
  subject: z.string()
    .max(200, 'Subject too long')
    .optional(),
});

export type ContactFormData = z.infer<typeof contactSchema>;
```

---

## Phase 2: Implementation Plan

### Implementation Sequence

#### Step 1: Core Infrastructure (30 minutes)

**Goal**: Set up theme system and install dependencies

**Tasks**:
1. Install npm packages: `next-themes`, `react-intersection-observer`, `resend`, `react-email`
2. Update `.env.local` or `.env` with Resend API key
3. Update `tailwind.config.ts` to enable `darkMode: 'class'`
4. Wrap app with `ThemeProvider` in `app/layout.tsx`
5. Create type definitions in `types/homepage.ts`
6. Create validation schemas in `lib/validations/contact.ts`
7. Create static data constants in `lib/constants/`

**Files to Create**:
- `types/homepage.ts`
- `lib/validations/contact.ts`
- `lib/constants/features.ts`
- `lib/constants/navigation.ts`

**Files to Modify**:
- `.env.local` (new)
- `tailwind.config.ts`
- `app/layout.tsx`
- `package.json` (via npm install)

**Acceptance Criteria**:
- [ ] All dependencies installed without errors
- [ ] `darkMode: 'class'` in Tailwind config
- [ ] ThemeProvider wraps app in layout
- [ ] Types compile without errors

---

#### Step 2: Theme System (45 minutes)

**Goal**: Implement dark/light theme toggle and apply to existing pages

**Tasks**:
1. Create `ThemeToggle` component with light/dark/system options
2. Add theme toggle to existing `Header` component
3. Update `globals.css` with CSS custom properties for dark mode
4. Add dark mode class names to auth pages (signin, signup)
5. Add dark mode class names to dashboard components
6. Add dark mode class names to chat components
7. Test theme persistence on page reload

**Files to Create**:
- `components/theme/theme-toggle.tsx`

**Files to Modify**:
- `components/layout/header.tsx` (add theme toggle)
- `app/globals.css` (dark mode CSS variables)
- `components/auth/auth-layout.tsx` (dark: classes)
- `components/tasks/*.tsx` (dark: classes)
- `components/chat/*.tsx` (dark: classes)

**Acceptance Criteria**:
- [ ] Theme toggle visible in header
- [ ] Theme switches without page flash
- [ ] Theme persists on reload
- [ ] All pages (home, auth, dashboard, chat) respect theme
- [ ] Color contrast meets WCAG 2.1 AA (4.5:1 normal, 3:1 large)

---

#### Step 3: Homepage Structure (2 hours)

**Goal**: Build all homepage sections with responsive layouts

**Tasks**:
1. Create `Navigation` component (sticky header, logo, nav links, theme toggle)
2. Create `HeroSection` component (headline, subheadline, dual CTAs, parallax bg)
3. Create `FeaturesSection` component (9 feature cards, 3×3 grid, responsive)
4. Create `VideoSection` component (YouTube embed, lazy load, auto-play muted)
5. Create `DeveloperSection` component (API overview, MCP info, docs link)
6. Create `ContactSection` component (form with validation, loading state)
7. Create `Footer` component (logo, nav columns, social links, copyright)
8. Create `HomePage` composition component (assemble all sections)
9. Replace `app/page.tsx` with homepage route

**Files to Create**:
- `components/homepage/navigation.tsx`
- `components/homepage/hero-section.tsx`
- `components/homepage/features-section.tsx`
- `components/homepage/video-section.tsx`
- `components/homepage/developer-section.tsx`
- `components/homepage/contact-section.tsx`
- `components/homepage/footer.tsx`
- `components/homepage/homepage.tsx`

**Files to Modify**:
- `app/page.tsx` (replace with HomePage)

**Acceptance Criteria**:
- [ ] All sections render without errors
- [ ] Responsive layout works (320px-1920px)
- [ ] Feature cards display in 3×3 grid (desktop), 2×4 (tablet), 1×9 (mobile)
- [ ] All content from spec.md is present
- [ ] Navigation scrolls to sections smoothly
- [ ] Parallax background visible in hero

---

#### Step 4: Interactive Features (1.5 hours)

**Goal**: Implement scroll effects, video behavior, and navigation highlighting

**Tasks**:
1. Implement smooth scroll for "Watch Demo" button (CL-001)
2. Add Intersection Observer for auto-play video on scroll
3. Add parallax CSS transforms to hero and section backgrounds
4. Implement navigation active state with `react-intersection-observer` (20% offset)
5. Add `prefers-reduced-motion` media query to disable parallax
6. Test keyboard navigation (Tab, Enter, Escape)

**Files to Create**:
- `hooks/use-section-observer.ts` (custom hook for scroll detection)

**Files to Modify**:
- `components/homepage/hero-section.tsx` (add scroll handler)
- `components/homepage/video-section.tsx` (add Intersection Observer)
- `components/homepage/navigation.tsx` (add active state logic)
- `app/globals.css` (parallax CSS, prefers-reduced-motion)

**Acceptance Criteria**:
- [ ] "Watch Demo" button scrolls to video section smoothly
- [ ] Video auto-plays (muted) when scrolled into view
- [ ] Navigation highlights active section at 20% viewport offset
- [ ] Parallax effects work on desktop
- [ ] Parallax disabled on mobile and with prefers-reduced-motion
- [ ] All interactions work via keyboard

---

#### Step 5: Email Integration (1 hour)

**Goal**: Implement contact form submission and email delivery

**Tasks**:
1. Create React Email template for contact notifications
2. Implement `/api/contact` route handler
3. Integrate Resend API with error handling
4. Add form submission logic to `ContactSection`
5. Add loading state and success/error messages
6. Test email delivery with test data
7. Add rate limiting middleware (5 requests/hour per IP)

**Files to Create**:
- `components/emails/contact-email.tsx`
- `app/api/contact/route.ts`

**Files to Modify**:
- `components/homepage/contact-section.tsx` (add submission logic)

**Acceptance Criteria**:
- [ ] Contact form validates inputs correctly
- [ ] Form shows loading state during submission
- [ ] Success message appears after successful submission
- [ ] Error message appears if submission fails
- [ ] Email arrives with correct formatting
- [ ] Reply-to header set to user's email
- [ ] Rate limiting prevents spam

---

#### Step 6: Polish & Accessibility (1 hour)

**Goal**: Ensure WCAG 2.1 Level AA compliance and optimize performance

**Tasks**:
1. Run Lighthouse accessibility audit
2. Fix any color contrast violations
3. Add ARIA labels where needed
4. Ensure all images have alt text
5. Test with screen reader (NVDA or JAWS)
6. Add focus indicators to all interactive elements
7. Test keyboard-only navigation
8. Optimize images (lazy load, proper sizing)
9. Run Lighthouse performance audit
10. Add meta tags for SEO

**Files to Modify**:
- All homepage components (add ARIA labels, alt text)
- `app/layout.tsx` (add meta tags)
- `app/globals.css` (focus indicators)

**Acceptance Criteria**:
- [ ] Lighthouse Accessibility score 90+
- [ ] Lighthouse Performance score 90+
- [ ] Lighthouse SEO score 90+
- [ ] Zero critical accessibility violations (axe DevTools)
- [ ] Color contrast 4.5:1 for normal text, 3:1 for large
- [ ] All interactive elements keyboard accessible
- [ ] Screen reader announces all content correctly
- [ ] Focus indicators visible on all interactive elements

---

### Component Dependency Graph

```
HomePage (composition)
├── Navigation
│   └── ThemeToggle
├── HeroSection
├── FeaturesSection
│   └── FeatureCard (9×)
├── VideoSection
├── DeveloperSection
├── ContactSection
│   ├── Input (ui)
│   ├── Button (ui)
│   └── Label (ui)
└── Footer
```

---

### Risk Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Resend API key invalid | High | Low | Test email sending early, use test domain |
| Parallax causes motion sickness | Medium | Low | Respect prefers-reduced-motion, disable on mobile |
| Dark mode flash on load | Medium | Medium | Use suppressHydrationWarning, test SSR |
| Video auto-play blocked | Low | Medium | Mute video, show play button if auto-play fails |
| Email delivery fails | High | Low | Add retry logic, show user helpful error message |
| Theme doesn't apply to old pages | Medium | Medium | Test all routes, add dark: classes systematically |

---

## Testing Strategy

### Manual Testing Checklist

**Theme System**:
- [ ] Theme toggle switches between light/dark/system
- [ ] Theme persists on page reload
- [ ] System theme detection works
- [ ] No flash of unstyled content
- [ ] All pages respect theme (home, auth, dashboard, chat)

**Homepage Sections**:
- [ ] Hero section displays correctly
- [ ] Feature cards display in correct grid (3×3, 2×4, 1×9)
- [ ] Video section loads YouTube embed
- [ ] Developer section shows API info
- [ ] Contact form renders correctly
- [ ] Footer displays all links

**Interactive Features**:
- [ ] "Watch Demo" button scrolls to video
- [ ] Video auto-plays when scrolled to
- [ ] Navigation highlights active section
- [ ] Parallax works on desktop
- [ ] Parallax disabled on mobile
- [ ] Smooth scrolling works
- [ ] Keyboard navigation works

**Contact Form**:
- [ ] Form validation works (name, email, message)
- [ ] Form shows error messages for invalid inputs
- [ ] Form submits successfully
- [ ] Loading state shows during submission
- [ ] Success message appears after submission
- [ ] Email arrives with correct content
- [ ] Reply-to header set correctly

**Responsive Design**:
- [ ] Mobile (375px) layout correct
- [ ] Tablet (768px) layout correct
- [ ] Desktop (1024px) layout correct
- [ ] Large desktop (1920px) layout correct
- [ ] All text readable at all sizes
- [ ] All buttons accessible at all sizes

**Accessibility**:
- [ ] Keyboard navigation works for all interactions
- [ ] Focus indicators visible
- [ ] Screen reader announces content correctly
- [ ] Color contrast meets WCAG 2.1 AA
- [ ] ARIA labels present where needed
- [ ] All images have alt text

### Automated Testing

```bash
# Build and start production server
npm run build
npm run start

# Open Lighthouse in Chrome DevTools
# Navigate to http://localhost:3000
# Run Lighthouse audit (Performance, Accessibility, SEO)
# Target: All scores 90+

# Install axe DevTools Chrome extension
# Run accessibility scan
# Fix all critical and serious issues
```

---

## Deployment Checklist

- [ ] All environment variables set in production
- [ ] Resend API key valid and verified
- [ ] Email domain verified in Resend dashboard
- [ ] YouTube video uploaded and embed enabled
- [ ] Meta tags and OG images configured
- [ ] Lighthouse scores 90+ for all categories
- [ ] Dark mode tested in production
- [ ] All links functional
- [ ] Contact form tested end-to-end
- [ ] Mobile responsive verified

---

## Success Criteria (from spec.md)

- [ ] SC-001: 60%+ homepage visitors click "Sign Up"
- [ ] SC-002: 40%+ visitors play demo video
- [ ] SC-003: Average time on homepage 2+ minutes
- [ ] SC-004: Homepage loads hero in < 2s on 3G
- [ ] SC-005: Bounce rate < 40%
- [ ] SC-006: 80%+ visitors scroll past fold
- [ ] SC-007: Mobile visitors 45%+ with similar engagement
- [ ] SC-008: 15%+ developer section visitors click API docs
- [ ] SC-009: Lighthouse 90+ for Performance/Accessibility/SEO
- [ ] SC-010: Zero critical accessibility violations

---

## References

- **Feature Specification**: [`spec.md`](./spec.md)
- **Research Document**: [`research.md`](./research.md)
- **Data Model**: [`data-model.md`](./data-model.md)
- **API Contract**: [`contracts/contact-api.yaml`](./contracts/contact-api.yaml)
- **Quick start Guide**: [`quickstart.md`](./quickstart.md)

---

## Next Steps

1. ✅ Planning complete - All artifacts generated
2. ⏭️ Run `/sp.tasks` to generate detailed task breakdown
3. ⏭️ Begin implementation following Step 1 (Core Infrastructure)
4. ⏭️ Test each phase before proceeding to next
5. ⏭️ Run final accessibility audit before deployment

**Implementation Time Estimate**: 6-8 hours for complete MVP including testing
