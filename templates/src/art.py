"""
Vektor-Kunst-Generator fuer die Vorlagen-Serie.

Erzeugt SVG-Markup fuer botanische Ranken, Ornamente und Effekt-Bausteine.
Alles rein prozedural — keine fremden Cliparts, damit die Vorlagen ohne
Lizenzfragen weiterverkauft werden koennen.

Koordinatensystem: jede Funktion liefert Pfade in ihrem eigenen viewBox-Raum,
die Aufrufer setzen den Rahmen.
"""

import math
import random


# ---------------------------------------------------------------- Hilfsmittel

def _bezier(p0, p1, p2, p3, t):
    """Punkt auf einer kubischen Bezier-Kurve."""
    u = 1 - t
    x = (u ** 3 * p0[0] + 3 * u * u * t * p1[0]
         + 3 * u * t * t * p2[0] + t ** 3 * p3[0])
    y = (u ** 3 * p0[1] + 3 * u * u * t * p1[1]
         + 3 * u * t * t * p2[1] + t ** 3 * p3[1])
    return x, y


def _bezier_tangent(p0, p1, p2, p3, t):
    """Tangentenwinkel (Grad) an der Stelle t."""
    u = 1 - t
    dx = (3 * u * u * (p1[0] - p0[0]) + 6 * u * t * (p2[0] - p1[0])
          + 3 * t * t * (p3[0] - p2[0]))
    dy = (3 * u * u * (p1[1] - p0[1]) + 6 * u * t * (p2[1] - p1[1])
          + 3 * t * t * (p3[1] - p2[1]))
    return math.degrees(math.atan2(dy, dx))


