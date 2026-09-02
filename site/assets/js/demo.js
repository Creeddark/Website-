/* =========================================================================
   CONVIVIO — Live-Demo
   Alles läuft ausschließlich im Browser des Besuchers. Es wird nichts
   gesendet und nichts gespeichert. Die Texte sagen das auch so.
   ========================================================================= */
(function () {
  "use strict";

  /* ---- RSVP ------------------------------------------------------------ */
  var rsvp = document.getElementById("rsvp-form");
  if (rsvp) {
    rsvp.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!rsvp.checkValidity()) { rsvp.reportValidity(); return; }

      var name = rsvp.querySelector("#rsvp-name").value.trim() || "Ihr";
      var coming = rsvp.querySelector('input[name="attending"]:checked');
      var yes = coming && coming.value === "ja";
      var out = document.getElementById("rsvp-result");

      out.hidden = false;
      out.textContent = yes
        ? name + ", eure Zusage wäre jetzt beim Brautpaar. In dieser Demo bleibt sie in eurem Browser."
        : "Schade — auch die Absage wäre jetzt übermittelt. In dieser Demo bleibt sie in eurem Browser.";
      out.focus();
    });
  }

  /* ---- Gästebuch ------------------------------------------------------- */
  var gb = document.getElementById("guestbook-form");
  var gbList = document.getElementById("guestbook-list");
  if (gb && gbList) {
    gb.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!gb.checkValidity()) { gb.reportValidity(); return; }

      var name = document.getElementById("gb-name").value.trim();
      var msg = document.getElementById("gb-msg").value.trim();
      if (!name || !msg) return;

      var li = document.createElement("li");
      li.className = "is-new";

      var p = document.createElement("p");
      p.className = "guestbook__msg";
      p.textContent = msg;                     // textContent: kein HTML aus Nutzereingaben

      var from = document.createElement("p");
      from.className = "guestbook__from";
      from.textContent = name + " · gerade eben";

      li.appendChild(p);
      li.appendChild(from);
      gbList.insertBefore(li, gbList.firstChild);

      gb.reset();
      document.getElementById("gb-name").focus();
    });
  }

  /* ---- Foto-Upload ----------------------------------------------------- */
  var input = document.getElementById("photo-input");
  var grid = document.getElementById("photo-grid");
  if (input && grid) {
    input.addEventListener("change", function () {
      var files = Array.prototype.slice.call(input.files || []).slice(0, 12);
      files.forEach(function (file) {
        if (!/^image\//.test(file.type)) return;
        var url = URL.createObjectURL(file);
        var fig = document.createElement("div");
        fig.className = "uploader__item";
        var img = document.createElement("img");
        img.src = url;
        img.alt = "Hochgeladenes Foto: " + file.name;
        img.loading = "lazy";
        img.addEventListener("load", function () { URL.revokeObjectURL(url); });
        fig.appendChild(img);
        grid.insertBefore(fig, grid.firstChild);
      });
      input.value = "";
    });
  }

  /* ---- Gästemappe: Abschnittsnavigation --------------------------------- */
  var guide = document.querySelector("[data-guide]");
  if (guide) {
    var tabs = guide.querySelectorAll("[data-guide-tab]");
    var panels = guide.querySelectorAll("[data-guide-panel]");

    var show = function (key) {
      tabs.forEach(function (t) {
        var on = t.getAttribute("data-guide-tab") === key;
        t.setAttribute("aria-selected", String(on));
        t.tabIndex = on ? 0 : -1;
      });
      panels.forEach(function (p) {
        p.hidden = p.getAttribute("data-guide-panel") !== key;
      });
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
  }
})();
