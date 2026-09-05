#!/usr/bin/env python3
"""
AMBRA — Klangteppich.

Erzeugt die Hintergrundmusik der Einladung. Selbst synthetisiert, damit sie
lizenzfrei ist: fuer eine verkaufte Einladung braucht Hintergrundmusik eine
Lizenz, und eine selbst erzeugte Tonspur hat keine. Wer etwas Schoeneres
will, ersetzt die Datei; siehe themes/README.md.

Ein langsames Arpeggio in D-Dur, jeder Ton klingt ueber Sekunden aus, darunter
ein leiser Bordun. Die Schleife ist nahtlos: der Nachklang der letzten Sekunden
wird an den Anfang zurueckaddiert, sodass es an der Nahtstelle nichts zu hoeren
gibt.

    python3 build/art/ambra_ton.py
"""
from __future__ import annotations

import array
import math
import pathlib
import subprocess
import wave

RATE = 44100
LOOP = 24.0          # Sekunden bis zur Wiederholung
TAIL = 6.0           # Nachklang, der in den Anfang zurueckgefaltet wird

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
OUT = ROOT / "themes" / "ambra" / "assets" / "audio"
OUT.mkdir(parents=True, exist_ok=True)

FFMPEG = ("/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/"
          "ffmpeg-linux-x86_64-v7.0.2")


def ton(hz: float) -> list[float]:
    """Ein gezupfter Ton: Grundton und drei Teiltoene, exponentiell abklingend.
    Die hoeheren Teiltoene verklingen schneller, so klingt es nach Saite und
    nicht nach Sinusgenerator."""
    laenge = int(RATE * 5.2)
    teile = ((1, 1.00, 3.1), (2, 0.32, 2.1), (3, 0.15, 1.5), (5, 0.06, 1.1))
    anschlag = int(RATE * 0.006)
    aus = [0.0] * laenge
    for n, amp, halb in teile:
        w = 2 * math.pi * hz * n / RATE
        d = math.log(2) / (halb * RATE)
        for i in range(laenge):
            aus[i] += amp * math.exp(-d * i) * math.sin(w * i)
    for i in range(anschlag):                      # weicher Einsatz, kein Knacks
        aus[i] *= i / anschlag
    return aus


def main() -> None:
    n_loop = int(RATE * LOOP)
    n_ges = int(RATE * (LOOP + TAIL))
    misch = [0.0] * n_ges

    # D3 A3 D4 Fis4 A4 D5 — ein aufsteigendes Arpeggio, das zweimal durch die
    # Schleife laeuft und dabei die Reihenfolge leicht aendert.
    stufen = {"D3": 146.83, "A3": 220.00, "D4": 293.66,
              "Fis4": 369.99, "A4": 440.00, "D5": 587.33}
    vorrat = {k: ton(v) for k, v in stufen.items()}

    folge = ["D4", "A3", "Fis4", "D5", "A4", "D4", "A3", "Fis4",
             "A4", "D5", "Fis4", "D4"]
    for i, name in enumerate(folge):
        start = int(RATE * (i * LOOP / len(folge)))
        lautstaerke = 0.30 if name in ("D5", "A4") else 0.22
        quelle = vorrat[name]
        for j, s in enumerate(quelle):
            if start + j < n_ges:
                misch[start + j] += s * lautstaerke

    # Bordun: zwei tiefe Sinus, ganz leise, mit langsamer Schwebung.
    for hz, amp in ((73.42, 0.055), (110.00, 0.035)):
        w = 2 * math.pi * hz / RATE
        for i in range(n_ges):
            atem = 0.75 + 0.25 * math.sin(2 * math.pi * i / (RATE * 11.0))
            misch[i] += amp * atem * math.sin(w * i)

    # Nahtlos: was nach dem Schleifenende noch klingt, kommt vorn wieder herein.
    for i in range(n_ges - n_loop):
        misch[i] += misch[n_loop + i]
    misch = misch[:n_loop]

    spitze = max(abs(s) for s in misch) or 1.0
    faktor = 0.82 / spitze
    roh = array.array("h", (int(max(-1.0, min(1.0, s * faktor)) * 32767) for s in misch))

    wav = OUT / "_ambra.wav"
    with wave.open(str(wav), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(RATE)
        f.writeframes(roh.tobytes())

    m4a = OUT / "ambra.m4a"
    subprocess.run([FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
                    "-i", str(wav), "-c:a", "aac", "-b:a", "64k", str(m4a)],
                   check=True)
    wav.unlink()
    print(f"  ambra.m4a  {m4a.stat().st_size // 1024} KB  ({LOOP:.0f} s, nahtlos)")


if __name__ == "__main__":
    main()
