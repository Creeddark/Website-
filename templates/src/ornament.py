"""
Generator fuer gravierte Ornamentik — Schnoerkel, Akanthus, Rahmen, Kartuschen.

Der Kern ist `tapered_curve`: ein Strich, dessen Breite sich entlang der Kurve
aendert. Genau das trennt eine Gravur von einer Vektorlinie — der Stichel wird
beim Ziehen schmaler, und eine Linie mit gleichbleibender Staerke sieht darum
immer nach Clipart aus.

Alles ist gespiegelt aufgebaut: eine Haelfte wird gerechnet, die andere per
Transform gespiegelt. So sitzt die Symmetrie exakt, wie beim Stahlstich.
"""

import math

from art import _fmt


# ------------------------------------------------------- Strich mit Verjuengung

def tapered_curve(points, widths, *, close_start=True, close_end=True):
    """
    Geschlossener Pfad um eine Mittellinie, der die angegebenen Halbbreiten
    einhaelt. points und widths muessen gleich lang sein.
    """
    n = len(points)
    if n < 2:
        return ""
    normals = []
    for i in range(n):
        if i == 0:
            dx, dy = points[1][0] - points[0][0], points[1][1] - points[0][1]
        elif i == n - 1:
            dx, dy = points[-1][0] - points[-2][0], points[-1][1] - points[-2][1]
        else:
            dx = points[i + 1][0] - points[i - 1][0]
            dy = points[i + 1][1] - points[i - 1][1]
        ln = math.hypot(dx, dy) or 1.0
        normals.append((-dy / ln, dx / ln))

    left = [(points[i][0] + normals[i][0] * widths[i],
             points[i][1] + normals[i][1] * widths[i]) for i in range(n)]
    right = [(points[i][0] - normals[i][0] * widths[i],
              points[i][1] - normals[i][1] * widths[i]) for i in range(n)]

    d = "M" + ",".join(_fmt(v) for v in left[0])
    for p in left[1:]:
        d += " L" + ",".join(_fmt(v) for v in p)
    if close_end:
        d += " L" + ",".join(_fmt(v) for v in right[-1])
    for p in reversed(right[:-1]):
        d += " L" + ",".join(_fmt(v) for v in p)
    if close_start:
        d += " Z"
    return d


# ------------------------------------------------------------------ Schnoerkel

def scroll(cx, cy, r0, *, turns=1.35, start_deg=0, decay=0.52, w0=4.4,
           w1=0.35, steps=90, direction=1):
    """
    Eingerollter Schnoerkel — die Spirale wird nach innen enger und der Strich
    duenner. Das ist das Grundelement jeder Gravur.

    r0        Aussenradius am Anfang
    decay     wie schnell sich die Spirale einrollt (kleiner = enger)
    w0, w1    Halbbreite aussen und innen
    """
    pts, wds = [], []
    total = turns * math.tau
    for i in range(steps + 1):
        t = i / steps
        ang = math.radians(start_deg) + direction * total * t
        r = r0 * math.exp(-decay * total * t / math.tau * 2)
        pts.append((cx + math.cos(ang) * r, cy + math.sin(ang) * r))
        wds.append(w1 + (w0 - w1) * (1 - t) ** 1.35)
    return tapered_curve(pts, wds)


def c_scroll(p0, p1, p2, p3, *, w0=4.0, w1=0.6, steps=64, bulge=0.5):
    """
    Geschwungener Strich entlang einer Bezier, am dicksten in der Mitte.
    Der klassische C-Bogen, aus dem Rahmenwerk gebaut ist.
    """
    pts, wds = [], []
    for i in range(steps + 1):
        t = i / steps
        u = 1 - t
        x = (u ** 3 * p0[0] + 3 * u * u * t * p1[0]
             + 3 * u * t * t * p2[0] + t ** 3 * p3[0])
        y = (u ** 3 * p0[1] + 3 * u * u * t * p1[1]
             + 3 * u * t * t * p2[1] + t ** 3 * p3[1])
        pts.append((x, y))
        # Glocke: an den Enden spitz, in der Mitte am breitesten
        bell = math.sin(math.pi * t) ** bulge
        wds.append(w1 + (w0 - w1) * bell)
    return tapered_curve(pts, wds)


