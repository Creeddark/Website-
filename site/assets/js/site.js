/* =========================================================================
   CONVIVIO — Interaktion
   Keine Abhängigkeiten. Alles degradiert ohne JS zu vollständigem Inhalt.
   Motion-Regeln: docs/03-design-system.md (§8)
   ========================================================================= */
(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var desktop = window.matchMedia("(min-width: 900px)");

  /* ---- Header: Linie erst nach dem Scrollen ---------------------------- */
  var header = document.querySelector(".site-header");
  if (header) {
    var onScroll = function () {
      header.classList.toggle("is-stuck", window.scrollY > 8);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---- Mobile Navigation ---------------------------------------------- */
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

  /* ---- Hero-Textreveal beim Laden -------------------------------------- */
  /* Zeilenweiser Reveal der Seitenüberschrift.
     Ausgelöst am Wurzelelement, nicht an einem Container: sonst bleiben
     Überschriften auf Seiten ohne .hero/.cover dauerhaft unsichtbar. */
  document.querySelectorAll(".reveal-line").forEach(function (line, i) {
    var group = line.parentNode;
    var index = Array.prototype.indexOf.call(group.querySelectorAll(".reveal-line"), line);
    line.style.setProperty("--line-delay", (index < 0 ? i : index) * 90 + "ms");
  });
  requestAnimationFrame(function () {
    requestAnimationFrame(function () {
      document.documentElement.classList.add("is-ready");
    });
  });

  /* ---- Reveal beim Scrollen -------------------------------------------- */
  var revealables = document.querySelectorAll("[data-reveal]");
  if (!("IntersectionObserver" in window) || reduced) {
    revealables.forEach(function (el) { el.classList.add("is-visible"); });
  } else {
    // Gestaffelt innerhalb einer Gruppe, max. 5 Elemente in Folge
    document.querySelectorAll("[data-reveal-group]").forEach(function (group) {
      var kids = group.querySelectorAll("[data-reveal]");
      for (var i = 0; i < kids.length && i < 5; i++) {
        kids[i].style.setProperty("--reveal-delay", i * 60 + "ms");
      }
    });

    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -6% 0px" }
    );
    revealables.forEach(function (el) { io.observe(el); });
  }

  /* ---- Parallax: max. 6 %, nur Desktop ---------------------------------- */
  var parallaxItems = Array.prototype.slice.call(document.querySelectorAll("[data-parallax]"));
  if (parallaxItems.length && !reduced) {
    var ticking = false;
    var applyParallax = function () {
      ticking = false;
      if (!desktop.matches) {
        parallaxItems.forEach(function (el) { el.style.transform = ""; });
        return;
      }
      var vh = window.innerHeight;
      parallaxItems.forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.bottom < -200 || r.top > vh + 200) return;
        var progress = (r.top + r.height / 2 - vh / 2) / vh; // -1 … 1
        var strength = parseFloat(el.getAttribute("data-parallax")) || 6;
        el.style.transform = "translate3d(0," + (progress * strength).toFixed(2) + "%,0)";
      });
    };
    var requestParallax = function () {
      if (!ticking) { ticking = true; requestAnimationFrame(applyParallax); }
    };
    applyParallax();
    window.addEventListener("scroll", requestParallax, { passive: true });
    window.addEventListener("resize", requestParallax);
  }

  /* ---- Sticky Split: Schritt steuert die Telefonansicht ----------------- */
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
    var stepIo = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          var idx = Array.prototype.indexOf.call(steps, entry.target);
          if (idx > -1) activate(idx);
        });
      },
      { rootMargin: "-45% 0px -45% 0px", threshold: 0 }
    );
    steps.forEach(function (s) { stepIo.observe(s); });
  });

  /* ---- Nur ein <details> pro FAQ-Gruppe offen -------------------------- */
  document.querySelectorAll("[data-faq-exclusive]").forEach(function (group) {
    var items = group.querySelectorAll("details");
    items.forEach(function (d) {
      d.addEventListener("toggle", function () {
        if (!d.open) return;
        items.forEach(function (other) { if (other !== d) other.open = false; });
      });
    });
  });

  /* ---- Warenkorb ------------------------------------------------------- */
  /* Der Shop hat noch kein Backend. Statt einen Kauf vorzutäuschen, sagt der
     Knopf, was Sache ist — siehe site/README.md, Abschnitt "Was noch fehlt". */
  document.querySelectorAll("[data-cart]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var out = btn.parentNode.querySelector("[data-cart-status]");
      if (!out) return;
      out.hidden = false;
      out.textContent =
        "Der Checkout ist noch nicht angebunden. Sobald der Shop live ist, " +
        "landet das Produkt hier im Warenkorb.";
    });
  });

  /* ---- Formulare: Demo-Modus ------------------------------------------- */
  /* Ohne Backend gibt es keinen Versand. Statt einen Erfolg vorzutäuschen,
     sagt das Formular klar, dass hier noch kein Endpunkt angebunden ist. */
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
