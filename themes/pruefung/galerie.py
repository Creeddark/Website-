#!/usr/bin/env python3
"""
Der Bilderlauf in der Galerie, im echten Browser.

Der Streifen wischt von selbst nach links, damit ein Gast alle Fotos sieht,
ohne zu wischen. Damit das nie endet, steht jedes Foto zweimal da; nach genau
einer Runde springt der Streifen um diese Runde zurueck, und weil dort
dasselbe Bild steht, sieht man den Sprung nicht.

Daran haengen Regeln, die man beim naechsten Umbau leicht versehentlich
umdreht — darum stehen sie hier als Pruefungen:

  * er laeuft gleichmaessig nach links, ohne Halt
  * die Naht ist unsichtbar: das Bild dort ist Punkt fuer Punkt dasselbe
  * wer selbst wischt oder rollt, hat ab da das Sagen
  * ein Tipp aufs Foto ist kein Wischen: danach laeuft er weiter
  * Zeiger darauf und Tastaturfokus halten nur an
  * ausserhalb des Bildes, im Raster und bei reduzierter Bewegung: nichts
  * die Zweitfotos sind fuer das Auge da, nicht fuer Vorlesehilfe und Tabulator

    cd themes/ambra && python3 -m http.server 8100 &
    python3 themes/pruefung/galerie.py

Gibt die Zahl der Fehlschlaege zurueck.
"""
import hashlib
import sys

from playwright.sync_api import sync_playwright

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
WEB = "http://127.0.0.1:8100/"
POS = "document.querySelector('[data-galerie]').scrollLeft"

gut = bad = 0


def pruef(name, ok, notiz=""):
    global gut, bad
    if ok:
        gut += 1
        print(f"  ok    {name} {notiz}")
    else:
        bad += 1
        print(f"  FEHLT {name} {notiz}")


def oeffnen(pg):
    """Umschlag ueberspringen und die Galerie in die Mitte holen."""
    pg.goto(WEB, wait_until="networkidle")
    pg.evaluate("document.body.dataset.state='open'")
    pg.eval_on_selector("[data-galerie]", "e=>e.scrollIntoView({block:'center'})")
    pg.wait_for_timeout(700)


def steht(pg, sekunden=4.0):
    """Wahr, wenn sich der Streifen in dieser Zeit nicht bewegt."""
    a = pg.evaluate(POS)
    pg.wait_for_timeout(int(sekunden * 1000))
    return pg.evaluate(POS) == a


