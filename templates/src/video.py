"""
Erklaervideo: "So setzt du dein eigenes Foto ein".

Zwei Filme aus einer Quelle:

  A  howto-photo-*   1920 x 1080, rund 20 s. Ein nachgebauter Canva-Editor,
     in dem der Ablauf einmal komplett vorgefuehrt wird. Das ist der Film,
     den der Kaeufer nach dem Kauf bekommt.

  B  listing-photo-* 1080 x 1080, 12 s. Nur die Karte, das Foto fliegt in
     den Rahmen. Das ist das Video fuer die Angebotsseite: dort laeuft es
     stumm und klein, eine Bedienoberflaeche waere darin nicht lesbar.

Nicht aufgezeichnet, sondern Bild fuer Bild gerechnet: die HTML-Seite hat
eine Funktion seek(t), die den Zustand zum Zeitpunkt t setzt. Der Recorder
ruft sie fuer jedes Einzelbild auf. Dadurch ist jedes Bild exakt dort, wo
es hingehoert — eine Bildschirmaufnahme haette schwankende Bildabstaende.
"""

import base64
import json
import pathlib

from common import FONT_DIR, ASSET_DIR

ROOT = pathlib.Path(__file__).resolve().parent.parent
PREVIEWS = ROOT / "previews"
PREVIEWS_DEMO = ROOT / "previews-demo"      # dieselben Seiten mit Foto

# Je Anlass eine Szene. Der Ablauf in Canva ist immer derselbe, die Karte und
# das Foto nicht — und ein Kaeufer, der ein Baby-Set kauft, soll im Video sein
# Set sehen und nicht das der Hochzeit.
SCENES = {
    "wedding": {
        "slug": "08-times-wedding",
        "photo": "demo-wedding-landscape.png",
        "slot": (64, 462, 622, 366),          # Bildfenster auf Seite eins
        "thumbs": ["10-cover-wedding-1-cover.png",
                   "01-wedding-ambra-1-invitation.png"],
        "de": ("Hochzeitszeitung",
               "Titel &middot; Innenseite &middot; Details &middot; Dank"),
        "en": ("The wedding gazette",
               "Front &middot; Inside &middot; Details &middot; Thanks"),
    },
    "birthday": {
        "slug": "08-times-birthday",
        "photo": "demo-birthday-landscape.png",
        "slot": (64, 462, 622, 366),
        "thumbs": ["02-birthday-confetti-1-invitation.png",
                   "09-ruban-birthday-1-invitation.png"],
        "de": ("Geburtstagszeitung",
               "Titel &middot; Innenseite &middot; Details &middot; Dank"),
        "en": ("The birthday gazette",
               "Front &middot; Inside &middot; Details &middot; Thanks"),
    },
    "baby": {
        "slug": "08-times-baby",
        "photo": "demo-baby-landscape.png",
        "slot": (64, 462, 622, 366),
        "thumbs": ["04-baby-shower-1-invitation.png",
                   "09-ruban-baby-1-invitation.png"],
        "de": ("Geburtsanzeige als Zeitung",
               "Titel &middot; Innenseite &middot; Details &middot; Dank"),
        "en": ("The baby gazette",
               "Front &middot; Inside &middot; Details &middot; Thanks"),
    },
}


def _pages(slug, demo=False):
    """Die Seiten einer Suite in der richtigen Reihenfolge."""
    src = PREVIEWS_DEMO if demo else PREVIEWS
    return sorted(src.glob(f"{slug}-*.png"))

PURPLE = "#8B3DFF"
PURPLE_SOFT = "#F3E9FF"
INK = "#0E1318"
GREY = "#6B7280"
LINE = "#E6E7EB"


def _b64(path, mime):
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


def _font(fname, fam, weight):
    return (f"@font-face{{font-family:'{fam}';font-weight:{weight};"
            f"font-display:block;src:url({_b64(FONT_DIR / fname, 'font/woff2')}) "
            f"format('woff2');}}")


UI_FONTS = "\n".join([
    _font("poppins-2.woff2", "UI", "400"),
    _font("poppins-3.woff2", "UI", "600"),
    _font("poppins-4.woff2", "UI", "700"),
    _font("playfair-2.woff2", "Display", "400 900"),
])


# --------------------------------------------------------------- Bausteine ---

def _cursor():
    """Zeiger als SVG, damit er in jeder Groesse scharf bleibt."""
    return """
<div id="cur">
 <svg width="26" height="34" viewBox="0 0 26 34">
  <path d="M2,1 L2,25.5 L8.2,19.8 L12.3,29.6 L16.6,27.8 L12.6,18.2 L21,17.6 Z"
        fill="#fff" stroke="#111" stroke-width="1.6" stroke-linejoin="round"/>
 </svg>
 <div id="ring"></div>
</div>"""


RAIL = [("Design", "M4 4h7v7H4zM13 4h7v4h-7zM13 10h7v10h-7zM4 13h7v7H4z"),
        ("Elements", "M12 3l2.6 6.1L21 10l-4.7 4.3L17.6 21 12 17.7 6.4 21l1.3-6.7"
                     "L3 10l6.4-.9z"),
        ("Text", "M4 5h16v3M12 5v14M8.5 19h7"),
        ("Brand", "M12 3l8 4.5v9L12 21l-8-4.5v-9z"),
        ("Uploads", "M12 16V5M7.5 9.5L12 5l4.5 4.5M4 18.5h16"),
        ("Draw", "M4 20l3-1 11-11-2-2L5 17z"),
        ("Projects", "M4 7h6l1.6 2H20v9H4z"),
        ("Apps", "M4 4h6v6H4zM14 4h6v6h-6zM4 14h6v6H4zM14 14h6v6h-6z")]