def _teardrop(cx, cy, length, width, angle, *, round_base=0.62):
    """Ein Lappen: spitz an der Aussenseite, rund am Ansatz."""
    a = math.radians(angle)
    ca, sa = math.cos(a), math.sin(a)

    def P(dx, dy):
        return (cx + dx * ca - dy * sa, cy + dx * sa + dy * ca)

    tip = P(length, 0)
    b = width / 2
    return (f"M{_fmt(P(0, 0)[0])},{_fmt(P(0, 0)[1])} "
            f"C{_fmt(P(length * 0.10, -b * round_base * 1.7)[0])},"
            f"{_fmt(P(length * 0.10, -b * round_base * 1.7)[1])} "
            f"{_fmt(P(length * 0.58, -b * 0.92)[0])},{_fmt(P(length * 0.58, -b * 0.92)[1])} "
            f"{_fmt(tip[0])},{_fmt(tip[1])} "
            f"C{_fmt(P(length * 0.58, b * 0.92)[0])},{_fmt(P(length * 0.58, b * 0.92)[1])} "
            f"{_fmt(P(length * 0.10, b * round_base * 1.7)[0])},"
            f"{_fmt(P(length * 0.10, b * round_base * 1.7)[1])} "
            f"{_fmt(P(0, 0)[0])},{_fmt(P(0, 0)[1])} Z")


def acanthus(bx, by, length, width, angle, *, lobes=5, bend=-0.20, flip=1,
             lean=52, curl=1.0):
    """
    Akanthusblatt — das Ornamentblatt der Renaissance.

    Aufgebaut als Mittelrippe plus ueberlappende Lappen, nicht als eine
    Umrisslinie mit Kerben. Der Umriss-Ansatz erzeugt Saegezaehne, sobald die
    Kerbe tief genug fuer die typische Silhouette wird; ueberlappende Lappen
    verschmelzen dagegen zuverlaessig zu einer geschlossenen Form.

    Alle Teilpfade laufen gleichsinnig, damit die Nonzero-Fuellregel sie
    vereinigt statt Loecher zu stanzen.
    """
    a = math.radians(angle)
    ca, sa = math.cos(a), math.sin(a)

    def to_world(dx, dy):
        dy *= flip
        return (bx + dx * ca - dy * sa, by + dx * sa + dy * ca)

    def spine(t):
        return length * t, bend * length * math.sin(math.pi * t) * 0.5

    # Mittelrippe als sich verjuengender Koerper
    pts, wds = [], []
    for i in range(28):
        t = i / 27
        sx, sy = spine(t)
        pts.append(to_world(sx, sy))
        wds.append(width * 0.46 * (1 - t * 0.66) + width * 0.06)
    parts = [tapered_curve(pts, wds)]

    for i in range(lobes):
        t = (i + 0.28) / lobes
        sx, sy = spine(t)
        env = math.sin(math.pi * (0.22 + 0.78 * t)) * (1 - t * 0.40)
        ln = length * 0.48 * env
        wd = width * 0.92 * env
        base = to_world(sx, sy)
        parts.append(_teardrop(base[0], base[1], ln, wd,
                               angle - flip * (86 - lean - i * 7)))

    # eingerollte Spitze
    tipx, tipy = spine(1.0)
    tw = to_world(tipx, tipy)
    parts.append(scroll(tw[0], tw[1], length * 0.16 * curl, turns=0.95,
                        start_deg=angle - flip * 70, w0=width * 0.17,
                        w1=width * 0.03, direction=flip))
    return " ".join(parts)


def acanthus_pair(cx, cy, length, width, angle, *, lobes=4, spread=24,
                  color="#C6A96B"):
    """Zwei gespiegelte Akanthusblaetter — die uebliche Fuellung einer Ecke."""
    up = acanthus(cx, cy, length, width, angle - spread, lobes=lobes, flip=1)
    dn = acanthus(cx, cy, length * 0.72, width * 0.82, angle + spread,
                  lobes=max(lobes - 1, 2), flip=-1)
    return (f'<path d="{up}" fill="{color}"/>'
            f'<path d="{dn}" fill="{color}" opacity="0.8"/>')


def beading(p0, p1, *, n=9, r0=2.2, r1=1.0, color="#C6A96B"):
    """Perlschnur — Punkte, die zum Ende hin kleiner werden."""
    out = []
    for i in range(n):
        t = i / max(n - 1, 1)
        x = p0[0] + (p1[0] - p0[0]) * t
        y = p0[1] + (p1[1] - p0[1]) * t
        r = r0 + (r1 - r0) * t
        out.append(f'<circle cx="{_fmt(x)}" cy="{_fmt(y)}" r="{_fmt(r)}" fill="{color}"/>')
    return "".join(out)


