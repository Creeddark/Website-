/* =========================================================================
   ATRIA — Live-Beispiele
   Alles läuft ausschließlich im Browser des Besuchers. Es wird nichts
   gesendet und nichts gespeichert. Die Texte sagen das auch so.
   ========================================================================= */
(function () {
  "use strict";

  /* ---- Anmeldung (Eventseite) ------------------------------------------ */
  var rsvp = document.getElementById("rsvp-form");
  if (rsvp) {
    rsvp.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!rsvp.checkValidity()) { rsvp.reportValidity(); return; }
      var name = (rsvp.querySelector("#rsvp-name").value || "").trim() || "Ihre Anmeldung";
      var choice = rsvp.querySelector('input[name="attending"]:checked');
      var yes = choice && choice.value === "ja";
      var out = document.getElementById("rsvp-result");
      out.hidden = false;
      out.textContent = yes
        ? name + ", Ihre Zusage wäre jetzt bei der Organisation. In diesem Beispiel bleibt sie in Ihrem Browser."
        : "Schade — auch die Absage wäre jetzt übermittelt. In diesem Beispiel bleibt sie in Ihrem Browser.";
      out.focus();
    });
  }

  /* ---- Reiter-Navigation ------------------------------------------------ */
  document.querySelectorAll("[data-guide]").forEach(function (guide) {
    var tabs = guide.querySelectorAll("[data-guide-tab]");
    var panels = guide.querySelectorAll("[data-guide-panel]");
    if (!tabs.length) return;

    var show = function (key) {
      tabs.forEach(function (t) {
        var on = t.getAttribute("data-guide-tab") === key;
        t.setAttribute("aria-selected", String(on));
        t.tabIndex = on ? 0 : -1;
      });
      panels.forEach(function (p) { p.hidden = p.getAttribute("data-guide-panel") !== key; });
    };

    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { show(t.getAttribute("data-guide-tab")); });
      t.addEventListener("keydown", function (e) {
        var dir = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
        if (!dir) return;
        e.preventDefault();
        var next = tabs[(i + dir + tabs.length) % tabs.length];
        next.focus();
        show(next.getAttribute("data-guide-tab"));
      });
    });
    show(tabs[0].getAttribute("data-guide-tab"));
  });

  /* ---- Foto in der Schadensmeldung -------------------------------------- */
  /* Zeigt nur an, dass eine Datei gewählt wurde — hochgeladen wird nichts. */
  var foto = document.getElementById("s-foto");
  if (foto) {
    foto.addEventListener("change", function () {
      var drop = foto.closest("label");
      var label = drop && drop.querySelector(".label");
      if (label && foto.files && foto.files[0]) {
        label.textContent = "Foto ausgewählt: " + foto.files[0].name.slice(0, 28);
      }
    });
  }
})();