def _fmt(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


# ------------------------------------------------------------------- Blaetter

def leaf_path(cx, cy, length, width, angle, curve=0.35):
    """Ein einzelnes Blatt als geschlossener Pfad — zwei gespiegelte Boegen."""
    a = math.radians(angle)
    ca, sa = math.cos(a), math.sin(a)

    def pt(dx, dy):
        return (cx + dx * ca - dy * sa, cy + dx * sa + dy * ca)

    tip = pt(length, 0)
    base = pt(0, 0)
    c1 = pt(length * curve, -width)
    c2 = pt(length * (1 - curve), -width * 0.75)
    c3 = pt(length * (1 - curve), width * 0.75)
    c4 = pt(length * curve, width)
    return (f"M{_fmt(base[0])},{_fmt(base[1])} "
            f"C{_fmt(c1[0])},{_fmt(c1[1])} {_fmt(c2[0])},{_fmt(c2[1])} "
            f"{_fmt(tip[0])},{_fmt(tip[1])} "
            f"C{_fmt(c3[0])},{_fmt(c3[1])} {_fmt(c4[0])},{_fmt(c4[1])} "
            f"{_fmt(base[0])},{_fmt(base[1])} Z")


def round_leaf(cx, cy, r, angle, squash=0.78):
    """Rundes Eukalyptus-Blatt — leicht gestaucht, damit es organisch wirkt."""
    a = math.radians(angle)
    k = 0.5523 * r
    pts = []
    for dx, dy in ((0, -r), (r, 0), (0, r), (-r, 0)):
        pts.append((dx, dy * squash))
    ca, sa = math.cos(a), math.sin(a)

    def rot(p):
        return (cx + p[0] * ca - p[1] * sa, cy + p[0] * sa + p[1] * ca)

    top, right, bottom, left = [rot(p) for p in pts]
    kx, ky = k, k * squash
    c = [rot((kx, -r * squash)), rot((r, -ky)),
         rot((r, ky)), rot((kx, r * squash)),
         rot((-kx, r * squash)), rot((-r, ky)),
         rot((-r, -ky)), rot((-kx, -r * squash))]
    return (f"M{_fmt(top[0])},{_fmt(top[1])} "
            f"C{_fmt(c[0][0])},{_fmt(c[0][1])} {_fmt(c[1][0])},{_fmt(c[1][1])} {_fmt(right[0])},{_fmt(right[1])} "
            f"C{_fmt(c[2][0])},{_fmt(c[2][1])} {_fmt(c[3][0])},{_fmt(c[3][1])} {_fmt(bottom[0])},{_fmt(bottom[1])} "
            f"C{_fmt(c[4][0])},{_fmt(c[4][1])} {_fmt(c[5][0])},{_fmt(c[5][1])} {_fmt(left[0])},{_fmt(left[1])} "
            f"C{_fmt(c[6][0])},{_fmt(c[6][1])} {_fmt(c[7][0])},{_fmt(c[7][1])} {_fmt(top[0])},{_fmt(top[1])} Z")


def ovate_leaf(bx, by, length, width, angle, *, belly=0.34, tip_round=0.86):
    """
    Ovales Blatt, das mit der Spitze am Stiel ansetzt — so wachsen Blaetter
    wirklich. Der Unterschied zu einem Kreis auf einem Strich ist genau das,
    was eine Vorlage nach Handzeichnung statt nach Clipart aussehen laesst.

    bx, by  Ansatzpunkt direkt auf dem Zweig
    belly   wo das Blatt am breitesten ist (0 = am Ansatz, 1 = an der Spitze)
    """
    a = math.radians(angle)
    ca, sa = math.cos(a), math.sin(a)

    def pt(dx, dy):
        return (bx + dx * ca - dy * sa, by + dx * sa + dy * ca)

    L, Wd = length, width / 2
    base = pt(0, 0)
    tip = pt(L, 0)
    up1 = pt(L * belly * 0.45, -Wd * 1.05)
    up2 = pt(L * (belly + 0.34), -Wd * tip_round)
    dn1 = pt(L * (belly + 0.34), Wd * tip_round)
    dn2 = pt(L * belly * 0.45, Wd * 1.05)
    return (f"M{_fmt(base[0])},{_fmt(base[1])} "
            f"C{_fmt(up1[0])},{_fmt(up1[1])} {_fmt(up2[0])},{_fmt(up2[1])} "
            f"{_fmt(tip[0])},{_fmt(tip[1])} "
            f"C{_fmt(dn1[0])},{_fmt(dn1[1])} {_fmt(dn2[0])},{_fmt(dn2[1])} "
            f"{_fmt(base[0])},{_fmt(base[1])} Z")


def leaf_vein(bx, by, length, angle, *, reach=0.72):
    """Mittelrippe — eine einzige feine Linie, die dem Blatt Volumen gibt."""
    a = math.radians(angle)
    ex = bx + math.cos(a) * length * reach
    ey = by + math.sin(a) * length * reach
    return (f'M{_fmt(bx)},{_fmt(by)} L{_fmt(ex)},{_fmt(ey)}')


# ------------------------------------------------------------------- Zweige

def eucalyptus_branch(p0, p1, p2, p3, *, leaves=13, r0=13.0, r1=6.5,
                      stroke="#B79C86", fill="none", stroke_width=1.4,
                      seed=7, alternate=True, spread=1.0, veins=True,
                      lean=22, aspect=1.42):
    """
    Eukalyptus-Zweig entlang einer Bezier-Spine.

    Die Blaetter sitzen mit dem Ansatz direkt auf dem Zweig, neigen sich zur
    Spitze hin und werden kleiner. Genau diese drei Eigenschaften trennen eine
    gezeichnete Ranke von einer Reihe Kreise auf einer Linie.

    lean    Neigung der Blaetter in Wuchsrichtung (Grad)
    aspect  Laenge zu Breite eines Blatts; 1.0 waere kreisrund
    """
    rnd = random.Random(seed)
    spine = (f"M{_fmt(p0[0])},{_fmt(p0[1])} C{_fmt(p1[0])},{_fmt(p1[1])} "
             f"{_fmt(p2[0])},{_fmt(p2[1])} {_fmt(p3[0])},{_fmt(p3[1])}")
    out = [f'<path d="{spine}" fill="none" stroke="{stroke}" '
           f'stroke-width="{stroke_width}" stroke-linecap="round"/>']

    for i in range(leaves):
        t = 0.05 + (i / max(leaves - 1, 1)) * 0.95
        x, y = _bezier(p0, p1, p2, p3, t)
        tangent = _bezier_tangent(p0, p1, p2, p3, t)
        taper = (1 - t) ** 0.7
        r = r1 + (r0 - r1) * taper
        r *= 0.86 + rnd.random() * 0.28
        side = 1 if (i % 2 == 0 or not alternate) else -1
        # 90 Grad waere rechtwinklig vom Zweig weg; lean zieht das Blatt
        # in Wuchsrichtung, wie es die Schwerkraft und das Wachstum tun.
        off = (90 - lean + rnd.uniform(-9, 9)) * side * spread
        ang = tangent + off
        length = r * aspect
        width = r * 2 / aspect * 0.92
        out.append(f'<path d="{ovate_leaf(x, y, length, width, ang)}" '
                   f'fill="{fill}" stroke="{stroke}" '
                   f'stroke-width="{stroke_width * 0.8:.2f}" stroke-linejoin="round"/>')
        if veins:
            out.append(f'<path d="{leaf_vein(x, y, length, ang)}" fill="none" '
                       f'stroke="{stroke}" stroke-width="{stroke_width * 0.45:.2f}" '
                       f'opacity="0.6" stroke-linecap="round"/>')
    return "\n".join(out)


def olive_branch(p0, p1, p2, p3, *, leaves=16, length=26.0, width=7.0,
                 stroke="#8A9A7B", fill="none", stroke_width=1.3, seed=3):
    """Schmalblaettriger Olivenzweig — feiner und strenger als Eukalyptus."""
    rnd = random.Random(seed)
    spine = (f"M{_fmt(p0[0])},{_fmt(p0[1])} C{_fmt(p1[0])},{_fmt(p1[1])} "
             f"{_fmt(p2[0])},{_fmt(p2[1])} {_fmt(p3[0])},{_fmt(p3[1])}")
    out = [f'<path d="{spine}" fill="none" stroke="{stroke}" '
           f'stroke-width="{stroke_width}" stroke-linecap="round"/>']
    for i in range(leaves):
        t = 0.05 + (i / max(leaves - 1, 1)) * 0.95
        x, y = _bezier(p0, p1, p2, p3, t)
        tangent = _bezier_tangent(p0, p1, p2, p3, t)
        taper = (1 - t) ** 0.6
        ln = length * (0.5 + 0.5 * taper) * (0.9 + rnd.random() * 0.2)
        wd = width * (0.55 + 0.45 * taper)
        side = 1 if i % 2 == 0 else -1
        ang = tangent + (42 + rnd.random() * 20) * side
        out.append(f'<path d="{leaf_path(x, y, ln, wd, ang)}" fill="{fill}" '
                   f'stroke="{stroke}" stroke-width="{stroke_width * 0.85:.2f}"/>')
    return "\n".join(out)


def sprig(bx, by, angle, *, leaves=5, length=54.0, leaf_r=11.0, curve=26.0,
          stroke="#8A9A7B", fill="none", stroke_width=1.3, seed=1,
          aspect=1.4, lean=24, veins=True, taper=0.55):
    """
    Kurzer Einzelzweig — der Baustein fuer dichtes Laub.

    Aus vielen kleinen Zweigen wird ein Bogen oder Kranz, der wirklich nach
    gebundenem Gruen aussieht. Ein einzelner langer Zweig mit Blaettern in
    gleichem Abstand sieht dagegen immer nach Vektor-Clipart aus.
    """
    rnd = random.Random(seed)
    a = math.radians(angle)
    ex = bx + math.cos(a) * length
    ey = by + math.sin(a) * length
    # leichte Kruemmung senkrecht zur Wuchsrichtung
    nx, ny = -math.sin(a), math.cos(a)
    bend = curve * rnd.uniform(-1, 1)
    c1 = (bx + math.cos(a) * length * 0.35 + nx * bend * 0.5,
          by + math.sin(a) * length * 0.35 + ny * bend * 0.5)
    c2 = (bx + math.cos(a) * length * 0.7 + nx * bend,
          by + math.sin(a) * length * 0.7 + ny * bend)
    p0, p1, p2, p3 = (bx, by), c1, c2, (ex, ey)

    out = [f'<path d="M{_fmt(bx)},{_fmt(by)} C{_fmt(c1[0])},{_fmt(c1[1])} '
           f'{_fmt(c2[0])},{_fmt(c2[1])} {_fmt(ex)},{_fmt(ey)}" fill="none" '
           f'stroke="{stroke}" stroke-width="{stroke_width}" stroke-linecap="round"/>']

    for i in range(leaves):
        t = 0.18 + (i / max(leaves - 1, 1)) * 0.82
        x, y = _bezier(p0, p1, p2, p3, t)
        tangent = _bezier_tangent(p0, p1, p2, p3, t)
        r = leaf_r * (1 - taper * t) * rnd.uniform(0.85, 1.15)
        side = 1 if i % 2 == 0 else -1
        ang = tangent + (90 - lean + rnd.uniform(-12, 12)) * side
        ln = r * aspect
        wd = r * 2 / aspect * 0.92
        out.append(f'<path d="{ovate_leaf(x, y, ln, wd, ang)}" fill="{fill}" '
                   f'stroke="{stroke}" stroke-width="{stroke_width * 0.8:.2f}" '
                   f'stroke-linejoin="round"/>')
        if veins:
            out.append(f'<path d="{leaf_vein(x, y, ln, ang)}" fill="none" '
                       f'stroke="{stroke}" stroke-width="{stroke_width * 0.42:.2f}" '
                       f'opacity="0.55" stroke-linecap="round"/>')
    # Endblatt auf der Spitze, sonst wirkt der Zweig abgeschnitten
    tip_r = leaf_r * (1 - taper) * 0.95
    out.append(f'<path d="{ovate_leaf(ex, ey, tip_r * aspect, tip_r * 2 / aspect * 0.92, angle)}" '
               f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width * 0.8:.2f}" '
               f'stroke-linejoin="round"/>')
    return "".join(out)


