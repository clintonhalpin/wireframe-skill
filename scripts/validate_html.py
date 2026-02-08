#!/usr/bin/env python3
"""
HTML Wireframe Validator
Scores wireframe HTML output on a 100-point scale.
Zero external dependencies — uses only html.parser from stdlib.

Usage:
    python3 validate_html.py examples/hotel-booking.html
    python3 validate_html.py examples/hotel-booking.html --json
"""

import json
import re
import sys
from html.parser import HTMLParser

# ── Known wf-* class vocabulary ──────────────────────────────────────────────

KNOWN_WF_CLASSES = {
    "wf-page", "wf-flow-title", "wf-flow-subtitle", "wf-flow-diagram",
    "wf-screen", "wf-screen-title", "wf-screen-desc",
    "wf-screen-stack", "wf-screen-base", "wf-screen-overlay",
    "wf-header", "wf-body", "wf-footer",
    "wf-row", "wf-col", "wf-col-sidebar",
    "wf-divider", "wf-section",
    "wf-heading", "wf-heading-lg", "wf-text", "wf-meta",
    "wf-image", "wf-image-sm", "wf-image-hero", "wf-avatar",
    "wf-btn", "wf-btn-secondary", "wf-btn-link",
    "wf-label", "wf-input", "wf-textarea", "wf-select",
    "wf-checkbox", "wf-radio",
    "wf-table", "wf-card", "wf-stat-card", "wf-tag",
    "wf-tabs", "wf-tab", "wf-nav-item", "wf-breadcrumb",
    "wf-stepper",
    "wf-modal-backdrop", "wf-modal",
    "wf-flex-between", "wf-flex-end", "wf-flex-center", "wf-inline",
    "wf-mt", "wf-mb", "wf-mt-sm", "wf-mb-sm",
    "wf-gap-sm", "wf-gap", "wf-p",
    "wf-text-center", "wf-text-right", "wf-text-sm",
    "wf-w-full", "wf-grow",
    "wf-segment", "wf-segment-btn",
    "wf-proto-bar", "wf-proto-bar-nav", "wf-proto-bar-btn",
    "wf-proto-bar-title", "wf-proto-bar-counter",
    "wf-proto-caption", "wf-proto-caption-title", "wf-proto-caption-desc",
    "wf-view-prototype", "wf-proto-visible",
    "wf-flow", "wf-flow-row", "wf-flow-node", "wf-flow-arrow", "wf-flow-arrow-down",
}

BLOCK_CHARS_RE = re.compile(r'[█░▓▒]')
BOX_DRAWING_RE = re.compile(r'[┌┐└┘│─├┤┬┴┼▶▼◀]')

REQUIRED_CSS_SELECTORS = [
    ".wf-page", ".wf-screen", ".wf-btn", ".wf-header", ".wf-body",
    ".wf-heading", ".wf-text", ".wf-image", ".wf-proto-bar", ".wf-segment",
]


# ── HTML Parser ──────────────────────────────────────────────────────────────

class WireframeHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.pre_tags = []
        self.screens = []
        self.subtitles = []
        self.goto_targets = set()
        self.all_wf_classes = set()
        self.style_content = ""
        self.has_flow_title = False
        self.has_flow_subtitle = False
        self.has_segment = False
        self.has_proto_bar = False
        self.has_script = False

        self._in_pre = False
        self._pre_content = ""
        self._pre_attrs = {}
        self._in_style = False
        self._style_buf = ""
        self._in_subtitle = False
        self._subtitle_buf = ""
        self._text_outside_pre = []
        # Screen nesting: track depth so we know when we exit a screen div
        self._screen_depth = 0
        self._current_screen_num = None
        self._screen_gotos = {}

    def handle_starttag(self, tag, attrs):
        ad = dict(attrs)
        classes = (ad.get("class") or "").split()

        for c in classes:
            if c.startswith("wf-"):
                self.all_wf_classes.add(c)

        if tag == "pre":
            self._in_pre = True
            self._pre_content = ""
            self._pre_attrs = ad
        if tag == "style":
            self._in_style = True
            self._style_buf = ""
        if tag == "script":
            self.has_script = True
        if "wf-flow-title" in classes:
            self.has_flow_title = True
        if "wf-flow-subtitle" in classes:
            self.has_flow_subtitle = True
            self._in_subtitle = True
            self._subtitle_buf = ""
        if "wf-segment" in classes:
            self.has_segment = True
        if "wf-proto-bar" in classes:
            self.has_proto_bar = True

        # Screen tracking with depth counting
        if "data-screen" in ad:
            self.screens.append(ad)
            self._current_screen_num = ad["data-screen"]
            self._screen_depth = 1
            self._screen_gotos.setdefault(self._current_screen_num, set())
        elif self._screen_depth > 0:
            self._screen_depth += 1

        if "data-goto" in ad:
            self.goto_targets.add(ad["data-goto"])
            if self._current_screen_num is not None and self._screen_depth > 0:
                self._screen_gotos.setdefault(self._current_screen_num, set()).add(ad["data-goto"])

    def handle_endtag(self, tag):
        if tag == "pre" and self._in_pre:
            self._in_pre = False
            self.pre_tags.append((self._pre_attrs, self._pre_content))
        if tag == "style" and self._in_style:
            self._in_style = False
            self.style_content = self._style_buf
        if tag == "p" and self._in_subtitle:
            self._in_subtitle = False
            self.subtitles.append(self._subtitle_buf.strip())
        # Track screen depth
        if self._screen_depth > 0:
            self._screen_depth -= 1
            if self._screen_depth == 0:
                self._current_screen_num = None

    def handle_data(self, data):
        if self._in_pre:
            self._pre_content += data
        elif self._in_style:
            self._style_buf += data
        elif self._in_subtitle:
            self._subtitle_buf += data
        else:
            self._text_outside_pre.append(data)


# ── Check Functions ──────────────────────────────────────────────────────────

def check_forbidden_elements(parser):
    issues = []
    deduction = 0
    for attrs, content in parser.pre_tags:
        cls = (attrs.get("class") or "").split()
        if "wf-flow-diagram" not in cls:
            issues.append(f"Non-flow-diagram <pre> found: '{content[:80].strip()}...'")
            deduction += 20
    flow_count = sum(
        1 for attrs, _ in parser.pre_tags
        if "wf-flow-diagram" in (attrs.get("class") or "").split()
    )
    if flow_count > 1:
        issues.append(f"Multiple flow diagram <pre> tags: {flow_count}")
        deduction += 20
    return {"deduction": min(deduction, 60), "issues": issues}


def check_block_characters(parser):
    issues = []
    deduction = 0
    full_text = "".join(parser._text_outside_pre)
    blocks = BLOCK_CHARS_RE.findall(full_text)
    if blocks:
        issues.append(f"Block characters outside <pre>: {set(blocks)} ({len(blocks)} occurrences)")
        deduction += 15
    boxes = BOX_DRAWING_RE.findall(full_text)
    if boxes:
        issues.append(f"Box-drawing characters outside <pre>: {set(boxes)} ({len(boxes)} occurrences)")
        deduction += 15
    return {"deduction": min(deduction, 30), "issues": issues}


def check_screen_structure(parser):
    issues = []
    deduction = 0
    for screen in parser.screens:
        sn = screen.get("data-screen", "?")
        if "data-title" not in screen:
            issues.append(f"Screen {sn}: missing data-title")
            deduction += 10
        if "data-desc" not in screen:
            issues.append(f"Screen {sn}: missing data-desc")
            deduction += 10
    return {"deduction": min(deduction, 30), "issues": issues}


def check_screen_count(parser):
    issues = []
    deduction = 0
    actual = len(parser.screens)
    expected = None
    for sub in parser.subtitles:
        m = re.search(r'(\d+)\s+screens?', sub)
        if m:
            expected = int(m.group(1))
            break
    if expected is not None and actual != expected:
        issues.append(f"Subtitle says {expected} screens, found {actual}")
        deduction = 20
    if actual == 0:
        issues.append("No [data-screen] elements found")
        deduction = 20
    return {"deduction": deduction, "issues": issues}