def hatch(x, y, w, h, *, angle=32, gap=3.4, stroke_width=0.55, color="#C6A96B",
          opacity=0.45):
    """
    Schraffur — die parallelen Striche, mit denen ein Stecher Flaechen tont.
    Ein einzelnes Detail, das eine Zeichnung sofort nach Gravur aussehen laesst.
    """
    a = math.radians(angle)
    dx, dy = math.cos(a), math.sin(a)
    diag = math.hypot(w, h)
    lines = []
    steps = int(diag * 2 / gap)
    for i in range(-steps, steps):
        off = i * gap
        px, py = x + w / 2 - dy * off, y + h / 2 + dx * off
        lines.append(f'M{_fmt(px - dx * diag)},{_fmt(py - dy * diag)} '
                     f'L{_fmt(px + dx * diag)},{_fmt(py + dy * diag)}')
    return (f'<g clip-path="url(#hatchclip)" opacity="{opacity}">'
            f'<path d="{" ".join(lines)}" stroke="{color}" '
            f'stroke-width="{stroke_width}" fill="none"/></g>')


# ------------------------------------------------------------------ Kartuschen

def corner_flourish(x, y, size, *, color="#C6A96B", flip_x=1, flip_y=1,
                    weight=1.0):
    """
    Eckornament: gegenlaeufige Schnoerkel, eingerollte Enden, Akanthusfuellung
    und eine Perlreihe in der Diagonale. Vier Ebenen, weil ein Stich seine
    Dichte aus geschichteten Motiven bezieht, nicht aus einer dicken Linie.
    """
    s = size / 100.0
    w = weight
    parts = [
        c_scroll((2 * s, 100 * s), (2 * s, 44 * s), (44 * s, 2 * s), (100 * s, 2 * s),
                 w0=3.4 * s * w, w1=0.6 * s * w),
        c_scroll((13 * s, 88 * s), (16 * s, 48 * s), (48 * s, 16 * s), (88 * s, 13 * s),
                 w0=1.9 * s * w, w1=0.4 * s * w),
        c_scroll((26 * s, 74 * s), (30 * s, 50 * s), (50 * s, 30 * s), (74 * s, 26 * s),
                 w0=1.1 * s * w, w1=0.3 * s * w),
        scroll(100 * s, 14 * s, 11 * s, turns=1.5, start_deg=-96, w0=2.6 * s * w,
               w1=0.3 * s * w, direction=-1),
        scroll(14 * s, 100 * s, 11 * s, turns=1.5, start_deg=-6, w0=2.6 * s * w,
               w1=0.3 * s * w, direction=1),
        scroll(58 * s, 58 * s, 15 * s, turns=1.25, start_deg=135, w0=2.0 * s * w,
               w1=0.25 * s * w, direction=1),
    ]
    body = "".join(f'<path d="{d}" fill="{color}"/>' for d in parts)
    body += acanthus_pair(30 * s, 82 * s, 52 * s, 15 * s, -34, lobes=4, color=color)
    body += acanthus_pair(82 * s, 30 * s, 52 * s, 15 * s, -56, lobes=4, color=color)
    body += acanthus_pair(44 * s, 44 * s, 34 * s, 10 * s, 45, lobes=3, color=color)
    body += beading((64 * s, 64 * s), (94 * s, 94 * s), n=6, r0=1.9 * s,
                    r1=0.7 * s, color=color)
    return (f'<g transform="translate({_fmt(x)},{_fmt(y)}) '
            f'scale({flip_x},{flip_y})">{body}</g>')


def side_flourish(cx, cy, size, *, color="#C6A96B", rotate=0, weight=1.0):
    """Mittelornament fuer die Rahmenseiten — gespiegelte Schnoerkel um ein Auge."""
    s = size / 100.0
    w = weight
    half = "".join(f'<path d="{d}" fill="{color}"/>' for d in [
        c_scroll((0, 0), (26 * s, -14 * s), (54 * s, -10 * s), (72 * s, 4 * s),
                 w0=3.2 * s * w, w1=0.5 * s * w),
        scroll(74 * s, 12 * s, 11 * s, turns=1.2, start_deg=-88, w0=2.8 * s * w,
               w1=0.35 * s * w, direction=-1),
        acanthus(20 * s, -2 * s, 34 * s, 9 * s, -12, lobes=3),
    ])
    eye = (f'<circle cx="0" cy="{_fmt(2 * s)}" r="{_fmt(5.5 * s)}" fill="none" '
           f'stroke="{color}" stroke-width="{_fmt(1.5 * s * w)}"/>'
           f'<circle cx="0" cy="{_fmt(2 * s)}" r="{_fmt(2.2 * s)}" fill="{color}"/>')
    return (f'<g transform="translate({_fmt(cx)},{_fmt(cy)}) rotate({rotate})">'
            f'{half}<g transform="scale(-1,1)">{half}</g>{eye}</g>')