def _rail():
    out = []
    for i, (label, d) in enumerate(RAIL):
        fill = "none"
        out.append(
            f'<div class="rail-item" id="rail{i}" style="top:{52 + i * 62}px">'
            f'<svg viewBox="0 0 24 24" width="23" height="23">'
            f'<path d="{d}" fill="{fill}" stroke="currentColor" stroke-width="1.6" '
            f'stroke-linecap="round" stroke-linejoin="round"/></svg>'
            f'<span>{label}</span></div>')
    return "".join(out)


def _panel(photo, thumbs):
    tiles = []
    for i, src in enumerate(thumbs):
        col, row = i % 2, i // 2
        tiles.append(
            f'<div class="thumb" id="th{i}" '
            f'style="left:{16 + col * 140}px;top:{{}}px">'
            f'<img src="{src}"></div>'.format(150 + row * 108))
    return f"""
<div id="panel">
  <div class="search"><svg viewBox="0 0 24 24" width="14" height="14">
    <circle cx="11" cy="11" r="6.5" fill="none" stroke="#9aa0a6" stroke-width="2"/>
    <path d="M16 16l4.5 4.5" stroke="#9aa0a6" stroke-width="2"
          stroke-linecap="round"/></svg><span>Search your uploads</span></div>
  <div class="upbtn" id="upbtn">
    <svg viewBox="0 0 24 24" width="15" height="15"><path d="M12 16V5M7.5 9.5L12 5
      l4.5 4.5M4 18.5h16" fill="none" stroke="#fff" stroke-width="1.9"
      stroke-linecap="round" stroke-linejoin="round"/></svg>
    <span id="upbtntxt">Upload files</span></div>
  <div class="ptitle" id="ptitle">Recent</div>
  {''.join(tiles)}
</div>"""


def _topbar():
    return """
<div id="top">
  <div class="logo"></div>
  <span class="mi">File</span><span class="mi">Resize</span>
  <span class="mi">Editing</span>
  <div class="share">Share</div>
</div>"""


# --------------------------------------------------------------- Film A ------

HOWTO_CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000;font-family:'UI',system-ui,sans-serif;
     -webkit-font-smoothing:antialiased}
#stage{position:relative;width:1280px;height:720px;overflow:hidden;
       background:#F5F5F7}
#top{position:absolute;left:0;top:0;width:1280px;height:44px;background:#fff;
     border-bottom:1px solid #E6E7EB;display:flex;align-items:center;
     gap:18px;padding:0 16px;z-index:5}