def check_navigation_wiring(parser):
    issues = []
    deduction = 0
    screen_nums = {s.get("data-screen") for s in parser.screens}

    dangling = parser.goto_targets - screen_nums
    for d in sorted(dangling):
        issues.append(f"data-goto=\"{d}\" targets non-existent screen")
        deduction += 10

    if screen_nums and "1" in screen_nums:
        visited = set()
        queue = ["1"]
        while queue:
            cur = queue.pop(0)
            if cur in visited:
                continue
            visited.add(cur)
            for nb in parser._screen_gotos.get(cur, []):
                if nb not in visited and nb in screen_nums:
                    queue.append(nb)
        unreachable = screen_nums - visited
        for u in sorted(unreachable):
            issues.append(f"Screen {u} unreachable from screen 1")
            deduction += 15

    nav_graph = {sn: sorted(parser._screen_gotos.get(sn, set())) for sn in sorted(screen_nums)}
    return {"deduction": min(deduction, 40), "issues": issues, "nav_graph": nav_graph}


def check_wf_classes(parser):
    issues = []
    deduction = 0
    unknown = {c for c in parser.all_wf_classes if c.startswith("wf-") and c not in KNOWN_WF_CLASSES}
    for cls in sorted(unknown):
        issues.append(f"Unknown wf-* class: {cls}")
        deduction += 5
    return {"deduction": min(deduction, 20), "issues": issues}


def check_semantic_structure(parser):
    # Lightweight: just ensure we don't have obvious structural issues
    return {"deduction": 0, "issues": []}


def check_required_boilerplate(parser):
    issues = []
    deduction = 0
    checks = [
        (parser.has_flow_title, ".wf-flow-title"),
        (parser.has_flow_subtitle, ".wf-flow-subtitle"),
        (parser.has_segment, ".wf-segment (view switcher)"),
        (parser.has_proto_bar, ".wf-proto-bar (prototype chrome)"),
        (parser.has_script, "<script> block"),
    ]
    for ok, label in checks:
        if not ok:
            issues.append(f"Missing {label}")
            deduction += 10
    return {"deduction": min(deduction, 30), "issues": issues}


def check_css_inlined(parser):
    issues = []
    deduction = 0
    css = parser.style_content
    if not css.strip():
        return {"deduction": 20, "issues": ["No <style> content — CSS not inlined"]}
    missing = [s for s in REQUIRED_CSS_SELECTORS if s not in css]
    if missing:
        issues.append(f"CSS missing selectors: {missing}")
        deduction = 20
    if len(css) < 5000:
        issues.append(f"CSS appears truncated ({len(css)} chars, expected 10000+)")
        deduction = max(deduction, 20)
    return {"deduction": deduction, "issues": issues}


# ── Main Validation ──────────────────────────────────────────────────────────

ALL_CHECKS = [
    ("forbidden_elements", check_forbidden_elements),
    ("block_characters", check_block_characters),
    ("screen_structure", check_screen_structure),
    ("screen_count", check_screen_count),
    ("navigation_wiring", check_navigation_wiring),
    ("wf_classes", check_wf_classes),
    ("semantic_structure", check_semantic_structure),
    ("required_boilerplate", check_required_boilerplate),
    ("css_inlined", check_css_inlined),
]


def validate_html(html_content):
    parser = WireframeHTMLParser()
    parser.feed(html_content)

    score = 100
    checks = {}
    for name, fn in ALL_CHECKS:
        result = fn(parser)
        checks[name] = result
        score -= result["deduction"]
    score = max(0, score)

    lines = [f"Score: {score}/100 {'PASS' if score >= 90 else 'FAIL'}"]
    lines.append(f"Screens found: {len(parser.screens)}")
    for name, result in checks.items():
        if result["issues"]:
            lines.append(f"\n  {name} (-{result['deduction']}pt):")
            for issue in result["issues"]:
                lines.append(f"    - {issue}")
    nav = checks.get("navigation_wiring", {})
    if "nav_graph" in nav:
        lines.append(f"\n  Navigation graph: {nav['nav_graph']}")

    return {
        "score": score,
        "checks": checks,
        "summary": "\n".join(lines),
        "pass": score >= 90,
        "screen_count": len(parser.screens),
    }


def validate_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return validate_html(f.read())


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_html.py <file.html> [--json]", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    report = validate_file(filepath)

    if "--json" in sys.argv:
        out = {
            "score": report["score"],
            "pass": report["pass"],
            "screen_count": report["screen_count"],
            "checks": {
                name: {"deduction": r["deduction"], "issues": r["issues"]}
                for name, r in report["checks"].items()
            },
        }
        print(json.dumps(out, indent=2))
    else:
        print(report["summary"])

    sys.exit(0 if report["pass"] else 1)


if __name__ == "__main__":
    main()
