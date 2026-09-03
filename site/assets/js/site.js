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
