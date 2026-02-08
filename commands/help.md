---
description: "Show wireframe skill usage and reference"
---

# Wireframe Skill — Help

Print the following help information to the user:

---

## Usage

**Direct mode** — generate wireframes in one pass:
```
/wireframe user signup for a SaaS app
/wireframe e-commerce checkout flow
/wireframe admin dashboard for managing users
```

**Wizard mode** — interactive flow planning:
```
/wireframe
```
The wizard will ask what you're building, generate a flow diagram, let you refine it, then generate wireframes for each screen.

## Block Character Reference

Wireframes use block characters instead of placeholder text for visual hierarchy:

| Character | Meaning |
|-----------|---------|
| `████` | Headings and titles |
| `░░░░` | Body text and paragraphs |
| `▓▓▓▓` | Images, media, and avatars |
| `▒▒▒▒` | Secondary text and metadata |

## Other Conventions

| Pattern | Meaning |
|---------|---------|
| `[Button Label]` | Primary action button |
| `(Button Label)` | Secondary action button |
| `[_______________]` | Input field |
| `┌─┐ │ └─┘` | Box-drawing borders |

## Design Philosophy

Every element on a screen must earn its place. Wireframes follow a critical-path approach:
- Each screen = one clear user action
- Only elements needed for that action are included
- No decorative chrome, no filler content

## Post-Processing

Wireframes are automatically validated through a Python fixer that ensures:
- All borders are fully closed rectangles
- All lines are the same width
- Internal junctions are preserved

---