def foliage_arc(cx, cy, rx, ry, start_deg, end_deg, *, sprigs=20,
                stroke="#8A9A7B", fill="none", stroke_width=1.3,
                length=58.0, leaf_r=11.0, seed=1, outward=1,
                density_ends=0.45, spread=34, aspect=1.4, jitter=8):
    """
    Laub-Bogen: viele kurze Zweige entlang einer Ellipsenbahn.

    density_ends  wie stark die Zweige zu den Enden hin schrumpfen
    outward       1 = Zweige zeigen nach aussen, -1 = nach innen
    spread        Streuung der Wuchsrichtung um die Normale (Grad)
    """
    rnd = random.Random(seed)
    out = []
    for i in range(sprigs):
        t = i / max(sprigs - 1, 1)
        deg = start_deg + (end_deg - start_deg) * t
        a = math.radians(deg)
        px = cx + math.cos(a) * rx
        py = cy + math.sin(a) * ry
        # Groessen-Huellkurve: in der Mitte des Bogens am kraeftigsten
        env = math.sin(math.pi * t) ** 0.55
        scale = density_ends + (1 - density_ends) * env
        normal = math.degrees(math.atan2(math.sin(a) * rx, math.cos(a) * ry))
        ang = normal * outward + (0 if outward > 0 else 180) \
            + rnd.uniform(-spread, spread)
        out.append(sprig(px + rnd.uniform(-jitter, jitter),
                         py + rnd.uniform(-jitter, jitter), ang,
                         leaves=rnd.choice([3, 4, 5]),
                         length=length * scale * rnd.uniform(0.8, 1.2),
                         leaf_r=leaf_r * scale * rnd.uniform(0.85, 1.15),
                         curve=length * 0.3, stroke=stroke, fill=fill,
                         stroke_width=stroke_width, seed=seed * 31 + i,
                         aspect=aspect))
    return "".join(out)


def fern_frond(p0, p1, p2, p3, *, pairs=18, length=22.0, stroke="#7C8B6E",
               stroke_width=1.1, seed=11):
    """Farnwedel — sehr feine Fiedern, gut fuer Baby-Shower und Botanik."""
    rnd = random.Random(seed)
    spine = (f"M{_fmt(p0[0])},{_fmt(p0[1])} C{_fmt(p1[0])},{_fmt(p1[1])} "
             f"{_fmt(p2[0])},{_fmt(p2[1])} {_fmt(p3[0])},{_fmt(p3[1])}")
    out = [f'<path d="{spine}" fill="none" stroke="{stroke}" '
           f'stroke-width="{stroke_width}" stroke-linecap="round"/>']
    for i in range(pairs):
        t = 0.04 + (i / max(pairs - 1, 1)) * 0.96
        x, y = _bezier(p0, p1, p2, p3, t)
        tangent = _bezier_tangent(p0, p1, p2, p3, t)
        ln = length * (1 - t) ** 0.55 * (0.9 + rnd.random() * 0.2)
        for side in (1, -1):
            ang = tangent + 52 * side
            ex = x + math.cos(math.radians(ang)) * ln
            ey = y + math.sin(math.radians(ang)) * ln
            cx_ = x + math.cos(math.radians(ang - 18 * side)) * ln * 0.6
            cy_ = y + math.sin(math.radians(ang - 18 * side)) * ln * 0.6
            out.append(f'<path d="M{_fmt(x)},{_fmt(y)} Q{_fmt(cx_)},{_fmt(cy_)} '
                       f'{_fmt(ex)},{_fmt(ey)}" fill="none" stroke="{stroke}" '
                       f'stroke-width="{stroke_width * 0.75:.2f}" stroke-linecap="round"/>')
    return "\n".join(out)


