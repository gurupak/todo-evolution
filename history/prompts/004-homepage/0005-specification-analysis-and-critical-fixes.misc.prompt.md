---
id: 0005
title: Specification Analysis and Critical Fixes
stage: misc
date: 2025-12-27
surface: agent
model: claude-sonnet-4-5
feature: 004-homepage
branch: 004-homepage
user: developer
command: /sp.analyze
labels: ["analysis", "quality-assurance", "coverage", "consistency", "critical-fixes"]
links:
  spec: specs/004-homepage/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/004-homepage/spec.md (modified - added FR-051 to FR-055, updated FR-015, added Contact Submission entity)
tests:
 - None (analysis and fixes phase)
---

## Prompt

Run cross-artifact consistency analysis on spec.md, plan.md, and tasks.md for the 004-homepage feature. Identify duplications, ambiguities, coverage gaps, and constitution violations. User requested to "fix C1 and C2 first" after receiving the analysis report.

**Analysis Scope**:
- 50 functional requirements (FR-001 to FR-050)
- 10 success criteria (SC-001 to SC-010)
- 59 tasks (T001 to T059)
- Constitution alignment check

**Critical Issues Identified**:
- **C1**: Video autoplay contradiction between FR-015 and CL-001/T020
- **C2**: Contact form missing from spec requirements despite 6 tasks (T043-T048)

## Response snapshot

**Analysis Results**:
- Total Requirements: 60 (50 FR + 10 SC)
- Total Tasks: 59
- Coverage Rate: 96.7% (58/60 requirements covered)
- Critical Issues: 2
- High Priority Issues: 3
- Medium Priority Issues: 4
- Low Priority Issues: 2
- Constitution Violations: 0

**Key Findings**:
1. **C1 - Video Autoplay Contradiction**: FR-015 stated "Video MUST start paused (not autoplay)" but CL-001 clarification and T020 specified "auto-play muted when scrolled into view" - direct contradiction
2. **C2 - Contact Form Missing**: Tasks T043-T048 implement contact form with Resend email integration, but no corresponding functional requirements in spec.md
3. **H1 - Pricing Links Undefined**: FR-001 and FR-031 reference "Pricing" navigation link but Out of Scope section excludes pricing page
4. **H2 - Placeholder Pages**: Footer links to About, Blog, Changelog pages that don't exist
5. **M2 - Parallax Duplication**: FR-012, FR-018, FR-023 duplicate FR-036 to FR-039

**Critical Fixes Applied**:

**C1 Fix**: Updated FR-015 from "Video MUST start paused (not autoplay) for accessibility" to "Video MUST auto-play muted when scrolled into view (per CL-001), respecting `prefers-reduced-motion` for accessibility"

**C2 Fix**: Added 5 new functional requirements:
- FR-051: Contact section MUST be displayed at bottom of homepage before footer
- FR-052: Contact form MUST include fields (name 2-100 chars, email, message 10-1000 chars, optional subject max 200 chars)
- FR-053: Contact form MUST validate inputs client-side using Zod schema
- FR-054: Contact form MUST send email via Resend API with reply-to header
- FR-055: Contact form MUST show loading/success/error states

Also added **Contact Submission** entity to Key Entities section.

**Remaining Issues**: 3 high priority (pricing links, placeholder pages, vague headline), 4 medium priority (terminology, duplication, analytics, env vars), 2 low priority (emoji, nav link types)

## Outcome

- ✅ Impact: 2 critical contradictions resolved. Spec.md now has complete coverage for all 59 tasks. Video autoplay behavior aligned across spec, clarifications, and tasks. Contact form properly documented as FR-051 to FR-055.
- 🧪 Tests: No tests in analysis phase. Analysis identified that success criteria (SC-001 to SC-010) have no corresponding analytics tracking tasks - noted as M3 medium priority issue.
- 📁 Files: Modified specs/004-homepage/spec.md (3 edits: FR-015 updated, FR-051 to FR-055 added, Contact Submission entity added)
- 🔁 Next prompts: Ready for implementation. Optionally fix H1-H2 (pricing/placeholder pages) and M2 (parallax duplication), or proceed with implementation and address during/after MVP.
- 🧠 Reflection: Cross-artifact analysis caught critical contradiction (C1) that would have caused confusion during implementation - FR-015 vs CL-001 autoplay conflict. Contact form gap (C2) showed importance of validating that all tasks have corresponding requirements. Analysis detected 11 total issues but only 2 were critical blockers.

## Evaluation notes (flywheel)

- Failure modes observed: None - all critical issues successfully identified and fixed
- Graders run and results (PASS/FAIL): PASS - Analysis correctly identified contradictions, coverage gaps, and duplications across artifacts
- Prompt variant (if applicable): Standard /sp.analyze workflow with targeted detection passes
- Next experiment (smallest change to try): Consider running /sp.analyze automatically after /sp.tasks to catch issues before implementation starts
