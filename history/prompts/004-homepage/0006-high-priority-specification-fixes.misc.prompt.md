---
id: 0006
title: High Priority Specification Fixes (H1-H3)
stage: misc
date: 2025-12-28
surface: agent
model: claude-sonnet-4-5
feature: 004-homepage
branch: 004-homepage
user: developer
command: manual fixes
labels: ["quality-assurance", "testability", "consistency", "navigation"]
links:
  spec: specs/004-homepage/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/004-homepage/spec.md (modified - fixed FR-001, FR-008, FR-031)
tests:
 - None (specification fixes phase)
---

## Prompt

Fix the 3 high priority issues identified in /sp.analyze report:
- **H1**: Pricing links contradiction (FR-001 and FR-031 reference Pricing page but Out of Scope excludes it)
- **H2**: Placeholder pages (Footer links to About, Blog, Changelog that don't exist)
- **H3**: Vague headline requirement (FR-008 "compelling headline" is subjective and not testable)

## Response snapshot

**H1 - Pricing Links Contradiction - FIXED**

**Issue**: FR-001 header nav included "Pricing, About" and FR-031 footer included "Pricing, Changelog, About, Blog" but Out of Scope section explicitly states "Pricing page implementation" and "Blog or changelog functionality" are excluded.

**Fix Applied**:
- **FR-001**: Removed "Pricing, About" from header navigation links. Now shows only: Home, Features, Developers
- **FR-031**: Removed "Pricing, Changelog, About, Blog, SDKs" from footer. Added explicit guidance: "Links to unimplemented pages (About, Blog, Changelog, Pricing) MUST be omitted or marked 'Coming Soon'"

**Rationale**: Navigation links should only include implemented pages. Referencing out-of-scope pages creates confusion during implementation and broken links in production.

---

**H2 - Placeholder Pages - FIXED**

**Issue**: Footer navigation included links to pages that don't exist and aren't planned (About, Blog, Changelog, Pricing).

**Fix Applied**: Updated FR-031 to explicitly state these pages should be omitted or marked "Coming Soon" if included. Footer now only shows links to implemented sections:
- Product: Features (scroll anchor on homepage)
- Developers: API Docs, MCP Integration (existing or planned pages)
- Company: Contact (contact form on homepage)
- Legal: Privacy Policy, Terms of Service (standard required pages)

**Rationale**: Footer should provide useful navigation, not dead links. Gives implementer clear guidance on what to include.

---

**H3 - Vague Headline Requirement - FIXED**

**Issue**: FR-008 stated "Hero section MUST display a compelling headline" - "compelling" is subjective and not testable.

**Fix Applied**: Changed FR-008 from "compelling headline describing Todo-Evolution's value proposition" to "headline describing Todo-Evolution as an AI-powered task management solution"

**Rationale**: 
- ✅ Testable: Can verify headline mentions "AI-powered task management"
- ✅ Specific: Defines what content headline must communicate
- ✅ Leaves creative freedom: Doesn't dictate exact wording
- ✅ Aligned with FR-009: Subheadline also references "AI-powered task management"

**Example headlines that satisfy FR-008**:
- "AI-Powered Task Management That Understands You"
- "Manage Your Tasks with AI Assistance"
- "The AI-Powered Solution for Task Management"

All three are testable (contain required concepts) while allowing design/copywriting flexibility.

## Outcome

- ✅ Impact: All 3 high priority issues resolved. Navigation requirements now consistent with out-of-scope section. Headline requirement is now objectively testable. No broken links will appear in footer.
- 🧪 Tests: No tests in specification phase. Requirements are now testable - can verify FR-008 headline contains "AI-powered task management" concept.
- 📁 Files: Modified specs/004-homepage/spec.md (3 edits: FR-001 simplified navigation, FR-031 clarified footer links, FR-008 made testable)
- 🔁 Next prompts: Optional: address 4 medium priority issues (M1-M4: terminology drift, parallax duplication, analytics tracking, env vars). Or proceed directly to implementation.
- 🧠 Reflection: H1 and H2 caught navigation inconsistency early - would have caused confusion during implementation ("should I build pricing page or not?"). H3 fix demonstrates importance of testable requirements - "compelling" cannot be objectively verified in automated tests or acceptance criteria.

## Evaluation notes (flywheel)

- Failure modes observed: None - all fixes applied cleanly
- Graders run and results (PASS/FAIL): PASS - Requirements now testable and internally consistent
- Prompt variant (if applicable): Standard specification refinement based on analysis findings
- Next experiment (smallest change to try): Consider adding testability check to /sp.specify workflow to catch subjective language ("compelling", "beautiful", "intuitive") before /sp.plan phase