# ------------------------------------------------------------------ Ornamente

def flourish(cx, cy, w, *, stroke="#B79C86", stroke_width=1.2, flip=False):
    """Symmetrisches Trenn-Ornament — ersetzt die uebliche gerade Linie."""
    h = w * 0.16
    s = -1 if flip else 1
    d = (f"M{_fmt(cx - w / 2)},{_fmt(cy)} "
         f"C{_fmt(cx - w * 0.32)},{_fmt(cy - h * s)} {_fmt(cx - w * 0.14)},{_fmt(cy - h * s)} "
         f"{_fmt(cx)},{_fmt(cy)} "
         f"C{_fmt(cx + w * 0.14)},{_fmt(cy + h * s)} {_fmt(cx + w * 0.32)},{_fmt(cy + h * s)} "
         f"{_fmt(cx + w / 2)},{_fmt(cy)}")
    dot = (f'<circle cx="{_fmt(cx)}" cy="{_fmt(cy)}" r="{_fmt(stroke_width * 1.9)}" '
           f'fill="{stroke}"/>')
    return (f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{stroke_width}" '
            f'stroke-linecap="round"/>{dot}')


def tapered_rule(cx, cy, w, *, color="#B79C86", thickness=1.6):
    """Linie, die zu beiden Enden ausduennt — wirkt teurer als eine 1px-Linie."""
    h = thickness
    d = (f"M{_fmt(cx - w / 2)},{_fmt(cy)} "
         f"Q{_fmt(cx - w / 4)},{_fmt(cy - h / 2)} {_fmt(cx)},{_fmt(cy - h / 2)} "
         f"Q{_fmt(cx + w / 4)},{_fmt(cy - h / 2)} {_fmt(cx + w / 2)},{_fmt(cy)} "
         f"Q{_fmt(cx + w / 4)},{_fmt(cy + h / 2)} {_fmt(cx)},{_fmt(cy + h / 2)} "
         f"Q{_fmt(cx - w / 4)},{_fmt(cy + h / 2)} {_fmt(cx - w / 2)},{_fmt(cy)} Z")
    return f'<path d="{d}" fill="{color}"/>'


def arch_frame(x, y, w, h, *, stroke="#B79C86", stroke_width=1.4, fill="none",
               radius_ratio=0.5):
    """Rundbogen-Rahmen — das Leitmotiv fast aller Premium-Hochzeitsvorlagen."""
    r = w * radius_ratio
    d = (f"M{_fmt(x)},{_fmt(y + h)} L{_fmt(x)},{_fmt(y + r)} "
         f"A{_fmt(r)},{_fmt(r)} 0 0 1 {_fmt(x + w)},{_fmt(y + r)} "
         f"L{_fmt(x + w)},{_fmt(y + h)} Z")
    return (f'<path d="{d}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{stroke_width}"/>')


def wreath(cx, cy, r, *, stroke="#B79C86", fill="none", stroke_width=1.3,
           seed=5, gap_deg=52, leaf_r=11, sprigs=17, length=34,
           aspect=1.35, ry=None, outward=1):
    """
    Kranz aus zwei gespiegelten Laubhaelften mit Luecke oben.

    Beide Haelften laufen von der Luecke nach unten — dadurch zeigen alle
    Blattspitzen nach unten aussen, so wie bei einem wirklich gebundenen Kranz.
    """
    ry = r if ry is None else ry
    right = foliage_arc(cx, cy, r, ry, -90 + gap_deg / 2, 90,
                        sprigs=sprigs, stroke=stroke, fill=fill,
                        stroke_width=stroke_width, length=length,
                        leaf_r=leaf_r, seed=seed, outward=outward,
                        density_ends=0.62, spread=22, aspect=aspect)
    left = foliage_arc(cx, cy, r, ry, -90 - gap_deg / 2, -270,
                       sprigs=sprigs, stroke=stroke, fill=fill,
                       stroke_width=stroke_width, length=length,
                       leaf_r=leaf_r, seed=seed + 13, outward=outward,
                       density_ends=0.62, spread=22, aspect=aspect)
    return right + left


# --------------------------------------------------------------- Effekt-Filter

def paper_grain(fid="grain", opacity=0.055, freq=0.82, octaves=4):
    """Feines Papierkorn — nimmt Flaechen das Digitale."""
    return f'''<filter id="{fid}" x="0" y="0" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency="{freq}" numOctaves="{octaves}" seed="9" result="n"/>
  <feColorMatrix in="n" type="saturate" values="0"/>
  <feComponentTransfer><feFuncA type="linear" slope="{opacity}"/></feComponentTransfer>
</filter>'''


def soft_shadow(fid="soft", dy=6, blur=14, opacity=0.28, color="0 0 0"):
    return f'''<filter id="{fid}" x="-40%" y="-40%" width="180%" height="180%">
  <feDropShadow dx="0" dy="{dy}" stdDeviation="{blur}" flood-color="rgb({color})" flood-opacity="{opacity}"/>
</filter>'''


def inner_glow(fid="glow", blur=10, color="#FFD98A"):
    return f'''<filter id="{fid}" x="-50%" y="-50%" width="200%" height="200%">
  <feGaussianBlur stdDeviation="{blur}" result="b"/>
  <feFlood flood-color="{color}" result="c"/>
  <feComposite in="c" in2="b" operator="in" result="g"/>
  <feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>'''


