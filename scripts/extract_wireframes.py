#!/usr/bin/env python3
"""
Markdown Wireframe Parser
Extracts structured data (title, flow diagram, screens) from .md wireframe files.

Usage:
    python3 extract_wireframes.py examples/hotel-booking.md
    python3 extract_wireframes.py examples/hotel-booking.md --json
"""

import json
import re
import sys


def extract_wireframes(md_content):
    """Parse a wireframe markdown file and return structured data.

    Returns dict with:
        title: str
        flow_diagram: str (ASCII diagram)
        screen_count: int
        screens: list of {step, title, wireframe, description}
    """
    lines = md_content.split("\n")

    # Extract title from "# Flow: ..."
    title = ""
    for line in lines:
        match = re.match(r'^#\s+Flow:\s+(.+)', line)
        if match:
            title = match.group(1).strip()
            break

    # Extract flow diagram (first code block after "## Flow Diagram")
    flow_diagram = ""
    in_flow_section = False
    in_code_block = False
    code_lines = []

    for line in lines:
        if re.match(r'^##\s+Flow Diagram', line):
            in_flow_section = True
            continue

        if in_flow_section:
            if line.strip().startswith("```") and not in_code_block:
                in_code_block = True
                continue
            elif line.strip().startswith("```") and in_code_block:
                flow_diagram = "\n".join(code_lines)
                in_flow_section = False
                in_code_block = False
                code_lines = []
                continue
            elif in_code_block:
                code_lines.append(line)
                continue

        if re.match(r'^##\s+', line) and not re.match(r'^##\s+Flow', line):
            in_flow_section = False

    # Extract screens from "### Step N: ..." sections
    screens = []
    current_screen = None
    in_screen_code = False
    screen_code_lines = []
    description_lines = []

    for i, line in enumerate(lines):
        step_match = re.match(r'^###\s+Step\s+(\d+):\s+(.+)', line)

        if step_match:
            # Save previous screen
            if current_screen:
                current_screen["description"] = " ".join(description_lines).strip()
                screens.append(current_screen)

            current_screen = {
                "step": int(step_match.group(1)),
                "title": step_match.group(2).strip(),
                "wireframe": "",
                "description": "",
            }
            in_screen_code = False
            screen_code_lines = []
            description_lines = []
            continue

        if current_screen:
            if line.strip().startswith("```") and not in_screen_code:
                in_screen_code = True
                continue
            elif line.strip().startswith("```") and in_screen_code:
                current_screen["wireframe"] = "\n".join(screen_code_lines)
                in_screen_code = False
                screen_code_lines = []
                continue
            elif in_screen_code:
                screen_code_lines.append(line)
                continue
            elif line.strip() == "---":
                continue
            elif line.strip() and not current_screen["wireframe"]:
                # Pre-wireframe content (screen list), skip
                continue
            elif line.strip() and current_screen["wireframe"]:
                description_lines.append(line.strip())

    # Save last screen
    if current_screen:
        current_screen["description"] = " ".join(description_lines).strip()
        screens.append(current_screen)

    return {
        "title": title,
        "flow_diagram": flow_diagram,
        "screen_count": len(screens),
        "screens": screens,
    }


def extract_file(filepath):
    """Extract wireframe data from a markdown file."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    return extract_wireframes(content)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 extract_wireframes.py <file.md> [--json]", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    use_json = "--json" in sys.argv

    data = extract_file(filepath)

    if use_json:
        print(json.dumps(data, indent=2))
    else:
        print(f"Title: {data['title']}")
        print(f"Screens: {data['screen_count']}")
        for s in data["screens"]:
            print(f"  Step {s['step']}: {s['title']}")
            if s["description"]:
                print(f"    {s['description'][:80]}...")

    sys.exit(0)


if __name__ == "__main__":
    main()
