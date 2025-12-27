# Tasks: Professional Homepage & Developer Portal

**Input**: Design documents from `/specs/004-homepage/`  
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Tests**: No test tasks included (manual testing + Lighthouse audit specified in plan.md)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

---

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

**Web application** (Next.js frontend):
- Frontend: `phase-3/frontend/src/`
- Components: `phase-3/frontend/src/components/`
- App Routes: `phase-3/frontend/src/app/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Install dependencies, configure theme system, create shared types and constants

**Estimated Time**: 30 minutes

- [X] T001 Install npm packages: `next-themes`, `react-intersection-observer`, `resend`, `react-email`, `@react-email/components` in phase-3/frontend
- [X] T002 Create environment file `.env.local` with RESEND_API_KEY, CONTACT_EMAIL_TO, CONTACT_EMAIL_FROM (see quickstart.md section "Set Up Environment Variables" for details and Resend setup instructions)
- [X] T003 [P] Update `phase-3/frontend/tailwind.config.ts` to enable `darkMode: 'class'`
- [X] T004 [P] Create TypeScript types in `phase-3/frontend/src/types/homepage.ts` for ContactSubmission, ThemePreference, NavigationSection, FeatureCard, ContactEmailProps
- [X] T005 [P] Create Zod validation schema in `phase-3/frontend/src/lib/validations/contact.ts` for contact form
- [X] T006 [P] Create feature cards constants in `phase-3/frontend/src/lib/constants/features.ts` with 9 feature definitions
- [X] T007 [P] Create navigation sections constants in `phase-3/frontend/src/lib/constants/navigation.ts`
- [X] T008 Update `phase-3/frontend/src/app/layout.tsx` to wrap children with ThemeProvider from next-themes
- [X] T009 [P] Update `phase-3/frontend/src/app/globals.css` with CSS custom properties for dark mode colors

**Checkpoint**: Dependencies installed, theme infrastructure ready, types and constants defined

---

## Phase 2: Foundational (Theme System - Blocking for All User Stories)

**Purpose**: Implement dark/light theme system and apply to ALL existing pages

**⚠️ CRITICAL**: This must be complete before implementing homepage sections (US1) because theme toggle will be in navigation

**Estimated Time**: 45 minutes

- [X] T010 [P] Create ThemeToggle component in `phase-3/frontend/src/components/theme/theme-toggle.tsx` with light/dark/system options
- [X] T011 Update existing Header component in `phase-3/frontend/src/components/layout/header.tsx` to include ThemeToggle
- [X] T012 [P] Add dark mode class names to auth layout in `phase-3/frontend/src/components/auth/auth-layout.tsx`
- [X] T013 [P] Add dark mode class names to all auth pages: `phase-3/frontend/src/app/auth/signin/page.tsx` and `phase-3/frontend/src/app/auth/signup/page.tsx`
- [X] T014 [P] Add dark mode class names to dashboard components in `phase-3/frontend/src/app/dashboard/page.tsx`
- [X] T015 [P] Add dark mode class names to task components: `phase-3/frontend/src/components/tasks/task-list.tsx`, `task-item.tsx`, `task-form.tsx`
- [X] T016 [P] Add dark mode class names to chat components: `phase-3/frontend/src/components/chat/chat-interface.tsx`, `message-list.tsx`, `conversation-sidebar.tsx`
- [X] T017 Test theme toggle functionality: verify theme switches without flash, persists on reload, applies to all pages (home, auth, dashboard, chat)

**Checkpoint**: Theme system fully functional across all routes, no flash on load, localStorage persistence working

---

## Phase 3: User Story 1 - First-Time Visitor Conversion (Priority: P1) 🎯 MVP

**Goal**: New visitors land on homepage, understand value proposition, see demo video, and are motivated to sign up

**Independent Test**: Visit http://localhost:3000, verify hero section loads, navigation works, video section visible, "Sign Up" redirects to /auth/signup, "Watch Demo" scrolls to video

**Estimated Time**: 3 hours

### Implementation for User Story 1

- [X] T018 [P] [US1] Create Navigation component in `phase-3/frontend/src/components/homepage/navigation.tsx` with sticky header, logo, nav links (Home, Features, Demo, Developers, Contact), Sign In/Sign Up buttons, and ThemeToggle
- [X] T019 [P] [US1] Create HeroSection component in `phase-3/frontend/src/components/homepage/hero-section.tsx` with headline, subheadline, "Get Started Free" CTA, "Watch Demo" CTA with smooth scroll handler
- [X] T020 [P] [US1] Create VideoSection component in `phase-3/frontend/src/components/homepage/video-section.tsx` with YouTube iframe (privacy mode), lazy loading via Intersection Observer, auto-play muted when scrolled into view
- [X] T021 [US1] Add parallax CSS to hero section background in `phase-3/frontend/src/app/globals.css` using `transform: translateZ()` with `@media (prefers-reduced-motion)` fallback
- [X] T022 [US1] Implement smooth scroll behavior for "Watch Demo" button in HeroSection component (scroll to video section with `scrollIntoView`)
- [X] T023 [US1] Create custom hook `phase-3/frontend/src/hooks/use-section-observer.ts` for navigation active state detection using react-intersection-observer with 20% viewport offset
- [X] T024 [US1] Update Navigation component to highlight active section using use-section-observer hook
- [X] T025 [US1] Create HomePage composition component in `phase-3/frontend/src/components/homepage/homepage.tsx` assembling Navigation, HeroSection, VideoSection (placeholder for other sections)
- [X] T026 [US1] Replace `phase-3/frontend/src/app/page.tsx` to render HomePage component
- [X] T027 [US1] Test User Story 1: Verify homepage loads, hero section displays, navigation highlights sections, video auto-plays when scrolled to, "Watch Demo" scrolls smoothly, Sign In/Sign Up links work

**Checkpoint**: MVP homepage functional with hero, video, and navigation. Visitors can understand product and navigate to sign up.

---

## Phase 4: User Story 2 - Feature Discovery & Understanding (Priority: P2)

**Goal**: Visitors explore 9 feature cards in responsive grid and understand Todo-Evolution capabilities

**Independent Test**: Scroll to features section, verify 9 cards display in 3×3 grid (desktop), 2×4/2×5 (tablet), 1×9 (mobile), each card has icon/title/description

**Estimated Time**: 1 hour

### Implementation for User Story 2

- [X] T028 [P] [US2] Create FeaturesSection component in `phase-3/frontend/src/components/homepage/features-section.tsx` with responsive grid layout (3×3 desktop, 2 columns tablet, 1 column mobile)
- [X] T029 [US2] Map feature cards from constants/features.ts in FeaturesSection, rendering Lucide icons, title, description, optional "Learn More" link
- [X] T030 [US2] Add parallax background to features section in `phase-3/frontend/src/app/globals.css`
- [X] T031 [US2] Update HomePage composition to include FeaturesSection after VideoSection
- [X] T032 [US2] Test User Story 2: Verify 9 feature cards display correctly, responsive grid works at all breakpoints (375px, 768px, 1024px, 1920px), parallax background visible

**Checkpoint**: Feature discovery complete. Visitors can see all 9 capabilities of Todo-Evolution in organized grid.

---

## Phase 5: User Story 3 - Developer API Discovery (Priority: P3)

**Goal**: Developers find API/MCP information and navigate to documentation

**Independent Test**: Scroll to "For Developers" section, verify API overview displayed, MCP server details visible, "View Full Documentation" link present

**Estimated Time**: 45 minutes

### Implementation for User Story 3

- [X] T033 [P] [US3] Create DeveloperSection component in `phase-3/frontend/src/components/homepage/developer-section.tsx` with API overview, MCP (Model Context Protocol) explanation, JWT authentication mention, code snippet preview
- [X] T034 [US3] Add "View Full Documentation" button linking to `/developers` or `/docs/api` (placeholder page for future)
- [X] T035 [US3] Update HomePage composition to include DeveloperSection after FeaturesSection
- [X] T036 [US3] Test User Story 3: Verify developer section displays API capabilities, MCP server information visible, documentation link present

**Checkpoint**: Developer discovery complete. Developers can find API information and know how to integrate.

---

## Phase 6: User Story 4 - Mobile & Responsive Experience (Priority: P2)

**Goal**: Ensure all homepage sections work perfectly on mobile and tablet devices

**Independent Test**: Test homepage on 320px (mobile), 768px (tablet), 1024px (desktop), verify navigation hamburger menu, stacked content, readable text

**Estimated Time**: 1 hour

### Implementation for User Story 4

- [ ] T037 [US4] Add hamburger menu to Navigation component for mobile (<768px) with slide-in drawer for nav links
- [ ] T038 [US4] Update HeroSection for mobile: ensure text sizes scale appropriately (min 18px body, 32px headline), buttons stack vertically on small screens
- [ ] T039 [US4] Update VideoSection for mobile: ensure video player maintains aspect ratio, controls accessible on touch devices
- [ ] T040 [US4] Update FeaturesSection responsive classes: confirm 1-column layout on mobile, 2-column on tablet, 3-column on desktop
- [ ] T041 [US4] Test responsive breakpoints: 320px (iPhone SE), 375px (iPhone 12), 768px (iPad), 1024px (desktop), 1920px (large desktop)
- [ ] T042 [US4] Test touch interactions on mobile: verify scroll, tap targets min 44x44px, video controls accessible

**Checkpoint**: Fully responsive homepage. Mobile and tablet users have excellent experience with proper layouts and interactions.

---

## Phase 7: Contact Form & Email Integration (Cross-Cutting Feature)

**Purpose**: Add contact form at bottom of homepage with email sending via Resend API

**⚠️ Note**: This feature spans multiple user stories but is implemented as one cohesive unit

**Estimated Time**: 1.5 hours

- [ ] T043 [P] Create React Email template in `phase-3/frontend/src/components/emails/contact-email.tsx` using @react-email/components for contact notifications
- [ ] T044 [P] Create ContactSection component in `phase-3/frontend/src/components/homepage/contact-section.tsx` with form fields (name, email, message, optional subject) using React Hook Form + Zod validation
- [ ] T045 Create POST /api/contact route handler in `phase-3/frontend/src/app/api/contact/route.ts` with Resend integration, server-side validation, error handling
- [ ] T046 Add form submission logic to ContactSection: handle loading state, success message, error message, call /api/contact endpoint
- [ ] T047 Test contact form: verify validation works (name min 2 chars, email format, message min 10 chars), form submits successfully, email arrives with correct formatting, reply-to header set to user's email
- [ ] T048 Add rate limiting middleware (5 requests/hour per IP) to /api/contact route (optional enhancement)

**Checkpoint**: Contact form functional. Visitors can submit inquiries and team receives emails via Resend.

---

## Phase 8: Footer & Final Polish (Cross-Cutting)

**Purpose**: Complete homepage with footer and final accessibility/performance optimizations

**Estimated Time**: 1.5 hours

- [ ] T049 [P] Create Footer component in `phase-3/frontend/src/components/homepage/footer.tsx` with Todo-Evolution logo, navigation columns (Product, Developers, Company, Legal), social media links (GitHub, Twitter, LinkedIn), copyright notice
- [ ] T050 Update HomePage composition to include ContactSection and Footer at the end
- [ ] T051 Add meta tags for SEO in `phase-3/frontend/src/app/layout.tsx` (title, description, Open Graph tags)
- [ ] T052 Add ARIA labels to all interactive elements (buttons, links, form inputs) across all homepage components
- [ ] T053 Add alt text to all images and icons across homepage components
- [ ] T054 Add visible focus indicators to all interactive elements in `phase-3/frontend/src/app/globals.css`
- [ ] T055 Run Lighthouse accessibility audit: fix any color contrast violations (4.5:1 for normal text, 3:1 for large text)
- [ ] T056 Run Lighthouse performance audit: ensure FCP < 1.5s, LCP < 2.0s, optimize images if needed
- [ ] T057 Test keyboard navigation: verify all interactions work with Tab, Enter, Escape keys, no keyboard traps
- [ ] T058 Test with screen reader (NVDA or JAWS): verify all content announced correctly, form labels readable
- [ ] T059 Final cross-browser testing: Chrome, Firefox, Safari, Edge - verify all features work
- [ ] T060 [P] Implement analytics tracking for success criteria in `phase-3/frontend/src/lib/analytics/homepage-tracking.ts`: track CTA clicks (SC-001), video play events (SC-002), time on page (SC-003), scroll depth (SC-006), developer section engagement (SC-008). Use existing analytics solution or add event hooks for future integration.

**Checkpoint**: Homepage complete with footer, fully accessible (WCAG 2.1 Level AA), performant (Lighthouse 90+), cross-browser compatible, analytics tracking implemented.

---

## Dependencies & Completion Order

### User Story Dependencies

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational - Theme System)
    ↓
┌────────────────────────────────────────┐
│ Phase 3: US1 (P1) - MVP               │ ← Start here after foundation
│ Hero + Video + Navigation              │
└────────────────────────────────────────┘
    ↓
┌─────────────────────┬──────────────────┐
│ Phase 4: US2 (P2)   │ Phase 5: US3 (P3)│ ← Parallel implementation
│ Feature Cards       │ Developer Section│
└─────────────────────┴──────────────────┘
    ↓
Phase 6: US4 (P2) - Responsive
    ↓
Phase 7: Contact Form (Cross-cutting)
    ↓
Phase 8: Footer & Polish (Cross-cutting)
```