def gold_gradient(gid="gold", angle=105):
    """Metallischer Verlauf mit mehreren Kanten — der Kern der Folien-Optik."""
    a = math.radians(angle)
    x1, y1 = 0.5 - math.cos(a) / 2, 0.5 - math.sin(a) / 2
    x2, y2 = 0.5 + math.cos(a) / 2, 0.5 + math.sin(a) / 2
    stops = [
        (0.00, "#8A6A3A"), (0.12, "#C9A465"), (0.24, "#F3E3B8"),
        (0.34, "#FFF8E3"), (0.44, "#D9B978"), (0.58, "#A8834C"),
        (0.70, "#E8D2A0"), (0.82, "#FBF1D6"), (0.92, "#C29B5C"),
        (1.00, "#8A6A3A"),
    ]
    body = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return (f'<linearGradient id="{gid}" x1="{x1:.3f}" y1="{y1:.3f}" '
            f'x2="{x2:.3f}" y2="{y2:.3f}">{body}</linearGradient>')


def sphere_gradients(gid, base, light="#FFFFFF", shade=None):
    """
    Verlaufs-Set fuer eine 3D-Kugel: Koerper, Glanzlicht, Bodenreflex.
    Damit sehen Ballons und Kugeln plastisch aus, ohne 3D-Renderer.
    """
    shade = shade or base
    return f'''<radialGradient id="{gid}-body" cx="0.34" cy="0.28" r="0.82">
  <stop offset="0" stop-color="{light}" stop-opacity="0.92"/>
  <stop offset="0.16" stop-color="{base}" stop-opacity="0.98"/>
  <stop offset="0.72" stop-color="{base}"/>
  <stop offset="1" stop-color="{shade}"/>
</radialGradient>
<radialGradient id="{gid}-spec" cx="0.5" cy="0.5" r="0.5">
  <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.95"/>
  <stop offset="0.55" stop-color="#FFFFFF" stop-opacity="0.28"/>
  <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
</radialGradient>
<radialGradient id="{gid}-bounce" cx="0.5" cy="0.5" r="0.5">
  <stop offset="0" stop-color="{light}" stop-opacity="0.5"/>
  <stop offset="1" stop-color="{light}" stop-opacity="0"/>
</radialGradient>'''


def balloon(cx, cy, r, gid, *, tilt=-8, string=True, string_len=210,
            string_sway=34):
    """
    Ballon mit Koerper, Glanzlicht, Bodenreflex, Knoten und Schnur.
    Braucht sphere_gradients(gid, ...) in den <defs>.
    """
    ry = r * 1.14
    body = (f'<ellipse cx="{_fmt(cx)}" cy="{_fmt(cy)}" rx="{_fmt(r)}" ry="{_fmt(ry)}" '
            f'fill="url(#{gid}-body)"/>')
    spec = (f'<ellipse cx="{_fmt(cx - r * 0.34)}" cy="{_fmt(cy - ry * 0.38)}" '
            f'rx="{_fmt(r * 0.34)}" ry="{_fmt(ry * 0.26)}" fill="url(#{gid}-spec)" '
            f'transform="rotate(-24 {_fmt(cx - r * 0.34)} {_fmt(cy - ry * 0.38)})"/>')
    bounce = (f'<ellipse cx="{_fmt(cx + r * 0.28)}" cy="{_fmt(cy + ry * 0.52)}" '
              f'rx="{_fmt(r * 0.42)}" ry="{_fmt(ry * 0.22)}" fill="url(#{gid}-bounce)"/>')
    knot = (f'<path d="M{_fmt(cx - r * 0.12)},{_fmt(cy + ry * 0.98)} '
            f'L{_fmt(cx + r * 0.12)},{_fmt(cy + ry * 0.98)} '
            f'L{_fmt(cx)},{_fmt(cy + ry * 1.11)} Z" fill="url(#{gid}-body)"/>')
    parts = [body, spec, bounce, knot]
    if string:
        sy = cy + ry * 1.11
        parts.append(
            f'<path d="M{_fmt(cx)},{_fmt(sy)} '
            f'C{_fmt(cx + string_sway)},{_fmt(sy + string_len * 0.3)} '
            f'{_fmt(cx - string_sway)},{_fmt(sy + string_len * 0.65)} '
            f'{_fmt(cx + string_sway * 0.3)},{_fmt(sy + string_len)}" '
            f'fill="none" stroke="#FFFFFF" stroke-opacity="0.42" stroke-width="1.6"/>')
    g = "".join(parts)
    return (f'<g transform="rotate({tilt} {_fmt(cx)} {_fmt(cy)})">{g}</g>')


def confetti(n, w, h, colors, *, seed=4, rmin=3, rmax=11,
             shapes=("rect", "circle"), avoid=(), tries=40):
    """
    Konfetti mit Tiefenschaerfe — hintere Teile kleiner und blasser.

    avoid  Liste von (x, y, breite, hoehe): dort wird nichts gesetzt. Ohne
           solche Sperrzonen landen Schnipsel mitten in der Schrift und die
           Karte wirkt unsauber statt lebendig.
    """
    rnd = random.Random(seed)

    def blocked(x, y, pad):
        for (ax, ay, aw, ah) in avoid:
            if ax - pad <= x <= ax + aw + pad and ay - pad <= y <= ay + ah + pad:
                return True
        return False

    out = []
    for i in range(n):
        depth = rnd.random()
        size = rmin + (rmax - rmin) * (depth ** 0.8)
        for _ in range(tries):
            x, y = rnd.random() * w, rnd.random() * h
            if not blocked(x, y, size * 1.6):
                break
        else:
            continue
        col = colors[i % len(colors)]
        op = 0.32 + depth * 0.62
        rot = rnd.random() * 360
        shape = shapes[i % len(shapes)]
        if shape == "circle":
            out.append(f'<circle cx="{_fmt(x)}" cy="{_fmt(y)}" r="{_fmt(size * 0.5)}" '
                       f'fill="{col}" opacity="{op:.2f}"/>')
        else:
            out.append(f'<rect x="{_fmt(x)}" y="{_fmt(y)}" width="{_fmt(size * 1.9)}" '
                       f'height="{_fmt(size * 0.62)}" rx="{_fmt(size * 0.3)}" fill="{col}" '
                       f'opacity="{op:.2f}" transform="rotate({rot:.1f} {_fmt(x)} {_fmt(y)})"/>')
    return "\n".join(out)


