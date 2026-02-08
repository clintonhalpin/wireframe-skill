#!/usr/bin/env python3
"""Unit tests for validate_html.py check functions."""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from validate_html import validate_html, validate_file, WireframeHTMLParser, ALL_CHECKS

# Minimal valid boilerplate for constructing test HTML
CSS_STUB = """
.wf-page { color: #333; } .wf-screen { border: 1px solid; }
.wf-btn { background: #333; } .wf-header { padding: 12px; }
.wf-body { padding: 16px; } .wf-heading { height: 14px; }
.wf-text { height: 10px; } .wf-image { height: 120px; }
.wf-proto-bar { display: none; } .wf-segment { display: flex; }
""" + ("x" * 5000)  # Pad to avoid truncation warning


def _make_html(body, css=CSS_STUB, script=True):
    script_block = """
    <script>
    function showScreen(n) {}
    function setView(v) {}
    function goScreen(d) {}
    </script>
    """ if script else ""
    return f"""<!DOCTYPE html><html><head><style>{css}</style></head>
    <body class="wf-page">
    <h1 class="wf-flow-title">Test</h1>
    <p class="wf-flow-subtitle">2 screens</p>
    <pre class="wf-flow-diagram">A -> B</pre>
    <div class="wf-segment"><button class="wf-segment-btn">Screens</button></div>
    <div class="wf-proto-bar"><span class="wf-proto-bar-title"></span></div>
    {body}
    {script_block}
    </body></html>"""


def _screen(num, title="Screen", desc="Desc", content="", goto_next=None):
    goto = f' data-goto="{goto_next}"' if goto_next else ""
    btn = f'<span class="wf-btn"{goto}>Next</span>' if goto_next else ""
    return f"""
    <h2 class="wf-screen-title">Step {num}</h2>
    <p class="wf-screen-desc">{desc}</p>
    <div class="wf-screen" data-screen="{num}" data-title="{title}" data-desc="{desc}">
      <div class="wf-body">{content}{btn}</div>
    </div>"""


# ── Tests ────────────────────────────────────────────────────────────────────

def test_perfect_score():
    """A well-formed HTML should score 100."""
    html = _make_html(
        _screen(1, "Search", "User searches", goto_next="2") +
        _screen(2, "Results", "User views results")
    )
    report = validate_html(html)
    assert report["score"] == 100, f"Expected 100, got {report['score']}\n{report['summary']}"
    assert report["pass"] is True
    print("  PASS: Perfect HTML scores 100")


def test_forbidden_pre():
    """Extra <pre> wrapping a screen should deduct 20."""
    html = _make_html(
        _screen(1, "Search", "S", goto_next="2") +
        _screen(2, "Results", "R") +
        "<pre>Some ASCII wireframe here</pre>"
    )
    report = validate_html(html)
    assert report["checks"]["forbidden_elements"]["deduction"] == 20
    print("  PASS: Extra <pre> deducts 20")


def test_block_characters():
    """Block chars outside <pre> should deduct points."""
    html = _make_html(
        _screen(1, "S", "D", content="<div>████ heading</div>", goto_next="2") +
        _screen(2, "R", "D")
    )
    report = validate_html(html)
    assert report["checks"]["block_characters"]["deduction"] > 0
    print("  PASS: Block characters detected and penalized")


def test_missing_data_title():
    """Screen without data-title should deduct 10."""
    html = _make_html("""
    <div class="wf-screen" data-screen="1" data-desc="D">
      <div class="wf-body"><span class="wf-btn" data-goto="2">Next</span></div>
    </div>
    <div class="wf-screen" data-screen="2" data-title="R" data-desc="D">
      <div class="wf-body"></div>
    </div>
    """)
    report = validate_html(html)
    assert report["checks"]["screen_structure"]["deduction"] == 10
    print("  PASS: Missing data-title deducts 10")