def engraved_frame(x, y, w, h, *, color="#C6A96B", corner=112, weight=1.0,
                   rules=True, sides=True):
    """
    Vollstaendiger Gravur-Rahmen: Haarlinien, vier Eckornamente, vier
    Seitenmotive. Das Leitmotiv der viktorianischen Einladung.
    """
    out = []
    if rules:
        for inset, sw, op in ((0, 2.0 * weight, 0.95), (7, 0.7 * weight, 0.6),
                              (13, 0.45 * weight, 0.4)):
            out.append(f'<rect x="{_fmt(x + inset)}" y="{_fmt(y + inset)}" '
                       f'width="{_fmt(w - inset * 2)}" height="{_fmt(h - inset * 2)}" '
                       f'fill="none" stroke="{color}" stroke-width="{_fmt(sw)}" '
                       f'opacity="{op}"/>')
    c = corner
    out.append(corner_flourish(x, y, c, color=color, flip_x=1, flip_y=1, weight=weight))
    out.append(corner_flourish(x + w, y, c, color=color, flip_x=-1, flip_y=1, weight=weight))
    out.append(corner_flourish(x, y + h, c, color=color, flip_x=1, flip_y=-1, weight=weight))
    out.append(corner_flourish(x + w, y + h, c, color=color, flip_x=-1, flip_y=-1,
                               weight=weight))
    if sides:
        out.append(side_flourish(x + w / 2, y + 4, c * 0.52, color=color, rotate=0,
                                 weight=weight))
        out.append(side_flourish(x + w / 2, y + h - 4, c * 0.52, color=color,
                                 rotate=180, weight=weight))
        out.append(side_flourish(x + 4, y + h / 2, c * 0.46, color=color, rotate=90,
                                 weight=weight))
        out.append(side_flourish(x + w - 4, y + h / 2, c * 0.46, color=color,
                                 rotate=-90, weight=weight))
    return "".join(out)


# ------------------------------------------------------------------ Wappentier

def swan(cx, cy, size, *, color="#F0E4CB", outline=None, outline_width=1.0):
    """
    Schwan im Profil, als ruhige Silhouette.

    Drei Verhaeltnisse tragen die Form: der Hals ist gut doppelt so hoch wie
    der Koerper, er ist schmal, und die Schwanzspitze laeuft nach hinten oben
    aus. Fehlt eines davon, liest sich die Figur als Ente.
    """
    s = size / 100.0

    def P(dx, dy):
        return f"{_fmt(cx + dx * s)},{_fmt(cy + dy * s)}"

    # Koerper mit ausgezogener Schwanzspitze in einem Zug
    body = (f"M{P(-58, -14)} "
            f"C{P(-46, -6)} {P(-40, 0)} {P(-36, 6)} "
            f"C{P(-30, -6)} {P(-14, -13)} {P(4, -12)} "
            f"C{P(30, -11)} {P(48, -2)} {P(50, 10)} "
            f"C{P(51, 20)} {P(28, 28)} {P(-2, 28)} "
            f"C{P(-28, 28)} {P(-44, 22)} {P(-48, 12)} "
            f"C{P(-52, 2)} {P(-56, -6)} {P(-58, -14)} Z")
    # Hals: schmales S, oben zum Kopf verdickt
    neck = (f"M{P(2, -8)} "
            f"C{P(-8, -28)} {P(-6, -50)} {P(8, -62)} "
            f"C{P(18, -70)} {P(31, -69)} {P(34, -60)} "
            f"C{P(36, -53)} {P(30, -49)} {P(24, -51)} "
            f"C{P(14, -55)} {P(6, -44)} {P(11, -26)} "
            f"C{P(13, -18)} {P(13, -12)} {P(12, -7)} Z")
    beak = f"M{P(33, -62)} L{P(48, -57)} L{P(33, -53)} Z"
    wing = (f"M{P(-30, 4)} "
            f"C{P(-18, -8)} {P(6, -10)} {P(26, 0)} "
            f"C{P(18, 12)} {P(-4, 19)} {P(-22, 14)} "
            f"C{P(-28, 12)} {P(-31, 8)} {P(-30, 4)} Z")
    stroke_attr = (f' stroke="{outline}" stroke-width="{_fmt(1.2 * s * outline_width)}"'
                   f' stroke-linejoin="round"' if outline else "")
    shade = "#00000018"
    return (f'<g>'
            f'<path d="{body}" fill="{color}"{stroke_attr}/>'
            f'<path d="{neck}" fill="{color}"{stroke_attr}/>'
            f'<path d="{beak}" fill="{color}"{stroke_attr}/>'
            f'<path d="{wing}" fill="{shade}"/>'
            f'<path d="{wing}" fill="none" stroke="{outline or "#00000030"}" '
            f'stroke-width="{_fmt(1.0 * s * outline_width)}"/>'
            f'<circle cx="{_fmt(cx + 27 * s)}" cy="{_fmt(cy - 61 * s)}" '
            f'r="{_fmt(2.0 * s)}" fill="#2A1A18"/></g>')