def starfield(n, w, h, *, seed=2, color="#FFFFFF", rmin=0.6, rmax=2.4):
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x, y = rnd.random() * w, rnd.random() * h
        r = rmin + rnd.random() * (rmax - rmin)
        op = 0.2 + rnd.random() * 0.7
        out.append(f'<circle cx="{_fmt(x)}" cy="{_fmt(y)}" r="{_fmt(r)}" '
                   f'fill="{color}" opacity="{op:.2f}"/>')
    return "\n".join(out)


# ------------------------------------------------- Verlaeufe und Lichtstimmung

def linear_bg(gid, stops, angle=90):
    """Linearer Verlauf. stops = [(offset, farbe), ...] oder [(o, farbe, alpha)]."""
    a = math.radians(angle)
    x1, y1 = 0.5 - math.cos(a) / 2, 0.5 - math.sin(a) / 2
    x2, y2 = 0.5 + math.cos(a) / 2, 0.5 + math.sin(a) / 2
    body = ""
    for st in stops:
        o, c = st[0], st[1]
        op = f' stop-opacity="{st[2]}"' if len(st) > 2 else ""
        body += f'<stop offset="{o}" stop-color="{c}"{op}/>'
    return (f'<linearGradient id="{gid}" x1="{x1:.3f}" y1="{y1:.3f}" '
            f'x2="{x2:.3f}" y2="{y2:.3f}">{body}</linearGradient>')


def radial_bg(gid, stops, cx=0.5, cy=0.5, r=0.75):
    body = ""
    for st in stops:
        o, c = st[0], st[1]
        op = f' stop-opacity="{st[2]}"' if len(st) > 2 else ""
        body += f'<stop offset="{o}" stop-color="{c}"{op}/>'
    return (f'<radialGradient id="{gid}" cx="{cx}" cy="{cy}" r="{r}">'
            f'{body}</radialGradient>')


def glow(cx, cy, r, color, *, opacity=0.5, gid=None):
    """Weicher Lichtschein. Braucht radial_bg(gid, ...) in den defs."""
    return (f'<circle cx="{_fmt(cx)}" cy="{_fmt(cy)}" r="{_fmt(r)}" '
            f'fill="url(#{gid})" opacity="{opacity}"/>')


def bokeh(n, w, h, color, *, seed=6, rmin=8, rmax=52, opacity=0.16):
    """Unscharfe Lichtpunkte — gibt flachen Verlaeufen Tiefe."""
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x, y = rnd.random() * w, rnd.random() * h
        r = rmin + rnd.random() * (rmax - rmin)
        op = opacity * (0.35 + rnd.random() * 0.65)
        out.append(f'<circle cx="{_fmt(x)}" cy="{_fmt(y)}" r="{_fmt(r)}" '
                   f'fill="{color}" opacity="{op:.3f}"/>')
    return "".join(out)


# --------------------------------------------------------------- 3D-Bausteine

def bauble(cx, cy, r, gid, *, cap="#C9A465", string_top=0, tilt=0,
           highlight=True):
    """
    Christbaumkugel: Koerper, Glanzlicht, Bodenreflex, Kappe, Aufhaenger.
    Braucht sphere_gradients(gid, ...) in den defs.
    """
    cap_w, cap_h = r * 0.44, r * 0.30
    cap_y = cy - r - cap_h * 0.72
    parts = [
        f'<line x1="{_fmt(cx)}" y1="{_fmt(string_top)}" x2="{_fmt(cx)}" '
        f'y2="{_fmt(cap_y)}" stroke="{cap}" stroke-width="1.4" opacity="0.7"/>',
        f'<circle cx="{_fmt(cx)}" cy="{_fmt(cy)}" r="{_fmt(r)}" fill="url(#{gid}-body)"/>',
        f'<ellipse cx="{_fmt(cx + r * 0.3)}" cy="{_fmt(cy + r * 0.55)}" '
        f'rx="{_fmt(r * 0.44)}" ry="{_fmt(r * 0.26)}" fill="url(#{gid}-bounce)"/>',
    ]
    if highlight:
        parts.append(
            f'<ellipse cx="{_fmt(cx - r * 0.36)}" cy="{_fmt(cy - r * 0.4)}" '
            f'rx="{_fmt(r * 0.3)}" ry="{_fmt(r * 0.2)}" fill="url(#{gid}-spec)" '
            f'transform="rotate(-28 {_fmt(cx - r * 0.36)} {_fmt(cy - r * 0.4)})"/>')
    parts += [
        f'<path d="M{_fmt(cx - cap_w / 2)},{_fmt(cap_y + cap_h)} '
        f'L{_fmt(cx - cap_w / 2)},{_fmt(cap_y)} L{_fmt(cx + cap_w / 2)},{_fmt(cap_y)} '
        f'L{_fmt(cx + cap_w / 2)},{_fmt(cap_y + cap_h)} Z" fill="{cap}"/>',
        f'<circle cx="{_fmt(cx)}" cy="{_fmt(cap_y - r * 0.13)}" r="{_fmt(r * 0.13)}" '
        f'fill="none" stroke="{cap}" stroke-width="{_fmt(r * 0.06)}"/>',
    ]
    g = "".join(parts)
    return f'<g transform="rotate({tilt} {_fmt(cx)} {_fmt(cy)})">{g}</g>'


