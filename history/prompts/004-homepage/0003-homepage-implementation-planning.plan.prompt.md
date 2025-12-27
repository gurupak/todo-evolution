---
id: 0003
title: Homepage Implementation Planning
stage: plan
date: 2025-12-27
surface: agent
model: claude-sonnet-4-5
feature: 004-homepage
branch: 004-homepage
user: developer
command: /sp.plan
labels: ["planning", "homepage", "dark-mode", "theme", "parallax", "contact-form", "email", "resend", "next-themes"]
links:
  spec: specs/004-homepage/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/004-homepage/plan.md
 - specs/004-homepage/research.md
 - specs/004-homepage/data-model.md
 - specs/004-homepage/quickstart.md
 - specs/004-homepage/contracts/contact-api.yaml
 - CLAUDE.md
tests:
 - None (planning phase)
---

## Prompt

User requested implementation planning for professional homepage with additional requirements:

**Original Spec Requirements** (from /sp.specify):
- Professional and elegant homepage with parallax design
- Hero banner, video player, feature cards, developer API section, footer
- Sign in/sign up links in header
- YouTube video demonstrating task importance

**Additional Planning Requirements** (from /sp.plan):
- Make changes in phase-3/frontend folder (Next.js project)
- Use shadcn components (already installed)
- Use Context7 MCP to get library documentation
- Add contact form at bottom that emails user details
- Implement dark/light theme toggle
- Apply theme to ALL pages: homepage, signin, signup, dashboard, chat

**Clarifications from /sp.clarify**:
- CL-001: Auto-scroll to video section + auto-play (muted)
- CL-002: YouTube with privacy-enhanced mode (youtube-nocookie.com)
- CL-003: WCAG 2.1 Level AA accessibility compliance
- CL-004: 8-9 feature cards in 3×3 or 4×2 grid
- CL-005: Navigation active state at 20% viewport offset

## Response snapshot

**Phase 0: Research & Technology Selection**
- Researched 8 key technology decisions using Context7 MCP
- Selected next-themes for dark/light mode (86.2 benchmark score, 78 snippets)
- Selected react-intersection-observer for scroll detection (89.9 score, 58 snippets)
- Selected Resend + React Email for contact form (82.8 score, 98 snippets)
- Chose CSS-based parallax over libraries for performance + accessibility
- YouTube privacy mode for video hosting (free, GDPR-friendly)
- Documented all decisions with rationale in research.md

**Phase 1: Design & Data Model**
- Defined 5 core entities: ContactSubmission, ThemePreference, NavigationSection, FeatureCard, ContactEmailProps
- Created Zod validation schemas for contact form
- Designed email-only contact strategy (no DB persistence for MVP)
- Documented theme storage strategy (localStorage via next-themes)
- Created OpenAPI 3.1 contract for POST /api/contact endpoint
- Defined complete TypeScript type system

**Implementation Plan Structure**:
- 6-step implementation sequence (6-8 hours estimated)
- Step 1: Core Infrastructure (30 min) - Install deps, ThemeProvider setup
- Step 2: Theme System (45 min) - Toggle component, apply to all pages
- Step 3: Homepage Structure (2 hrs) - 7 section components + composition
- Step 4: Interactive Features (1.5 hrs) - Parallax, scroll, navigation
- Step 5: Email Integration (1 hr) - React Email template + API route
- Step 6: Polish & Accessibility (1 hr) - WCAG audit, Lighthouse optimization

**Key Architecture Decisions**:
- Reuse existing shadcn/ui components (no new component library)
- Extend existing React Hook Form + Zod for validation (already installed)
- Client-side theme with SSR-safe next-themes (no flash)
- Static feature cards (TypeScript constants, not CMS)
- Email-only contact form (no database for MVP)

**Accessibility Strategy**:
- WCAG 2.1 Level AA compliance required
- Color contrast: 4.5:1 normal text, 3:1 large text
- Parallax respects prefers-reduced-motion
- Keyboard navigation for all interactions
- Screen reader testing with NVDA/JAWS

**Performance Targets**:
- FCP < 1.5s, LCP < 2.0s
- Lighthouse scores 90+ (Performance, Accessibility, SEO)
- Lazy load video, code splitting via Next.js App Router

## Outcome

- ✅ Impact: Complete implementation plan with research, data model, API contracts, and quickstart guide generated. All clarification decisions integrated. Ready for /sp.tasks command.
- 🧪 Tests: No tests in planning phase (manual testing checklist and Lighthouse audit strategy defined)
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, contracts/contact-api.yaml. Updated CLAUDE.md with new technologies.
- 🔁 Next prompts: /sp.tasks to generate task breakdown, then begin Step 1 implementation (Core Infrastructure)
- 🧠 Reflection: Context7 MCP integration provided high-quality library documentation (next-themes, Resend, react-intersection-observer), enabling confident technology decisions. Comprehensive planning reduces implementation risk. Dark mode retrofitting across 4 existing routes adds complexity but ensures consistent UX.

## Evaluation notes (flywheel)

- Failure modes observed: None - all research successful, all decisions documented with rationale
- Graders run and results (PASS/FAIL): PASS - All Constitution gates passed (simplicity, reuse, accessibility, performance, testing)
- Prompt variant (if applicable): Standard /sp.plan workflow with Context7 MCP integration for library research
- Next experiment (smallest change to try): Validate email sending works with Resend test domain before implementing full contact form