### Task Dependencies Within Phases

**Phase 1 (Setup)**:
- T001 → T002-T009 (all parallel after deps installed)

**Phase 2 (Foundational)**:
- T010 → T011 (theme toggle must exist before adding to header)
- T012-T016 (all parallel - different files)
- T017 (testing, depends on all above)

**Phase 3 (US1)**:
- T018-T020, T023 (parallel - independent components)
- T021 (parallel - CSS file)
- T022 (depends on T019 - HeroSection must exist)
- T024 (depends on T018, T023 - Navigation + hook)
- T025 (depends on T018-T020 - needs components)
- T026 (depends on T025 - needs HomePage)
- T027 (testing, depends on all above)

**Phase 4 (US2)**:
- T028-T030 (parallel)
- T031 (depends on T028 - needs FeaturesSection)
- T032 (testing, depends on all above)

**Phase 5 (US3)**:
- T033-T034 (parallel)
- T035 (depends on T033)
- T036 (testing, depends on all above)

**Phase 6 (US4)**:
- T037-T040 (modifications to existing components - sequential or parallel depending on familiarity)
- T041-T042 (testing, depends on all above)

**Phase 7 (Contact)**:
- T043-T044 (parallel)
- T045 (parallel with T043-T044)
- T046 (depends on T044-T045)
- T047-T048 (testing and enhancement)

