#!/usr/bin/env python3
"""
Telefonaufnahmen aus der Einladung, als Material fuer die Produktbilder.

Nimmt die Einladung im echten Browser auf, an den Stellen, die etwas
verkaufen: der verschlossene Umschlag, die Namen ueber dem Film, der
Countdown, die Galerie, der Ort, das Antwortformular. Dazu die Liste, die
nur das Paar sieht.

    cd themes/ambra && python3 -m http.server 8100 &
    python3 build/etsy/aufnahmen.py

Legt PNG-Dateien in build/etsy/aufnahmen/ ab. Dreifache Aufloesung, damit
sie in einem 2000er Produktbild noch scharf sind.
"""
import pathlib
import sys

from playwright.sync_api import sync_playwright

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
WEB = "http://127.0.0.1:8100/"
HIER = pathlib.Path(__file__).resolve().parent
ZIEL = HIER / "aufnahmen"


def telefon(b):
    return b.new_page(viewport={"width": 390, "height": 844},
                      device_scale_factor=3, has_touch=True)


def zu(pg, wahl, oben=0):
    """Zu einem Abschnitt scrollen und die Bewegung zur Ruhe kommen lassen."""
    pg.eval_on_selector(wahl, "(e,o)=>window.scrollTo(0, e.getBoundingClientRect().top"
                              " + scrollY - o)", oben)
    pg.wait_for_timeout(1400)


def ablegen(pg, name):
    pg.screenshot(path=str(ZIEL / f"{name}.png"))
    print(f"  {name}.png")


def main():
    ZIEL.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)

        # --- Der verschlossene Umschlag -------------------------------------
        pg = telefon(b)
        pg.goto(WEB, wait_until="networkidle")
        pg.wait_for_timeout(1200)
        ablegen(pg, "01-umschlag")

        # Waehrend er sich oeffnet: die Lasche steht schraeg im Raum.
        pg.click("[data-open]")
        pg.wait_for_timeout(760)
        ablegen(pg, "02-oeffnet")

        pg.wait_for_timeout(2000)
        # Der Film braucht einen Moment, bis er wirklich laeuft.
        pg.wait_for_timeout(2500)
        ablegen(pg, "03-hero")

        zu(pg, ".countdown", 40)
        ablegen(pg, "04-countdown")

        zu(pg, "[aria-labelledby='t-weg']", 0)
        pg.wait_for_timeout(900)
        ablegen(pg, "05-weg")

        # Der Streifen soll das Bild fuellen, nicht oben kleben.
        zu(pg, "[data-galerie]", 230)
        pg.mouse.move(5, 5)
        pg.wait_for_timeout(1200)
        ablegen(pg, "06-galerie")

        zu(pg, "[aria-labelledby='t-tag']", 0)
        ablegen(pg, "07-ablauf")

        zu(pg, "[aria-labelledby='t-ort']", 0)
        ablegen(pg, "08-ort")

        # Das Formular halb ausgefuellt: ein leeres Formular verkauft nichts.
        zu(pg, "[aria-labelledby='t-rsvp']", 0)
        pg.fill("#r-name", "Katharina Vogt")
        pg.fill("#r-mail", "katharina.vogt@example.org")
        pg.check("input[name='zusage'][value='ja']")
        pg.wait_for_timeout(300)
        pg.fill("#r-anzahl", "2")
        pg.select_option("#r-essen", "vegetarisch")
        pg.evaluate("document.activeElement.blur()")
        pg.wait_for_timeout(500)
        ablegen(pg, "09-rsvp")

        # Der Lichtkasten: ein Foto gross.
        zu(pg, "[data-galerie]", 120)
        pg.wait_for_timeout(400)
        pg.eval_on_selector("[data-galerie] li:nth-child(3) button", "e=>e.click()")
        pg.wait_for_timeout(900)
        ablegen(pg, "10-lupe")
        pg.close()

        # --- Englisch: derselbe Hero, andere Sprache ------------------------
        pg = telefon(b)
        pg.goto(WEB, wait_until="networkidle")
        pg.evaluate("document.body.dataset.state='open'")
        pg.wait_for_timeout(600)
        pg.eval_on_selector("[data-lang='en']", "e=>e.click()")
        pg.wait_for_timeout(600)
        zu(pg, "[aria-labelledby='t-tag']", 0)
        ablegen(pg, "11-englisch")
        pg.close()

        b.close()
    print(f"\nLiegt in {ZIEL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
