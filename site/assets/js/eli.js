/* =========================================================================
   ELI — der digitale Assistent von VELORA
   Keine Abhängigkeiten, keine Anfrage nach außen, kein Tracking.

   WICHTIG, und die Seite sagt es auch offen: Eli ist KEIN Sprachmodell.
   Es gibt kein Backend, an das er fragen könnte. Eli führt durch feste
   Themen und beantwortet aus hinterlegten Inhalten. Alles, was er sagt,
   steht auch an anderer Stelle auf dieser Website.

   Das ist Absicht. Ein Chat, der freie Antworten vortäuscht, wäre genau
   die Sorte Versprechen, die der Rest dieser Seite vermeidet.
   ========================================================================= */
(function () {
  "use strict";

  var root = document.querySelector("[data-eli]");
  if (!root) return;

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var base = root.getAttribute("data-eli-base") || "";
  var ctx = root.getAttribute("data-eli-context") || "start";
  var seg = root.getAttribute("data-eli-seg") || "";

  var panel = root.querySelector("[data-eli-panel]");
  var openBtn = root.querySelector("[data-eli-open]");
  var closeBtn = root.querySelector("[data-eli-close]");
  var log = root.querySelector("[data-eli-log]");
  var chipBar = root.querySelector("[data-eli-chips]");
  var form = root.querySelector("[data-eli-form]");
  var input = root.querySelector("[data-eli-input]");
  var teaser = root.querySelector("[data-eli-teaser]");

  /* ---- Die Fakten der Seite ---------------------------------------------
     Auf einer Gästeseite liest Eli, was der Gastgeber hinterlegt hat. Aus
     der Seite, nicht aus einer Kopie hier im Skript: eine Kopie läuft
     auseinander, und dann nennt der Assistent ein Passwort, das nicht mehr
     gilt. Steht nichts da, sagt Eli das — er erfindet nichts. */
  var FACTS = null;
  try {
    var raw = document.getElementById("velora-facts");
    if (raw) FACTS = JSON.parse(raw.textContent);
  } catch (err) { FACTS = null; }

  /* ---- Inhalte ---------------------------------------------------------
     Jede Antwort ist eine Aussage, die so auch auf der Website steht.
     Wo eine Zahl vorkommt, ist es dieselbe wie auf der Preisseite. */

  var SEGMENTS = {
    ferien:     { name: "Ferienunterkünfte", href: "segmente/ferienunterkuenfte.html" },
    hotels:     { name: "Hotels & Pensionen", href: "segmente/hotels.html" },
    camping:    { name: "Campingplätze", href: "segmente/campingplaetze.html" },
    events:     { name: "Firmenevents", href: "segmente/firmenevents.html" },
    verwaltung: { name: "Hausverwaltungen", href: "segmente/hausverwaltungen.html" },
    seminar:    { name: "Seminarhäuser", href: "segmente/seminarhaeuser.html" }
  };

  var TOPICS = {
    was: {
      label: "Was ist Velora?",
      say: [
        "Velora ist eine digitale Infomappe für Orte, an denen Menschen ankommen.",
        "Ihre Gäste scannen einen QR-Code und finden alles an einer Stelle: WLAN, Check-in, Hausregeln, Ablauf, Ihre Empfehlungen. Ohne App, ohne Konto, ohne Anmeldung.",
        "Sie pflegen die Inhalte an einer Stelle — die Seite ist damit immer aktuell."
      ],
      link: { label: "Live-Beispiel öffnen", href: "demo/gaestemappe.html" },
      next: ["fuerwen", "kosten", "berater"]
    },
    fuerwen: {
      label: "Für wen ist das?",
      say: ["Sechs Bereiche, dasselbe Produkt mit anderen Bausteinen. Wählen Sie Ihren — dort steht, was konkret drinsteckt und was es kostet."],
      segChips: true,
      next: ["berater", "kosten"]
    },
    kosten: {
      label: "Was kostet Velora?",
      say: [
        "Drei Tarife, und Sie wählen die Abrechnung: monatlich, jährlich oder einmalig für drei Jahre.",
        "Solo 19 € im Monat, 190 € im Jahr oder 490 € einmalig.\nTeam 39 € / 390 € / 990 €.\nPro 79 € / 790 € / 1.990 €.",
        "Monatlich ist am flexibelsten und aufs Jahr rund 20 % teurer. Jährlich ist der günstigste laufende Preis. Alle Beträge netto zzgl. USt."
      ],
      link: { label: "Preise ansehen", href: "preise.html" },
      next: ["berater", "abrechnung", "kuendigen"]
    },
    abrechnung: {
      label: "Monatlich, jährlich oder einmalig?",
      say: [
        "Kurz: monatlich, wenn Sie flexibel bleiben wollen. Jährlich, wenn Sie laufend am günstigsten fahren wollen. Einmalig, wenn Sie es einmal zahlen und drei Jahre Ruhe haben wollen.",
        "„Einmalig“ heißt bei uns drei Jahre Laufzeit, nicht unbegrenzt. Wir schulden Ihnen dauerhaft Betrieb und Erreichbarkeit — ein einmaliger Betrag gegen eine unbegrenzte Pflicht wäre ein Versprechen, das irgendwann bricht. Danach entscheiden Sie neu; es verlängert sich nichts von selbst."
      ],
      link: { label: "Preise ansehen", href: "preise.html" },
      next: ["kosten", "kuendigen"]
    },
    kuendigen: {
      label: "Wie komme ich wieder raus?",
      say: [
        "Bei jährlich: ein Jahr Mindestlaufzeit, danach jährlich kündbar. Bei monatlich: monatlich.",
        "Der Wechsel weg von uns kostet nichts. Sie exportieren Ihre Inhalte, wir löschen. Wir halten niemanden über die Daten fest."
      ],
      next: ["kosten", "berater"]
    },
    funktionen: {
      label: "Welche Funktionen gibt es?",
      say: [
        "WLAN mit Netzwerk und Passwort, Check-in und Check-out mit Uhrzeiten, Geräte erklärt mit Fotos, Hausregeln, Ihre Empfehlungen für die Umgebung, Kontakt für den Fall, dass doch etwas ist.",
        "Dazu QR-Code mit Druckvorlage, unbegrenzte Änderungen, Datenexport. Ab Team zweisprachig und Rückmeldung mit Foto, ab Pro eigene Domain und Ihr Branding."
      ],
      link: { label: "Alle Bausteine ansehen", href: "produkt.html" },
      next: ["kosten", "berater"]
    },
    grenzen: {
      label: "Was kann Velora nicht?",
      say: [
        "Wir sind kein Buchungssystem, keine Kasse und kein Channel-Manager. Wir ersetzen kein PMS.",
        "Und ich selbst bin kein Sprachmodell: Ich führe durch feste Themen und gebe wieder, was auf dieser Website steht. Für alles darüber hinaus schreiben Sie am besten direkt."
      ],
      link: { label: "Kontakt aufnehmen", href: "kontakt.html" },
      next: ["was", "kosten"]
    }
  };

  /* ---- Gästethemen: gebaut aus dem, was der Gastgeber hinterlegt hat ----
     Hier liegt der eigentliche Nutzen. Eli erzählt nicht nur, er handelt:
     Passwort kopieren, QR zum Verbinden, Karte öffnen, anrufen, schreiben.
     Was nicht hinterlegt ist, taucht gar nicht erst als Vorschlag auf. */

  function hatFakt(pfad) {
    if (!FACTS) return false;
    var teile = pfad.split("."), v = FACTS;
    for (var i = 0; i < teile.length; i++) {
      if (!v || typeof v !== "object" || !v[teile[i]]) return false;
      v = v[teile[i]];
    }
    return true;
  }

  /* Zum passenden Abschnitt der Gästeseite springen: der vorhandene Reiter
     wird geklickt, damit die Seite ihre eigene Logik behält. */
  function springeZu(abschnitt) {
    var tab = document.querySelector('[data-guide-tab="' + abschnitt.tab + '"]');
    if (tab) tab.click();
    var ziel = document.getElementById(abschnitt.id);
    if (ziel) {
      if (window.innerWidth <= 640) close();
      ziel.scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "start" });
    }
  }

  function abschnittMit(tab) {
    var liste = (FACTS && FACTS.abschnitte) || [];
    for (var i = 0; i < liste.length; i++) if (liste[i].tab === tab) return liste[i];
    return null;
  }

  /* Aktionsknopf im Gespräch. `run` statt href: eine Aktion, kein Link. */
  function aktion(label, run, zweitrangig) {
    var b = el("button", "eli__link" + (zweitrangig ? " eli__link--alt" : ""), label);
    b.type = "button";
    b.addEventListener("click", run);
    return b;
  }

  function kopieren(text, knopf, erfolg) {
    var fertig = function () {
      var alt = knopf.textContent;
      knopf.textContent = erfolg;
      window.setTimeout(function () { knopf.textContent = alt; }, 2200);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(fertig, function () { markiere(text); });
    } else { markiere(text); }
  }

  /* Wo die Zwischenablage nicht darf (älteres Safari, kein sicherer Kontext),
     wird der Wert wenigstens markiert — dann genügt ein langer Fingerdruck. */
  function markiere(text) {
    var f = document.createElement("input");
    f.value = text; f.readOnly = true;
    f.style.cssText = "position:absolute;left:-9999px";
    document.body.appendChild(f); f.select();
    try { document.execCommand("copy"); } catch (err) { /* dann eben nicht */ }
    document.body.removeChild(f);
  }

  var GAST = {
    g_wlan: {
      wenn: function () { return hatFakt("wlan.ssid") && hatFakt("wlan.pass"); },
      label: "WLAN & Technik",
      bauen: function () {
        var w = FACTS.wlan;
        var box = el("div", "eli__actions");
        var kopf = aktion("Passwort kopieren", function () {
          kopieren(w.pass, kopf, "Kopiert ✓");
        });
        box.appendChild(kopf);
        if (FACTS.wlanqr) {
          box.appendChild(aktion("Mit QR verbinden", function () { zeigeQR(w); }, true));
        }
        var abschnitt = abschnittMit("technik");
        if (abschnitt) box.appendChild(aktion("Zum Abschnitt", function () { springeZu(abschnitt); }, true));
        return {
          say: ["Netzwerk: **" + w.ssid + "**\nPasswort: **" + w.pass + "**"],
          extra: box
        };
      },
      next: ["g_checkin", "g_kontakt"]
    },
    g_checkin: {
      wenn: function () { return hatFakt("checkin") || hatFakt("checkout"); },
      label: "Anreise & Check-in",
      bauen: function () {
        var zeilen = [];
        if (FACTS.checkin) zeilen.push("**Check-in** — " + FACTS.checkin);
        if (FACTS.checkout) zeilen.push("**Check-out** — " + FACTS.checkout);
        var box = el("div", "eli__actions");
        var a = abschnittMit("ankommen") || abschnittMit("abreise");
        if (a) box.appendChild(aktion("Zum Abschnitt", function () { springeZu(a); }, true));
        return { say: zeilen, extra: box };
      },
      next: ["g_weg", "g_wlan"]
    },
    g_weg: {
      wenn: function () { return hatFakt("adresse"); },
      label: "Adresse & Parken",
      bauen: function () {
        var box = el("div", "eli__actions");
        var adr = FACTS.adresse;
        /* OpenStreetMap statt eines Kartendienstes, der mitschreibt — es
           öffnet sich auf jedem Gerät und passt zu dem, was diese Seite
           über Tracking verspricht. */
        var a = el("a", "eli__link", "Auf der Karte zeigen");
        a.href = "https://www.openstreetmap.org/search?query=" + encodeURIComponent(adr);
        a.target = "_blank"; a.rel = "noopener noreferrer";
        box.appendChild(a);
        var kopf = aktion("Adresse kopieren", function () {
          kopieren(adr, kopf, "Kopiert ✓");
        }, true);
        box.appendChild(kopf);
        var zeilen = ["**" + ((FACTS && FACTS.objekt) || "Adresse") + "**\n" + adr];
        if (FACTS.parken) zeilen.push("**Parken** — " + FACTS.parken);
        return { say: zeilen, extra: box };
      },
      next: ["g_checkin", "g_kontakt"]
    },
    g_kontakt: {
      wenn: function () { return hatFakt("kontakt.name"); },
      label: "Wen frage ich, wenn etwas ist?",
      bauen: function () {
        var k = FACTS.kontakt;
        var zeilen = ["**" + k.name + "**" + (k.rolle ? " · " + k.rolle : "")];
        if (k.zeiten) zeilen.push("Erreichbar " + k.zeiten + ".");
        if (FACTS.notruf) zeilen.push(FACTS.notruf);
        var box = el("div", "eli__actions");
        if (k.tel) {
          var t = el("a", "eli__link", "Anrufen");
          t.href = "tel:" + k.tel.replace(/[^+0-9]/g, "");
          box.appendChild(t);
        }
        if (k.mail) box.appendChild(mailKnopf(k, "", true));
        return { say: zeilen, extra: box };
      },
      next: ["g_wlan", "g_checkin"]
    }
  };

  /* Der wichtigste Knopf überhaupt: keine Sackgasse. Was Eli nicht weiß,
     geht mit einem Tipp an den Gastgeber — Frage und Objekt schon drin. */
  function mailKnopf(k, frage, zweitrangig) {
    var betreff = "Frage zu " + ((FACTS && FACTS.objekt) || "Ihrem Objekt");
    var text = frage
      ? frage + "\n\n(Gesendet über die Infoseite von " + ((FACTS && FACTS.objekt) || "VELORA") + ")"
      : "";
    var a = el("a", "eli__link" + (zweitrangig ? " eli__link--alt" : ""),
               frage ? "Diese Frage an " + kurz(k.name) + " senden" : "Schreiben");
    a.href = "mailto:" + k.mail + "?subject=" + encodeURIComponent(betreff)
           + (text ? "&body=" + encodeURIComponent(text) : "");
    return a;
  }
  function kurz(name) { return name.split(" ")[0]; }

  function zeigeQR(w) {
    var li = el("li", "eli__row");
    var karte = el("div", "eli__qr");
    var img = document.createElement("img");
    img.src = FACTS.wlanqr; img.width = 168; img.height = 168;
    img.alt = "QR-Code, der das Telefon mit dem Netzwerk " + w.ssid + " verbindet";
    karte.appendChild(img);
    karte.appendChild(el("p", null, "Kamera öffnen, Code scannen — das Telefon verbindet sich selbst."));
    li.appendChild(karte);
    log.appendChild(li);
    scrollDown();
  }

  function gastThemen() {
    var ids = [];
    for (var k in GAST) if (GAST.hasOwnProperty(k) && GAST[k].wenn()) ids.push(k);
    return ids;
  }

  function runGast(id) {
    var t = GAST[id];
    if (!t) return;
    addUser(t.label);
    speak(function () {
      var r = t.bauen();
      addEli(r.say, r.extra && r.extra.childNodes.length ? r.extra : null);
      /* Alle übrigen Themen bleiben stehen. Es sind wenige, und ein Gast,
         der gerade das WLAN gesucht hat, sucht als Nächstes oft die
         Check-out-Zeit — nicht das, was ich ihm vorgebe. */
      setChips(gastChips(gastThemen().filter(function (n) { return n !== id; })));
    });
  }

  function gastChips(ids) {
    var out = ids.map(function (id) {
      return { label: GAST[id].label, run: function () { runGast(id); } };
    });
    if (hatFakt("kontakt.mail") || hatFakt("kontakt.tel")) {
      out.push({ label: "Etwas anderes fragen", run: andereFrage });
    }
    return out;
  }

  function andereFrage() {
    addUser("Etwas anderes fragen");
    speak(function () {
      var k = FACTS.kontakt;
      var box = el("div", "eli__actions");
      if (k.mail) box.appendChild(mailKnopf(k, "", false));
      if (k.tel) {
        var t = el("a", "eli__link eli__link--alt", "Anrufen");
        t.href = "tel:" + k.tel.replace(/[^+0-9]/g, "");
        box.appendChild(t);
      }
      addEli(["Alles, was hier nicht hinterlegt ist, weiß " + kurz(k.name) + " am besten." +
              (k.zeiten ? " Erreichbar " + k.zeiten + "." : "")], box);
      setChips(gastChips(gastThemen()));
    });
  }

  /* ---- Bedarfsanalyse ---------------------------------------------------
     Ein kurzer, ehrlicher Weg zur passenden Empfehlung. Zwei Fragen,
     dann eine Antwort mit Begründung — und, wo es zutrifft, der Hinweis,
     dass das günstigere Angebot reicht. */

  var BETRIEB = [
    { id: "hotels", label: "Hotel oder Pension" },
    { id: "ferien", label: "Ferienwohnung oder Ferienhaus" },
    { id: "camping", label: "Campingplatz" },
    { id: "events", label: "Eventlocation oder Firmenevents" },
    { id: "verwaltung", label: "Hausverwaltung" },
    { id: "seminar", label: "Seminarhaus" }
  ];
  var MENGE = [
    { id: "1", label: "Ein Objekt" },
    { id: "2-5", label: "2 bis 5" },
    { id: "6-15", label: "6 bis 15" },
    { id: "15+", label: "Mehr als 15" }
  ];

  var TARIF = {
    solo: { name: "Solo", preis: "190 € im Jahr oder 19 € im Monat", key: "solo" },
    team: { name: "Team", preis: "390 € im Jahr oder 39 € im Monat", key: "team" },
    pro:  { name: "Pro",  preis: "790 € im Jahr oder 79 € im Monat", key: "pro" }
  };

  function empfehlung(betrieb, menge) {
    /* Sonderfälle zuerst — sie folgen nicht der Einheitenlogik. */
    if (betrieb === "events") {
      return {
        titel: "Einzelnes Event oder Jahresvertrag",
        text: ["Für Firmenevents rechnen wir pro Termin ab: 290 € für ein Event, sechs Monate Laufzeit.",
               "Wenn Sie mehrere Termine im Jahr haben, lohnt sich der Jahresvertrag für 790 €. Ab etwa drei Terminen im Jahr sind Sie damit günstiger."],
        href: "preise.html", cta: "Preise ansehen"
      };
    }
    if (betrieb === "verwaltung") {
      return {
        titel: "Preis je Objekt",
        text: ["Für Hausverwaltungen rechnen wir pro Objekt: 190 € im Jahr, ab 10 Objekten 140 €, ab 25 Objekten 110 €.",
               "40 Häuser kosten damit 4.400 € im Jahr. Sie können es selbst nachrechnen, bevor Sie uns schreiben — deshalb steht es auf der Seite."],
        href: "segmente/hausverwaltungen.html", cta: "Details ansehen"
      };
    }
    if (menge === "15+") {
      return {
        titel: "Pro mit Aufschlag",
        text: ["Pro deckt bis 15 Einheiten ab und kostet 790 € im Jahr. Darüber kommen 35 € je weiterer Einheit dazu.",
               "Ein Haus mit 25 Einheiten kostet also 1.140 € im Jahr."],
        href: "preise.html?tarif=pro&abrechnung=jahr", cta: "Pro ansehen"
      };
    }

    var t = menge === "1" ? TARIF.solo : (menge === "2-5" ? TARIF.team : TARIF.pro);
    var text = ["**" + t.name + "** — " + t.preis + "."];

    if (menge === "1") {
      text.push("Ein Objekt, eine Seite, alle Bausteine. Solo reicht dafür vollständig aus.");
      if (betrieb === "hotels" || betrieb === "seminar") {
        text.push("Ehrlich gesagt: Pro brauchen Sie erst, wenn Sie eine eigene Domain und Ihr eigenes Branding wollen. Solange das nicht wichtig ist, wäre Pro rausgeworfenes Geld.");
      } else {
        text.push("Wenn später weitere Objekte dazukommen, wechseln Sie jederzeit auf Team oder Pro — das ist kein neuer Vertrag.");
      }
    } else if (menge === "2-5") {
      text.push("Bis 5 Einheiten, jede mit eigenem Guide und eigenem QR-Code. Dazu zweisprachig, Vorlagen zum Einmal-Pflegen und Rückmeldung mit Foto.");
      text.push("Team ist der Tarif, den die meisten wählen. Solo würde hier nicht reichen — es deckt nur eine Einheit ab.");
    } else {
      text.push("Bis 15 Einheiten, zentral verwaltet, mit eigener Domain und Ihrem Branding ohne unseren Hinweis im Fuß.");
      text.push("Wenn Ihnen eigene Domain und Branding egal sind und Sie unter 6 Einheiten liegen, tut es auch Team für 390 €. Fragen Sie sich das ehrlich, bevor Sie Pro nehmen.");
    }

    var s = SEGMENTS[betrieb];
    return {
      titel: "Meine Empfehlung",
      text: text,
      href: "preise.html?tarif=" + t.key + "&abrechnung=jahr",
      cta: "Zu " + t.name + " im Detail",
      zweit: s ? { label: "Seite für " + s.name, href: s.href } : null
    };
  }

  /* ---- Startvorschläge je Seite ---------------------------------------- */
  function startChips() {
    if (ctx === "demo") return null;      // Gästeseiten laufen über gastChips
    if (ctx === "preise") return ["berater", "abrechnung", "kuendigen", "kosten"];
    if (ctx === "segment" && SEGMENTS[seg]) return ["berater", "kosten", "funktionen", "was"];
    if (ctx === "produkt") return ["funktionen", "grenzen", "kosten", "berater"];
    return ["was", "fuerwen", "berater", "kosten"];
  }

  function startGruss() {
    if (ctx === "demo") {
      var ort = (FACTS && FACTS.objekt) ? " für " + FACTS.objekt : "";
      return ["Hallo 👋 Ich bin Eli, Ihr digitaler Assistent" + ort + ".",
              "WLAN, Check-in, Anfahrt — fragen Sie mich, ich habe alles griffbereit."];
    }
    if (ctx === "segment" && SEGMENTS[seg]) {
      return ["Hallo 👋 Ich bin Eli, der digitale Assistent von Velora.",
              "Sie sind auf der Seite für " + SEGMENTS[seg].name + ". Ich helfe Ihnen, das passende Angebot zu finden."];
    }
    if (ctx === "preise") {
      return ["Hallo 👋 Ich bin Eli, der digitale Assistent von Velora.",
              "Preise sind schnell erklärt — und wenn Sie mögen, finde ich in zwei Fragen heraus, welcher Tarif zu Ihnen passt."];
    }
    return ["Hallo 👋 Ich bin Eli, der digitale Assistent von Velora.",
            "Schön, dass Sie da sind. Ich helfe Ihnen, Informationen zu finden oder herauszufinden, welche Lösung zu Ihnen passt."];
  }

  /* ---- Darstellung ------------------------------------------------------ */

  var busy = false;

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function scrollDown() { log.scrollTop = log.scrollHeight; }

  function addUser(text) {
    var li = el("li", "eli__row eli__row--me");
    li.appendChild(el("p", "eli__bubble", text));
    log.appendChild(li);
    scrollDown();
  }

  /* Fettung nur für **so markierte** Stellen — kein HTML aus Inhalten. */
  function richText(p, s) {
    s.split("**").forEach(function (part, i) {
      if (!part) return;
      if (i % 2) p.appendChild(el("strong", null, part));
      else p.appendChild(document.createTextNode(part));
    });
  }

  function addEli(lines, extra) {
    var li = el("li", "eli__row");
    var bubble = el("p", "eli__bubble eli__bubble--eli");
    lines.forEach(function (line, i) {
      if (i) bubble.appendChild(el("span", "eli__break"));
      richText(bubble, line);
    });
    li.appendChild(bubble);
    if (extra) li.appendChild(extra);
    log.appendChild(li);
    scrollDown();
    return li;
  }

  function linkOut(label, href) {
    var a = el("a", "eli__link", label);
    a.href = base + href;
    return a;
  }

  function setChips(items) {
    chipBar.innerHTML = "";
    items.forEach(function (it) {
      var b = el("button", "eli__chip", it.label);
      b.type = "button";
      b.addEventListener("click", function () { it.run(); });
      chipBar.appendChild(b);
    });
    chipBar.hidden = items.length === 0;
  }

  /* Kurze Tippanzeige, bevor Eli antwortet — sie macht den Wechsel
     lesbar. Bei reduzierter Bewegung entfällt sie. */
  var queue = [];
  function speak(fn) {
    if (reduced) { fn(); return; }
    if (busy) { queue.push(fn); return; }   // nie verschlucken, nur anstellen
    busy = true;
    var li = el("li", "eli__row");
    var t = el("span", "eli__typing");
    t.setAttribute("aria-hidden", "true");
    t.appendChild(el("i")); t.appendChild(el("i")); t.appendChild(el("i"));
    li.appendChild(t);
    log.appendChild(li);
    scrollDown();
    window.setTimeout(function () {
      li.remove(); busy = false; fn();
      if (queue.length) speak(queue.shift());
    }, 520);
  }

  function topicChips(ids) {
    return ids.filter(function (id) { return id === "berater" || TOPICS[id]; })
      .map(function (id) {
        if (id === "berater") return { label: "Welches Angebot passt zu mir?", run: startBerater };
        return { label: TOPICS[id].label, run: function () { runTopic(id); } };
      });
  }

  function runTopic(id) {
    var t = TOPICS[id];
    if (!t) return;
    addUser(t.label);
    speak(function () {
      var extra = null;
      if (t.link) { extra = el("div", "eli__actions"); extra.appendChild(linkOut(t.link.label, t.link.href)); }
      addEli(t.say, extra);
      if (t.segChips) {
        setChips(Object.keys(SEGMENTS).map(function (k) {
          return { label: SEGMENTS[k].name, run: function () { gotoSegment(k); } };
        }).concat(topicChips(t.next || [])));
      } else {
        setChips(topicChips(t.next || []));
      }
    });
  }

  function gotoSegment(k) {
    var s = SEGMENTS[k];
    addUser(s.name);
    speak(function () {
      var extra = el("div", "eli__actions");
      extra.appendChild(linkOut("Seite für " + s.name + " öffnen", s.href));
      addEli(["Dort steht, welche Bausteine für " + s.name + " typisch sind, was es kostet und wie ein fertiges Beispiel aussieht."], extra);
      setChips(topicChips(["berater", "kosten", "was"]));
    });
  }

  /* ---- Der Berater ------------------------------------------------------ */
  function startBerater() {
    addUser("Welches Angebot passt zu mir?");
    speak(function () {
      addEli(["Gerne — zwei Fragen, dann sage ich Ihnen, was ich empfehlen würde.",
              "Was betreiben Sie hauptsächlich?"]);
      setChips(BETRIEB.map(function (b) {
        return { label: b.label, run: function () { frageMenge(b.id, b.label); } };
      }));
    });
  }

  function frageMenge(betrieb, label) {
    addUser(label);
    if (betrieb === "events" || betrieb === "verwaltung") { zeigeEmpfehlung(betrieb, null); return; }
    speak(function () {
      addEli(["Und wie viele Einheiten sind das — Wohnungen, Zimmer, Häuser oder Stellplätze?"]);
      setChips(MENGE.map(function (m) {
        return { label: m.label, run: function () { addUser(m.label); zeigeEmpfehlung(betrieb, m.id); } };
      }));
    });
  }

  function zeigeEmpfehlung(betrieb, menge) {
    speak(function () {
      var e = empfehlung(betrieb, menge);
      var extra = el("div", "eli__actions");
      extra.appendChild(linkOut(e.cta, e.href));
      if (e.zweit) extra.appendChild(linkOut(e.zweit.label, e.zweit.href));
      addEli([e.titel].concat(e.text), extra);
      setChips([
        { label: "Nochmal von vorn", run: startBerater },
        { label: "Monatlich, jährlich oder einmalig?", run: function () { runTopic("abrechnung"); } },
        { label: "Direkt anfragen", run: function () { window.location.href = base + "kontakt.html"; } }
      ]);
    });
  }

  /* ---- Freitext ---------------------------------------------------------
     Eli kann keine freien Fragen beantworten. Statt etwas zu erfinden,
     sucht er das nächstliegende Thema und sagt sonst offen, dass er
     hier nicht weiterkommt. */

  var STICHWORTE = [
    { hit: ["wlan", "wifi", "w-lan", "internet", "passwort"], id: "g_wlan", gast: true },
    { hit: ["check-in", "checkin", "anreise", "schlüssel", "schluessel", "ankunft", "ankommen"], id: "g_checkin", gast: true },
    { hit: ["check-out", "checkout", "abreise", "wann müssen wir raus", "auschecken"], id: "g_checkin", gast: true },
    { hit: ["parken", "parkplatz", "stellplatz", "auto"], id: "g_weg", gast: true },
    { hit: ["adresse", "anfahrt", "wo ist", "wie komme ich", "navi", "karte", "wo liegt"], id: "g_weg", gast: true },
    { hit: ["kontakt", "ansprechpartner", "notfall", "hilfe", "erreiche ich", "anrufen"], id: "g_kontakt", gast: true },
    { hit: ["preis", "kosten", "teuer", "tarif", "euro", "€"], id: "kosten" },
    { hit: ["monatlich", "jährlich", "jaehrlich", "einmalig", "abrechnung", "zahlung", "rechnung"], id: "abrechnung" },
    { hit: ["kündig", "kuendig", "laufzeit", "vertrag", "wechseln"], id: "kuendigen" },
    { hit: ["funktion", "kann velora", "bausteine", "features", "was gibt"], id: "funktionen" },
    { hit: ["passt", "angebot", "paket", "empfehl", "welcher tarif"], id: "berater" },
    { hit: ["was ist", "wer seid", "worum geht"], id: "was" },
    { hit: ["für wen", "fuer wen", "zielgruppe", "branche"], id: "fuerwen" },
    { hit: ["kann nicht", "grenzen", "buchung", "pms", "kasse"], id: "grenzen" }
  ];

  function beantworte(text) {
    var q = text.toLowerCase();
    for (var i = 0; i < STICHWORTE.length; i++) {
      var eintrag = STICHWORTE[i];
      /* Gästethemen greifen nur, wenn der Gastgeber sie auch hinterlegt hat. */
      if (eintrag.gast && !(GAST[eintrag.id] && GAST[eintrag.id].wenn())) continue;
      for (var j = 0; j < eintrag.hit.length; j++) {
        if (q.indexOf(eintrag.hit[j]) > -1) {
          var id = eintrag.id;
          var istGast = !!eintrag.gast;
          speak(function () {
            addEli(["Freie Fragen kann ich nicht deuten — aber das hier passt vermutlich:"]);
            if (id === "berater") { startBerater(); }
            else if (istGast) { runGast(id); }
            else { runTopic(id); }
          });
          return;
        }
      }
    }

    /* Auf einer Gästeseite ist die ehrliche Antwort nicht „weiß ich nicht",
       sondern der kürzeste Weg zu jemandem, der es weiß. */
    if (ctx === "demo" && FACTS && FACTS.kontakt && (FACTS.kontakt.mail || FACTS.kontakt.tel)) {
      var frage = text;
      speak(function () {
        var k = FACTS.kontakt;
        var box = el("div", "eli__actions");
        if (k.mail) box.appendChild(mailKnopf(k, frage, false));
        if (k.tel) {
          var t = el("a", "eli__link eli__link--alt", "Anrufen");
          t.href = "tel:" + k.tel.replace(/[^+0-9]/g, "");
          box.appendChild(t);
        }
        addEli(["Dazu hat " + kurz(k.name) + " nichts hinterlegt — ich rate hier nicht.",
                "Ich habe Ihre Frage fertig vorbereitet. Ein Tipp, und sie ist unterwegs." +
                (k.zeiten ? " Erreichbar " + k.zeiten + "." : "")], box);
        setChips(gastChips(gastThemen()));
      });
      return;
    }
    speak(function () {
      var extra = el("div", "eli__actions");
      extra.appendChild(linkOut("Direkt schreiben", "kontakt.html"));
      addEli([
        "Dazu habe ich leider nichts hinterlegt.",
        "Ich bin kein Sprachmodell — ich führe durch feste Themen und gebe wieder, was auf dieser Website steht. Für alles darüber hinaus schreiben Sie am besten direkt; Sie bekommen werktags binnen 24 Stunden Antwort."
      ], extra);
      setChips(topicChips(startChips() || ["was", "fuerwen", "berater", "kosten"]));
    });
  }

  /* ---- Öffnen und Schließen -------------------------------------------- */

  var started = false;
  var lastFocus = null;

  function begruessen() {
    if (started) return;
    started = true;
    addEli(startGruss());
    if (ctx === "demo" && FACTS) { setChips(gastChips(gastThemen())); }
    else { setChips(topicChips(startChips() || ["was", "fuerwen", "berater", "kosten"])); }
  }

  function open() {
    lastFocus = document.activeElement;
    root.classList.add("is-open");
    panel.hidden = false;
    openBtn.setAttribute("aria-expanded", "true");
    hideTeaser();
    begruessen();
    window.setTimeout(function () {
      var first = chipBar.querySelector("button") || closeBtn;
      if (first) first.focus();
      log.scrollTop = 0;          // die Begrüßung steht am Anfang, nicht am Ende
    }, reduced ? 0 : 220);
  }

  function close() {
    root.classList.remove("is-open");
    panel.hidden = true;
    openBtn.setAttribute("aria-expanded", "false");
    if (lastFocus && lastFocus.focus) lastFocus.focus(); else openBtn.focus();
  }

  openBtn.addEventListener("click", function () {
    if (root.classList.contains("is-open")) close(); else open();
  });
  if (closeBtn) closeBtn.addEventListener("click", close);

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && root.classList.contains("is-open")) { close(); }
  });

  /* Der Fokus bleibt im Fenster, solange es offen ist. */
  panel.addEventListener("keydown", function (e) {
    if (e.key !== "Tab") return;
    var f = panel.querySelectorAll('button, a[href], input, [tabindex]:not([tabindex="-1"])');
    var vis = Array.prototype.filter.call(f, function (n) { return n.offsetParent !== null; });
    if (!vis.length) return;
    var first = vis[0], last = vis[vis.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });

  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var v = (input.value || "").trim();
      if (!v) return;
      addUser(v);
      input.value = "";
      beantworte(v);
    });
  }

  /* ---- Der kleine Hinweis am Knopf --------------------------------------
     Einmal je Sitzung, nach ein paar Sekunden, und er verschwindet von
     selbst. Der Merker liegt in sessionStorage — kein Cookie, keine
     Kennung, nichts, was jemanden wiedererkennt. */
  function hideTeaser() { if (teaser) teaser.hidden = true; }

  if (teaser) {
    var shown = false;
    try { shown = window.sessionStorage.getItem("velora.eli.hi") === "1"; } catch (err) { shown = false; }
    if (!shown && !reduced) {
      window.setTimeout(function () {
        if (root.classList.contains("is-open")) return;
        teaser.hidden = false;
        try { window.sessionStorage.setItem("velora.eli.hi", "1"); } catch (err) { /* egal */ }
        window.setTimeout(hideTeaser, 9000);
      }, 4200);
    }
    var dismiss = teaser.querySelector("[data-eli-teaser-close]");
    if (dismiss) dismiss.addEventListener("click", function (e) { e.stopPropagation(); hideTeaser(); });
    teaser.addEventListener("click", function (e) {
      if (e.target.closest("[data-eli-teaser-close]")) return;
      open();
    });
  }
})();