**Phase 8 (Polish)**:
- T049-T050 (sequential)
- T051-T054 (parallel - different files)
- T055-T059 (sequential - testing and fixes)

---

## Parallel Execution Opportunities

### Maximum Parallelization Strategy

**After Phase 1 & 2 Complete**:

**Sprint 1 (User Story 1 - MVP)**: 1 developer, 3 hours
- Implement T018-T027 sequentially or with 2-3 developers in parallel

**Sprint 2 (User Stories 2 & 3)**: 2 developers in parallel, 1.5 hours
- Developer A: T028-T032 (US2 - Feature Cards)
- Developer B: T033-T036 (US3 - Developer Section)

**Sprint 3 (Responsive + Contact)**: 1-2 developers, 2.5 hours
- T037-T042 (US4 - Responsive)
- T043-T048 (Contact Form) - can overlap with responsive work

**Sprint 4 (Final Polish)**: 1 developer, 1.5 hours
- T049-T059 (Footer + Accessibility + Performance)

### Task Parallelization Examples

**Example 1: Independent Component Development** (Phase 3)
```
Developer A: T018 (Navigation)
Developer B: T019 (HeroSection)  
Developer C: T020 (VideoSection)
Developer D: T023 (use-section-observer hook)
Then: Merge and assemble in T025 (HomePage composition)
```

