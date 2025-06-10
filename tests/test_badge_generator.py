
import os
import tempfile
import pytest
from audit.badge_generator import generate_badge
import datetime

@pytest.mark.parametrize("status, expected_color", [
    ("Secure", "#4c1"),
    ("Outdated", "#dfb317"),
    ("Vulnerable", "#e05d44"),
    ("UnknownStatus", "#9f9f9f")
])

def test_generate_badge_colors(status, expected_color):
    with tempfile.TemporaryDirectory() as tmpdir:
        svg_path = os.path.join(tmpdir, "badge.svg")
        generate_badge(status=status, output_path_svg=svg_path)
        
        with open(svg_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert expected_color in content, f"Expected color {expected_color} not found for status {status}"

def test_generate_badge_includes_date_and_status():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    with tempfile.TemporaryDirectory() as tmpdir:
        svg_path = os.path.join(tmpdir, "badge.svg")
        generate_badge(status="Secure", vulnerabilities_count=5, output_path_svg=svg_path)
        
        with open(svg_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert today in content, "Date not found in the badge"
            assert "Secure (5)" in content, "Status text with vulnerabilities not found in the badge"

def test_generate_badge_includes_report_link():
    report_link = "https://example.com/report"
    with tempfile.TemporaryDirectory() as tmpdir:
        svg_path = os.path.join(tmpdir, "badge.svg")
        generate_badge(status="Secure", output_path_svg=svg_path, report_link=report_link)
        
        with open(svg_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert report_link in content, "Report link not found in the badge"

@pytest.mark.skip(reason="PNG generation requires additional cairosvg configuration.")
def test_generate_badge_png_creation():
    with tempfile.TemporaryDirectory() as tmpdir:
        svg_path = os.path.join(tmpdir, "badge.svg")
        png_path = os.path.join(tmpdir, "badge.png")
        generate_badge(status="Secure", output_path_svg=svg_path, output_path_png=png_path)
        
        assert os.path.exists(png_path), "PNG file was not generated"

def test_generate_badge_overwrite():
    with tempfile.TemporaryDirectory() as tmpdir:
        svg_path = os.path.join(tmpdir, "badge.svg")
        generate_badge(status="Secure", output_path_svg=svg_path)
        # Overwrite the file
        generate_badge(status="Outdated", output_path_svg=svg_path)
        
        with open(svg_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "Outdated" in content, "Badge file was not overwritten correctly with the new status"

#test for invalid path. 
def test_generate_badge_invalid_path():
    invalid_path = "/invalid/directory/badge.svg"
    with pytest.raises(Exception):  # Adjust the exception (OSError, etc.)
        generate_badge(status="Secure", output_path_svg=invalid_path)

# Test to ensure the generated badge contains necessary SVG tags
def test_generate_badge_contains_svg_tags():
    with tempfile.TemporaryDirectory() as tmpdir:
        svg_path = os.path.join(tmpdir, "badge.svg")
        generate_badge(status="Secure", output_path_svg=svg_path)
        
        with open(svg_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert '<svg' in content, "The <svg> tag is missing in the generated badge"
            assert '<rect' in content, "The <rect> tag is missing in the generated badge"
            assert '<text' in content, "The <text> tag is missing in the generated badge"
