# audit/badge_generator.py

import datetime
import cairosvg

# Template para el badge
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
    Genera un badge SVG y opcionalmente PNG.

    :param status: Estado general ('Seguro', 'Desactualizado', 'Vulnerable').
    :param vulnerabilities_count: Número de vulnerabilidades encontradas.
    :param output_path_svg: Ruta donde se guardará el badge SVG.
    :param output_path_png: Ruta para el badge PNG (opcional).
    :param report_link: Enlace al reporte detallado.
    """
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Elegir color según estado
    if status.lower() == "seguro":
        color = "#4c1"        # Verde
    elif status.lower() == "desactualizado":
        color = "#dfb317"    # Amarillo
    elif status.lower() == "vulnerable":
        color = "#e05d44"    # Rojo
    else:
        color = "#9f9f9f"    # Gris por defecto

    # Texto del estado (con fecha y vulnerabilidades)
    status_text = f"{status} ({vulnerabilities_count}) - {date}"

    # Renderizar el badge
    badge_content = BADGE_TEMPLATE.format(color=color, status=status_text, report_link=report_link)

    # Guardar el SVG
    with open(output_path_svg, "w") as f:
        f.write(badge_content)

    print(f"[+] Badge SVG generado: {output_path_svg}")

    # Opcional: convertir a PNG
    if output_path_png:
        cairosvg.svg2png(bytestring=badge_content.encode('utf-8'), write_to=output_path_png)
        print(f"[+] Badge PNG generado: {output_path_png}")