def lauf():
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        pg = b.new_page(viewport={"width": 390, "height": 844}, has_touch=True)
        fehler = []
        pg.on("pageerror", lambda e: fehler.append(str(e)))

        print("— Der Streifen wischt selbst —")
        oeffnen(pg)
        proben = []
        for _ in range(30):
            proben.append(pg.evaluate(POS))
            pg.wait_for_timeout(200)
        schritte = [proben[i + 1] - proben[i] for i in range(len(proben) - 1)]
        tempo = (proben[-1] - proben[0]) / (0.2 * (len(proben) - 1))
        pruef("laeuft nach links", all(s > 0 for s in schritte), f"{tempo:.0f} px/s")
        pruef("gleichmaessig", max(schritte) - min(schritte) <= 2,
              f"{min(schritte):.0f}…{max(schritte):.0f} px je 200ms")

        print("— Die Naht —")
        # Anhalten und rasten abschalten, damit exakte Stellen messbar sind.
        pg.eval_on_selector("[data-galerie]",
                            "e=>{e.dispatchEvent(new MouseEvent('mouseenter'));"
                            "e.style.scrollSnapType='none';}")
        pg.wait_for_timeout(300)
        masse = pg.eval_on_selector("[data-galerie]", """e => {
          const k = e.querySelectorAll('li'), n = k.length / 2;
          const rand = e.getBoundingClientRect().left;
          return {basis: k[0].getBoundingClientRect().left - rand + e.scrollLeft,
                  periode: k[n].getBoundingClientRect().left
                         - k[0].getBoundingClientRect().left,
                  weite: e.scrollWidth - e.clientWidth}; }""")
        basis, periode = masse["basis"], masse["periode"]
        pruef("eine Runde passt in den Bildlauf", masse["weite"] >= basis + periode,
              f"Runde {periode:.0f}px, Bildlauf {masse['weite']:.0f}px")

        streifen = pg.locator("[data-galerie]")
        # Die Naht selbst liegt bei basis: dort springt der Streifen hin. Die
        # weiteren Stellen sind Zugabe und muessen mitsamt ihrer Gegenstelle
        # in den Bildlauf passen — sonst prueft man eine Stelle, die der
        # Browser abschneidet und die der Streifen nie erreicht.
        weit = min(1.0, (masse["weite"] - basis - periode) / periode)
        stellen = [0.0] + [a for a in (0.14, 0.39, 0.72, 0.95) if a <= weit]
        for anteil in stellen:
            x = basis + periode * anteil
            bilder = []
            for stelle in (x, x + periode):
                pg.eval_on_selector("[data-galerie]", "(e,v)=>e.scrollLeft=v", stelle)
                pg.wait_for_timeout(220)
                bilder.append(hashlib.sha256(streifen.screenshot()).hexdigest()[:16])
            pruef(f"Naht bei {x:>6.0f} und {x + periode:>6.0f} gleich",
                  bilder[0] == bilder[1], bilder[0])

        print("— Der Gast uebernimmt —")
        oeffnen(pg)
        pg.wait_for_timeout(2000)
        k = pg.eval_on_selector("[data-galerie]", "e=>{const r=e.getBoundingClientRect();"
                                "return {x:r.left+r.width/2, y:r.top+r.height/2};}")
        pg.mouse.move(k["x"], k["y"])
        pg.mouse.down()
        for dx in (-25, -70, -120):
            pg.mouse.move(k["x"] + dx, k["y"])
            pg.wait_for_timeout(40)
        pg.mouse.up()
        pg.mouse.move(5, 5)
        pg.wait_for_timeout(600)
        pruef("nach dem Wischen still", steht(pg, 6))
        pruef("und das Rasten ist zurueck",
              pg.eval_on_selector("[data-galerie]",
                                  "e=>getComputedStyle(e).scrollSnapType") != "none")

        oeffnen(pg)
        pg.mouse.move(k["x"], k["y"])
        pg.mouse.wheel(60, 0)
        pg.mouse.move(5, 5)
        pg.wait_for_timeout(600)
        pruef("nach dem Rollrad still", steht(pg, 6))

        print("— Tippen ist nicht Wischen —")
        oeffnen(pg)
        pg.click("[data-galerie] li:first-child button")
        pg.wait_for_timeout(300)
        pruef("hinter dem Lichtkasten still", steht(pg, 5))
        pg.evaluate("document.querySelector('dialog[open]').close()")
        pg.mouse.move(5, 5)
        pg.wait_for_timeout(400)
        pruef("danach laeuft er weiter", not steht(pg, 4))

        print("— Anhalten —")
        oeffnen(pg)
        pg.hover("[data-galerie] li:first-child button")
        pruef("Zeiger darauf haelt an", steht(pg, 5))
        pg.mouse.move(5, 5)
        pg.wait_for_timeout(300)
        pruef("Zeiger weg, laeuft weiter", not steht(pg, 4))

        oeffnen(pg)
        pg.eval_on_selector("[data-galerie] li:first-child button", "e=>e.focus()")
        pg.keyboard.press("Tab")
        pg.wait_for_timeout(200)
        pruef("Tastaturfokus haelt an", steht(pg, 5))

        print("— Die Zweitfotos —")
        oeffnen(pg)
        pruef("jedes Foto zweimal",
              pg.eval_on_selector_all("[data-galerie] li", "l=>l.length") ==
              2 * pg.eval_on_selector_all("[data-galerie] li:not(.kopie)", "l=>l.length"))
        pruef("Kopien nicht vorlesen",
              pg.eval_on_selector_all("[data-galerie] li.kopie",
                                      "l=>l.every(e=>e.getAttribute('aria-hidden')==='true')"))
        pruef("Kopien nicht im Tabulator",
              pg.eval_on_selector_all("[data-galerie] li.kopie button",
                                      "l=>l.every(e=>e.tabIndex===-1)"))

        print("— Ausserhalb des Bildes —")
        oeffnen(pg)
        pg.evaluate("window.scrollTo(0, 0)")
        pg.wait_for_timeout(600)
        pruef("weggescrollt: keine Bewegung", steht(pg, 5))
        pg.close()

        print("— Rechner und reduzierte Bewegung —")
        pg = b.new_page(viewport={"width": 1100, "height": 900})
        oeffnen(pg)
        pruef("Raster: untaetig", steht(pg, 5) and pg.evaluate(POS) == 0)
        pruef("Raster: keine Zweitfotos sichtbar",
              pg.eval_on_selector_all("[data-galerie] li.kopie",
                                      "l=>l.every(e=>e.offsetParent===null)"))
        pg.close()

        pg = b.new_page(viewport={"width": 390, "height": 844}, reduced_motion="reduce")
        oeffnen(pg)
        pruef("weniger Bewegung: aus", steht(pg, 5) and pg.evaluate(POS) == 0)
        pruef("weniger Bewegung: gar keine Zweitfotos",
              pg.eval_on_selector_all("[data-galerie] li", "l=>l.length") == 4)
        pruef("keine Fehler", not fehler, str(fehler))
        b.close()


lauf()
print(f"\n{gut} bestanden, {bad} fehlgeschlagen")
sys.exit(bad)
