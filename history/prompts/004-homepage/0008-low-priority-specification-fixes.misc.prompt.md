---
id: 0008
title: Low Priority Specification Fixes (L1-L2)
stage: misc
date: 2025-12-28
surface: agent
model: claude-sonnet-4-5
feature: 004-homepage
branch: 004-homepage
user: developer
command: manual fixes
labels: ["quality-assurance", "clarity", "professionalism"]
links:
  spec: specs/004-homepage/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/004-homepage/spec.md (modified - updated FR-001, FR-006, FR-034)
tests:
 - None (specification fixes phase)
---

## Prompt

Fix the 2 low priority issues identified in /sp.analyze report:
- **L1**: Emoji in requirement (FR-034 contains ❤️ emoji - unprofessional in formal specification)
- **L2**: Navigation link types unclear (FR-001 and FR-006 don't specify whether links are scroll anchors or route navigation)

## Response snapshot

**L1 - Emoji in Requirement - FIXED**

**Issue**: FR-034 included emoji in requirement text: "Footer MUST include 'Built with ❤️ by [Team/Company Name]' attribution"

**Why this is a problem**:
- Emojis in formal specification documents appear unprofessional
- Requirements should be implementation-neutral (emoji rendering varies by platform)
- The heart emoji is decorative, not functional - doesn't add testable value
- Implementer can still add emoji in actual UI if desired

**Fix Applied**: Changed FR-034 from:
```markdown
- **FR-034**: Footer MUST include "Built with ❤️ by [Team/Company Name]" attribution
```

To:
```markdown
- **FR-034**: Footer MUST include "Built by [Team/Company Name]" attribution text
```

**Rationale**:
- ✅ Professional tone: Specifications should be emoji-free
- ✅ Implementation flexibility: Removes prescriptive UI detail
- ✅ Testable: Can verify "Built by [Team Name]" text exists
- ✅ Intent preserved: Attribution requirement still clear

**Note**: Implementation can still add "with ❤️" or other decorative elements as polish - requirement just doesn't mandate it.

---

**L2 - Navigation Link Types Unclear - FIXED**

**Issue**: FR-001 and FR-006 mentioned "navigation links" but didn't clarify whether these are:
- **Scroll anchors**: In-page links that scroll to sections (e.g., `<a href="#features">`)
- **Route navigation**: Links to different pages (e.g., `<Link href="/features">`)

This ambiguity could cause implementation confusion.

**Evidence from tasks.md**:
- T018: Navigation component has "nav links (Home, Features, Demo, Developers, Contact)"
- T022: "Implement smooth scroll behavior... with `scrollIntoView`"
- T024: "Update Navigation component to highlight active section using use-section-observer hook"

Conclusion: These are **scroll anchors** (in-page navigation), not route links.

**Fix Applied**:

**FR-001** changed from:
```markdown
- **FR-001**: Homepage MUST display a fixed header at the top containing the Todo-Evolution logo, navigation links (Home, Features, Developers), and Sign In / Sign Up buttons
```

To:
```markdown
- **FR-001**: Homepage MUST display a fixed header at the top containing the Todo-Evolution logo, in-page navigation links as scroll anchors (Home, Features, Demo, Developers, Contact), and Sign In / Sign Up buttons
```

**FR-006** changed from:
```markdown
- **FR-006**: Navigation links MUST highlight the current section when scrolling (active state)
```

To:
```markdown
- **FR-006**: In-page navigation links MUST highlight the currently visible section when scrolling using active state styling (detected via Intersection Observer)
```

**Changes made**:
1. ✅ Clarified "in-page navigation links as scroll anchors" (not route navigation)
2. ✅ Added complete list from T018: Home, Features, Demo, Developers, Contact (was missing Demo and Contact)
3. ✅ Added implementation detail: "detected via Intersection Observer" (aligns with T023, T024)
4. ✅ Clarified "currently visible section" (not just "current section" which is ambiguous)

**Rationale**:
- Removes ambiguity: Implementer knows to use scroll anchors, not Next.js routing
- Aligns with tasks: Matches T018, T022, T023, T024 implementation approach
- Complete information: All 5 navigation items listed (not partial list)
- Testable: Can verify Intersection Observer is used for active state detection

**Before**: Navigation could be interpreted as separate pages  
**After**: Clear that it's single-page scrolling with section highlighting

## Outcome

- ✅ Impact: All 2 low priority issues resolved. Emoji removed from FR-034 for professional tone. Navigation link types clarified as scroll anchors with complete list (Home, Features, Demo, Developers, Contact) and Intersection Observer implementation detail added.
- 🧪 Tests: No tests in specification phase. Requirements now clearer for implementation and testing.
- 📁 Files: Modified specs/004-homepage/spec.md (3 edits: FR-001 clarified with complete nav list, FR-006 updated with implementation detail, FR-034 emoji removed)
- 🔁 Next prompts: All analysis issues resolved (2 critical, 3 high, 4 medium, 2 low). Specification is ready for implementation. Run /sp.implement or begin manual implementation following tasks.md.
- 🧠 Reflection: L2 shows importance of precise terminology in requirements - "navigation links" is ambiguous (could be routing or scrolling). Being explicit ("in-page navigation links as scroll anchors") removes implementation confusion. L1 demonstrates that specifications should be formal documents - emojis belong in UI, not requirement definitions.

## Evaluation notes (flywheel)

- Failure modes observed: None - all fixes applied cleanly
- Graders run and results (PASS/FAIL): PASS - Requirements now clear, professional, and implementation-specific
- Prompt variant (if applicable): Standard specification refinement based on analysis findings
- Next experiment (smallest change to try): Consider adding terminology glossary to spec template defining common terms like "navigation link", "scroll anchor", "route", "section" to prevent ambiguity in future specs