def snowflake(cx, cy, r, *, arms=6, color="#FFFFFF", stroke_width=1.4,
              opacity=0.85, seed=1, barbs=3):
    """Sechsstrahlige Schneeflocke mit Seitenaesten."""
    rnd = random.Random(seed)
    out = []
    for i in range(arms):
        a = math.radians(i * 360 / arms)
        ex, ey = cx + math.cos(a) * r, cy + math.sin(a) * r
        out.append(f'<line x1="{_fmt(cx)}" y1="{_fmt(cy)}" x2="{_fmt(ex)}" '
                   f'y2="{_fmt(ey)}" stroke="{color}" stroke-width="{stroke_width}" '
                   f'stroke-linecap="round"/>')
        for b in range(1, barbs + 1):
            t = b / (barbs + 1)
            bx, by = cx + math.cos(a) * r * t, cy + math.sin(a) * r * t
            bl = r * 0.3 * (1 - t) * (0.8 + rnd.random() * 0.4)
            for s in (1, -1):
                ba = a + math.radians(52 * s)
                out.append(
                    f'<line x1="{_fmt(bx)}" y1="{_fmt(by)}" '
                    f'x2="{_fmt(bx + math.cos(ba) * bl)}" '
                    f'y2="{_fmt(by + math.sin(ba) * bl)}" stroke="{color}" '
                    f'stroke-width="{stroke_width * 0.72:.2f}" stroke-linecap="round"/>')
    return f'<g opacity="{opacity}">{"".join(out)}</g>'


def snowfall(n, w, h, *, seed=3, color="#FFFFFF", avoid=(), tries=30):
    """
    Schneefall mit Tiefe: vorne gross und deckend, hinten klein und blass.

    avoid  Sperrzonen (x, y, breite, hoehe) — sonst liegen Flocken auf der
           Schrift und die Karte wirkt fleckig statt verschneit.
    """
    rnd = random.Random(seed)

    def blocked(x, y):
        return any(ax <= x <= ax + aw and ay <= y <= ay + ah
                   for (ax, ay, aw, ah) in avoid)

    out = []
    for _ in range(n):
        depth = rnd.random()
        for _ in range(tries):
            x, y = rnd.random() * w, rnd.random() * h
            if not blocked(x, y):
                break
        else:
            continue
        r = 1.1 + depth * 3.4
        op = 0.18 + depth * 0.6
        out.append(f'<circle cx="{_fmt(x)}" cy="{_fmt(y)}" r="{_fmt(r)}" '
                   f'fill="{color}" opacity="{op:.2f}"/>')
    return "".join(out)


# ------------------------------------------------------------------ Halloween

def moon(cx, cy, r, *, color="#F6E6BE", craters=7, seed=4, crater_color="#E3CE9B"):
    """Vollmond mit dezenten Kratern."""
    rnd = random.Random(seed)
    out = [f'<circle cx="{_fmt(cx)}" cy="{_fmt(cy)}" r="{_fmt(r)}" fill="{color}"/>']
    for _ in range(craters):
        a = rnd.random() * math.tau
        d = rnd.random() ** 0.6 * r * 0.76
        cr = r * (0.06 + rnd.random() * 0.13)
        out.append(f'<circle cx="{_fmt(cx + math.cos(a) * d)}" '
                   f'cy="{_fmt(cy + math.sin(a) * d)}" r="{_fmt(cr)}" '
                   f'fill="{crater_color}" opacity="{0.3 + rnd.random() * 0.35:.2f}"/>')
    return "".join(out)


def bat(cx, cy, w, *, color="#14121A", flap=0.0, rotate=0):
    """
    Fledermaus-Silhouette mit gezackter Fluegelhinterkante.

    Die Zacken sind das Erkennungsmerkmal — ohne sie liest sich die Form als
    Schnurrbart statt als Fledermaus. flap zwischen -1 und 1 hebt und senkt die
    Fluegelspitzen, damit ein Schwarm nicht aus identischen Stempeln besteht.

    Der Pfad laeuft in einem Zug: vom Kopf ueber den linken Fluegel nach unten
    zur Schwanzspitze und ueber den rechten Fluegel zurueck.
    """
    h = w * 0.5
    lift = flap * 0.16

    def P(ux, uy):
        return f"{cx + ux * w:.2f},{cy + uy * h:.2f}"

    def wing(sgn, forward):
        """Eine Fluegelhaelfte. forward=True zeichnet vom Kopf zur Schwanzspitze."""
        knots = [
            ("C", (sgn * 0.09, -0.20), (sgn * 0.22, -0.30 - lift),
             (sgn * 0.34, -0.34 - lift * 1.4)),
            ("C", (sgn * 0.42, -0.36 - lift * 1.5), (sgn * 0.48, -0.30 - lift),
             (sgn * 0.50, -0.20 - lift)),
            ("L", (sgn * 0.41, -0.05 - lift * 0.6)),
            ("C", (sgn * 0.40, -0.16), (sgn * 0.33, -0.14), (sgn * 0.29, -0.04)),
            ("L", (sgn * 0.22, 0.10)),
            ("C", (sgn * 0.20, -0.02), (sgn * 0.14, -0.02), (sgn * 0.09, 0.06)),
        ]
        if forward:
            return " ".join(k[0] + " ".join(P(*pt) for pt in k[1:]) for k in knots)
        # rueckwaerts: Reihenfolge der Knoten und der Stuetzpunkte umdrehen
        pts = [(0.09, 0.06)]
        for k in knots:
            pts.extend(k[1:])
        pts = [(sgn * abs(x) if x else x, y) for x, y in pts]
        out, i = [], len(pts) - 1
        rev = list(reversed(pts))
        j = 1
        for k in reversed(knots):
            if k[0] == "L":
                out.append("L" + P(*rev[j]))
                j += 1
            else:
                out.append("C" + " ".join(P(*rev[j + n]) for n in range(3)))
                j += 3
        return " ".join(out)

    d = (f"M{P(0, -0.14)} " + wing(-1, True)
         + f" L{P(0, 0.30)} " + wing(1, False) + " Z")
    ears = (f'<path d="M{P(-0.05, -0.20)} L{P(-0.08, -0.44)} L{P(-0.01, -0.24)} Z" '
            f'fill="{color}"/>'
            f'<path d="M{P(0.05, -0.20)} L{P(0.08, -0.44)} L{P(0.01, -0.24)} Z" '
            f'fill="{color}"/>')
    body = (f'<ellipse cx="{_fmt(cx)}" cy="{_fmt(cy - h * 0.02)}" '
            f'rx="{_fmt(w * 0.062)}" ry="{_fmt(h * 0.26)}" fill="{color}"/>')
    return (f'<g transform="rotate({rotate} {_fmt(cx)} {_fmt(cy)})">'
            f'<path d="{d}" fill="{color}"/>{body}{ears}</g>')


