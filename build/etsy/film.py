#!/usr/bin/env python3
"""
Das Produktvideo fuer Etsy.

Kein nachgestellter Zusammenschnitt, sondern eine Aufnahme der echten Seite:
der Umschlag oeffnet sich wirklich, der Film laeuft wirklich, der
Bilderstreifen wandert wirklich. Was der Kaeufer im Video sieht, bekommt er.

    cd themes/ambra && python3 -m http.server 8100 &
    python3 build/etsy/film.py

Heraus kommt ein Quadrat, 1080 x 1080, etwa dreizehn Sekunden, ohne Ton —
Etsy laesst zwischen fuenf und fuenfzehn Sekunden zu und schaltet den Ton
ohnehin stumm.
"""
from __future__ import annotations

import pathlib
import re
import shutil
import subprocess
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from werkstatt import ersetzen, kopf                        # noqa: E402

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
FFMPEG = ("/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/"
          "ffmpeg-linux-x86_64-v7.0.2")
WEB = "http://127.0.0.1:8100/"
KANTE = 1080
HIER = pathlib.Path(__file__).resolve().parent
ZIEL = HIER / "bilder"

# Das Telefon im Quadrat: der Schirm 852 Punkte hoch, darin die Einladung in
# ihrer eigenen Breite von 390. Oben und unten bleibt Luft fuer die Adresse —
# im Video ist sie das Einzige, was jemand abtippen muss.
SCHIRM_B, SCHIRM_H = 390, 844
MASS = 852 / SCHIRM_H

BUEHNE = """
<div style="width:@@k@@px; height:@@k@@px; background:var(--night);
            display:flex; flex-direction:column; align-items:center;
            justify-content:center; gap:24px; position:relative;
            overflow:hidden; font-family:var(--ff-text)">
  <div style="position:absolute; inset:0;
       background:radial-gradient(58% 40% at 50% 26%,
       rgba(216,182,119,0.16), transparent 72%)"></div>
  <div style="position:relative; padding:13px; border-radius:44px;
       background:linear-gradient(150deg,#3B342A,#16120D 42%,#2A241C);
       box-shadow:0 40px 80px rgba(0,0,0,0.55),
                  inset 0 0 0 1px rgba(242,231,211,0.14)">
    <iframe src="@@web@@" scrolling="no"
            style="width:@@sb@@px; height:@@sh@@px; border:0; display:block;
                   border-radius:33px; transform:scale(@@m@@);
                   transform-origin:top left;
                   margin-right:@@dx@@px; margin-bottom:@@dy@@px"></iframe>
  </div>
  <p style="position:relative; margin:0; color:#D8B677; font-size:25px;
     letter-spacing:0.22em; text-transform:uppercase">simeah.netlify.app</p>

  <!-- Ein Telefon ist schmaler als ein Quadrat. Die beiden Abzeichen fuellen
       die Seiten mit dem, was die Einladung kann, statt mit Schwarz. -->
  <div style="position:absolute; left:96px; top:50%;
              transform:translateY(-50%); display:flex; flex-direction:column;
              gap:34px; align-items:center">@@abz@@</div>
</div>"""

ABZEICHEN = """
  <div style="width:150px; height:150px; border-radius:50%;
              background:#1E1811; border:2px solid #D8B677;
              box-shadow:0 14px 34px rgba(0,0,0,0.5);
              display:grid; place-items:center">
    <span style="font-family:var(--ff-display); font-size:41px; line-height:1;
                 color:#D8B677">RSVP</span>
  </div>
  <div style="width:150px; height:150px; border-radius:50%;
              background:#1E1811; border:2px solid #D8B677;
              box-shadow:0 14px 34px rgba(0,0,0,0.5);
              display:grid; place-items:center">
    <svg viewBox="0 0 24 24" width="62" height="62" fill="none"
         stroke="#D8B677" stroke-width="1.3" stroke-linecap="round"
         stroke-linejoin="round">
      <path d="M9 18V5l10-2v13"/><circle cx="6.5" cy="18" r="2.6"/>
      <circle cx="16.5" cy="16" r="2.6"/>
    </svg>
  </div>"""


