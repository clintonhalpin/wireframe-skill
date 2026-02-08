# wireframe-skill

A Claude Code plugin that generates ASCII wireframes and user flow diagrams using box-drawing characters and block elements.

## Install

```bash
claude plugin add /path/to/wireframe-skill
```

## Usage

**Direct mode** — generate wireframes in one pass:

```
/wireframe user signup for a SaaS app
/wireframe e-commerce checkout flow
```

**Wizard mode** — interactive flow planning:

```
/wireframe
```

The wizard asks what you're building, generates a flow diagram for review, then produces wireframes for each screen.

## What it generates

1. **Flow diagrams** — ASCII box-drawing diagrams showing the user journey between screens
2. **Screen wireframes** — detailed ASCII layouts for each screen in the flow

Wireframes use block characters for visual hierarchy:

| Character | Meaning |
|-----------|---------|
| `████` | Headings / titles |
| `░░░░` | Body text |
| `▓▓▓▓` | Images / media |
| `▒▒▒▒` | Secondary text / metadata |

## Structure

```
commands/       Skill command definitions
scripts/        Template library and post-processing tools
```

## Author

Clinton Halpin
