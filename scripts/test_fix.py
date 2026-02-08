#!/usr/bin/env python3
"""Quick tests for fix_wireframe.py"""

from fix_wireframe import fix_wireframe


def test_uneven_content_lines():
    """Lines of different lengths should be padded to match."""
    wf = "\n".join([
        "┌──────────────────────────────────────────────────┐",
        "│ ▒▒▒▒      Home   About   Products   Contact      │",
        "├──────────────────────────────────────────────────┤",
        "│                                                    │",
        "│  ████████████████                              │",
        "│                                          │",
        "│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │",
        "│  ░░░░░░░░░░░░░░░░░░░░░░░░│",
        "└──────────────────────────────────────────────────┘",
    ])
    fixed = fix_wireframe(wf)
    lines = fixed.split("\n")
    widths = [len(line) for line in lines if line.strip()]
    assert len(set(widths)) == 1, f"Widths not uniform: {widths}"
    print(f"  PASS: All {len(lines)} lines are {widths[0]} chars wide")
    print(fixed)
    print()


def test_missing_right_border():
    """Lines missing │ on the right should get one added."""
    wf = "\n".join([
        "┌────────────────────────────────────┐",
        "│  Hello world",
        "│  More content here",
        "└────────────────────────────────────┘",
    ])
    fixed = fix_wireframe(wf)
    lines = fixed.split("\n")
    for line in lines:
        if line.strip():
            assert line[-1] in "┐┤┘│", f"Line doesn't end with border: {repr(line)}"
    widths = [len(line) for line in lines if line.strip()]
    assert len(set(widths)) == 1, f"Widths not uniform: {widths}"
    print(f"  PASS: Missing borders fixed, all {widths[0]} chars wide")
    print(fixed)
    print()


def test_multi_column():
    """Sidebar + content layout should preserve internal │."""
    wf = "\n".join([
        "┌──────────────┬───────────────────────────────┐",
        "│ SIDEBAR      │ Content area                   │",
        "│ * Dashboard  │ ░░░░░░░░░░░░░░░░░░░░ │",
        "│   Settings   │ ░░░░░░░░░░░│",
        "├──────────────┼───────────────────────────────┤",
        "│   Help       │ ████████████             │",
        "└──────────────┴───────────────────────────────┘",
    ])
    fixed = fix_wireframe(wf)
    lines = fixed.split("\n")
    widths = [len(line) for line in lines if line.strip()]
    assert len(set(widths)) == 1, f"Widths not uniform: {widths}"
    print(f"  PASS: Multi-column, all {widths[0]} chars wide")
    print(fixed)
    print()


def test_short_horizontal_divider():
    """Horizontal dividers should be extended to match target width."""
    wf = "\n".join([
        "┌──────────────────────────────────────────────────┐",
        "│ Header                                            │",
        "├────────────────────────┤",
        "│ Content                                           │",
        "└──────────────────────────────────────────────────┘",
    ])
    fixed = fix_wireframe(wf)
    lines = fixed.split("\n")
    widths = [len(line) for line in lines if line.strip()]
    assert len(set(widths)) == 1, f"Widths not uniform: {widths}"
    print(f"  PASS: Short divider extended, all {widths[0]} chars wide")
    print(fixed)
    print()


def test_already_perfect():
    """A correctly-formed wireframe should pass through unchanged."""
    wf = "\n".join([
        "┌──────────────────────────────┐",
        "│  ████████████████            │",
        "│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░ │",
        "│                              │",
        "│  [Submit]        (Cancel)    │",
        "└──────────────────────────────┘",
    ])
    fixed = fix_wireframe(wf)
    assert fixed == wf, "Perfect wireframe was modified!"
    print("  PASS: Perfect wireframe unchanged")
    print(fixed)
    print()


def test_plain_text_stdin():
    """Plain text mode via main() should fix a single wireframe."""
    import subprocess
    import os

    script = os.path.join(os.path.dirname(__file__), "fix_wireframe.py")
    wf = "\n".join([
        "┌──────────────────────────────────────┐",
        "│  Hello world",
        "│  More content",
        "└──────────────────────────────────────┘",
    ])
    result = subprocess.run(
        ["python3", script],
        input=wf,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Script failed: {result.stderr}"
    lines = result.stdout.split("\n")
    widths = [len(line) for line in lines if line.strip()]
    assert len(set(widths)) == 1, f"Widths not uniform: {widths}"
    # Should NOT be JSON — plain text mode returns plain text
    assert not result.stdout.strip().startswith("["), "Plain text mode returned JSON"
    print(f"  PASS: Plain text stdin mode, all {widths[0]} chars wide")
    print(result.stdout)
    print()


def test_json_stdin():
    """JSON mode via main() should still work."""
    import subprocess
    import os
    import json

    script = os.path.join(os.path.dirname(__file__), "fix_wireframe.py")
    steps = [{"step": 1, "title": "Test", "description": "Test",
              "wireframe": "┌────────────┐\n│  Hello\n└────────────┘"}]
    result = subprocess.run(
        ["python3", script],
        input=json.dumps(steps),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Script failed: {result.stderr}"
    data = json.loads(result.stdout)
    assert isinstance(data, list), "JSON mode should return array"
    lines = data[0]["wireframe"].split("\n")
    widths = [len(line) for line in lines if line.strip()]
    assert len(set(widths)) == 1, f"Widths not uniform: {widths}"
    print(f"  PASS: JSON stdin mode, all {widths[0]} chars wide")
    print(data[0]["wireframe"])
    print()


if __name__ == "__main__":
    print("=== fix_wireframe tests ===\n")
    test_already_perfect()
    test_uneven_content_lines()
    test_missing_right_border()
    test_multi_column()
    test_short_horizontal_divider()
    test_plain_text_stdin()
    test_json_stdin()
    print("All tests passed!")
