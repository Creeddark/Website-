"""
Zweiter Durchlauf der Vorlagen mit eingesetztem Beispielfoto.

Fuer die Verkaufsbilder soll im Bildfenster ein Foto stehen und nicht ein
grauer Kasten — ein Kaeufer sieht in einer Sekunde, was er bekommt. In der
ausgelieferten Vorlage bleibt der Platzhalter dagegen erhalten.

Ergebnis: dist-demo/*.html und previews-demo/*.png, parallel zu den echten.
"""

import pathlib
import subprocess
import sys

SRC = pathlib.Path(__file__).resolve().parent
ROOT = SRC.parent
sys.path.insert(0, str(SRC))

DIST = ROOT / "dist-demo"
PREV = ROOT / "previews-demo"

# Nur die Systeme mit Bildfenster; alle anderen Seiten waeren identisch.
MODULES = ["t08_times", "t10_cover"]

# Suite -> Anlass des Beispielfotos (siehe photo_crops.PHOTOS).
#
# Wer hier fehlt, behaelt auch im Verkaufsbild den neutralen Platzhalter. Das
# ist Absicht: ein Hochzeitskuss in einer Geburtsanzeige waere schlimmer als
# ein grauer Kasten — der Kasten ist erkennbar ein Platzhalter, das falsche
# Foto sieht nach Schlamperei aus.
DEMO_SUITES = {
    "08-times-wedding": "wedding",
    "08-times-baby":    "baby",
    "10-cover-wedding": "wedding",
}


def main():
    import common

    DIST.mkdir(exist_ok=True)
    PREV.mkdir(exist_ok=True)
    files = []
    for name in MODULES:
        mod = __import__(name)
        for c in mod.SUITES:
            theme = DEMO_SUITES.get(c["file"])
            if not theme:
                continue
            # common.image() liest die Variable beim Aufruf, nicht beim Import
            common.DEMO_PHOTOS = theme
            f = DIST / f"{c['file']}.html"
            f.write_text(mod.build(c), encoding="utf-8")
            files.append(f)
            print(f"  {f.name:26} {theme:8} {f.stat().st_size // 1024} KB")
    for f in files:
        subprocess.run(["node", str(SRC / "render.js"), str(f), str(PREV), "2"],
                       check=True, stdout=subprocess.DEVNULL)
    print(f"{len(list(PREV.glob('*.png')))} Seiten in {PREV.name}/")


if __name__ == "__main__":
    main()