**Example 2: Theme Retrofitting** (Phase 2)
```
Developer A: T012 (auth layout) + T013 (auth pages)
Developer B: T014 (dashboard) + T015 (task components)
Developer C: T016 (chat components)
All parallel - different files, no conflicts
```

**Example 3: Cross-Functional Work** (Phase 7)
```
Frontend Dev: T044 (ContactSection UI)
Backend Dev: T045 (API route handler)
Email Dev: T043 (React Email template)
All parallel, integrate in T046
```

---

## Implementation Strategy

### MVP Delivery (Minimum Viable Product)

**Scope**: Phase 1 + Phase 2 + Phase 3 (User Story 1 only)
**Time**: 4-5 hours
**Deliverable**: Functional homepage with hero, video, navigation, and theme system

**What's included**:
- ✅ Hero section with value proposition
- ✅ Video demonstration (YouTube embed)
- ✅ Navigation with theme toggle
- ✅ Sign In / Sign Up links working
- ✅ Dark/light theme across all pages
- ✅ Smooth scrolling
- ✅ Auto-play video on scroll

**What's deferred**:
- ⏭️ Feature cards grid (US2)
- ⏭️ Developer API section (US3)
- ⏭️ Mobile responsive refinements (US4)
- ⏭️ Contact form (Phase 7)
- ⏭️ Footer (Phase 8)

