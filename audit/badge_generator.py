# audit/badge_generator.py

import datetime
#Import cairosvg doing try and except to avoid issues if cairosvg is not installed
try:
    import cairosvg
    CAIROSVG_AVAILABLE = True
except ImportError: #pragma: no cover -optional dependency
    cairosvg = None
    CAIROSVG_AVAILABLE = False

# Template for the badge SVG
BADGE_TEMPLATE = """
<svg xmlns="http://www.w3.org/2000/svg" width="200" height="20">
  <linearGradient id="b" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <mask id="a">
    <rect width="200" height="20" rx="3" fill="#fff"/>
  </mask>
  <g mask="url(#a)">
    <rect width="110" height="20" fill="#555"/>
    <rect x="110" width="90" height="20" fill="{color}"/>
    <rect width="200" height="20" fill="url(#b)"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="Verdana" font-size="11">
    <text x="55" y="14">Estado de Dependencias</text>
    <text x="155" y="14">{status}</text>
  </g>
  <a xlink:href="{report_link}" target="_blank">
    <rect width="200" height="20" fill-opacity="0"/>
  </a>
</svg>
"""

# Función para generar el badge
def generate_badge(status, vulnerabilities_count=0, output_path_svg="badge.svg", output_path_png=None, report_link="https://example.com/report"):
    """
    Generates an SVG badge and optionally a PNG badge.

    :param status: Overall status ('Secure', 'Outdated', 'Vulnerable').
    :param vulnerabilities_count: Number of vulnerabilities found.
    :param output_path_svg: Path where the SVG badge will be saved.
    :param output_path_png: Path to the PNG badge (optional).
    :param report_link: Link to the detailed report.
    """
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Choose color based on status
    if status.lower() == "secure":
        color = "#4c1"        # Green
    elif status.lower() == "outdated":
        color = "#dfb317"    # Yellow
    elif status.lower() == "vulnerable":
        color = "#e05d44"    # Red
    else:
        color = "#9f9f9f"    # Grey (default)

    # Status text (with date and vulnerabilities)
    status_text = f"{status} ({vulnerabilities_count}) - {date}"

    # Render the badge
    badge_content = BADGE_TEMPLATE.format(color=color, status=status_text, report_link=report_link)

    # Save the SVG
    with open(output_path_svg, "w") as f:
        f.write(badge_content)

    print(f"[+] Badge SVG generated: {output_path_svg}")

    # Optional: convert to PNG
    if output_path_png:
        if not CAIROSVG_AVAILABLE:
            raise RuntimeError("cairosvg is required to convert SVG to PNG but is not installed.")
        cairosvg.svg2png(bytestring=badge_content.encode('utf-8'), write_to=output_path_png)
        print(f"[+] Badge PNG generated: {output_path_png}")
