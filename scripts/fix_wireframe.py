#!/usr/bin/env python3
"""
fix_wireframe.py — Post-process AI-generated ASCII wireframes to ensure
every screen is a perfect rectangle with aligned borders.

Usage:
  # JSON mode (array of FlowStep objects):
  echo '<json>' | python3 fix_wireframe.py

  # Plain text mode (single wireframe):
  echo '<wireframe text>' | python3 fix_wireframe.py

Detects mode automatically: if stdin starts with '[', treats as JSON array.
Otherwise treats as a plain wireframe text block.
"""

import json
import sys


# Box-drawing character sets
LEFT_JUNCTIONS = set("┌├└")
RIGHT_JUNCTIONS = set("┐┤┘")
HORIZONTAL = "─"
VERTICAL = "│"

# Map left-side junction → matching right-side junction
RIGHT_FOR_LEFT = {"┌": "┐", "├": "┤", "└": "┘"}


def fix_wireframe(wireframe: str) -> str:
    """Normalize a wireframe so every line is the same width with proper borders."""
    lines = wireframe.split("\n")

    # Strip empty leading/trailing lines
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()

    if not lines:
        return wireframe

    # Determine target width from the widest line
    widths = [len(line.rstrip()) for line in lines]
    target = max(widths)

    # Ensure target is at least as wide as top border
    top = lines[0].rstrip()
    if top and top[0] in LEFT_JUNCTIONS and top[-1] in RIGHT_JUNCTIONS:
        target = max(target, len(top))

    fixed = []
    for line in lines:
        stripped = line.rstrip()
        if not stripped:
            fixed.append("")
            continue

        ch = stripped[0]

        if ch in LEFT_JUNCTIONS:
            fixed.append(_fix_horizontal(stripped, target))
        elif ch == VERTICAL:
            fixed.append(_fix_content(stripped, target))
        else:
            # Fallback: pad to width
            fixed.append(stripped.ljust(target))

    return "\n".join(fixed)


def _fix_horizontal(line: str, target: int) -> str:
    """Fix a horizontal border/divider line to exactly `target` characters.

    Preserves internal junctions (┬ ┴ ┼ │) and extends/shrinks the last
    horizontal run before the right-side junction.
    """
    left = line[0]
    expected_right = RIGHT_FOR_LEFT.get(left, "┤")

    # Find the rightmost junction character
    right_pos = -1
    for i in range(len(line) - 1, 0, -1):
        if line[i] in RIGHT_JUNCTIONS:
            right_pos = i
            break

    if right_pos == -1:
        # No right junction found — append ─ and junction
        inner = line[1:]
        needed = target - 2
        if len(inner) < needed:
            return left + inner + HORIZONTAL * (needed - len(inner)) + expected_right
        return left + inner[:needed] + expected_right

    # Has a right junction. Grab everything between left and right junctions.
    inner = line[1:right_pos]
    right_char = line[right_pos]
    needed = target - 2  # target minus left and right border chars

    if len(inner) == needed:
        return left + inner + right_char

    if len(inner) < needed:
        # Extend: find the last run of ─ and stretch it
        diff = needed - len(inner)
        # Insert ─ before the right junction (extend the last ─ run)
        last_h = inner.rfind(HORIZONTAL)
        if last_h != -1:
            return left + inner[: last_h + 1] + HORIZONTAL * diff + inner[last_h + 1 :] + right_char
        else:
            # No ─ found; just append ─
            return left + inner + HORIZONTAL * diff + right_char

    # Shrink: truncate inner
    return left + inner[:needed] + right_char


def _fix_content(line: str, target: int) -> str:
    """Fix a content line to exactly `target` characters.

    Content lines start with │ and should end with │ at column `target-1`.
    Padding is added to the rightmost section (after the last internal │).
    """
    current = len(line)

    if current == target:
        # Already correct — but verify it ends with │
        if line[-1] == VERTICAL:
            return line
        # Ends with wrong char; swap last char
        return line[:-1] + VERTICAL

    if line[-1] == VERTICAL:
        # Line has a closing │ but is too short or too long
        if current < target:
            # Find the last │ (the border), insert spaces before it
            # This pads the rightmost cell
            inner = line[:-1]
            return inner + " " * (target - current) + VERTICAL
        else:
            # Too long — find content between first and last │, trim
            # Trim from the rightmost section
            return line[: target - 1] + VERTICAL
    else:
        # Missing right border
        if current < target:
            return line + " " * (target - 1 - current) + VERTICAL
        elif current == target - 1:
            return line + VERTICAL
        else:
            return line[: target - 1] + VERTICAL


def process(steps: list) -> list:
    """Fix wireframes in a list of FlowStep objects."""
    for step in steps:
        if "wireframe" in step and isinstance(step["wireframe"], str):
            step["wireframe"] = fix_wireframe(step["wireframe"])
    return steps


def main():
    raw = sys.stdin.read()
    stripped = raw.strip()

    if stripped.startswith("["):
        # JSON mode: array of FlowStep objects
        data = json.loads(stripped)
        fixed = process(data)
        json.dump(fixed, sys.stdout, ensure_ascii=False)
    else:
        # Plain text mode: single wireframe
        fixed = fix_wireframe(stripped)
        sys.stdout.write(fixed)


if __name__ == "__main__":
    main()
