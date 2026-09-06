#!/usr/bin/env python3
"""Nimmt die Uebersicht des laufenden RSVP-Dienstes auf. Aufruf aus liste.sh."""
import pathlib
import sys

from playwright.sync_api import sync_playwright

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
ZIEL = pathlib.Path(__file__).resolve().parent / "aufnahmen"

port, token = sys.argv[1], sys.argv[2]
ZIEL.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME)
    pg = b.new_page(viewport={"width": 1180, "height": 780}, device_scale_factor=2)
    pg.goto(f"http://127.0.0.1:{port}/uebersicht?kennung=marlene-anton",
            wait_until="networkidle")
    pg.fill("input[type=password]", token)
    pg.click("button")
    pg.wait_for_timeout(900)
    pg.screenshot(path=str(ZIEL / "12-liste.png"))
    print("  12-liste.png")
    b.close()
