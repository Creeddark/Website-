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
  (function kalender() {
    var knopf = $("[data-ics]");
    if (!knopf) return;

    knopf.addEventListener("click", function () {
      var ics = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//AMBRA//Einladung//DE",
        "CALSCALE:GREGORIAN",
        "BEGIN:VEVENT",
        "UID:ambra-marlene-anton@example.invalid",
        "DTSTAMP:" + stempel(new Date()),
        "DTSTART:20270613T120000Z",
        "DTEND:20270614T000000Z",
        "SUMMARY:Hochzeit von Marlene und Anton",
        "LOCATION:Gut Morgentau\\, Seeuferweg 8\\, 82335 Berg am Starnberger See",
        "DESCRIPTION:Trauung 15:00 Uhr im Obstgarten. Ankommen ab 14:00 Uhr.",
        "END:VEVENT",
        "END:VCALENDAR"
      ].join("\r\n");

      var url = URL.createObjectURL(new Blob([ics], { type: "text/calendar;charset=utf-8" }));
      var a = document.createElement("a");
      a.href = url;
      a.download = "marlene-und-anton.ics";
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
  (function rsvp() {
    var form = $("[data-rsvp]");
    if (!form) return;

    var knopf = $("[data-senden]", form);
    var quittung = $("[data-quittung]", form);
    var nurZusage = $$("[data-nur-zusage]", form);

    var texte = {
      de: {
        name: "Bitte tragt euren Namen ein.",
        mail: "Diese E-Mail-Adresse sieht nicht vollständig aus.",
        zusage: "Bitte wählt aus, ob ihr dabei seid.",
        ja: "Danke, {name}. Wir haben euch eingeplant.",
        nein: "Schade, {name}. Wir denken an euch.",
        demo: " In dieser Vorschau bleibt die Antwort in eurem Browser."
      },
      en: {
        name: "Please enter your name.",
        mail: "That email address looks incomplete.",
        zusage: "Please tell us whether you can come.",
        ja: "Thank you, {name}. We have you down.",
        nein: "We will miss you, {name}.",
        demo: " In this preview the reply stays in your browser."
      }
    };
    function t(k) { return texte[document.documentElement.lang] ? texte[document.documentElement.lang][k] : texte.de[k]; }

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

    form.addEventListener("submit", function (e) {
      e.preventDefault();

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

      knopf.dataset.busy = "true";

      // Eine echte Einladung sendet hier an die Engine. Die Vorschau wartet
      // nur kurz, damit der Zustand sichtbar wird, und behält alles hier.
      window.setTimeout(function () {
        knopf.dataset.busy = "false";
        knopf.disabled = true;
        var name = (form.elements.name.value || "").trim().split(" ")[0];
        quittung.textContent = t(wahl.value === "ja" ? "ja" : "nein").replace("{name}", name) + t("demo");
        quittung.hidden = false;
        quittung.focus();
      }, 900);
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
      if (v.src) return;
      v.src = v.dataset.quelle;
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