def sparkle(cx, cy, r, *, color="#F0E4CB", opacity=0.9, ratio=0.22):
    """Vierzackiger Funken — setzt Glanzpunkte neben ein Motiv."""
    k = r * ratio
    d = (f"M{_fmt(cx)},{_fmt(cy - r)} Q{_fmt(cx + k)},{_fmt(cy - k)} "
         f"{_fmt(cx + r)},{_fmt(cy)} Q{_fmt(cx + k)},{_fmt(cy + k)} "
         f"{_fmt(cx)},{_fmt(cy + r)} Q{_fmt(cx - k)},{_fmt(cy + k)} "
         f"{_fmt(cx - r)},{_fmt(cy)} Q{_fmt(cx - k)},{_fmt(cy - k)} "
         f"{_fmt(cx)},{_fmt(cy - r)} Z")
    return f'<path d="{d}" fill="{color}" opacity="{opacity}"/>'


# ----------------------------------------------------------------- Schleifen

def bow(cx, cy, size, *, color="#1A1A1A", highlight=None, tail_len=1.0,
        tilt=0):
    """
    Schleife mit zwei Schlaufen, Knoten und fallenden Baendern.

    Die Baender sind vorne breiter als am Knoten und haben eine leichte
    Drehung — ohne die wirkt eine gezeichnete Schleife wie ein Aufkleber.
    """
    s = size / 100.0

    def P(dx, dy):
        return f"{_fmt(dx * s)},{_fmt(dy * s)}"

    loop_l = (f"M{P(-4, -2)} "
              f"C{P(-26, -30)} {P(-62, -26)} {P(-58, -4)} "
              f"C{P(-55, 12)} {P(-24, 12)} {P(-4, 3)} Z")
    loop_r = (f"M{P(4, -2)} "
              f"C{P(26, -30)} {P(62, -26)} {P(58, -4)} "
              f"C{P(55, 12)} {P(24, 12)} {P(4, 3)} Z")
    tail_l = (f"M{P(-5, 4)} "
              f"C{P(-14, 26 * tail_len)} {P(-30, 44 * tail_len)} {P(-42, 56 * tail_len)} "
              f"L{P(-26, 58 * tail_len)} "
              f"C{P(-20, 40 * tail_len)} {P(-8, 20 * tail_len)} {P(0, 6)} Z")
    tail_r = (f"M{P(5, 4)} "
              f"C{P(14, 26 * tail_len)} {P(30, 44 * tail_len)} {P(42, 56 * tail_len)} "
              f"L{P(26, 58 * tail_len)} "
              f"C{P(20, 40 * tail_len)} {P(8, 20 * tail_len)} {P(0, 6)} Z")
    knot = (f"M{P(-7, -5)} C{P(-10, 4)} {P(-10, 8)} {P(-6, 11)} "
            f"L{P(6, 11)} C{P(10, 8)} {P(10, 4)} {P(7, -5)} Z")
    hi = ""
    if highlight:
        hi = (f'<path d="M{P(-46, -12)} C{P(-40, -20)} {P(-24, -20)} {P(-14, -10)}" '
              f'fill="none" stroke="{highlight}" stroke-width="{_fmt(2.2 * s)}" '
              f'stroke-linecap="round" opacity="0.5"/>'
              f'<path d="M{P(18, -12)} C{P(28, -19)} {P(42, -18)} {P(48, -10)}" '
              f'fill="none" stroke="{highlight}" stroke-width="{_fmt(2.0 * s)}" '
              f'stroke-linecap="round" opacity="0.4"/>')
    paths = "".join(f'<path d="{d}" fill="{color}"/>'
                    for d in (tail_l, tail_r, loop_l, loop_r, knot))
    return (f'<g transform="translate({_fmt(cx)},{_fmt(cy)}) rotate({tilt})">'
            f'{paths}{hi}</g>')