def buehne() -> str:
    return ersetzen(BUEHNE, {
        "k": str(KANTE), "web": WEB,
        "sb": str(SCHIRM_B), "sh": str(SCHIRM_H), "m": f"{MASS:.4f}",
        # Ein skaliertes Element behaelt seinen alten Platzbedarf. Ohne diese
        # beiden Zahlen stuende der Rahmen um die unskalierte Groesse herum.
        "dx": f"{SCHIRM_B * (MASS - 1):.1f}",
        "dy": f"{SCHIRM_H * (MASS - 1):.1f}",
        "abz": ABZEICHEN,
    })


def main() -> int:
    ZIEL.mkdir(parents=True, exist_ok=True)
    roh = HIER / "_film"
    shutil.rmtree(roh, ignore_errors=True)

    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        # Doppelt aufgeloest rendern, auf 1080 aufnehmen: das verkleinerte
        # Bild ist schaerfer als eines, das direkt in 1080 entsteht.
        kontext = b.new_context(
            viewport={"width": KANTE, "height": KANTE},
            device_scale_factor=2,
            record_video_dir=str(roh),
            record_video_size={"width": KANTE, "height": KANTE})
        pg = kontext.new_page()
        pg.set_content("<!doctype html><meta charset=utf-8>" + kopf()
                       + "<style>body{margin:0;background:#14100C}</style>"
                       + buehne(), wait_until="load")
        # Nicht frames[1] raten: das Fenster haengt an genau diesem Element,
        # und es ist erst da, wenn der Browser es angehaengt hat.
        rahmen = pg.wait_for_selector("iframe").content_frame()
        rahmen.wait_for_load_state("networkidle")
        rahmen.wait_for_selector("[data-open]", timeout=15000)
        pg.wait_for_timeout(700)

        def hin(wahl: str, oben: int = 0):
            rahmen.evaluate(
                """([w, o]) => { const e = document.querySelector(w);
                   window.scrollTo({top: e.getBoundingClientRect().top
                   + scrollY - o, behavior: 'smooth'}); }""", [wahl, oben])

        pg.wait_for_timeout(1500)                    # der verschlossene Umschlag
        rahmen.eval_on_selector("[data-open]", "e => e.click()")
        pg.wait_for_timeout(2300)                    # er oeffnet sich
        pg.wait_for_timeout(1600)                    # Namen ueber dem Film
        hin(".countdown", 60)
        pg.wait_for_timeout(1600)
        hin("[data-galerie]", 230)                   # der Streifen wandert
        pg.wait_for_timeout(1700)
        hin("[aria-labelledby='t-ort']", 0)
        pg.wait_for_timeout(1600)
        hin("[aria-labelledby='t-rsvp']", 0)
        pg.wait_for_timeout(1000)
        rahmen.fill("#r-name", "Katharina Vogt")
        pg.wait_for_timeout(300)
        rahmen.check("input[name='zusage'][value='ja']")
        pg.wait_for_timeout(700)

        pfad = pg.video.path()
        kontext.close()
        b.close()

    ziel = ZIEL / "video.mp4"
    # Etsy nimmt MP4. H.264, ohne Ton — Etsy schaltet ihn ohnehin stumm, und
    # eine leere Tonspur waere nur Ballast.
    subprocess.run([FFMPEG, "-y", "-ss", "1.1", "-t", "13.4", "-i", str(pfad),
                    "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "20",
                    "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                    "-vf", f"scale={KANTE}:{KANTE}:flags=lanczos",
                    str(ziel)], check=True, capture_output=True)
    shutil.rmtree(roh, ignore_errors=True)

    # Kein ffprobe zur Hand, also die Laenge aus dem Kopf der Datei lesen.
    kopfzeile = subprocess.run([FFMPEG, "-i", str(ziel)],
                               capture_output=True, text=True).stderr
    treffer = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", kopfzeile)
    h, m, sek = (float(x) for x in treffer.groups()) if treffer else (0, 0, 0)
    dauer = h * 3600 + m * 60 + sek
    mb = ziel.stat().st_size / 1048576
    print(f"  {ziel.name}  {mb:.1f} MB  {dauer:.1f} s")
    # Etsy nimmt fuenf bis fuenfzehn Sekunden und hoechstens hundert Megabyte.
    if not 5 <= dauer <= 15:
        print(f"  ACHTUNG: {dauer:.1f} s liegt ausserhalb von 5 bis 15.")
        return 1
    if mb > 100:
        print("  ACHTUNG: ueber 100 MB.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
