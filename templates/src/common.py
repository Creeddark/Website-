"""
Gemeinsames Geruest fuer alle Vorlagen.

Format: 750 x 1050 CSS-Pixel = 5 x 7 Zoll.
Beim Rendern mit deviceScaleFactor 2 entstehen 1500 x 2100 px = echte 300 DPI,
das ist die Druckaufloesung, die Kaeufer erwarten.

Jede Seite traegt data-document-role="page", damit Canva sie beim HTML-Import
als eigene Designseite anlegt.
"""

import base64
import pathlib

W, H = 750, 1050
FONT_DIR = pathlib.Path(__file__).resolve().parent.parent / "fonts"

# Datei -> (Familienname wie in Canva, weight, style)
FONT_FACES = {
    "playfair-2.woff2":   ("Playfair Display", "400 900", "normal"),
    "playfair-1.woff2":   ("Playfair Display", "400 900", "italic"),
    "cormorant-2.woff2":  ("Cormorant Garamond", "300 700", "normal"),
    "cormorant-1.woff2":  ("Cormorant Garamond", "300 700", "italic"),
    "montserrat-1.woff2": ("Montserrat", "100 900", "normal"),
    "bebas-1.woff2":      ("Bebas Neue", "400", "normal"),
    "greatvibes-1.woff2": ("Great Vibes", "400", "normal"),
    "cinzel-1.woff2":     ("Cinzel", "400 900", "normal"),
    "cinzeldeco-1.woff2": ("Cinzel Decorative", "400", "normal"),
    "cinzeldeco-2.woff2": ("Cinzel Decorative", "700", "normal"),
    "cinzeldeco-3.woff2": ("Cinzel Decorative", "900", "normal"),
    "creepster-1.woff2":  ("Creepster", "400", "normal"),
    "fredoka-1.woff2":    ("Fredoka", "300 700", "normal"),
    "dancing-1.woff2":    ("Dancing Script", "400 700", "normal"),
    "josefin-1.woff2":    ("Josefin Sans", "100 700", "normal"),
    "nunito-1.woff2":     ("Nunito", "200 900", "normal"),
    "poppins-1.woff2":    ("Poppins", "300", "normal"),
    "poppins-2.woff2":    ("Poppins", "400", "normal"),
    "poppins-3.woff2":    ("Poppins", "600", "normal"),
    "poppins-4.woff2":    ("Poppins", "700", "normal"),
    "fraktur-1.woff2":    ("UnifrakturMaguntia", "400", "normal"),
    "abril-1.woff2":      ("Abril Fatface", "400", "normal"),
    "bodoni-1.woff2":     ("Bodoni Moda", "400 900", "normal"),
    "archivoblack-1.woff2": ("Archivo Black", "400", "normal"),
    "oswald-1.woff2":     ("Oswald", "200 700", "normal"),
    "italiana-1.woff2":   ("Italiana", "400", "normal"),
    "ebgaramond-2.woff2": ("EB Garamond", "400 800", "normal"),
    "ebgaramond-1.woff2": ("EB Garamond", "400 800", "italic"),
    "pinyon-1.woff2":     ("Pinyon Script", "400", "normal"),
    "anticdidone-1.woff2": ("Antic Didone", "400", "normal"),
}


def font_css(families):
    """@font-face-Bloecke fuer die genannten Familien, Schrift als Data-URI.

    Selbsttragend heisst: der Import bei Canva und das lokale Rendern brauchen
    keine externe Verbindung, es kann also nichts halb fehlschlagen.
    """
    out = []
    for fname, (fam, weight, style) in FONT_FACES.items():
        if fam not in families:
            continue
        path = FONT_DIR / fname
        if not path.exists():
            continue
        b64 = base64.b64encode(path.read_bytes()).decode()
        out.append(
            f"@font-face{{font-family:'{fam}';font-style:{style};"
            f"font-weight:{weight};font-display:block;"
            f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}")
    return "\n".join(out)


BASE_CSS = f"""
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{background:#5A5750;}}
body{{display:flex;flex-direction:column;align-items:center;gap:40px;padding:40px;}}
.page{{
  position:relative;width:{W}px;height:{H}px;overflow:hidden;
  background:#FFFFFF;flex:0 0 auto;
}}
.art{{position:absolute;inset:0;width:100%;height:100%;display:block;}}
.t{{position:absolute;}}
"""


def page(inner, label, *, bg="#FFFFFF", extra_style=""):
    return (f'<div class="page" data-document-role="page" data-label="{label}" '
            f'style="background:{bg};{extra_style}">\n{inner}\n</div>')


def text(content, *, left, top, width=None, size=16, family="Montserrat",
         weight=400, color="#1C1A17", tracking=0, line=1.4, align="center",
         style="normal", transform="none", extra=""):
    """Absolut gesetzter Textblock.

    Breite und Position stehen explizit im style-Attribut — davon haengt ab,
    wie treffend Canva die Elemente beim Import platziert.
    """
    w = f"width:{width}px;" if width else ""
    return (f'<div class="t" style="left:{left}px;top:{top}px;{w}'
            f'font-family:\'{family}\',serif;font-size:{size}px;font-weight:{weight};'
            f'color:{color};letter-spacing:{tracking}em;line-height:{line};'
            f'text-align:{align};font-style:{style};text-transform:{transform};{extra}">'
            f'{content}</div>')


ASSET_DIR = pathlib.Path(__file__).resolve().parent.parent / "assets"


def image(name, *, left, top, width, height, alt="", extra="", radius=0):
    """
    Bild als eigenes Element — Canva legt daraus beim Import ein Bildfeld an,
    das der Kaeufer per Klick durch ein eigenes Foto ersetzt. Waere das Motiv
    Teil der SVG-Ebene, waere es fest eingebrannt.

    Die Datei wird als Data-URI eingebettet, damit der Import nichts nachladen
    muss und nicht halb fehlschlagen kann.
    """
    path = ASSET_DIR / name
    b64 = base64.b64encode(path.read_bytes()).decode()
    r = f"border-radius:{radius}px;" if radius else ""
    return (f'<img src="data:image/png;base64,{b64}" alt="{alt}" '
            f'style="position:absolute;left:{left}px;top:{top}px;'
            f'width:{width}px;height:{height}px;object-fit:cover;{r}{extra}">')


def svg_layer(defs, body, *, w=W, h=H, extra=""):
    return (f'<svg class="art" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none" {extra}>'
            f'<defs>{defs}</defs>{body}</svg>')


def document(title, families, pages, *, body_bg="#5A5750"):
    css = BASE_CSS.replace("background:#5A5750;", f"background:{body_bg};", 1)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
{font_css(families)}
{css}
</style>
</head>
<body>
{chr(10).join(pages)}
</body>
</html>"""