### Incremental Delivery

**Iteration 1** (MVP): Phases 1-3 → Deploy basic homepage
**Iteration 2** (Feature Rich): Add Phases 4-5 → Deploy with feature cards and developer section
**Iteration 3** (Complete): Add Phases 6-7 → Deploy with mobile optimization and contact form
**Iteration 4** (Polished): Add Phase 8 → Deploy with footer and full accessibility compliance

---

## Testing Strategy

### Manual Testing Checklist

**After Phase 3 (MVP)**:
- [ ] Homepage loads without errors at http://localhost:3000
- [ ] Hero section displays headline and CTAs
- [ ] "Get Started Free" redirects to /auth/signup
- [ ] "Watch Demo" smoothly scrolls to video section
- [ ] Video auto-plays (muted) when scrolled into view
- [ ] Navigation highlights active section on scroll
- [ ] Theme toggle switches between light/dark/system
- [ ] Theme persists on page reload
- [ ] Dark mode applies to auth, dashboard, chat pages

**After Phase 4 (Feature Cards)**:
- [ ] 9 feature cards display in 3×3 grid on desktop
- [ ] Feature cards reflow to 2 columns on tablet
- [ ] Feature cards stack to 1 column on mobile
- [ ] All icons render correctly (Lucide React)
- [ ] Parallax background visible in features section

**After Phase 5 (Developer Section)**:
- [ ] Developer section displays API overview
- [ ] MCP server information visible
- [ ] JWT authentication mentioned
- [ ] "View Full Documentation" link present

**After Phase 6 (Responsive)**:
- [ ] Navigation collapses to hamburger menu < 768px
- [ ] Hero text readable on 320px width
- [ ] Video player responsive on all screen sizes
- [ ] All content accessible on mobile

**After Phase 7 (Contact Form)**:
- [ ] Contact form validates name (min 2 chars)
- [ ] Contact form validates email format
- [ ] Contact form validates message (min 10 chars)
- [ ] Form shows loading state during submission
- [ ] Success message appears after submission
- [ ] Email arrives in inbox with correct formatting
- [ ] Reply-to header set to user's email

**After Phase 8 (Final)**:
- [ ] Footer displays all links correctly
- [ ] Social media links open in new tab
- [ ] Copyright year is current
- [ ] Lighthouse Performance score 90+
- [ ] Lighthouse Accessibility score 90+
- [ ] Lighthouse SEO score 90+
- [ ] Color contrast meets WCAG 2.1 AA (4.5:1 normal, 3:1 large)
- [ ] All interactive elements keyboard accessible
- [ ] Screen reader announces content correctly
- [ ] No keyboard traps
- [ ] Focus indicators visible on all elements

### Automated Testing (Lighthouse)

```bash
# After Phase 8 complete
npm run build
npm run start

# Open Chrome DevTools
# Navigate to http://localhost:3000
# Run Lighthouse audit
# Target: Performance 90+, Accessibility 90+, SEO 90+
```

---

## Success Metrics (from spec.md)

After full implementation, track:

- [ ] SC-001: 60%+ homepage visitors click "Sign Up" or "Get Started"
- [ ] SC-002: 40%+ visitors play demonstration video
- [ ] SC-003: Average time on homepage ≥ 2 minutes
- [ ] SC-004: Homepage hero loads in < 2s on 3G network
- [ ] SC-005: Bounce rate < 40%
- [ ] SC-006: 80%+ visitors scroll past fold
- [ ] SC-007: Mobile visitors ≥ 45% with similar engagement
- [ ] SC-008: 15%+ developer section visitors click API docs
- [ ] SC-009: Lighthouse 90+ (Performance/Accessibility/SEO)
- [ ] SC-010: Zero critical accessibility violations

