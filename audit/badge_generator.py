# audit/badge_generator.py

import datetime
import cairosvg
# Definition of the badge template
BADGE_TEMPLATE = """
<svg xmlns="http://www.w3.org/2000/svg" width="180" height="20">
  <linearGradient id="b" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <mask id="a">
    <rect width="180" height="20" rx="3" fill="#fff"/>
  </mask>
  <g mask="url(#a)">
    <rect width="110" height="20" fill="#555"/>
    <rect x="110" width="70" height="20" fill="{color}"/>
    <rect width="180" height="20" fill="url(#b)"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="Verdana" font-size="11">
    <text x="55" y="14">Security Audit</text>
    <text x="145" y="14">{status}</text>
  </g>
  <a xlink:href="{report_link}" target="_blank">
    <rect width="180" height="20" fill-opacity="0"/>
  </a>
</svg>
"""
# Function to generate the badge based on audit summary
def generate_badge(audit_summary, output_path_svg="badge.svg", output_path_png=None, report_link="https://example.com/report"):
    """
    Generates an SVG and optionally PNG badge depending on the audit summary.

    :param audit_summary: Dictionary with Keys:
        - status: 'Safe', 'Warning', 'Critical'
        - vulnerabilities_count: number of vulnerabilities found 
    :param output_path_svg: Path to save the SVG badge.
    :param output_path_png: Optional path to save the PNG badge.
    :param report_link: URL to link the badge to the detailed report.
    """
    status = audit_summary.get("status", "Unknown")
    vulns = audit_summary.get("vulnerabilities_count", 0)
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Elegir color según estado
    if status.lower() == "safe":
        color = "#4c1"  # Verde
    elif status.lower() == "warning":
        color = "#dfb317"  # Amarillo
    elif status.lower() == "critical":
        color = "#e05d44"  # Rojo
    else:
        color = "#9f9f9f"  # Gris

    # Montar el texto de estado
    status_text = f"{status} ({vulns}) - {date}"

    # Renderizar el badge
    badge_content = BADGE_TEMPLATE.format(color=color, status=status_text, report_link=report_link)

    with open(output_path_svg, "w") as f:
        f.write(badge_content)

    print(f"[+] Badge generated: {output_path_svg}")
    if output_path_png:
        cairosvg.svg2png(bytestring=badge_content.encode('utf-8'), write_to=output_path_png)
        print(f"[+] Badge PNG generated: {output_path_png}")
