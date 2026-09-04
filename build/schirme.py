"""Zweiter Schritt zu build/schirme.mjs: skaliert die Aufnahmen auf die
Groesse, die das Telefon wirklich braucht (540x1184 = 270x592 bei
doppelter Aufloesung), fuellt oben Luft fuer den Lautsprecherbalken und
unten die Restflaeche in der Farbe des jeweiligen Schnitts, und schreibt
WebP nach site/assets/img/."""
from PIL import Image
import pathlib, sys

QUELLE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/velora/schirme")
ZIEL   = pathlib.Path(__file__).resolve().parent.parent / "site" / "assets" / "img"
LUFT, RAHMEN, GROESSE = 44 * 2, 855 * 2, (540, 1184)
NAMEN = {"technik": "schirm-wlan", "umgebung": "schirm-umgebung",
         "kontakt": "schirm-kontakt"}

for quelle, ziel in NAMEN.items():
    im = Image.open(QUELLE / f"{quelle}.png").convert("RGB")
    oben, unten = im.getpixel((4, 1)), im.getpixel((4, im.height - 2))
    voll = Image.new("RGB", (im.width, RAHMEN), unten)
    voll.paste(Image.new("RGB", (im.width, LUFT), oben), (0, 0))
    voll.paste(im, (0, LUFT))
    aus = ZIEL / f"{ziel}.webp"
    voll.resize(GROESSE, Image.LANCZOS).save(aus, "WEBP", quality=86, method=6)
    print(f"  {aus.name:22} {aus.stat().st_size / 1024:5.1f} KB")
