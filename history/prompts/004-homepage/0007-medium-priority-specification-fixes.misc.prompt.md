---
id: 0007
title: Medium Priority Specification Fixes (M1-M4)
stage: misc
date: 2025-12-28
surface: agent
model: claude-sonnet-4-5
feature: 004-homepage
branch: 004-homepage
user: developer
command: manual fixes
labels: ["quality-assurance", "consistency", "analytics", "documentation"]
links:
  spec: specs/004-homepage/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/004-homepage/spec.md (modified - removed FR-012, FR-018, FR-023, updated FR-036, fixed title)
 - specs/004-homepage/tasks.md (modified - added T060 analytics task, updated T002 with quickstart reference)
tests:
 - None (specification fixes phase)
---

## Prompt

Fix the 4 medium priority issues identified in /sp.analyze report:
- **M1**: Terminology drift ("Developer Portal" in title vs "Developer section" in requirements)
- **M2**: Parallax duplication (FR-012, FR-018, FR-023 duplicate FR-036-039)
- **M3**: Analytics tracking missing (success criteria define metrics but no implementation tasks)
- **M4**: Env var setup details (T002 mentions env vars but no reference to setup documentation)

## Response snapshot

**M1 - Terminology Drift - FIXED**

**Issue**: Specification title was "Professional Homepage & Developer Portal" but all requirements and user stories referred to "Developer section" or "For Developers" section.

**Fix Applied**: Changed title from "Professional Homepage & Developer Portal" to "Professional Homepage"

**Rationale**: 
- "Developer Portal" implies a separate dedicated page/application
- Actual implementation is a single section on the homepage
- "Developer section" is more accurate and used consistently throughout requirements (FR-024 to FR-029)
- Removes confusion about scope

---

**M2 - Parallax Duplication - FIXED**

**Issue**: Three requirements duplicated parallax specifications:
- FR-012: "Hero section MUST use parallax effect with background moving at 50% scroll speed"
- FR-018: "Video section MUST use parallax effect for background elements"
- FR-023: "Features section MUST use parallax effect with layered background elements"

These were redundant with the dedicated Parallax Design section (FR-036 to FR-039) that already defined global parallax behavior.

**Fix Applied**:
1. **Removed** FR-012, FR-018, FR-023 (section-specific parallax requirements)
2. **Updated** FR-036 to explicitly list which sections get parallax: "Parallax effects MUST be applied to hero, video, and features sections with background elements moving at 30-50% of foreground scroll speed"
3. Kept FR-037 (prefers-reduced-motion), FR-038 (no layout shift), FR-039 (readability/contrast) unchanged

**Rationale**:
- ✅ DRY principle: Define parallax rules once in dedicated section
- ✅ Easier maintenance: Changes to parallax behavior only need one update
- ✅ Clearer requirements: Parallax Design section now owns all parallax specifications
- ✅ Preserved intent: FR-036 explicitly lists hero, video, features sections

**Before**: 7 parallax-related requirements (FR-012, FR-018, FR-023, FR-036, FR-037, FR-038, FR-039)  
**After**: 4 requirements (FR-036, FR-037, FR-038, FR-039) with no loss of information

---

**M3 - Analytics Tracking Missing - FIXED**

**Issue**: Success criteria (SC-001 to SC-010) define 10 measurable outcomes but no tasks existed for implementing analytics tracking to measure them:
- SC-001: 60%+ click "Sign Up" or "Get Started"
- SC-002: 40%+ play demo video
- SC-003: Average time ≥ 2 minutes
- SC-004: Hero loads < 2s on 3G
- SC-005: Bounce rate < 40%
- SC-006: 80%+ scroll past fold
- SC-007: Mobile ≥ 45% traffic
- SC-008: 15%+ developer section visitors click API docs
- SC-009: Lighthouse 90+
- SC-010: Zero critical a11y violations

**Fix Applied**: Added new task **T060** to tasks.md after T059:

```markdown
- [ ] T060 [P] Implement analytics tracking for success criteria in `phase-3/frontend/src/lib/analytics/homepage-tracking.ts`: track CTA clicks (SC-001), video play events (SC-002), time on page (SC-003), scroll depth (SC-006), developer section engagement (SC-008). Use existing analytics solution or add event hooks for future integration.
```

**Rationale**:
- ✅ Makes success criteria measurable (can't track what you don't instrument)
- ✅ Flexible implementation: Allows using existing analytics or adding hooks
- ✅ Covers key user behavior metrics: CTAs, video engagement, scroll depth, time on page
- ✅ Marked [P] for parallel execution: Can implement alongside other polish tasks
- ✅ Specific file path: `phase-3/frontend/src/lib/analytics/homepage-tracking.ts`

**Note**: SC-004 (load time), SC-009 (Lighthouse), SC-010 (a11y) are measured via existing tools (Lighthouse audit, T056-T058), not custom tracking.

---

**M4 - Env Var Setup Details - FIXED**

**Issue**: Task T002 stated "Create environment file `.env.local` with RESEND_API_KEY, CONTACT_EMAIL_TO, CONTACT_EMAIL_FROM" but provided no guidance on:
- Where to get RESEND_API_KEY
- How to set up Resend account
- What values to use for testing vs production

**Fix Applied**: Updated T002 with reference to existing documentation:

```markdown
- [ ] T002 Create environment file `.env.local` with RESEND_API_KEY, CONTACT_EMAIL_TO, CONTACT_EMAIL_FROM (see quickstart.md section "Set Up Environment Variables" for details and Resend setup instructions)
```

**Rationale**:
- ✅ Points to authoritative source: quickstart.md already has comprehensive env var setup
- ✅ Includes Resend setup instructions: API key creation, domain verification, testing email
- ✅ Avoids duplication: Don't repeat setup steps in tasks.md
- ✅ Implementer-friendly: Clear path to get unblocked on env var configuration

**quickstart.md already contains**:
- Step-by-step Resend account setup
- Example `.env.local` format
- Testing email (`onboarding@resend.dev`)
- Production configuration guidance
- Troubleshooting common issues

## Outcome

- ✅ Impact: All 4 medium priority issues resolved. Terminology consistent ("Developer section" not "Portal"). Parallax requirements consolidated (7→4 requirements, no duplication). Analytics tracking task added for success criteria measurement. Env var setup guidance linked from T002.
- 🧪 Tests: No tests in specification phase. T060 adds analytics tracking implementation for measuring SC-001 to SC-010 outcomes.
- 📁 Files: Modified specs/004-homepage/spec.md (4 edits: title fixed, FR-012/FR-018/FR-023 removed, FR-036 clarified) and specs/004-homepage/tasks.md (2 edits: T060 added, T002 updated with quickstart reference)
- 🔁 Next prompts: Optional: address 2 low priority issues (L1: emoji removal, L2: nav link type clarity). Spec is now ready for implementation - all critical and high/medium issues resolved.
- 🧠 Reflection: M2 (parallax duplication) shows importance of DRY principle in requirements - having parallax defined in 7 places made it hard to maintain. Consolidating to 4 requirements in dedicated section improves clarity. M3 caught analytics gap - defining success criteria without implementation tasks leaves metrics unmeasurable.

## Evaluation notes (flywheel)

- Failure modes observed: None - all fixes applied cleanly
- Graders run and results (PASS/FAIL): PASS - Requirements now consistent, no duplication, analytics coverage added
- Prompt variant (if applicable): Standard specification refinement based on analysis findings
- Next experiment (smallest change to try): Consider adding DRY check to /sp.analyze to detect requirement duplication automatically (e.g., same concept defined in multiple places)
