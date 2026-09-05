#!/usr/bin/env python3
"""
AMBRA — Hero-Film in Webgroesse bringen.

Was aus einem Videogenerator kommt, ist fuer eine Website unbrauchbar: der
Rohclip hat rund 25 Mbit/s, das sind fuenfzehn Megabyte fuer fuenf Sekunden.
Eine Einladung wird unterwegs geoeffnet, oft mit schlechtem Empfang.

    python3 build/art/ambra_film.py <rohclip.mp4>

Erzeugt drei Dinge:

  assets/video/hero.webm  VP9, das kleinere Format, wird zuerst angeboten
  assets/video/hero.mp4   H.264 mit faststart, fuer alles was kein VP9 kann
  assets/img/hero.webp    das erste Bild des Films als Standbild

Beide Formate, weil kein einzelnes ueberall laeuft: aeltere Apple-Geraete
koennen kein VP9, und manche Chromium-Bauten sind ohne H.264 uebersetzt.

Das Standbild kommt bewusst aus dem Film selbst. Wuerde es aus einer anderen
Quelle stammen, saehe man beim Uebergang einen Sprung in Farbe und Ausschnitt.
"""
from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
THEME = ROOT / "themes" / "ambra" / "assets"

FFMPEG = ("/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/"
          "ffmpeg-linux-x86_64-v7.0.2")

CRF = 31          # H.264. Erfahrungswert: darunter wird die Datei schnell zu
                  # gross, darueber franst der dunkle Himmel in Stufen aus.
CRF_VP9 = 42      # VP9 zaehlt anders. 42 landet etwa dort, wo H.264
                  # mit 31 landet — bei aehnlicher Dateigroesse.
MAX_MB = 2.5      # Darueber lohnt eine Warnung.


def lauf(*args: str) -> None:
    subprocess.run([FFMPEG, "-y", "-hide_banner", "-loglevel", "error", *args],
                   check=True)


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print(__doc__.strip())
        return 2
    roh = pathlib.Path(argv[0])
    if not roh.exists():
        print(f"Nicht gefunden: {roh}")
        return 1

    video = THEME / "video"
    video.mkdir(parents=True, exist_ok=True)
    ziel = video / "hero.mp4"

    # -movflags +faststart schiebt die Kopfdaten an den Anfang. Ohne das
    # beginnt die Wiedergabe erst, wenn die ganze Datei da ist.
    lauf("-i", str(roh),
         "-c:v", "libx264", "-preset", "slow", "-crf", str(CRF),
         "-profile:v", "high", "-level", "4.0", "-pix_fmt", "yuv420p",
         "-movflags", "+faststart", "-an", str(ziel))

    webm = video / "hero.webm"
    lauf("-i", str(roh),
         "-c:v", "libvpx-vp9", "-crf", str(CRF_VP9), "-b:v", "0",
         "-row-mt", "1", "-cpu-used", "3", "-deadline", "good",
         "-pix_fmt", "yuv420p", "-an", str(webm))

    # Standbild aus dem ersten Vollbild — derselbe Ausschnitt, dieselbe Farbe.
    standbild = THEME / "img" / "hero.webp"
    lauf("-i", str(roh), "-frames:v", "1", "-quality", "76", str(standbild))

    mb = ziel.stat().st_size / 1048576
    print(f"  hero.webm   {webm.stat().st_size / 1048576:5.2f} MB")
    print(f"  hero.mp4    {mb:5.2f} MB   (roh: {roh.stat().st_size / 1048576:.2f} MB)")
    print(f"  hero.webp   {standbild.stat().st_size / 1024:5.0f} KB")
    if mb > MAX_MB:
        print(f"  Achtung: ueber {MAX_MB} MB. CRF erhoehen oder kuerzer schneiden.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
