#!/usr/bin/env python3
"""
Der Bilderlauf in der Galerie, im echten Browser.

Der Streifen rueckt von selbst weiter, damit ein Gast alle Fotos sieht, ohne
zu wischen. Daran haengen ein paar Regeln, die man beim naechsten Umbau
leicht versehentlich umdreht — darum stehen sie hier als Pruefungen:

  * er geht alle vier Fotos durch und faengt wieder vorne an
  * wer selbst wischt oder rollt, hat ab da das Sagen
  * ein Tipp aufs Foto ist kein Wischen: danach laeuft er weiter
  * Zeiger darauf und Tastaturfokus halten nur an
  * ausserhalb des Bildes, im Raster und bei reduzierter Bewegung: nichts

    cd themes/ambra && python3 -m http.server 8100 &
    python3 themes/pruefung/galerie.py

Gibt die Zahl der Fehlschlaege zurueck.
"""
import sys

from playwright.sync_api import sync_playwright

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
POS = "document.querySelector('[data-galerie]').scrollLeft"
gut = bad = 0

def pruef(name, ok, notiz=""):
    global gut, bad
    if ok: gut += 1; print(f"  ok    {name} {notiz}")
    else:  bad += 1; print(f"  FEHLT {name} {notiz}")

def oeffnen(pg):
    pg.goto("http://127.0.0.1:8100/", wait_until="networkidle")
    pg.evaluate("document.body.dataset.state='open'")
    pg.eval_on_selector("[data-galerie]", "e=>e.scrollIntoView({block:'center'})")
    pg.wait_for_timeout(700)

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME)
    pg = b.new_page(viewport={"width": 390, "height": 844}, has_touch=True)
    f = []; pg.on("pageerror", lambda e: f.append(str(e)))

    print("— Durchlauf —")
    oeffnen(pg)
    spur = [round(pg.evaluate(POS))]
    for _ in range(5):
        pg.wait_for_timeout(4200); spur.append(round(pg.evaluate(POS)))
    pruef("alle vier Fotos und zurueck", spur == [0,194,444,638,0,194], str(spur))

    print("— Der Gast uebernimmt —")
    oeffnen(pg); pg.wait_for_timeout(4400)
    k = pg.eval_on_selector("[data-galerie]", "e=>{const r=e.getBoundingClientRect();"
        "return {x:r.left+r.width/2, y:r.top+r.height/2};}")
    pg.mouse.move(k["x"], k["y"]); pg.mouse.down()
    for dx in (-25, -70, -120): pg.mouse.move(k["x"]+dx, k["y"]); pg.wait_for_timeout(40)
    pg.mouse.up(); pg.mouse.move(5, 5)
    a = pg.evaluate(POS); pg.wait_for_timeout(9000)
    pruef("nach dem Wischen still", abs(pg.evaluate(POS)-a) < 2, f"{a:.0f} → {pg.evaluate(POS):.0f}")

    oeffnen(pg)
    pg.mouse.move(k["x"], k["y"]); pg.mouse.wheel(60, 0); pg.mouse.move(5, 5)
    pg.wait_for_timeout(400); a = pg.evaluate(POS); pg.wait_for_timeout(9000)
    pruef("nach dem Rollrad still", abs(pg.evaluate(POS)-a) < 2)

    print("— Tippen ist nicht Wischen —")
    oeffnen(pg)
    pg.click("[data-galerie] li:first-child button"); pg.wait_for_timeout(300)
    a = pg.evaluate(POS); pg.wait_for_timeout(8600)
    pruef("hinter dem Lichtkasten still", pg.evaluate(POS) == a)
    pg.evaluate("document.querySelector('dialog[open]').close()")
    pg.mouse.move(5, 5); pg.wait_for_timeout(300)
    a = pg.evaluate(POS); pg.wait_for_timeout(9000)
    pruef("danach laeuft er weiter", pg.evaluate(POS) != a, f"{a:.0f} → {pg.evaluate(POS):.0f}")

    print("— Anhalten —")
    oeffnen(pg)
    pg.hover("[data-galerie] li:first-child button")
    a = pg.evaluate(POS); pg.wait_for_timeout(9000)
    pruef("Zeiger darauf haelt an", pg.evaluate(POS) == a)
    pg.mouse.move(5, 5); pg.wait_for_timeout(4500)
    pruef("Zeiger weg, laeuft weiter", pg.evaluate(POS) != a)

    oeffnen(pg)
    pg.eval_on_selector("[data-galerie] li:first-child button", "e=>e.focus()")
    pg.keyboard.press("Tab"); pg.wait_for_timeout(200)
    a = pg.evaluate(POS); pg.wait_for_timeout(9000)
    pruef("Tastaturfokus haelt an", pg.evaluate(POS) == a)

    print("— Ausserhalb des Bildes —")
    oeffnen(pg)
    pg.evaluate("window.scrollTo(0, 0)"); pg.wait_for_timeout(500)
    a = pg.evaluate(POS); pg.wait_for_timeout(9000)
    pruef("weggescrollt: keine Bewegung", pg.evaluate(POS) == a)
    pg.close()

    print("— Rechner und reduzierte Bewegung —")
    pg = b.new_page(viewport={"width": 1100, "height": 900})
    oeffnen(pg); a = pg.evaluate(POS); pg.wait_for_timeout(9000)
    pruef("Raster: untaetig", pg.evaluate(POS) == a == 0)
    pg.close()
    pg = b.new_page(viewport={"width": 390, "height": 844}, reduced_motion="reduce")
    oeffnen(pg); a = pg.evaluate(POS); pg.wait_for_timeout(9000)
    pruef("weniger Bewegung: aus", pg.evaluate(POS) == a == 0)
    pruef("keine Fehler", not f, str(f))
    b.close()
print(f"\n{gut} bestanden, {bad} fehlgeschlagen")
sys.exit(bad)
