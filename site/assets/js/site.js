/* =========================================================================
   ATRIA — Interaktion
   Keine Abhängigkeiten. Ohne JavaScript bleibt jeder Inhalt lesbar.
   ========================================================================= */
(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var desktop = window.matchMedia("(min-width: 900px)");

  /* ---- Header ---------------------------------------------------------- */
  var header = document.querySelector(".site-header");
  if (header) {
    var onScroll = function () { header.classList.toggle("is-stuck", window.scrollY > 8); };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---- Mobile Navigation ----------------------------------------------- */
  var toggle = document.querySelector(".nav-toggle");
  var mobileNav = document.querySelector(".mobile-nav");
  if (toggle && mobileNav) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      mobileNav.classList.toggle("is-open", !open);
    });
    mobileNav.addEventListener("click", function (e) {
      if (e.target.closest("a")) {
        toggle.setAttribute("aria-expanded", "false");
        mobileNav.classList.remove("is-open");
      }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
        toggle.setAttribute("aria-expanded", "false");
        mobileNav.classList.remove("is-open");
        toggle.focus();
      }
    });
  }

  /* ---- Zeilenweiser Reveal der Seitenüberschrift ------------------------ */
  /* Ausgelöst am Wurzelelement: an einen Container gebunden bliebe die
     Überschrift auf Seiten ohne diesen Container dauerhaft unsichtbar. */
  document.querySelectorAll(".reveal-line").forEach(function (line) {
    var group = line.parentNode.querySelectorAll(".reveal-line");
    var index = Array.prototype.indexOf.call(group, line);
    line.style.setProperty("--line-delay", Math.max(0, index) * 85 + "ms");
  });
  requestAnimationFrame(function () {
    requestAnimationFrame(function () { document.documentElement.classList.add("is-ready"); });
  });

  /* ---- Reveal beim Scrollen -------------------------------------------- */
  var revealables = document.querySelectorAll("[data-reveal]");
  if (!("IntersectionObserver" in window) || reduced) {
    revealables.forEach(function (el) { el.classList.add("is-visible"); });
  } else {
    document.querySelectorAll("[data-reveal-group]").forEach(function (group) {
      var kids = group.querySelectorAll("[data-reveal]");
      for (var i = 0; i < kids.length && i < 6; i++) {
        kids[i].style.setProperty("--reveal-delay", i * 55 + "ms");
      }
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { entry.target.classList.add("is-visible"); io.unobserve(entry.target); }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });
    revealables.forEach(function (el) { io.observe(el); });
  }

  /* ---- Parallax: max. 6 %, nur Desktop ---------------------------------- */
  var parallaxItems = Array.prototype.slice.call(document.querySelectorAll("[data-parallax]"));
  if (parallaxItems.length && !reduced) {
    var ticking = false;
    var applyParallax = function () {
      ticking = false;
      if (!desktop.matches) { parallaxItems.forEach(function (el) { el.style.transform = ""; }); return; }
      var vh = window.innerHeight;
      parallaxItems.forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.bottom < -200 || r.top > vh + 200) return;
        var progress = (r.top + r.height / 2 - vh / 2) / vh;
        var strength = parseFloat(el.getAttribute("data-parallax")) || 6;
        el.style.transform = "translate3d(0," + (progress * strength).toFixed(2) + "%,0)";
      });
    };
    var requestParallax = function () { if (!ticking) { ticking = true; requestAnimationFrame(applyParallax); } };
    applyParallax();
    window.addEventListener("scroll", requestParallax, { passive: true });
    window.addEventListener("resize", requestParallax);
  }

  /* ---- Sticky Split: Schritt steuert die Telefonansicht ------------------ */
  document.querySelectorAll(".sticky-split").forEach(function (split) {
    var steps = split.querySelectorAll(".sticky-split__step");
    var slides = split.querySelectorAll(".phone__slide");
    if (!steps.length || !slides.length) return;
    var activate = function (index) {
      steps.forEach(function (s, i) { s.classList.toggle("is-current", i === index); });
      slides.forEach(function (s, i) { s.classList.toggle("is-active", i === index); });
    };
    activate(0);
    if (!("IntersectionObserver" in window)) {
      slides.forEach(function (s) { s.classList.add("is-active"); });
      return;
    }
    var stepIo = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var idx = Array.prototype.indexOf.call(steps, entry.target);
        if (idx > -1) activate(idx);
      });
    }, { rootMargin: "-45% 0px -45% 0px", threshold: 0 });
    steps.forEach(function (s) { stepIo.observe(s); });
  });

  /* ---- Segment-Karussell im Hero ---------------------------------------- */
  /* Die Bewegung selbst kommt aus CSS und läuft auch ohne dieses Skript.
     Hier kommen die Bedienelemente dazu: Punkte zum Anspringen und ein
     Pause-Knopf. WCAG 2.2.2 verlangt beides — was länger als fünf Sekunden
     automatisch läuft, muss anhaltbar sein, und „den Zeiger draufhalten"
     ist auf einem Telefon keine Bedienung. */
  var car = document.querySelector("[data-hero-car]");
  var carTrack = car && car.querySelector(".hero-car__track");
  if (car && carTrack && !reduced && carTrack.getAnimations) {
    var carSlides = carTrack.querySelectorAll(".hero-car__slide:not([aria-hidden])");
    var CAR_CYCLE = 36000;                        // identisch zu @keyframes hero-car-slide
    var CAR_STEP = CAR_CYCLE / carSlides.length;  // 6000 ms je Angebot
    var carPicked = -1;                           // vom Besucher gewählt, sonst -1
    var carDots = [];

    var PAUSE_ICON = '<svg viewBox="0 0 12 12" aria-hidden="true"><rect x="2" y="1.5" width="3" height="9"/><rect x="7" y="1.5" width="3" height="9"/></svg>';
    var PLAY_ICON = '<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M3 1.5 10.5 6 3 10.5Z"/></svg>';

    var bar = document.createElement("div");
    bar.className = "hero-car__bar";
    var dotWrap = document.createElement("div");
    dotWrap.className = "hero-car__dots";
    dotWrap.setAttribute("role", "group");
    dotWrap.setAttribute("aria-label", "Angebot wählen");
    var toggle = document.createElement("button");
    toggle.type = "button";
    toggle.className = "hero-car__toggle";

    var markDots = function () {
      carDots.forEach(function (d, i) {
        if (i === carPicked) { d.setAttribute("aria-current", "true"); }
        else { d.removeAttribute("aria-current"); }
      });
    };
    var setToggle = function (paused) {
      toggle.innerHTML = (paused ? PLAY_ICON : PAUSE_ICON) +
        "<span>" + (paused ? "Weiter" : "Anhalten") + "</span>";
      toggle.setAttribute("aria-pressed", String(paused));
    };
    /* Ein Punkt springt an sein Segment: die CSS-Animation wird auf den
       passenden Zeitpunkt gesetzt und angehalten. Wer wählt, will nicht
       drei Sekunden später weitergeschoben werden. */
    var showSlide = function (i) {
      var anims = carTrack.getAnimations();
      if (!anims.length) return;
      carPicked = i;
      anims[0].currentTime = i * CAR_STEP;
      /* Die Punkte mitziehen. Bleiben sie stehen, wo sie gerade waren,
         leuchten zwei gleichzeitig: der angeklickte und der, bei dem die
         Animation eingefroren wurde. */
      carDots.forEach(function (d) {
        var f = d.firstChild;
        if (f && f.getAnimations) f.getAnimations().forEach(function (a) { a.currentTime = i * CAR_STEP; });
      });
      car.classList.add("is-paused");
      setToggle(true);
      markDots();
    };

    carSlides.forEach(function (slide, i) {
      var dot = document.createElement("button");
      dot.type = "button";
      dot.className = "hero-car__dot";
      dot.setAttribute("aria-label", slide.querySelector(".hero-car__name").textContent.trim());
      var fill = document.createElement("i");
      /* Jeder Punkt leuchtet, wenn sein Angebot an der Reihe ist. Die
         Verzögerung steht hier und nicht im Stylesheet, weil die Punkte
         erst aus der Zahl der Karten entstehen. */
      fill.style.animationDelay = (i * CAR_STEP) + "ms";
      dot.appendChild(fill);
      dot.addEventListener("click", function () { showSlide(i); });
      dotWrap.appendChild(dot);
      carDots.push(dot);
    });

    toggle.addEventListener("click", function () {
      var paused = car.classList.toggle("is-paused");
      /* Beim Fortsetzen führt wieder die Animation — sonst bliebe ein
         Punkt hell stehen, der nicht mehr das gezeigte Angebot ist. */
      if (!paused) { carPicked = -1; markDots(); }
      setToggle(paused);
    });

    setToggle(false);
    bar.appendChild(dotWrap);
    bar.appendChild(toggle);
    car.appendChild(bar);
  }

  /* ---- Nachrichtenfenster ------------------------------------------------ */
  /* Der Verlauf schreibt sich einmal selbst, sobald er ins Bild kommt.
     WICHTIG: Das Verstecken der Zeilen macht dieses Skript (.is-armed), nicht
     das Stylesheet. Fehlt JavaScript oder bricht es hier ab, steht der ganze
     Verlauf da — eine ausbleibende Animation darf nie Inhalt verschlucken. */
  document.querySelectorAll("[data-chat]").forEach(function (chat) {
    var total = parseInt(chat.getAttribute("data-chat-total"), 10) || 9000;
    var skip = chat.querySelector("[data-chat-skip]");
    var timer = null;

    var finish = function () {
      window.clearTimeout(timer);
      chat.classList.remove("is-armed", "is-playing");
      chat.classList.add("is-done");
      if (skip) skip.hidden = true;
    };

    if (reduced || !("IntersectionObserver" in window)) return;   // alles steht sofort

    chat.classList.add("is-armed");
    if (skip) skip.addEventListener("click", finish);

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        io.unobserve(entry.target);
        chat.classList.add("is-playing");
        if (skip) skip.hidden = false;
        /* Grosszügig gerechnet: der Zeiger im Fenster hält die Animation an,
           dann läuft die Uhr weiter. Der Knopf ist der verlässliche Weg. */
        timer = window.setTimeout(finish, total + 900);
      });
    }, { threshold: 0.35 });
    io.observe(chat);
  });

  /* ---- FAQ: nur eine Antwort offen -------------------------------------- */
  document.querySelectorAll("[data-faq-exclusive]").forEach(function (group) {
    var items = group.querySelectorAll("details");
    items.forEach(function (d) {
      d.addEventListener("toggle", function () {
        if (!d.open) return;
        items.forEach(function (other) { if (other !== d) other.open = false; });
      });
    });
  });

  /* ---- Abrechnung wählen ------------------------------------------------- */
  /* Der Schalter blendet nur um. Ohne dieses Skript stehen alle drei Preise
     untereinander in der Kachel — es fehlt keine Angabe, nur die Auswahl. */
  var NOTES = {
    monat:  "Monatlich ist am flexibelsten und aufs Jahr gerechnet rund 20 % teurer.",
    jahr:   "Jährlich ist der günstigste laufende Preis. Monatlich kostet aufs Jahr rund 20 % mehr.",
    einmal: "Einmalig zahlen, drei Jahre nutzen — über die Laufzeit der günstigste Preis. " +
            "Danach entscheiden Sie neu; es verlängert sich nichts von selbst."
  };
  document.querySelectorAll("[data-pricing]").forEach(function (pricing) {
    var radios = pricing.querySelectorAll('[data-billing] input[type="radio"]');
    var note = pricing.querySelector("[data-billing-note]");
    if (!radios.length) return;

    var apply = function (mode) {
      pricing.setAttribute("data-billing-mode", mode);
      if (note && NOTES[mode]) note.textContent = NOTES[mode];
      /* Die gewählte Abrechnung reist mit in die Anfrage — dann muss niemand
         den Tarif noch einmal aushandeln. */
      pricing.querySelectorAll("[data-tier-cta]").forEach(function (cta) {
        var base = cta.getAttribute("href").split("?")[0];
        cta.setAttribute("href", base + "?tarif=" + cta.getAttribute("data-tier-cta") +
                                 "&abrechnung=" + mode);
      });
    };

    radios.forEach(function (r) {
      r.addEventListener("change", function () { if (r.checked) apply(r.value); });
      if (r.checked) apply(r.value);
    });
  });

  /* ---- Aufwandsrechner --------------------------------------------------- */
  /* Rechnet ausschließlich mit den Eingaben des Besuchers. Auch der Anteil
     der wegfallenden Fragen ist ein Regler — wir behaupten keine Quote. */
  var calc = document.querySelector("[data-calc]");
  if (calc) {
    var get = function (name) { return calc.querySelector('[data-calc-input="' + name + '"]'); };
    var inputs = {
      units: get("units"),
      requests: get("requests"),
      minutes: get("minutes"),
      rate: get("rate"),
      share: get("share")
    };
    var out = {
      units: calc.querySelector('[data-calc-out="units"]'),
      requests: calc.querySelector('[data-calc-out="requests"]'),
      minutes: calc.querySelector('[data-calc-out="minutes"]'),
      rate: calc.querySelector('[data-calc-out="rate"]'),
      share: calc.querySelector('[data-calc-out="share"]'),
      hours: calc.querySelector('[data-calc-out="hours"]'),
      value: calc.querySelector('[data-calc-out="value"]'),
      price: calc.querySelector('[data-calc-out="price"]'),
      net: calc.querySelector('[data-calc-out="net"]'),
      plan: calc.querySelector('[data-calc-out="plan"]')
    };

    var euro = function (n) {
      return n.toLocaleString("de-DE", { style: "currency", currency: "EUR", maximumFractionDigits: 0 });
    };

    // Tarif nach Anzahl Einheiten — identisch zu preise.html
    var planFor = function (units) {
      if (units <= 1) return { name: "Solo", price: 190 };
      if (units <= 5) return { name: "Team", price: 390 };
      return { name: "Pro", price: 790 };
    };

    var update = function () {
      var units = +inputs.units.value;
      var requests = +inputs.requests.value;
      var minutes = +inputs.minutes.value;
      var rate = +inputs.rate.value;
      var share = +inputs.share.value;

      var plan = planFor(units);
      var hoursPerYear = (units * requests * 12 * minutes * (share / 100)) / 60;
      var value = hoursPerYear * rate;
      var net = value - plan.price;

      out.units.textContent = units === 15 ? "15+" : units;
      out.requests.textContent = requests;
      out.minutes.textContent = minutes + " Min.";
      out.rate.textContent = euro(rate) + " / Std.";
      out.share.textContent = share + " %";

      out.hours.textContent = hoursPerYear.toLocaleString("de-DE", { maximumFractionDigits: 0 });
      out.value.textContent = euro(value);
      out.price.textContent = euro(plan.price);
      out.plan.textContent = plan.name;
      out.net.textContent = (net >= 0 ? "+ " : "− ") + euro(Math.abs(net));
      out.net.style.color = net >= 0 ? "var(--ok)" : "var(--err)";
    };

    Object.keys(inputs).forEach(function (k) {
      if (inputs[k]) inputs[k].addEventListener("input", update);
    });
    update();
  }

  /* ---- Tarif aus dem Link ins Formular ----------------------------------- */
  /* Wer auf der Preisseite „Starten" drückt, hat Tarif und Abrechnung schon
     gewählt. Hier stehen sie vorausgefüllt — kein zweites Mal aushandeln. */
  var planSelect = document.querySelector("[data-prefill-plan]");
  if (planSelect) {
    var params = new URLSearchParams(window.location.search);
    var tarif = params.get("tarif");
    var mode = params.get("abrechnung");
    var wanted = tarif === "event" ? "event" : (tarif && mode ? tarif + "|" + mode : "");
    if (wanted) {
      var hit = planSelect.querySelector('option[value="' + wanted.replace(/"/g, "") + '"]');
      if (hit) {
        planSelect.value = hit.value;
        var hint = document.querySelector("[data-plan-hint]");
        if (hint) {
          hint.hidden = false;
          hint.textContent = "Aus Ihrer Auswahl übernommen: " + hit.textContent.trim() +
                             ". Änderbar, solange Sie nicht abgeschickt haben.";
        }
      }
    }
  }

  /* ---- Formulare: noch kein Endpunkt ------------------------------------ */
  /* Statt einen Versand vorzutäuschen, sagt das Formular, was Sache ist. */
  document.querySelectorAll("form[data-demo-form]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var out = form.querySelector("[data-form-status]");
      if (!out) return;
      if (!form.checkValidity()) { form.reportValidity(); return; }
      out.hidden = false;
      out.textContent = form.getAttribute("data-demo-form");
      out.focus();
    });
  });
})();
