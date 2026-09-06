#!/usr/bin/env python3
"""
Prueft die Produktbilder, bevor sie hochgehen.

Ein QR-Code, den keine Kamera liest, faellt erst auf, wenn ein Kunde ihn
scannt und nichts passiert. Darum wird er hier gelesen — aus dem fertigen
Bild, so wie eine Kamera ihn sieht, und zusaetzlich aus einer verkleinerten
Fassung, wie sie auf einem Telefonbildschirm ankommt.

    python3 build/etsy/pruefung.py [erwartete-adresse]
"""
import pathlib
import sys

import cv2
import numpy as np
from PIL import Image

ORDNER = pathlib.Path(__file__).resolve().parent / "bilder"
KANTE = 2000
gut = schlecht = 0


def pruef(name, ok, notiz=""):
    global gut, schlecht
    if ok:
        gut += 1
        print(f"  ok    {name} {notiz}")
    else:
        schlecht += 1
        print(f"  FEHLT {name} {notiz}")


def lesen(pfad: pathlib.Path, breite: int) -> str:
    im = Image.open(pfad).convert("RGB")
    if breite != im.width:
        im = im.resize((breite, breite), Image.LANCZOS)
    roh = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
    text, _, _ = cv2.QRCodeDetector().detectAndDecode(roh)
    return text


def main(argv):
    erwartet = argv[0] if argv else None
    dateien = sorted(ORDNER.glob("*.png"))
    pruef("zehn Bilder", len(dateien) == 10, f"{len(dateien)} gefunden")

    for f in dateien:
        im = Image.open(f)
        pruef(f"{f.name}: {KANTE}x{KANTE}", im.size == (KANTE, KANTE),
              f"{im.size[0]}x{im.size[1]}")
        # Etsy nimmt bis 20 MB je Bild. Weit darunter zu bleiben spart dem
        # Kaeufer auf dem Telefon Ladezeit.
        mb = f.stat().st_size / 1048576
        pruef(f"{f.name}: unter 5 MB", mb < 5, f"{mb:.1f} MB")

    demo = ORDNER / "03-demo.png"
    if demo.is_file():
        voll = lesen(demo, KANTE)
        pruef("QR lesbar in voller Groesse", bool(voll), voll or "nichts gelesen")
        # So gross ist das Bild auf einem Telefon, wenn jemand es antippt.
        klein = lesen(demo, 800)
        pruef("QR lesbar bei 800 Punkten", klein == voll and bool(klein))
        if erwartet:
            pruef("QR zeigt auf die erwartete Adresse", voll == erwartet,
                  f"{voll}")
        else:
            print(f"        (zeigt auf {voll})")

    print(f"\n{gut} bestanden, {schlecht} fehlgeschlagen")
    return schlecht


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
