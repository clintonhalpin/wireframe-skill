# Ralph Loop: Wireframe HTML Quality Improvement

You are running an iterative quality improvement loop for the wireframe skill's HTML output. Your goal is to make all example HTML files score >= 95 on the validator, and to ensure both the **Screens view** (documentation) and **Prototype view** (clickable navigation) work correctly in the browser.

## Setup

Before starting iterations, ensure these tools are available:

```bash
# Validator
python3 scripts/validate_html.py examples/hotel-booking.html

# Test harness (all examples)
python3 scripts/test_html_conversion.py --all

# Open in browser to verify
open examples/hotel-booking.html
```

## Two Test Tracks

### Track A: Validate existing examples (focus iterations 1-15)
1. Run `python3 scripts/test_html_conversion.py --all`
2. Open each HTML in browser: `open examples/{file}.html`
3. Verify both **Screens view** and **Prototype view** work

### Track B: Generate fresh wireframes (focus iterations 10+)
1. Run the wireframe skill with fresh prompts:
   - `/wireframe task management kanban board`
   - `/wireframe food delivery checkout`
2. Choose "Browser" output for each
3. Run validator on the generated HTML
4. Open in browser to verify

## Each Iteration

1. Run `python3 scripts/test_html_conversion.py --all`
2. If all examples score >= 95 AND the 2 fresh wireframes also score >= 95:
   → Output `<promise>ALL_EXAMPLES_PASS</promise>` and stop
3. Analyze the lowest-scoring check category
4. Make **ONE targeted fix** (to `commands/wireframe.md`, `scripts/wireframe.css`, or a generated HTML)
5. Open the changed HTML in browser: `open examples/{file}.html`
6. Verify Screens + Prototype views work
7. Re-run tests, log the score delta
8. If score decreased → **revert** and try a different approach

## Fix Strategy Table

| Failure Pattern | Fix Target |
|----------------|------------|
| Block chars in HTML | `commands/wireframe.md` forbidden-chars callout |
| `<pre>` wrapping screens | `commands/wireframe.md` anti-pre guardrails |
| Missing data-goto | `commands/wireframe.md` wiring rules |
| Unknown wf-* class | `commands/wireframe.md` mapping table |
| Missing header/body/footer | `commands/wireframe.md` section-break rules |
| CSS truncated | `commands/wireframe.md` "FULL contents" emphasis |
| Screen count mismatch | `commands/wireframe.md` "every screen" emphasis |
| ASCII flow diagram instead of styled | `commands/wireframe.md` flow diagram HTML rules |
| Prototype view broken | Script block or data attributes in the HTML |
| Flow nodes not highlighting | `showScreen()` JS update |

## Convergence Rules

- **Never modify** `examples/hotel-booking.html` (gold standard) or `.md` source files
- **One fix per iteration** — small, targeted changes only
- **Revert on score regression** — if a fix makes things worse, undo it
- After **5 stalled iterations** (no score improvement), try a different strategy:
  - Add a new worked example to `wireframe.md`
  - Restructure the mapping table
  - Add more explicit forbidden-character callouts
  - Add a self-check step to the prompt
- **Always open in browser** after changes to verify the visual result

## Completion Criteria

The loop is complete when:
1. `python3 scripts/test_html_conversion.py --all` → all scores >= 95
2. `hotel-booking.html` still scores 100/100
3. All HTML files render correctly in the browser (Screens + Prototype views)
4. `python3 scripts/test_validate_html.py` → all unit tests pass
5. `python3 scripts/test_fix.py` → existing fixer tests still pass

Output `<promise>ALL_EXAMPLES_PASS</promise>` when all criteria are met.

## Progress Tracking

After each iteration, append to this section:

```
Iteration N: Score before → Score after | Fix: [description] | Target: [file]
```