---

## File Paths Quick Reference

### New Files Created

**Types & Validation**:
- `phase-3/frontend/src/types/homepage.ts`
- `phase-3/frontend/src/lib/validations/contact.ts`
- `phase-3/frontend/src/lib/constants/features.ts`
- `phase-3/frontend/src/lib/constants/navigation.ts`

**Components - Theme**:
- `phase-3/frontend/src/components/theme/theme-toggle.tsx`

**Components - Homepage**:
- `phase-3/frontend/src/components/homepage/navigation.tsx`
- `phase-3/frontend/src/components/homepage/hero-section.tsx`
- `phase-3/frontend/src/components/homepage/video-section.tsx`
- `phase-3/frontend/src/components/homepage/features-section.tsx`
- `phase-3/frontend/src/components/homepage/developer-section.tsx`
- `phase-3/frontend/src/components/homepage/contact-section.tsx`
- `phase-3/frontend/src/components/homepage/footer.tsx`
- `phase-3/frontend/src/components/homepage/homepage.tsx`

**Components - Email**:
- `phase-3/frontend/src/components/emails/contact-email.tsx`

**Hooks**:
- `phase-3/frontend/src/hooks/use-section-observer.ts`

**API Routes**:
- `phase-3/frontend/src/app/api/contact/route.ts`

### Modified Files

**Configuration**:
- `phase-3/frontend/.env.local` (new)
- `phase-3/frontend/tailwind.config.ts`
- `phase-3/frontend/package.json`

**Layout & Styling**:
- `phase-3/frontend/src/app/layout.tsx`
- `phase-3/frontend/src/app/page.tsx`
- `phase-3/frontend/src/app/globals.css`

**Existing Components (Theme Updates)**:
- `phase-3/frontend/src/components/layout/header.tsx`
- `phase-3/frontend/src/components/auth/auth-layout.tsx`
- `phase-3/frontend/src/app/auth/signin/page.tsx`
- `phase-3/frontend/src/app/auth/signup/page.tsx`
- `phase-3/frontend/src/app/dashboard/page.tsx`
- `phase-3/frontend/src/components/tasks/task-list.tsx`
- `phase-3/frontend/src/components/tasks/task-item.tsx`
- `phase-3/frontend/src/components/tasks/task-form.tsx`
- `phase-3/frontend/src/components/chat/chat-interface.tsx`
- `phase-3/frontend/src/components/chat/message-list.tsx`
- `phase-3/frontend/src/components/chat/conversation-sidebar.tsx`

---

## Total Task Count: 59 tasks

**Breakdown by Phase**:
- Phase 1 (Setup): 9 tasks
- Phase 2 (Foundational): 8 tasks
- Phase 3 (US1 - MVP): 10 tasks
- Phase 4 (US2): 5 tasks
- Phase 5 (US3): 4 tasks
- Phase 6 (US4): 6 tasks
- Phase 7 (Contact): 6 tasks
- Phase 8 (Polish): 11 tasks

**Breakdown by User Story**:
- User Story 1 (P1): 10 tasks
- User Story 2 (P2): 5 tasks
- User Story 3 (P3): 4 tasks
- User Story 4 (P2): 6 tasks
- Cross-cutting: 34 tasks (Setup, Foundational, Contact, Polish)

**Parallelization**:
- 23 tasks marked [P] (can run in parallel)
- 36 tasks sequential (dependencies or testing)

**Estimated Total Time**: 10-12 hours for complete implementation (6-8 hours for MVP)

---

## Next Steps

1. ✅ Review this task breakdown with team
2. ⏭️ Assign developers to user stories or phases
3. ⏭️ Start with Phase 1 (Setup) - all developers
4. ⏭️ Complete Phase 2 (Theme System) - foundational requirement
5. ⏭️ Implement Phase 3 (US1 - MVP) for first deployment
6. ⏭️ Iterate with Phases 4-8 for full feature set
7. ⏭️ Run final Lighthouse audit and accessibility testing
8. ⏭️ Deploy to production

**MVP-First Strategy**: Focus on Phases 1-3 first (4-5 hours) to deliver working homepage quickly, then iterate with additional features.