def bat_swarm(n, x, y, w, h, *, seed=8, color="#14121A", size=34):
    """Schwarm: Groesse, Neigung und Fluegelstellung streuen."""
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        depth = rnd.random()
        out.append(bat(x + rnd.random() * w, y + rnd.random() * h,
                       size * (0.4 + depth * 0.85), color=color,
                       flap=rnd.uniform(-0.8, 0.9),
                       rotate=rnd.uniform(-18, 18)))
    return "".join(out)


def spider_web(cx, cy, r, *, spokes=7, rings=5, color="#6B6478",
               stroke_width=1.1, start=180, end=270, sag=0.16):
    """Eckennetz — Faeden zwischen den Speichen haengen leicht durch."""
    out = []
    a0, a1 = math.radians(start), math.radians(end)
    angs = [a0 + (a1 - a0) * i / (spokes - 1) for i in range(spokes)]
    for a in angs:
        out.append(f'<line x1="{_fmt(cx)}" y1="{_fmt(cy)}" '
                   f'x2="{_fmt(cx + math.cos(a) * r)}" y2="{_fmt(cy + math.sin(a) * r)}" '
                   f'stroke="{color}" stroke-width="{stroke_width}" opacity="0.75"/>')
    for k in range(1, rings + 1):
        rr = r * k / rings
        d = ""
        for i, a in enumerate(angs):
            px, py = cx + math.cos(a) * rr, cy + math.sin(a) * rr
            if i == 0:
                d = f"M{_fmt(px)},{_fmt(py)}"
            else:
                pa = angs[i - 1]
                mx = cx + math.cos((a + pa) / 2) * rr * (1 - sag)
                my = cy + math.sin((a + pa) / 2) * rr * (1 - sag)
                d += f" Q{_fmt(mx)},{_fmt(my)} {_fmt(px)},{_fmt(py)}"
        out.append(f'<path d="{d}" fill="none" stroke="{color}" '
                   f'stroke-width="{stroke_width * 0.85:.2f}" opacity="0.68"/>')
    return "".join(out)



def pine_garland(cx, cy, half_w, sag, *, n=19, length=20.0, stroke="#2E6247",
                 stroke_light=None, stroke_width=1.1, seed=5, up_ratio=0.42,
                 spread=26, pairs=12):
    """
    Tannengirlande entlang einer Haengekurve.

    Je Ansatzpunkt wachsen mehrere Wedel nach unten und ein kuerzerer nach
    oben. Laenge, Winkel und Dichte streuen — ohne diese Streuung sieht eine
    Girlande aus wie ein Kamm mit gleich langen Zinken.
    """
    rnd = random.Random(seed)
    stroke_light = stroke_light or stroke
    out = []

    def point(t):
        x = cx - half_w + 2 * half_w * t
        y = cy + sag * math.sin(math.pi * t)
        return x, y

    for i in range(n):
        t = i / (n - 1)
        x, y = point(t)
        x2, y2 = point(min(t + 0.01, 1.0))
        tangent = math.degrees(math.atan2(y2 - y, x2 - x))
        # in der Mitte haengt die Girlande am dichtesten
        env = 0.6 + 0.4 * math.sin(math.pi * t) ** 0.5
        fronds = [(90, 1.0), (90, 0.78), (90, 0.62)]
        if rnd.random() < up_ratio:
            fronds.append((-90, 0.5))
        for base_ang, scale in fronds:
            ang = tangent + base_ang + rnd.uniform(-spread, spread)
            ln = length * env * scale * rnd.uniform(0.82, 1.18)
            reach = ln * 5.2
            a = math.radians(ang)
            ex, ey = x + math.cos(a) * reach, y + math.sin(a) * reach
            bend = rnd.uniform(-0.22, 0.22)
            c1 = (x + math.cos(a) * reach * 0.35 - math.sin(a) * reach * bend * 0.5,
                  y + math.sin(a) * reach * 0.35 + math.cos(a) * reach * bend * 0.5)
            c2 = (x + math.cos(a) * reach * 0.7 - math.sin(a) * reach * bend,
                  y + math.sin(a) * reach * 0.7 + math.cos(a) * reach * bend)
            col = stroke_light if scale > 0.9 and rnd.random() < 0.35 else stroke
            out.append(fern_frond((x, y), c1, c2, (ex, ey),
                                  pairs=pairs, length=ln, stroke=col,
                                  stroke_width=stroke_width,
                                  seed=seed * 13 + i * 5 + int(scale * 10)))
    return "".join(out)
