/* =========================================================================
   AMBRA — Hochzeitseinladung
   Alles läuft im Browser des Gastes. Es wird nichts gesendet, nichts
   gespeichert und nichts nachgeladen. Ohne JavaScript bleibt die Einladung
   vollständig lesbar; es entfällt nur der Umschlag.
   ========================================================================= */
(function () {
  "use strict";

  var body = document.body;
  var sanft = window.matchMedia("(prefers-reduced-motion: reduce)");

  var $  = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ------------------------------------------------------------ Umschlag -- */
  /* Der Umschlag steht im HTML auf hidden. Erst hier wird er sichtbar, damit
     ohne JavaScript niemand vor einer Tür steht, die sich nicht öffnen lässt. */
  (function umschlag() {
    var veil = $("[data-veil]");
    var knopf = $("[data-open]");
    if (!veil || !knopf) { body.dataset.state = "open"; return; }

    veil.hidden = false;
    window.scrollTo(0, 0);

    var offen = false;
    function oeffnen() {
      if (offen) return;
      offen = true;
      body.dataset.state = "opening";
      var dauer = sanft.matches ? 260 : 1950;
      window.setTimeout(function () {
        body.dataset.state = "open";
        // Der Fokus muss aus dem verschwundenen Umschlag heraus, sonst steht
        // er auf einem Element, das es nicht mehr gibt.
        var m = $("#einladung");
        if (m) m.focus({ preventScroll: true });
      }, dauer);
    }

    knopf.addEventListener("click", oeffnen);
    // Wer zu scrollen versucht, will hinein. Das ist die häufigste Geste.
    veil.addEventListener("wheel", oeffnen, { passive: true });
    veil.addEventListener("touchmove", oeffnen, { passive: true });

    window.setTimeout(function () { knopf.focus({ preventScroll: true }); }, 400);
  })();

  /* ------------------------------------------------------------ Bewegung -- */
  /* Ein Beobachter für alles, was beim Lesen hereinkommt. */
  (function reveal() {
    var ziele = $$(".rise, [data-spur]");
    if (!("IntersectionObserver" in window)) {
      ziele.forEach(function (el) { el.classList.add("is-in"); });
      return;
    }
    var beo = new IntersectionObserver(function (eintraege) {
      eintraege.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add("is-in");
        beo.unobserve(e.target);          // einmal ist genug
      });
    }, { rootMargin: "0px 0px -12% 0px", threshold: 0.08 });
    ziele.forEach(function (el) { beo.observe(el); });
  })();

  /* Ein Beobachter fuer den Scrollzustand: der Hinweis nach unten, die Farbe
     der Bedienleiste und ihr Zurueckweichen haengen alle daran.

     Die Leiste liegt fest oben rechts. Welcher Abschnitt gerade dahinter
     liegt, wird direkt gemessen — ein IntersectionObserver mit einem so
     schmalen Band braucht Pixelwerte, die sich bei jeder Drehung des Geraets
     aendern, und das ist mehr Aufwand als die Messung selbst. */
  (function scrollzustand() {
    var abschnitte = $$("[data-grund]");
    var letzteY = window.scrollY;
    var wartet = false;
    var BAND = 58;                     // Unterkante der Leiste

    function messen() {
      wartet = false;
      var y = window.scrollY;

      body.classList.toggle("is-scrolled", y > 40);

      // Nach unten weicht die Leiste zurueck, nach oben kommt sie wieder.
      var runter = y > letzteY + 4;
      var rauf = y < letzteY - 4;
      if (runter && y > 240) body.classList.add("chrome-weg");
      else if (rauf || y < 120) body.classList.remove("chrome-weg");
      if (runter || rauf) letzteY = y;

      for (var i = 0; i < abschnitte.length; i++) {
        var r = abschnitte[i].getBoundingClientRect();
        if (r.top <= BAND && r.bottom > BAND) {
          body.classList.toggle("chrome-hell", abschnitte[i].dataset.grund === "hell");
          break;
        }
      }
    }

    window.addEventListener("scroll", function () {
      if (wartet) return;
      wartet = true;
      window.requestAnimationFrame(messen);
    }, { passive: true });
    messen();
  })();

  /* ----------------------------------------------------------- Countdown -- */
  (function countdown() {
    var uhr = $("[data-uhr]");
    if (!uhr) return;

    var ziel = new Date(uhr.dataset.ziel).getTime();
    var vorbei = $("[data-uhr-vorbei]");
    var felder = {
      t: $("[data-uhr-t]", uhr), h: $("[data-uhr-h]", uhr),
      m: $("[data-uhr-m]", uhr), s: $("[data-uhr-s]", uhr)
    };

    function setz(el, wert) {
      var s = String(wert).padStart(2, "0");
      if (el.textContent === s) return;
      el.textContent = s;
      if (sanft.matches) return;
      el.classList.add("tick");
      window.setTimeout(function () { el.classList.remove("tick"); }, 120);
    }

    function tick() {
      var rest = ziel - Date.now();
      if (rest <= 0) {
        uhr.hidden = true;
        if (vorbei) vorbei.hidden = false;
        window.clearInterval(id);
        return;
      }
      var s = Math.floor(rest / 1000);
      setz(felder.t, Math.floor(s / 86400));
      setz(felder.h, Math.floor(s / 3600) % 24);
      setz(felder.m, Math.floor(s / 60) % 60);
      setz(felder.s, s % 60);
    }

    tick();
    var id = window.setInterval(tick, 1000);
  })();

  /* ------------------------------------------------------------- Galerie -- */
  /* ------------------------------------------------------------ Bilderlauf -- */
  /* Auf dem Telefon ist die Galerie ein Wischstreifen: ein Foto steht im
     Bild, drei liegen daneben. Wer nicht wischt, sieht sie nie — und die
     meisten wischen nicht. Also wischt der Streifen selbst, langsam und
     ohne Unterlass, von rechts nach links.

     Damit das nie endet, steht jedes Foto zweimal da. Sobald der Streifen
     genau eine Runde weit gelaufen ist, springt er um diese eine Runde
     zurueck — und weil an dieser Stelle dasselbe Bild steht wie am Anfang,
     sieht man den Sprung nicht. Ein Band ohne Anfang und Ende, aus vier
     Fotos.

     Am Rechner wird aus dem Streifen ein Raster mit allen vier Fotos. Dort
     verschwinden die Zweitfotos per CSS, es gibt nichts zu zeigen, und es
     passiert nichts. */
  (function bilderlauf() {
    var streifen = $("[data-galerie]");
    if (!streifen || sanft.matches) return;

    var urbild = $$("li", streifen);
    var anzahl = urbild.length;
    if (anzahl < 2) return;

    /* Die Zweitfotos sind fuer das Auge da, nicht fuer den Leser: eine
       Vorlesehilfe soll die Galerie nicht doppelt ansagen, und die
       Tabulatortaste soll nicht zweimal durch dieselben vier Bilder gehen. */
    urbild.forEach(function (li) {
      var kopie = li.cloneNode(true);
      kopie.classList.add("kopie");
      kopie.setAttribute("aria-hidden", "true");
      $$("button", kopie).forEach(function (b) { b.tabIndex = -1; });
      streifen.appendChild(kopie);
    });
    var kacheln = $$("li", streifen);

    var TEMPO = 22;                   // Bildpunkte je Sekunde
    var ort = 0, periode = 0, basis = 0, bild = null, letzte = 0, sichtbar = false;
    var abgegeben = false;            // der Gast wischt selbst: dann fuer immer
    /* Drei Gruende zu warten, unabhaengig voneinander. Ein einzelner Schalter
       wuerde sich gegenseitig ausknipsen: der Finger geht hoch, und der
       Streifen liefe unter dem Mauszeiger weiter, der noch daraufliegt. */
    var zeigt = false, tastatur = false, finger = false;
    function wartet() { return zeigt || tastatur || finger; }

    /* Eine Runde ist der Abstand von einem Foto zu seinem Zweitfoto. Der
       haengt an der Fensterbreite, also wird er neu gemessen, wenn sich die
       aendert — und nicht in jedem Einzelbild, das kostet jedes Mal ein
       neues Layout.

       Der Rueckstellpunkt liegt nicht bei null, sondern an der Kante des
       ersten Fotos. Vor dem ersten liegt die Polsterung des Streifens, vor
       dem fuenften liegt das vierte Foto — bei null saehe die Naht also um
       genau diese Polsterung anders aus, und der Sprung waere sichtbar. Ab
       der Kante des ersten Fotos ist beides gleich. */
    function messen() {
      var rand = streifen.getBoundingClientRect().left;
      basis = kacheln[0].getBoundingClientRect().left - rand + streifen.scrollLeft;
      periode = kacheln[anzahl].getBoundingClientRect().left
              - kacheln[0].getBoundingClientRect().left;
      var weite = streifen.scrollWidth - streifen.clientWidth;
      // Passt keine ganze Runde in den Bildlauf, waere der Sprung sichtbar.
      if (periode < 8 || weite < basis + periode) periode = 0;
      if (periode && ort >= basis + periode) ort = basis + (ort - basis) % periode;
    }

    /* Waehrend der Streifen von selbst laeuft, darf nichts einrasten: das
       Rasten zoege ihn bei jedem Einzelbild auf das naechste Foto zurueck.
       Sobald der Gast den Finger aufsetzt, ist es wieder da, damit sein
       Wisch sauber stehen bleibt. */
    var frei = false;
    function rasten(aus) {
      if (aus === frei) return;
      frei = aus;
      streifen.classList.toggle("laeuft", aus);
    }

    function schritt(jetzt) {
      bild = window.requestAnimationFrame(schritt);
      var dt = letzte ? Math.min((jetzt - letzte) / 1000, 0.1) : 0;
      letzte = jetzt;

      // Hinter dem Lichtkasten weiterzulaufen hiesse: der Gast schliesst ihn
      // und findet den Streifen woanders, als er ihn verlassen hat.
      if (wartet() || !periode || $("dialog[open]")) { rasten(false); return; }

      rasten(true);
      ort += TEMPO * dt;
      if (ort >= basis + periode) ort -= periode;   // die unsichtbare Naht
      streifen.scrollLeft = ort;
    }

    function starten() {
      if (bild || abgegeben) return;
      messen();
      // Passt keine ganze Runde hinein — zwei Fotos auf einem breiten Schirm —
      // dann gibt es nichts zu wischen und auch keinen Takt dafuer.
      if (!periode) return;
      ort = streifen.scrollLeft;
      letzte = 0;
      bild = window.requestAnimationFrame(schritt);
    }
    function stoppen() {
      if (bild) window.cancelAnimationFrame(bild);
      bild = null;
      rasten(false);
    }

    /* Sobald der Gast selbst wischt, ist er am Zug und bleibt es. Ein
       Streifen, der gegen den Daumen zurueckzieht, ist schlimmer als einer,
       der stillsteht. */
    function abgeben() {
      abgegeben = true;
      stoppen();
    }

    streifen.addEventListener("mouseenter", function () { zeigt = true; });
    streifen.addEventListener("mouseleave", function () { zeigt = false; });

    /* Nur der Fokus von der Tastatur haelt an: wer sich durchtabbt, soll
       nicht verlieren, wo er gerade steht. Beim Tippen setzt der Browser den
       Fokus ebenfalls auf den Knopf — der Streifen bliebe danach fuer immer
       stehen, obwohl der Gast nur ein Foto gross sehen wollte. Genau diesen
       Unterschied kennt :focus-visible. */
    function tastaturfokus() {
      var a = document.activeElement;
      try { return !!(a && a.matches && a.matches(":focus-visible")); }
      catch (e) { return true; }        // kennt der Browser nicht: anhalten
    }
    streifen.addEventListener("focusin", function () {
      tastatur = tastaturfokus();
    });
    streifen.addEventListener("focusout", function () { tastatur = false; });

    /* Tippen ist nicht Wischen. Ein Tipp oeffnet ein Foto gross und heisst
       nicht, dass der Gast von nun an selbst blaettern will — erst der
       gezogene Finger heisst das. Darum zaehlt nicht das Aufsetzen, sondern
       der zurueckgelegte Weg. */
    var aufgesetzt = null;
    streifen.addEventListener("pointerdown", function (e) {
      aufgesetzt = e.clientX;
      finger = true;
      rasten(false);                   // ab jetzt soll sein Wisch einrasten
    }, { passive: true });
    streifen.addEventListener("pointermove", function (e) {
      if (aufgesetzt !== null && Math.abs(e.clientX - aufgesetzt) > 10) abgeben();
    }, { passive: true });
    ["pointerup", "pointercancel"].forEach(function (art) {
      streifen.addEventListener(art, function () {
        aufgesetzt = null;
        finger = false;
      }, { passive: true });
    });
    // Am Rechner mit Rollrad oder Trackpad gibt es kein Ziehen — hier ist
    // schon die erste Bewegung eindeutig.
    streifen.addEventListener("wheel", abgeben, { passive: true });

    var neu_messen = null;
    window.addEventListener("resize", function () {
      window.clearTimeout(neu_messen);
      neu_messen = window.setTimeout(messen, 200);
    });

    /* Nur laufen, solange jemand hinsieht. Ein Einzelbild-Takt fuer eine
       Galerie zwei Bildschirme weiter oben ist verschenkte Rechenzeit. */
    if (!("IntersectionObserver" in window)) return;
    new IntersectionObserver(function (eintraege) {
      sichtbar = eintraege[0].isIntersecting;
      if (sichtbar) starten(); else stoppen();
    }, { threshold: 0.3 }).observe(streifen);
  })();

  (function galerie() {
    var lupe = $("[data-lupe]");
    var bild = $("[data-lupe-bild]");
    if (!lupe || !bild || typeof lupe.showModal !== "function") return;

    $$("[data-galerie] button").forEach(function (b) {
      b.addEventListener("click", function () {
        var q = $("img", b);
        bild.src = q.src;
        bild.alt = q.alt;
        lupe.showModal();
      });
    });

    // Klick auf den Hintergrund schließt. Der Dialog selbst füllt die Fläche,
    // also wird geprüft, ob der Klick außerhalb des Bildes lag.
    lupe.addEventListener("click", function (e) {
      if (e.target === lupe) lupe.close();
    });
  })();

  /* ------------------------------------------------------------- Kalender -- */
  /* Die Angaben stehen am Knopf, nicht hier. Stuenden sie hier, traegt das
     zweite Paar die Hochzeit des ersten in seinen Kalender ein. */
  (function kalender() {
    var knopf = $("[data-ics]");
    if (!knopf || !knopf.dataset.icsStart) return;

    /* In einer ICS-Datei sind Komma, Semikolon und Backslash Trennzeichen.
       Eine Adresse mit Komma zerlegt sonst den Eintrag. */
    function ics_text(t) {
      return String(t || "")
        .replace(/\\/g, "\\\\")
        .replace(/;/g, "\;")
        .replace(/,/g, "\\,")
        .replace(/\r?\n/g, "\\n");
    }

    /* Zeilen ueber 75 Oktett muessen umbrochen werden, sonst weisen strenge
       Kalenderprogramme die Datei zurueck. */
    function falten(zeile) {
      if (zeile.length <= 73) return zeile;
      var aus = zeile.slice(0, 73), rest = zeile.slice(73);
      while (rest.length) { aus += "\r\n " + rest.slice(0, 72); rest = rest.slice(72); }
      return aus;
    }

    knopf.addEventListener("click", function () {
      var d = knopf.dataset;
      var zeilen = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//AMBRA//Einladung//DE",
        "CALSCALE:GREGORIAN",
        "BEGIN:VEVENT",
        "UID:" + (d.icsKennung || "ambra") + "@einladung.invalid",
        "DTSTAMP:" + stempel(new Date()),
        "DTSTART:" + d.icsStart,
        "DTEND:" + d.icsEnde,
        "SUMMARY:" + ics_text(d.icsTitel),
        "LOCATION:" + ics_text(d.icsOrt),
        "DESCRIPTION:" + ics_text(d.icsText),
        "END:VEVENT",
        "END:VCALENDAR"
      ].map(falten).join("\r\n") + "\r\n";

      var url = URL.createObjectURL(new Blob([zeilen], { type: "text/calendar;charset=utf-8" }));
      var a = document.createElement("a");
      a.href = url;
      a.download = d.icsDatei || "einladung.ics";
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
    });

    function stempel(d) {
      return d.toISOString().replace(/[-:]/g, "").replace(/\.\d+/, "");
    }
  })();

  /* ------------------------------------------------------------- Formular -- */
  /* Ohne data-endpunkt bleibt die Antwort im Browser — so verhaelt sich die
     oeffentliche Vorschau. Mit Endpunkt geht sie an den RSVP-Dienst, und dann
     muss jeder Fehlerfall bedacht sein: kein Netz, langsames Netz, Server
     kaputt, zu viele Versuche. Ein Formular, das im Fehlerfall einfach nichts
     tut, kostet eine Zusage. */
  (function rsvp() {
    var form = $("[data-rsvp]");
    if (!form) return;

    var knopf = $("[data-senden]", form);
    var knopfText = $(".senden__text", knopf);
    var quittung = $("[data-quittung]", form);
    var nurZusage = $$("[data-nur-zusage]", form);

    var endpunkt = (form.dataset.endpunkt || "").replace(/\/+$/, "");
    var kennung = form.dataset.kennung || "";
    var gezeigt = Date.now();      // Grundlage der Zeitbremse gegen Roboter
    var laeuft = false;

    var texte = {
      de: {
        name: "Bitte tragt euren Namen ein.",
        mail: "Diese E-Mail-Adresse sieht nicht vollständig aus.",
        zusage: "Bitte wählt aus, ob ihr dabei seid.",
        ja: "Danke, {name}. Wir haben euch eingeplant.",
        nein: "Schade, {name}. Wir denken an euch.",
        demo: " In dieser Vorschau bleibt die Antwort in eurem Browser.",
        offline: "Ihr seid gerade offline. Die Antwort wurde noch nicht gesendet.",
        netz: "Das hat nicht geklappt. Bitte versucht es gleich noch einmal.",
        server: "Bei uns ist etwas schiefgelaufen. Bitte versucht es später noch einmal.",
        zuoft: "Das waren zu viele Versuche. Bitte wartet ein paar Minuten.",
        pruefen: "Bitte prüft eure Angaben.",
        nochmal: "Nochmal senden"
      },
      en: {
        name: "Please enter your name.",
        mail: "That email address looks incomplete.",
        zusage: "Please tell us whether you can come.",
        ja: "Thank you, {name}. We have you down.",
        nein: "We will miss you, {name}.",
        demo: " In this preview the reply stays in your browser.",
        offline: "You are offline. Your reply has not been sent yet.",
        netz: "That did not go through. Please try again in a moment.",
        server: "Something went wrong on our side. Please try again later.",
        zuoft: "That was too many attempts. Please wait a few minutes.",
        pruefen: "Please check your details.",
        nochmal: "Send again"
      }
    };
    function t(k) {
      return (texte[document.documentElement.lang] || texte.de)[k];
    }

    /* Zusatzfelder erscheinen nur bei einer Zusage. */
    $$('input[name="zusage"]', form).forEach(function (r) {
      r.addEventListener("change", function () {
        nurZusage.forEach(function (f) { f.hidden = r.value !== "ja"; });
      });
    });

    function pruefe(feld) {
      var id = feld.name;
      var meldung = "";
      if (id === "name" && !feld.value.trim()) meldung = t("name");
      if (id === "mail" && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(feld.value.trim())) meldung = t("mail");
      zeige(id, feld, meldung);
      return !meldung;
    }

    function zeige(id, feld, meldung) {
      var p = $("#e-" + id, form);
      if (p) p.textContent = meldung;
      if (feld) feld.setAttribute("aria-invalid", meldung ? "true" : "false");
    }

    /* Geprüft wird beim Verlassen des Feldes, nicht bei jedem Tastendruck.
       Wer noch tippt, hat noch nicht Unrecht. */
    ["name", "mail"].forEach(function (n) {
      var f = form.elements[n];
      if (f) f.addEventListener("blur", function () { pruefe(f); });
    });

    function quittieren(text, istFehler) {
      quittung.textContent = text;
      quittung.classList.toggle("quittung--fehler", !!istFehler);
      quittung.hidden = false;
      quittung.focus();
    }

    function fertig(wahl) {
      laeuft = false;
      knopf.dataset.busy = "false";
      knopf.disabled = true;
      var name = (form.elements.name.value || "").trim().split(" ")[0];
      quittieren(t(wahl.value === "ja" ? "ja" : "nein").replace("{name}", name)
                 + (endpunkt ? "" : t("demo")), false);
    }

    /* Scheitern heißt: der Knopf kommt zurück. Die Eingaben bleiben stehen,
       niemand tippt seine Antwort ein zweites Mal ein. */
    function scheitern(meldung) {
      laeuft = false;
      knopf.dataset.busy = "false";
      knopf.disabled = false;
      if (knopfText) knopfText.textContent = t("nochmal");
      quittieren(meldung, true);
    }

    function senden(wahl) {
      var daten = {
        kennung: kennung,
        name: form.elements.name.value.trim(),
        mail: form.elements.mail.value.trim(),
        zusage: wahl.value,
        anzahl: Number(form.elements.anzahl && form.elements.anzahl.value) || 1,
        essen: (form.elements.essen && form.elements.essen.value) || "alles",
        gruss: (form.elements.gruss && form.elements.gruss.value.trim()) || "",
        hp: (form.elements.web && form.elements.web.value) || "",
        dauer: Date.now() - gezeigt
      };

      // Ohne Frist wartet ein Telefon mit schlechtem Empfang ewig auf einer
      // Anzeige, die sich nicht mehr rührt.
      var opt = {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(daten)
      };
      if (window.AbortSignal && AbortSignal.timeout) opt.signal = AbortSignal.timeout(12000);

      window.fetch(endpunkt + "/rsvp", opt).then(function (a) {
        if (a.ok) { fertig(wahl); return; }
        if (a.status === 429) { scheitern(t("zuoft")); return; }
        if (a.status === 422) { scheitern(t("pruefen")); return; }
        scheitern(t("server"));
      }).catch(function () {
        scheitern(navigator.onLine === false ? t("offline") : t("netz"));
      });
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (laeuft || knopf.disabled) return;

      var ok = true;
      ["name", "mail"].forEach(function (n) { if (!pruefe(form.elements[n])) ok = false; });

      var wahl = form.querySelector('input[name="zusage"]:checked');
      zeige("zusage", null, wahl ? "" : t("zusage"));
      if (!wahl) ok = false;

      if (!ok) {
        var erstes = form.querySelector('[aria-invalid="true"], input[name="zusage"]');
        if (erstes) erstes.focus();
        return;
      }

      laeuft = true;
      knopf.dataset.busy = "true";
      quittung.hidden = true;

      if (!endpunkt) {
        // Vorschau: kurz warten, damit der Zustand sichtbar wird, und alles
        // bleibt hier.
        window.setTimeout(function () { fertig(wahl); }, 900);
        return;
      }
      senden(wahl);
    });
  })();
  /* ------------------------------------------------------------- Sprache -- */
  (function sprache() {
    var knoepfe = $$("[data-lang]");
    if (!knoepfe.length) return;

    /* Bei Texten mit einem Link darin darf nur der Textknoten getauscht
       werden, sonst verschwindet der Link. */
    function textknoten(el) {
      for (var i = 0; i < el.childNodes.length; i++) {
        var n = el.childNodes[i];
        if (n.nodeType === 3 && n.textContent.trim()) return n;
      }
      return null;
    }
    function lies(el) {
      var n = el.children.length ? textknoten(el) : null;
      return n ? n.textContent : el.textContent;
    }
    function schreib(el, wert) {
      var n = el.children.length ? textknoten(el) : null;
      if (n) n.textContent = wert; else el.textContent = wert;
    }

    function stelle(lang) {
      document.documentElement.lang = lang;
      $$("[data-en]").forEach(function (el) {
        if (!el.dataset.de) el.dataset.de = lies(el);
        schreib(el, lang === "en" ? el.dataset.en : el.dataset.de);
      });
      // Bildbeschreibungen gehoeren genauso uebersetzt wie der sichtbare Text.
      $$("[data-alt-en]").forEach(function (img) {
        if (!img.dataset.altDe) img.dataset.altDe = img.alt;
        img.alt = lang === "en" ? img.dataset.altEn : img.dataset.altDe;
      });
      knoepfe.forEach(function (b) {
        b.setAttribute("aria-pressed", String(b.dataset.lang === lang));
      });
    }

    knoepfe.forEach(function (b) {
      b.addEventListener("click", function () { stelle(b.dataset.lang); });
    });
  })();

  /* ----------------------------------------------------------------- Ton -- */
  (function ton() {
    var knopf = $("[data-ton]");
    var audio = $("[data-audio]");
    var icon = $("[data-ton-icon] use") || $("[data-ton-icon]");
    if (!knopf || !audio) return;

    /* Kein Autoplay. Browser unterbinden es, und es gehört sich auch nicht. */
    knopf.addEventListener("click", function () {
      if (audio.paused) {
        audio.volume = 0;
        audio.play().then(function () {
          setz(true);
          blende(0, 0.32, 900);          // langsam einblenden, nie hart
        }).catch(function () {
          knopf.hidden = true;           // keine Datei, kein Knopf
        });
      } else {
        blende(audio.volume, 0, 420, function () { audio.pause(); setz(false); });
      }
    });

    function setz(an) {
      knopf.setAttribute("aria-pressed", String(an));
      if (icon && icon.setAttribute) icon.setAttribute("href", an ? "#i-ton-an" : "#i-ton-aus");
    }

    function blende(von, nach, ms, fertig) {
      var start = performance.now();
      (function schritt(jetzt) {
        var p = Math.min((jetzt - start) / ms, 1);
        audio.volume = von + (nach - von) * p;
        if (p < 1) requestAnimationFrame(schritt); else if (fertig) fertig();
      })(start);
    }
  })();

  /* ----------------------------------------------------------------- Film -- */
  /* Der Hero-Film wird erst nach dem Oeffnen geladen. Vorher waeren es ein
     paar Megabyte fuer etwas, das noch niemand sieht — und eine Einladung
     wird unterwegs geoeffnet, oft mit schlechtem Empfang. */
  (function film() {
    var v = $("[data-hero-video]");
    if (!v || sanft.matches) return;          // weniger Bewegung: Standbild

    function starten() {
      var quellen = $$("source[data-quelle]", v);
      if (!quellen.length || quellen[0].src) return;
      // Zwei Formate: VP9 ist kleiner, H.264 laeuft ueberall. Der Browser
      // nimmt das erste, das er abspielen kann.
      quellen.forEach(function (s) { s.src = s.dataset.quelle; });
      v.addEventListener("canplay", function () {
        var lauf = v.play();
        if (!lauf || !lauf.then) { zeigen(); return; }
        lauf.then(zeigen).catch(function () { v.remove(); });
      }, { once: true });
      // Fehlt die Datei, bleibt das Standbild stehen. Lautlos.
      v.addEventListener("error", function () { v.remove(); }, { once: true });
      v.load();
    }

    function zeigen() {
      v.classList.add("is-da");
      var media = v.closest(".hero__media");
      if (media) media.classList.add("hat-film");
    }

    if (body.dataset.state === "open") { starten(); return; }
    // Auf das Oeffnen des Umschlags warten.
    new MutationObserver(function (m, beo) {
      if (body.dataset.state !== "sealed") { starten(); beo.disconnect(); }
    }).observe(body, { attributes: true, attributeFilter: ["data-state"] });
  })();

  /* ---------------------------------------------------------- Bildausfall -- */
  /* Fehlt ein optionales Foto, verschwindet es lautlos und der gezeichnete
     Grund bleibt stehen. Ein zerbrochenes Bildsymbol wäre schlimmer. */
  $$("[data-optional]").forEach(function (img) {
    img.addEventListener("error", function () { img.remove(); });
    if (img.complete && img.naturalWidth === 0) img.remove();
  });
})();