def test_screen_count_mismatch():
    """Subtitle says 2 screens but only 1 exists."""
    html = _make_html(_screen(1, "Only", "Only one"))
    report = validate_html(html)
    assert report["checks"]["screen_count"]["deduction"] == 20
    print("  PASS: Screen count mismatch deducts 20")


def test_dangling_goto():
    """data-goto targeting non-existent screen deducts 10."""
    html = _make_html(
        _screen(1, "S", "D", content='<span class="wf-btn" data-goto="99">Go</span>') +
        _screen(2, "R", "D")
    )
    # Screen 1 has goto to 99 (doesn't exist) plus potentially goto to 2 from _screen helper
    report = validate_html(html)
    assert report["checks"]["navigation_wiring"]["deduction"] > 0
    print("  PASS: Dangling goto detected")


def test_unreachable_screen():
    """Screen with no incoming gotos is unreachable."""
    html = _make_html(
        _screen(1, "Start", "D") +  # no goto — screen 2 unreachable
        _screen(2, "End", "D")
    )
    report = validate_html(html)
    nav = report["checks"]["navigation_wiring"]
    assert nav["deduction"] >= 15, f"Expected >= 15, got {nav['deduction']}"
    print("  PASS: Unreachable screen detected")


def test_unknown_wf_class():
    """Unknown wf-* class should deduct 5."""
    html = _make_html(
        '<div class="wf-nonexistent">Bad</div>' +
        _screen(1, "S", "D", goto_next="2") +
        _screen(2, "R", "D")
    )
    report = validate_html(html)
    assert report["checks"]["wf_classes"]["deduction"] == 5
    print("  PASS: Unknown wf-* class deducts 5")


def test_missing_boilerplate():
    """Missing segment control should deduct 10."""
    html = """<!DOCTYPE html><html><head><style>
    .wf-page {} .wf-screen {} .wf-btn {} .wf-header {} .wf-body {}
    .wf-heading {} .wf-text {} .wf-image {} .wf-proto-bar {} .wf-segment {}
    """ + ("x" * 5000) + """
    </style></head><body class="wf-page">
    <h1 class="wf-flow-title">T</h1>
    <p class="wf-flow-subtitle">1 screens</p>
    <pre class="wf-flow-diagram">A</pre>
    <div class="wf-screen" data-screen="1" data-title="S" data-desc="D">
      <div class="wf-body"></div>
    </div>
    </body></html>"""
    report = validate_html(html)
    bp = report["checks"]["required_boilerplate"]
    # Missing: segment, proto-bar, script
    assert bp["deduction"] >= 20, f"Expected >= 20, got {bp['deduction']}"
    print("  PASS: Missing boilerplate detected")


def test_missing_css():
    """Empty <style> should deduct 20."""
    html = _make_html(
        _screen(1, "S", "D", goto_next="2") +
        _screen(2, "R", "D"),
        css=""
    )
    report = validate_html(html)
    assert report["checks"]["css_inlined"]["deduction"] == 20
    print("  PASS: Missing CSS deducts 20")


def test_hotel_booking_gold_standard():
    """hotel-booking.html must score exactly 100."""
    html_path = os.path.join(os.path.dirname(__file__), "..", "examples", "hotel-booking.html")
    if not os.path.exists(html_path):
        print("  SKIP: hotel-booking.html not found")
        return
    report = validate_file(html_path)
    assert report["score"] == 100, f"Gold standard scored {report['score']}, not 100\n{report['summary']}"
    assert report["screen_count"] == 6
    print("  PASS: hotel-booking.html scores 100/100")


if __name__ == "__main__":
    print("=== validate_html tests ===\n")
    test_perfect_score()
    test_forbidden_pre()
    test_block_characters()
    test_missing_data_title()
    test_screen_count_mismatch()
    test_dangling_goto()
    test_unreachable_screen()
    test_unknown_wf_class()
    test_missing_boilerplate()
    test_missing_css()
    test_hotel_booking_gold_standard()
    print("\nAll tests passed!")