.logo{width:22px;height:22px;border-radius:6px;
      background:linear-gradient(135deg,#7D2AE8,#00C4CC)}
.mi{font-size:12.5px;color:#3C4043}
.share{position:absolute;right:16px;top:9px;height:26px;padding:0 16px;
       border-radius:13px;background:#8B3DFF;color:#fff;font-size:12.5px;
       font-weight:600;display:flex;align-items:center}
#rail{position:absolute;left:0;top:44px;width:72px;height:676px;background:#fff;
      border-right:1px solid #E6E7EB;z-index:4}
.rail-item{position:absolute;left:5px;width:62px;height:56px;border-radius:8px;
      display:flex;flex-direction:column;align-items:center;justify-content:center;
      gap:5px;color:#5B6167;font-size:10.5px}
.rail-item span{letter-spacing:.01em}
#panel{position:absolute;left:72px;top:44px;width:292px;height:676px;
       background:#fff;border-right:1px solid #E6E7EB;z-index:3;overflow:hidden}
.search{position:absolute;left:16px;top:16px;width:260px;height:32px;
        border-radius:8px;background:#F1F2F4;display:flex;align-items:center;
        gap:8px;padding:0 12px;font-size:11.5px;color:#9aa0a6}
.upbtn{position:absolute;left:16px;top:60px;width:260px;height:38px;
       border-radius:19px;background:#8B3DFF;color:#fff;font-size:12.5px;
       font-weight:600;display:flex;align-items:center;justify-content:center;
       gap:8px}
.ptitle{position:absolute;left:16px;top:118px;font-size:11.5px;font-weight:600;
        color:#3C4043}
.thumb{position:absolute;width:124px;height:92px;border-radius:6px;
       overflow:hidden;background:#E9EAEC}
.thumb img{width:100%;height:100%;object-fit:cover;display:block}
#card{position:absolute;width:375px;height:525px;
      box-shadow:0 4px 24px rgba(16,20,26,.14);background:#fff;z-index:2}
#card>img{width:100%;height:100%;display:block}
#slot{position:absolute;overflow:hidden;background:#EDEEF0;z-index:3}
#slot .ph{position:absolute;inset:0;display:flex;flex-direction:column;
          align-items:center;justify-content:center;gap:6px;color:#A9AEB4}
#slot img{position:absolute;width:100%;height:100%;object-fit:cover;
          display:block}
#ring2{position:absolute;border:2px solid #8B3DFF;border-radius:2px;z-index:6;
       pointer-events:none;box-shadow:0 0 0 6px rgba(139,61,255,.16)}
.handle{position:absolute;width:9px;height:9px;background:#fff;
        border:1.5px solid #8B3DFF;border-radius:50%;z-index:7}
#ghost{position:absolute;border-radius:5px;overflow:hidden;z-index:8;
       box-shadow:0 10px 26px rgba(16,20,26,.30)}
#ghost img{width:100%;height:100%;object-fit:cover;display:block}
#cur{position:absolute;z-index:20;filter:drop-shadow(0 2px 3px rgba(0,0,0,.35))}
#ring{position:absolute;left:-16px;top:-16px;width:58px;height:58px;
      border-radius:50%;border:2.5px solid #8B3DFF;opacity:0}
#cap{position:absolute;left:0;bottom:34px;width:1280px;text-align:center;
     z-index:22}
#cap span{display:inline-block;background:rgba(14,19,24,.90);color:#fff;
     font-size:20px;font-weight:600;letter-spacing:.005em;
     padding:13px 30px;border-radius:30px}
#cap b{color:#C9A8FF;font-weight:600}
#title{position:absolute;inset:0;z-index:30;background:#12161C;
       display:flex;flex-direction:column;align-items:center;
       justify-content:center;gap:14px}
#title .kick{font-size:13px;letter-spacing:.42em;color:#C9A8FF;font-weight:600}
#title h1{font-family:'Display',serif;font-size:62px;font-weight:400;
          color:#fff;letter-spacing:.005em}
#title p{font-size:17px;color:#9BA3AD}
#outro{position:absolute;inset:0;z-index:29;background:#12161C;opacity:0;
       display:flex;flex-direction:column;align-items:center;
       justify-content:center;gap:12px}
#outro h2{font-family:'Display',serif;font-size:46px;color:#fff;font-weight:400}
#outro p{font-size:16px;color:#9BA3AD}
#outro .kick{font-size:12px;letter-spacing:.4em;color:#C9A8FF;font-weight:600}
"""

HOWTO_JS = """
const S = JSON.parse(document.getElementById('cfg').textContent);
const E = id => document.getElementById(id);
const clamp = (v,a,b) => v<a?a:(v>b?b:v);
const seg = (t,a,b) => clamp((t-a)/(b-a),0,1);
const ease = p => p<.5 ? 4*p*p*p : 1-Math.pow(-2*p+2,3)/2;
const es = (t,a,b) => ease(seg(t,a,b));
const mix = (a,b,p) => a+(b-a)*p;
// weicher Ueberschwinger fuer das Einrasten
const back = p => { const c=1.70158+1, x=p-1; return 1 + (c+1)*x*x*x + c*x*x; };

const T = S.T, CAPS = S.caps;
const SLOT = S.slot, CARD_A = S.cardA, CARD_B = S.cardB;
const THUMB = S.thumb;

function cursorAt(t){
  // Wegpunkte: [zeitAnfang, zeitEnde, vonX, vonY, nachX, nachY]
  const legs = S.legs;
  let x = legs[0][2], y = legs[0][3];
  for (const [a,b,x0,y0,x1,y1] of legs){
    if (t >= a){ const p = es(t,a,b); x = mix(x0,x1,p); y = mix(y0,y1,p); }
  }
  return [x,y];
}

function seek(t){
  // --- Titel und Abspann
  E('title').style.opacity = 1 - seg(t, T.titleOut[0], T.titleOut[1]);
  E('title').style.transform =
      'scale(' + mix(1, 1.06, seg(t, T.titleOut[0], T.titleOut[1])) + ')';
  E('outro').style.opacity = seg(t, T.outro[0], T.outro[1]);

  // --- Seitenpanel
  const po = es(t, T.panel[0], T.panel[1]);
  E('panel').style.transform = 'translateX(' + mix(-292, 0, po) + 'px)';
  const cardX = mix(CARD_A, CARD_B, po);
  const zoom = mix(1, 1.045, es(t, T.zoom[0], T.zoom[1]));
  const card = E('card');
  card.style.left = cardX + 'px';
  card.style.top = S.cardY + 'px';
  card.style.transform = 'scale(' + zoom + ')';
  card.style.transformOrigin = '50% 50%';

  // --- Schienenmenue: Uploads wird aktiv
  for (let i=0;i<8;i++){
    const el = E('rail'+i), on = (i===4);
    const a = on ? seg(t, T.click[0], T.click[0]+0.18) : 0;
    const hov = on ? seg(t, T.rail[1]-0.15, T.rail[1]) * (1-a) : 0;
    el.style.background = a>0 ? 'rgba(139,61,255,'+(0.10*a)+')'
                        : (hov>0 ? 'rgba(0,0,0,'+(0.045*hov)+')' : 'transparent');
    el.style.color = a>0 ? '#8B3DFF' : '#5B6167';
  }

  // --- Miniaturen im Panel
  for (let i=0;i<3;i++){
    const el = E('th'+i);
    const p = seg(t, T.thumbs[0]+i*0.10, T.thumbs[0]+i*0.10+0.35);
    el.style.opacity = p;
    el.style.transform = 'translateY(' + mix(10,0,ease(p)) + 'px)';
  }
  if (t >= T.grab[0] && t < T.drop[1])
    E('th0').style.opacity = mix(1, 0.34, seg(t, T.grab[0], T.grab[1]));
  else if (t >= T.drop[1])
    E('th0').style.opacity = mix(0.34, 1, seg(t, T.drop[1], T.drop[1]+0.5));

  // --- Klickring
  const ring = E('ring');
  let rp = -1;
  for (const c of [T.click[0], T.dbl[0], T.dbl[0]+0.16]){
    if (t >= c && t < c+0.42) rp = (t-c)/0.42;
  }
  ring.style.opacity = rp<0 ? 0 : (1-rp)*0.85;
  ring.style.transform = 'scale(' + (rp<0 ? 0.2 : mix(0.25,1,rp)) + ')';

  // --- Zeiger
  const [cx,cy] = cursorAt(t);
  E('cur').style.transform = 'translate(' + cx + 'px,' + cy + 'px)';

  // --- Rahmen und Foto
  const slotX = SLOT.x + (cardX - CARD_B), slotY = SLOT.y;
  const slot = E('slot');
  slot.style.left = slotX+'px'; slot.style.top = slotY+'px';
  slot.style.width = SLOT.w+'px'; slot.style.height = SLOT.h+'px';

  const dragging = t >= T.grab[1] && t < T.drop[0];
  const over = seg(t, T.drop[0]-0.75, T.drop[0]-0.15);
  const snap = seg(t, T.drop[0], T.drop[1]);

  // Umrandung: erst beim Ueberfahren, dann nach dem Einrasten kurz als Blitz
  const hl = E('ring2');
  const flash = (t >= T.drop[1] && t < T.drop[1]+0.6)
                ? 1 - seg(t, T.drop[1], T.drop[1]+0.6) : 0;
  const sel = (t > T.dbl[1] && t < T.crop[1]) ? 1 : 0;
  const show = Math.max(dragging?over:0, snap>0&&snap<1?1:0, flash*0.9, sel);
  hl.style.opacity = show;
  hl.style.left = (slotX-2)+'px'; hl.style.top = (slotY-2)+'px';
  hl.style.width = (SLOT.w+4)+'px'; hl.style.height = (SLOT.h+4)+'px';
  hl.style.boxShadow = '0 0 0 ' + (6*show).toFixed(2) +
                       'px rgba(139,61,255,' + (0.16*show).toFixed(3) + ')';

  // Griffe fuer den Zuschnitt
  const hp = seg(t, T.crop[0], T.crop[0]+0.28) * (1 - seg(t, T.crop[1], T.crop[1]+0.25));
  document.querySelectorAll('.handle').forEach((h,i) => {
    h.style.opacity = hp;
    const gx = [0,.5,1,1,1,.5,0,0][i], gy = [0,0,0,.5,1,1,1,.5][i];
    h.style.left = (slotX + gx*SLOT.w - 4.5) + 'px';
    h.style.top  = (slotY + gy*SLOT.h - 4.5) + 'px';
  });

  // Platzhalter im Rahmen verschwindet, sobald das Foto drin ist
  E('ph').style.opacity = 1 - seg(t, T.drop[0]+0.10, T.drop[0]+0.35);

  // Das gezogene Bild
  const g = E('ghost');
  if (t < T.grab[0]){
    g.style.opacity = 0;
  } else if (t < T.drop[0]){
    const lift = es(t, T.grab[0], T.grab[1]);
    g.style.opacity = mix(0, 0.95, lift);
    g.style.width = THUMB.w+'px'; g.style.height = THUMB.h+'px';
    g.style.borderRadius = '5px';
    g.style.left = (cx - THUMB.w*0.42) + 'px';
    g.style.top  = (cy - THUMB.h*0.38) + 'px';
    g.style.transform = 'rotate(' + mix(0,-4,lift) + 'deg) scale(' +
                        mix(1,0.94,lift) + ')';
  } else {
    const p = snap<1 ? back(snap) : 1;
    g.style.opacity = 1;
    g.style.left = mix(cx - THUMB.w*0.42, slotX, clamp(p,0,1)) + 'px';
    g.style.top  = mix(cy - THUMB.h*0.38, slotY, clamp(p,0,1)) + 'px';
    g.style.width  = mix(THUMB.w, SLOT.w, clamp(p,0,1)) + 'px';
    g.style.height = mix(THUMB.h, SLOT.h, clamp(p,0,1)) + 'px';
    g.style.borderRadius = mix(5,0,clamp(snap*2,0,1)) + 'px';
    g.style.transform = 'rotate(' + mix(-4,0,clamp(snap*1.6,0,1)) + 'deg)';
    g.style.boxShadow = 'none';
    if (snap >= 1){
      // im Rahmen verschieben
      const rp2 = es(t, T.move[0], T.move[1]);
      const bx = mix(0, S.reposition[0], rp2), by = mix(0, S.reposition[1], rp2);
      g.querySelector('img').style.transform =
          'translate('+bx+'px,'+by+'px) scale('+mix(1,1.14,rp2)+')';
    }
  }

  // --- Bildunterschrift
  let txt = '';
  for (const c of CAPS){ if (t >= c[0] && t < c[1]) txt = c[2]; }
  const capEl = E('cap');
  if (txt){
    if (capEl.dataset.txt !== txt){ capEl.dataset.txt = txt;
      capEl.querySelector('span').innerHTML = txt; }
    let o = 1;
    for (const c of CAPS){
      if (t >= c[0] && t < c[1]){
        o = Math.min(seg(t,c[0],c[0]+0.22), 1-seg(t,c[1]-0.22,c[1]));
      }
    }
    capEl.style.opacity = o;
    capEl.style.transform = 'translateY(' + mix(8,0,seg(t, 0, 0.01)+o*0) + 'px)';
  } else { capEl.style.opacity = 0; }
}
window.seek = seek;
window.__duration = S.duration;
seek(0);
"""


def howto(lang, theme="wedding"):
    sc = SCENES[theme]
    sx, sy, sw, sh = sc["slot"]
    photo = _b64(ASSET_DIR / sc["photo"], "image/png")
    card_png = _b64(_pages(sc["slug"])[0], "image/png")
    other = [_b64(PREVIEWS / n, "image/png") for n in sc["thumbs"]
             if (PREVIEWS / n).exists()]
    while len(other) < 2:
        other.append(photo)

    # Karte: 750 x 1050 auf halbe Groesse
    SC = 0.52
    cardW, cardH = 750 * SC, 1050 * SC
    cardY = 44 + (676 - cardH) / 2 - 24
    cardA = 72 + (1280 - 72 - cardW) / 2            # Panel zu
    cardB = 72 + 292 + (1280 - 72 - 292 - cardW) / 2  # Panel offen
    slot = {"x": cardB + sx * SC, "y": cardY + sy * SC,
            "w": sw * SC, "h": sh * SC}
    thumb = {"w": 124, "h": 92}
    th0 = (16 + 72 + 62, 150 + 44 + 46)             # Mitte Miniatur 1

    T = {
        "titleOut": [1.55, 2.25],
        "rail":     [2.35, 3.25],
        "click":    [3.28, 3.70],
        "panel":    [3.45, 4.05],
        "thumbs":   [4.05, 4.70],
        "grab":     [5.55, 5.90],
        "drop":     [8.05, 8.75],
        "dbl":      [10.35, 10.75],
        "crop":     [10.80, 14.60],
        "move":     [11.70, 13.50],
        "zoom":     [15.10, 16.60],
        "outro":    [17.70, 18.45],
    }
    slot_c = (slot["x"] + slot["w"] / 2, slot["y"] + slot["h"] / 2)
    legs = [
        [0.0, 0.01, 660, 640, 660, 640],
        [2.30, 3.25, 660, 640, 36, 327],
        [4.60, 5.55, 36, 327, th0[0], th0[1]],
        [5.90, 8.05, th0[0], th0[1], slot_c[0] + 6, slot_c[1] + 4],
        [9.55, 10.35, slot_c[0] + 6, slot_c[1] + 4, slot_c[0] - 4, slot_c[1] - 2],
        [11.70, 13.50, slot_c[0] - 4, slot_c[1] - 2, slot_c[0] - 34, slot_c[1] - 20],
        [14.70, 15.40, slot_c[0] - 34, slot_c[1] - 20, 1160, 650],
    ]

    if lang == "de":
        title = ("SO GEHT&rsquo;S", "Dein Foto einsetzen",
                 "Drei Schritte in Canva &mdash; ganz ohne Vorkenntnisse")
        caps = [
            [2.45, 4.45, "<b>1</b>&nbsp;&nbsp;Links auf <b>Uploads</b> klicken "
                         "und dein Foto hochladen"],
            [5.05, 8.30, "<b>2</b>&nbsp;&nbsp;Das Foto einfach auf die Fotofläche "
                         "ziehen"],
            [8.70, 10.10, "Es rastet von selbst in den Rahmen ein"],
            [10.60, 14.55, "<b>3</b>&nbsp;&nbsp;Doppelklick, dann im Rahmen "
                           "verschieben, bis der Ausschnitt sitzt"],
            [15.20, 17.60, "Fertig. Herunterladen als PDF &mdash; und drucken."],
        ]
        outro = ("BEREIT ZUM DRUCK", "Das war alles.",
                 "Teilen &rarr; Herunterladen &rarr; PDF Druck")
        upload = "Dateien hochladen"
        recent = "Zuletzt verwendet"
        search = "Uploads durchsuchen"
    else:
        title = ("HOW IT WORKS", "Add your own photo",
                 "Three steps in Canva &mdash; no design skills needed")
        caps = [
            [2.45, 4.45, "<b>1</b>&nbsp;&nbsp;Open <b>Uploads</b> on the left and "
                         "add your picture"],
            [5.05, 8.30, "<b>2</b>&nbsp;&nbsp;Drag it onto the photo area"],
            [8.70, 10.10, "It snaps into the frame by itself"],
            [10.60, 14.55, "<b>3</b>&nbsp;&nbsp;Double-click, then drag inside the "
                           "frame until the crop looks right"],
            [15.20, 17.60, "Done. Download as PDF &mdash; and print."],
        ]
        outro = ("READY TO PRINT", "That&rsquo;s all it takes.",
                 "Share &rarr; Download &rarr; PDF Print")
        upload = "Upload files"
        recent = "Recent"
        search = "Search your uploads"

    cfg = {
        "T": T, "caps": caps, "legs": legs,
        "slot": slot, "cardA": cardA, "cardB": cardB, "cardY": cardY,
        "thumb": thumb, "reposition": [-26, -14], "duration": 19.4,
    }
    handles = "".join('<div class="handle"></div>' for _ in range(8))
    panel = _panel(photo, [photo, other[0], other[1]])
    panel = (panel.replace("Upload files", upload)
                  .replace(">Recent<", f">{recent}<")
                  .replace("Search your uploads", search))

    ph_label = "Dein Foto" if lang == "de" else "Your photo"
    return f"""<!DOCTYPE html><html lang="{lang}"><head><meta charset="utf-8">
<title>Canva — photo</title><style>
{UI_FONTS}
{HOWTO_CSS}
</style></head><body>
<div id="stage">
  {_topbar()}
  <div id="rail">{_rail()}</div>
  {panel}
  <div id="card"><img src="{card_png}"></div>
  <div id="slot"><div class="ph" id="ph">
     <svg viewBox="0 0 24 24" width="26" height="26"><rect x="3" y="5" width="18"
       height="14" rx="2" fill="none" stroke="currentColor" stroke-width="1.5"/>
       <circle cx="8.5" cy="10" r="1.6" fill="currentColor"/>
       <path d="M4 17l5-5 3.5 3.5L16 12l4 4" fill="none" stroke="currentColor"
         stroke-width="1.5" stroke-linejoin="round"/></svg>
     <span style="font-size:11px">{ph_label}</span></div></div>
  <div id="ring2"></div>{handles}
  <div id="ghost"><img src="{photo}"></div>
  {_cursor()}
  <div id="cap"><span></span></div>
  <div id="title"><div class="kick">{title[0]}</div><h1>{title[1]}</h1>
     <p>{title[2]}</p></div>
  <div id="outro"><div class="kick">{outro[0]}</div><h2>{outro[1]}</h2>
     <p>{outro[2]}</p></div>
</div>
<script type="application/json" id="cfg">{json.dumps(cfg)}</script>
<script>{HOWTO_JS}</script>
</body></html>"""


# --------------------------------------------------------------- Film B ------

LIST_CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000;font-family:'UI',system-ui,sans-serif;
     -webkit-font-smoothing:antialiased}
#stage{position:relative;width:1080px;height:1080px;overflow:hidden;
       background:#EFE9E1}
#bg{position:absolute;inset:0;
    background:radial-gradient(120% 90% at 50% 34%,#FBF7F1 0%,#EDE5DA 58%,
               #DED3C4 100%)}
#grain{position:absolute;inset:0;opacity:.5;mix-blend-mode:multiply}
.sheet{position:absolute;width:375px;height:525px;background:#fff;
       box-shadow:0 18px 44px rgba(60,44,30,.22),0 2px 6px rgba(60,44,30,.12);
       transform-origin:50% 50%}
.sheet img{width:100%;height:100%;display:block}
#hero{z-index:5}
#slot{position:absolute;overflow:hidden;z-index:6;background:#EDEEF0}
#slot img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
#ph{position:absolute;inset:0;display:flex;align-items:center;
    justify-content:center;color:#B3B7BC}
#fly{position:absolute;z-index:9;border-radius:6px;overflow:hidden;
     box-shadow:0 16px 34px rgba(40,28,18,.34);border:5px solid #fff}
#fly img{width:100%;height:100%;object-fit:cover;display:block}
#mark{position:absolute;z-index:8;border:2px dashed rgba(120,90,60,.75);
      border-radius:2px}
#cap{position:absolute;left:0;bottom:64px;width:1080px;text-align:center;
     z-index:20}
#cap .k{font-size:14px;letter-spacing:.40em;color:#9C8straight;font-weight:600;
        margin-bottom:12px}
#cap h2{font-family:'Display',serif;font-size:48px;font-weight:400;color:#2B231B;
        line-height:1.14}
#cap p{margin-top:12px;font-size:19px;color:#7A6B5B;letter-spacing:.02em}
#kick{position:absolute;left:0;top:88px;width:1080px;text-align:center;
      z-index:20;font-size:13px;letter-spacing:.44em;color:#9C8straight;
      font-weight:600}
""".replace("#9C8straight", "#9C8straight").replace("#9C8straight", "#A08C6F")

LIST_JS = """
const S = JSON.parse(document.getElementById('cfg').textContent);
const E = id => document.getElementById(id);
const clamp=(v,a,b)=>v<a?a:(v>b?b:v);
const seg=(t,a,b)=>clamp((t-a)/(b-a),0,1);
const ease=p=>p<.5?4*p*p*p:1-Math.pow(-2*p+2,3)/2;
const es=(t,a,b)=>ease(seg(t,a,b));
const mix=(a,b,p)=>a+(b-a)*p;
const back=p=>{const c=2.2,x=p-1;return 1+(c+1)*x*x*x+c*x*x;};
const T=S.T, SLOT=S.slot, HERO=S.hero, FAN=S.fan;

function seek(t){
  // Kamera: leichte Fahrt auf den Fotorahmen zu und wieder zurueck
  const inZ = es(t, T.push[0], T.push[1]);
  const outZ = es(t, T.pull[0], T.pull[1]);
  const z = mix(1, S.zoom, inZ) - mix(0, S.zoom-1, outZ);
  const px = mix(0, S.pan[0], inZ) - mix(0, S.pan[0], outZ);
  const py = mix(0, S.pan[1], inZ) - mix(0, S.pan[1], outZ);
  const world = E('world');
  world.style.transform = 'translate('+px+'px,'+py+'px) scale('+z+')';

  // Heldenkarte
  const ap = es(t, T.enter[0], T.enter[1]);
  const hero = E('hero');
  hero.style.opacity = ap;
  hero.style.left = HERO.x+'px'; hero.style.top = HERO.y+'px';
  hero.style.transform = 'translateY('+mix(26,0,ap)+'px) rotate('+
      mix(-1.6, S.heroRot, ap).toFixed(2)+'deg) scale('+mix(.96,1,ap)+')';

  // Rahmen im Blatt
  const slot=E('slot');
  slot.style.left=SLOT.x+'px'; slot.style.top=SLOT.y+'px';
  slot.style.width=SLOT.w+'px'; slot.style.height=SLOT.h+'px';
  const mk=E('mark');
  const mp = seg(t,T.mark[0],T.mark[1]) * (1-seg(t,T.land[0],T.land[0]+0.3));
  mk.style.opacity=mp;
  mk.style.left=(SLOT.x-6)+'px'; mk.style.top=(SLOT.y-6)+'px';
  mk.style.width=(SLOT.w+12)+'px'; mk.style.height=(SLOT.h+12)+'px';

  // Das fliegende Foto
  const fly=E('fly');
  const fp = seg(t, T.fly[0], T.land[0]);
  const lp = seg(t, T.land[0], T.land[1]);
  if (t < T.fly[0]) { fly.style.opacity=0; }
  else if (lp <= 0) {
    fly.style.opacity = Math.min(1, fp*4);
    const w=mix(196,196,fp), h=w*0.60;
    fly.style.width=w+'px'; fly.style.height=h+'px';
    fly.style.left = mix(S.from[0], SLOT.x+SLOT.w/2-w/2 + 46, ease(fp))+'px';
    fly.style.top  = mix(S.from[1], SLOT.y+SLOT.h/2-h/2 - 30, ease(fp))+'px';
    fly.style.transform='rotate('+mix(-13,-4,ease(fp))+'deg)';
    fly.style.borderWidth='5px'; fly.style.borderRadius='6px';
  } else {
    const p = clamp(back(lp),0,1.06);
    const w=mix(196,SLOT.w,clamp(p,0,1)), h=mix(196*0.60,SLOT.h,clamp(p,0,1));
    fly.style.opacity=1;
    fly.style.width=w+'px'; fly.style.height=h+'px';
    fly.style.left=mix(SLOT.x+SLOT.w/2-196/2+46, SLOT.x, clamp(p,0,1))+'px';
    fly.style.top =mix(SLOT.y+SLOT.h/2-196*0.30-30, SLOT.y, clamp(p,0,1))+'px';
    fly.style.transform='rotate('+mix(-4,0,clamp(lp*1.5,0,1))+'deg)';
    fly.style.borderWidth=mix(5,0,clamp(lp*1.6,0,1))+'px';
    fly.style.borderRadius=mix(6,0,clamp(lp*1.6,0,1))+'px';
    fly.style.boxShadow = lp>0.85 ? 'none' :
        '0 '+mix(16,0,lp)+'px '+mix(34,0,lp)+'px rgba(40,28,18,.34)';
  }
  E('ph').style.opacity = 1 - seg(t, T.land[0], T.land[0]+0.25);

  // Die uebrigen Blaetter faechern auf
  FAN.forEach((f,i)=>{
    const el=E('fan'+i);
    const p=es(t, T.fan[0]+i*0.16, T.fan[0]+i*0.16+0.85);
    el.style.opacity=p*0.999;
    el.style.left=f.x+'px'; el.style.top=f.y+'px';
    el.style.transform='translate('+mix(f.dx,0,p)+'px,'+mix(f.dy,0,p)+
        'px) rotate('+mix(f.r0,f.r,p).toFixed(2)+'deg) scale('+
        mix(.88,f.s,p).toFixed(3)+')';
  });

  // Text
  let cur=null;
  for (const c of S.caps){ if (t>=c[0] && t<c[1]) cur=c; }
  const cap=E('cap');
  if (cur){
    if (cap.dataset.i !== String(cur[0])){
      cap.dataset.i=String(cur[0]);
      cap.innerHTML = (cur[2]?'<div class="k">'+cur[2]+'</div>':'')+
                      '<h2>'+cur[3]+'</h2>'+(cur[4]?'<p>'+cur[4]+'</p>':'');
    }
    const o=Math.min(seg(t,cur[0],cur[0]+0.30), 1-seg(t,cur[1]-0.30,cur[1]));
    cap.style.opacity=o;
    cap.style.transform='translateY('+mix(14,0,seg(t,cur[0],cur[0]+0.45))+'px)';
  } else cap.style.opacity=0;
  E('kick').style.opacity = seg(t,0.5,1.2)*(1-seg(t,T.fan[0]-0.4,T.fan[0]));
}
window.seek=seek; window.__duration=S.duration; seek(0);
"""


def listing(lang, theme="wedding"):
    sc = SCENES[theme]
    sx, sy, sw, sh = sc["slot"]
    photo = _b64(ASSET_DIR / sc["photo"], "image/png")
    # Seite eins ohne Foto — dort fliegt es hinein. Die Begleitblaetter im
    # Faecher dagegen mit Foto, sonst stehen dort leere Kaesten.
    plain = _pages(sc["slug"])
    filled = _pages(sc["slug"], demo=True) or plain
    pngs = [_b64(plain[0], "image/png")] + [_b64(f, "image/png")
                                            for f in filled[1:4]]

    SC = 0.50
    cw, ch = 750 * SC, 1050 * SC                             # 375 x 525
    hero = {"x": (1080 - cw) / 2, "y": 268}
    slot = {"x": hero["x"] + sx * SC, "y": hero["y"] + sy * SC,
            "w": sw * SC, "h": sh * SC}
    fan = [
        {"x": hero["x"] - 268, "y": hero["y"] + 62, "dx": 74, "dy": 30,
         "r0": 0, "r": -12.0, "s": 0.78},
        {"x": hero["x"] - 150, "y": hero["y"] + 46, "dx": 46, "dy": 22,
         "r0": 0, "r": -5.5, "s": 0.82},
        {"x": hero["x"] + 214, "y": hero["y"] + 54, "dx": -62, "dy": 26,
         "r0": 0, "r": 9.5, "s": 0.80},
    ]

    T = {"enter": [0.20, 1.20], "push": [1.70, 3.00], "mark": [2.20, 2.70],
         "fly": [3.10, 3.10], "land": [4.30, 4.95], "pull": [5.60, 6.90],
         "fan": [6.55, 6.55], "outro": [9.60, 10.0]}

    if lang == "de":
        kick = "SOFORT-DOWNLOAD  &middot;  IN CANVA BEARBEITBAR"
        caps = [
            [1.30, 3.05, "", sc["de"][0], "5 &times; 7 Zoll &middot; 300 dpi"],
            [3.20, 5.90, "", "Dein eigenes Foto", "Hineinziehen &mdash; es rastet ein"],
            [6.20, 9.10, "", "Vier passende Karten", sc["de"][1]],
            [9.30, 12.0, "", "In Minuten fertig", "Bearbeiten in Canva &middot; "
                             "zu Hause drucken"],
        ]
    else:
        kick = "INSTANT DOWNLOAD  &middot;  EDITABLE IN CANVA"
        caps = [
            [1.30, 3.05, "", sc["en"][0], "5 &times; 7 inches &middot; 300 dpi"],
            [3.20, 5.90, "", "Your own photo", "Drag it in &mdash; it snaps to fit"],
            [6.20, 9.10, "", "Four matching cards", sc["en"][1]],
            [9.30, 12.0, "", "Ready in minutes", "Edit in Canva &middot; print at home"],
        ]

    cfg = {"T": T, "caps": caps, "slot": slot, "hero": hero, "fan": fan,
           "heroRot": -1.2, "zoom": 1.42, "pan": [0, -165],
           "from": [1210, 236], "duration": 12.0}

    sheets = "".join(
        f'<div class="sheet" id="fan{i}" style="opacity:0">'
        f'<img src="{pngs[i + 1]}"></div>' for i in range(len(pngs) - 1))

    return f"""<!DOCTYPE html><html lang="{lang}"><head><meta charset="utf-8">
<title>Listing — photo</title><style>
{UI_FONTS}
{LIST_CSS}
</style></head><body>
<div id="stage">
  <div id="bg"></div>
  <svg id="grain" viewBox="0 0 1080 1080" preserveAspectRatio="none">
    <filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.9"
      numOctaves="3" seed="4"/><feColorMatrix type="saturate" values="0"/>
      </filter>
    <rect width="1080" height="1080" filter="url(#g)" opacity="0.07"/></svg>
  <div id="kick">{kick}</div>
  <div id="world" style="transform-origin:50% 50%">
    {sheets}
    <div class="sheet" id="hero" style="opacity:0"><img src="{pngs[0]}"></div>
    <div id="slot"><div id="ph">
      <svg viewBox="0 0 24 24" width="30" height="30"><rect x="3" y="5" width="18"
        height="14" rx="2" fill="none" stroke="currentColor" stroke-width="1.4"/>
        <circle cx="8.5" cy="10" r="1.5" fill="currentColor"/>
        <path d="M4 17l5-5 3.5 3.5L16 12l4 4" fill="none" stroke="currentColor"
          stroke-width="1.4" stroke-linejoin="round"/></svg></div></div>
    <div id="mark" style="opacity:0"></div>
    <div id="fly" style="opacity:0"><img src="{photo}"></div>
  </div>
  <div id="cap"></div>
</div>
<script type="application/json" id="cfg">{json.dumps(cfg)}</script>
<script>{LIST_JS}</script>
</body></html>"""


# ------------------------------------------------------------------- CLI -----

if __name__ == "__main__":
    out = ROOT / "video"
    out.mkdir(exist_ok=True)
    for theme in SCENES:
        for lang in ("en", "de"):
            (out / f"howto-photo-{theme}-{lang}.html").write_text(
                howto(lang, theme), encoding="utf-8")
            (out / f"listing-photo-{theme}-{lang}.html").write_text(
                listing(lang, theme), encoding="utf-8")
    for f in sorted(out.glob("*.html")):
        print(f"{f.name:34} {f.stat().st_size // 1024} KB")
