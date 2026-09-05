#!/usr/bin/env python3
"""
Fährt einen echten Browser durch das Antwortformular.

Wird von test-ende-zu-ende.sh aufgerufen und gibt Zeilen der Form
schluessel=wert aus, die das Prüfskript auswertet.

    python3 browser.py senden|fehler
"""
import os
import sys

from playwright.sync_api import sync_playwright

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
WEB = os.environ.get("WEB", "8100")


def oeffnen(pg):
    """Umschlag aufmachen und zum Formular scrollen."""
    pg.goto(f"http://localhost:{WEB}/", wait_until="networkidle")
    pg.wait_for_timeout(500)
    pg.click("[data-open]")
    pg.wait_for_timeout(2400)
    pg.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    pg.wait_for_timeout(500)


def ausfuellen(pg):
    pg.fill("#r-name", "Theresa Baumgartner")
    pg.fill("#r-mail", "theresa@example.org")
    pg.check("input[name='zusage'][value='ja']")
    pg.wait_for_timeout(200)
    pg.fill("#r-anzahl", "3")
    pg.select_option("#r-essen", "vegan")
    pg.fill("#r-gruss", "Wir kommen sehr gern.")


def zustand(pg):
    return pg.evaluate("""() => {
        const q = document.querySelector('[data-quittung]');
        const k = document.querySelector('[data-senden]');
        return {
            sichtbar: !q.hidden,
            text: (q.textContent || '').trim(),
            fehler: q.classList.contains('quittung--fehler'),
            knopf: k.disabled ? 'gesperrt' : 'bereit',
            busy: k.dataset.busy,
            name: document.querySelector('#r-name').value,
            hinweis: !!document.querySelector('form[data-rsvp] .hinweis'),
            honig: !!document.querySelector('#r-web')
        };
    }""")


def main() -> int:
    was = sys.argv[1] if len(sys.argv) > 1 else "senden"
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        pg = b.new_page(viewport={"width": 402, "height": 874})
        fehler = []
        pg.on("pageerror", lambda e: fehler.append(str(e)))

        oeffnen(pg)
        print(f"hinweis={'ja' if zustand(pg)['hinweis'] else 'nein'}")
        print(f"honigtopf={'ja' if zustand(pg)['honig'] else 'nein'}")
        ausfuellen(pg)
        pg.click("[data-senden]")
        pg.wait_for_timeout(3000)

        z = zustand(pg)
        print(f"sichtbar={'ja' if z['sichtbar'] else 'nein'}")
        print(f"fehlerklasse={'ja' if z['fehler'] else 'nein'}")
        print(f"knopf={z['knopf']}")
        print(f"text={z['text'][:90]}")
        if was == "senden":
            print("quittung=danke" if "Danke" in z["text"] or "Thank" in z["text"]
                  else "quittung=?")
        else:
            print("name=erhalten" if z["name"] == "Theresa Baumgartner" else "name=weg")
        print(f"js-fehler={len(fehler)}")
        for f in fehler:
            print(f"  {f}")
        b.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
