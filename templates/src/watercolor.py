"""
Aquarell-Renderer. NOCH NICHT IN EINER VORLAGE VERWENDET.

Der Versuch, gemalt wirkende Motive zu erzeugen statt Vektorflaechen. Das
Ergebnis kommt naeher, liest sich aber weiterhin als Vektor mit rauem Filter
und nicht als Aquarell — darum steht der Baustein hier, wird aber von keiner
Suite eingebunden. Wer ihn weiterfuehrt, findet unten die vier Eigenschaften,
auf die es ankommt.


Eine Vektorfläche mit glattem Rand liest sich immer als Clipart. Echtes
Aquarell hat vier Eigenschaften, und alle vier lassen sich in SVG erzeugen:

  1. Unruhiger Rand      Das Papier saugt ungleichmäßig — die Kontur zittert.
                         feTurbulence + feDisplacementMap.
  2. Randpigment         Beim Trocknen wandert Pigment nach außen und sammelt
                         sich als dunklerer Saum. feMorphology + Komposit.
  3. Granulation         Pigmentkörner setzen sich in der Papierstruktur ab.
                         Feines Rauschen, multiplikativ auf die Fläche.
  4. Lasuren             Mehrere halbtransparente Schichten mit leichtem
                         Versatz ergeben die Tiefe, die eine einzelne Fläche
                         nie hat.

Die Schichten bekommen unterschiedliche Seeds, damit ihre Ränder auseinander
laufen. Genau dieses Auseinanderlaufen ist der Effekt.
"""

import math
import random

from art import _fmt


def wc_filter(fid, *, seed=1, warp=13.0, freq=0.014, octaves=3,
              rim=2.6, rim_blur=1.6, granulation=0.42, grain_freq=0.85,
              soften=0.5):
    """
    Ein Aquarell-Filter. Reihenfolge ist wichtig: erst verzerren, dann den
    Randsaum aus der verzerrten Form ableiten, zuletzt Granulation auflegen.
    """
    return f'''<filter id="{fid}" x="-30%" y="-30%" width="160%" height="160%"
        color-interpolation-filters="sRGB">
  <feTurbulence type="fractalNoise" baseFrequency="{freq}" numOctaves="{octaves}"
                seed="{seed}" result="warpNoise"/>
  <feDisplacementMap in="SourceGraphic" in2="warpNoise" scale="{warp}"
                     xChannelSelector="R" yChannelSelector="G" result="shape"/>
  <feGaussianBlur in="shape" stdDeviation="{soften}" result="shapeSoft"/>

  <feMorphology in="shapeSoft" operator="erode" radius="{rim}" result="core"/>
  <feComposite in="shapeSoft" in2="core" operator="out" result="rimBand"/>
  <feGaussianBlur in="rimBand" stdDeviation="{rim_blur}" result="rimSoft"/>

  <feTurbulence type="fractalNoise" baseFrequency="{grain_freq}" numOctaves="4"
                seed="{seed * 7 + 3}" result="grainNoise"/>
  <feColorMatrix in="grainNoise" type="saturate" values="0" result="grainGrey"/>
  <feComponentTransfer in="grainGrey" result="grainAlpha">
    <feFuncA type="linear" slope="{granulation}" intercept="-{granulation * 0.42:.3f}"/>
  </feComponentTransfer>
  <feComposite in="grainAlpha" in2="shapeSoft" operator="in" result="grain"/>

  <feMerge>
    <feMergeNode in="shapeSoft"/>
    <feMergeNode in="rimSoft"/>
    <feMergeNode in="grain"/>
  </feMerge>
</filter>'''


def wc_defs(base, n=4, **kw):
    """Ein Satz Filter mit verschiedenen Seeds — einer je Lasur, dazu ein
    weicher fuer grossflaechige Fluesse und Schattierungen."""
    out = [wc_filter(f"{base}{i}", seed=1 + i * 17, **kw) for i in range(n)]
    out.append(soft_filter(f"{base}soft"))
    return "".join(out)


def washes(path_d, color, base, *, layers=3, opacity=0.30, jitter=2.2,
           scale_step=0.012, seed=5, rotate=0.0, cx=0, cy=0):
    """
    Dieselbe Form mehrfach übereinander, jede mit eigenem Filter, leichtem
    Versatz und minimal anderer Größe. Erst dadurch entsteht die Tiefe.
    """
    rnd = random.Random(seed)
    out = []
    for i in range(layers):
        dx = rnd.uniform(-jitter, jitter)
        dy = rnd.uniform(-jitter, jitter)
        sc = 1 + rnd.uniform(-scale_step, scale_step)
        rot = rotate + rnd.uniform(-0.8, 0.8)
        op = opacity * (1.0 if i == 0 else rnd.uniform(0.72, 1.0))
        out.append(
            f'<g transform="translate({_fmt(dx)},{_fmt(dy)}) '
            f'rotate({rot:.2f} {_fmt(cx)} {_fmt(cy)}) '
            f'translate({_fmt(cx)},{_fmt(cy)}) scale({sc:.4f}) '
            f'translate({_fmt(-cx)},{_fmt(-cy)})">'
            f'<path d="{path_d}" fill="{color}" opacity="{op:.3f}" '
            f'filter="url(#{base}{i % 4})"/></g>')
    return "".join(out)


def soft_filter(fid, *, blur=18, seed=5, freq=0.010, warp=22):
    """Weicher Verlauf fuer grosse Fluesse — ohne die starke Weichzeichnung
    bleibt ein Farbfleck eine Flaeche mit ausgefranster Kante."""
    return f'''<filter id="{fid}" x="-45%" y="-45%" width="190%" height="190%"
        color-interpolation-filters="sRGB">
  <feTurbulence type="fractalNoise" baseFrequency="{freq}" numOctaves="3"
                seed="{seed}" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="{warp}"
                     xChannelSelector="R" yChannelSelector="G" result="d"/>
  <feGaussianBlur in="d" stdDeviation="{blur}"/>
</filter>'''


def shade(path_d, color, base, *, cover=0.5, from_bottom=True, opacity=0.22,
          seed=6, bbox=None):
    """
    Ein zweiter, dunklerer Auftrag ueber nur einen Teil der Flaeche.

    Echtes Aquarell ist innerhalb einer Flaeche nie gleichmaessig — es ist dort
    dunkler, wo sich die Farbe gesammelt hat. Genau diese Ungleichmaessigkeit
    fehlt einer Vektorfuellung, und sie herzustellen kostet nur einen Clip.
    """
    if bbox is None:
        return ""
    x, y, w, h = bbox
    cid = f"{base}-clip{seed}"
    cy0 = y + h * (1 - cover) if from_bottom else y
    return (f'<clipPath id="{cid}"><path d="{path_d}"/></clipPath>'
            f'<g clip-path="url(#{cid})">'
            f'<rect x="{_fmt(x - w)}" y="{_fmt(cy0)}" width="{_fmt(w * 3)}" '
            f'height="{_fmt(h * 1.4)}" fill="{color}" opacity="{opacity}" '
            f'filter="url(#{base}soft)"/></g>')


def bloom(cx, cy, r, color, base, *, opacity=0.22, seed=3, lobes=7):
    """
    Ein Farbfleck mit ausgefransten Rändern — das, was entsteht, wenn nasse
    Farbe auf nasses Papier trifft. Gut als Hintergrundhauch hinter Objekten.
    """
    rnd = random.Random(seed)
    pts = []
    for i in range(lobes):
        a = i * math.tau / lobes
        rr = r * rnd.uniform(0.74, 1.22)
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    d = f"M{_fmt(pts[0][0])},{_fmt(pts[0][1])}"
    for i in range(lobes):
        p = pts[(i + 1) % lobes]
        prev = pts[i]
        mx = (prev[0] + p[0]) / 2 + rnd.uniform(-r * 0.18, r * 0.18)
        my = (prev[1] + p[1]) / 2 + rnd.uniform(-r * 0.18, r * 0.18)
        d += f" Q{_fmt(mx)},{_fmt(my)} {_fmt(p[0])},{_fmt(p[1])}"
    d += " Z"
    return (f'<path d="{d}" fill="{color}" opacity="{opacity:.3f}" '
            f'filter="url(#{base}soft)"/>')


def ink_stroke(points, base_width, *, color="#2A2724", opacity=0.8, seed=4,
               vary=0.55, fid=None):
    """
    Federstrich mit wechselndem Druck. Die Breite schwankt entlang der Linie —
    ein gleichmaessiger Strich ist das sicherste Erkennungszeichen von Vektor.
    """
    from ornament import tapered_curve
    rnd = random.Random(seed)
    n = len(points)
    wds = []
    phase = rnd.uniform(0, math.tau)
    for i in range(n):
        t = i / max(n - 1, 1)
        # zwei ueberlagerte Wellen, damit das Muster nicht periodisch wirkt
        m = (math.sin(t * 5.3 + phase) * 0.6 + math.sin(t * 11.7 + phase * 2) * 0.4)
        wds.append(base_width * (1 + vary * m * 0.5) * 0.5)
    f = f' filter="url(#{fid})"' if fid else ""
    return (f'<path d="{tapered_curve(points, wds)}" fill="{color}" '
            f'opacity="{opacity}"{f}/>')


def sample_path(cmds, steps=90):
    """Punkte entlang einer Folge kubischer Bezier-Segmente."""
    from art import _bezier
    pts = []
    per = max(2, steps // max(len(cmds), 1))
    for (p0, p1, p2, p3) in cmds:
        for i in range(per):
            pts.append(_bezier(p0, p1, p2, p3, i / (per - 1)))
    return pts


def ink_line(path_d, *, color="#2A2724", width=1.5, opacity=0.85, fid=None):
    """
    Lose Konturlinie. Sie folgt der Fläche absichtlich nicht exakt — bei
    Aquarell mit Federzeichnung liegt die Linie nie deckungsgleich auf dem
    Farbauftrag, und genau das macht die Handschrift aus.
    """
    f = f' filter="url(#{fid})"' if fid else ""
    return (f'<path d="{path_d}" fill="none" stroke="{color}" '
            f'stroke-width="{width}" stroke-linecap="round" '
            f'stroke-linejoin="round" opacity="{opacity}"{f}/>')


def paper(w, h, *, fid="wcPaper", tint="#6E6558", opacity=0.10):
    """Papierstruktur über der ganzen Seite — bindet die Farbaufträge ein."""
    return (f'<rect width="{w}" height="{h}" fill="{tint}" '
            f'filter="url(#{fid})" opacity="{opacity}"/>')


def paper_filter(fid="wcPaper", *, freq=0.62, octaves=5, slope=0.16):
    return f'''<filter id="{fid}" x="0" y="0" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency="{freq}" numOctaves="{octaves}"
                seed="17" result="n"/>
  <feColorMatrix in="n" type="saturate" values="0"/>
  <feComponentTransfer><feFuncA type="linear" slope="{slope}"/></feComponentTransfer>
</filter>'''


# ------------------------------------------------------------------- Objekte

def coupe_glass(cx, cy, size, base, *, glass="#BFCDD2", liquid="#E9D9A6",
                liquid_deep="#C9A85E", ink="#3A342C", ink_width=2.6,
                seed=7, bubbles=True):
    """
    Coupe-Glas als Aquarell mit Federzeichnung.

    Vier Dinge trennen das vom Vektorbild: der Farbauftrag ist innerhalb der
    Flaeche ungleichmaessig, die Fluessigkeit ist unten dichter, der Meniskus
    ist der dunkelste Punkt, und die Kontur schwankt in der Strichstaerke.
    """
    rnd = random.Random(seed)
    s_ = size / 100.0

    def W(dx, dy):
        return (cx + dx * s_, cy + dy * s_)

    def P(dx, dy):
        x, y = W(dx, dy)
        return f"{_fmt(x)},{_fmt(y)}"

    bowl_cmds = [
        (W(-50, -46), W(-49, -18), W(-30, 2), W(0, 3)),
        (W(0, 3), W(30, 2), W(49, -18), W(50, -46)),
    ]
    bowl = (f"M{P(-50, -46)} C{P(-49, -18)} {P(-30, 2)} {P(0, 3)} "
            f"C{P(30, 2)} {P(49, -18)} {P(50, -46)} Z")
    fill_ = (f"M{P(-46.5, -33)} C{P(-45, -13)} {P(-28, 0)} {P(0, 1)} "
             f"C{P(28, 0)} {P(45, -13)} {P(46.5, -33)} Z")
    stem_cmds = [(W(-4.2, 3), W(-4.0, 18), W(-3.6, 32), W(-3.5, 44))]
    stem = f"M{P(-4.5, 3)} L{P(-3.5, 44)} L{P(3.5, 44)} L{P(4.5, 3)} Z"
    foot_cmds = [
        (W(-26, 52), W(-26, 45), W(-12, 44), W(0, 44)),
        (W(0, 44), W(12, 44), W(26, 45), W(26, 52)),
    ]
    foot = (f"M{P(-26, 52)} C{P(-26, 45)} {P(-12, 44)} {P(0, 44)} "
            f"C{P(12, 44)} {P(26, 45)} {P(26, 52)} "
            f"C{P(26, 55)} {P(12, 56)} {P(0, 56)} "
            f"C{P(-12, 56)} {P(-26, 55)} {P(-26, 52)} Z")

    bx, by = cx - 52 * s_, cy - 50 * s_
    bw, bh = 104 * s_, 110 * s_

    out = [
        washes(bowl, glass, base, layers=2, opacity=0.26, jitter=1.8,
               seed=seed, cx=cx, cy=cy),
        shade(bowl, glass, base, cover=0.42, opacity=0.20, seed=seed + 1,
              bbox=(bx, by, bw, bh)),
        washes(stem, glass, base, layers=2, opacity=0.30, jitter=1.0,
               seed=seed + 4, cx=cx, cy=cy),
        washes(foot, glass, base, layers=2, opacity=0.30, jitter=1.2,
               seed=seed + 8, cx=cx, cy=cy),
        washes(fill_, liquid, base, layers=3, opacity=0.32, jitter=2.0,
               seed=seed + 12, cx=cx, cy=cy),
        # unten dichter — dort sammelt sich das Pigment
        shade(fill_, liquid_deep, base, cover=0.55, opacity=0.26,
              seed=seed + 13, bbox=(bx, cy - 36 * s_, bw, 40 * s_)),
        f'<path d="M{P(-46.5, -33)} C{P(-30, -26)} {P(30, -26)} {P(46.5, -33)}" '
        f'fill="none" stroke="{liquid_deep}" stroke-width="{_fmt(3.0 * s_)}" '
        f'opacity="0.6" filter="url(#{base}1)"/>',
    ]
    if bubbles:
        for _ in range(8):
            ux, uy = rnd.uniform(-36, 36), rnd.uniform(-27, -6)
            out.append(f'<circle cx="{_fmt(cx + ux * s_)}" cy="{_fmt(cy + uy * s_)}" '
                       f'r="{_fmt(rnd.uniform(1.0, 2.2) * s_)}" fill="#FFFDF6" '
                       f'opacity="{rnd.uniform(0.45, 0.9):.2f}"/>')
    # Federzeichnung mit wechselndem Druck, leicht neben dem Farbauftrag
    ink_g = [
        ink_stroke(sample_path(bowl_cmds, 100), ink_width * s_, color=ink,
                   opacity=0.82, seed=seed, fid=f"{base}2"),
        ink_stroke(sample_path(foot_cmds, 70), ink_width * 0.8 * s_, color=ink,
                   opacity=0.75, seed=seed + 3, fid=f"{base}0"),
        ink_stroke(sample_path(stem_cmds, 40), ink_width * 0.55 * s_, color=ink,
                   opacity=0.7, seed=seed + 5, fid=f"{base}3"),
        ink_stroke([W(4.2, 3), W(4.0, 18), W(3.6, 32), W(3.5, 44)],
                   ink_width * 0.55 * s_, color=ink, opacity=0.7, seed=seed + 6,
                   fid=f"{base}1"),
    ]
    out.append(f'<g transform="translate({_fmt(1.2 * s_)},{_fmt(-0.9 * s_)})">'
               + "".join(ink_g) + '</g>')
    return "".join(out)


def satin_bow(cx, cy, size, base, *, color="#1E1B1A", sheen="#6E6864",
              shadow="#0B0A0A", tilt=-4, tail_len=1.0, seed=11):
    """
    Schleife aus Satin statt aus Vektor.

    Drei Dinge machen den Unterschied: die Schlaufen bekommen einen Verlauf
    von der Kante zur Mitte, jede Schlaufe eine Faltenlinie, und die Bänder
    verjüngen sich zum Knoten hin. Ohne das bleibt eine Schleife ein Aufkleber.
    """
    s = size / 100.0

    def P(dx, dy):
        return f"{_fmt(dx * s)},{_fmt(dy * s)}"

    loop_l = (f"M{P(-4, -2)} C{P(-26, -32)} {P(-64, -27)} {P(-59, -4)} "
              f"C{P(-56, 13)} {P(-24, 13)} {P(-4, 3)} Z")
    loop_r = (f"M{P(4, -2)} C{P(26, -32)} {P(64, -27)} {P(59, -4)} "
              f"C{P(56, 13)} {P(24, 13)} {P(4, 3)} Z")
    tail_l = (f"M{P(-5, 4)} C{P(-15, 27 * tail_len)} {P(-32, 46 * tail_len)} "
              f"{P(-45, 58 * tail_len)} L{P(-27, 60 * tail_len)} "
              f"C{P(-21, 41 * tail_len)} {P(-8, 20 * tail_len)} {P(0, 6)} Z")
    tail_r = (f"M{P(5, 4)} C{P(15, 27 * tail_len)} {P(32, 46 * tail_len)} "
              f"{P(45, 58 * tail_len)} L{P(27, 60 * tail_len)} "
              f"C{P(21, 41 * tail_len)} {P(8, 20 * tail_len)} {P(0, 6)} Z")
    knot = (f"M{P(-7.5, -5)} C{P(-11, 4)} {P(-11, 9)} {P(-6, 12)} "
            f"L{P(6, 12)} C{P(11, 9)} {P(11, 4)} {P(7.5, -5)} Z")

    grad = (f'<linearGradient id="{base}-satinL" x1="0" y1="0" x2="1" y2="0.4">'
            f'<stop offset="0" stop-color="{shadow}"/>'
            f'<stop offset="0.42" stop-color="{color}"/>'
            f'<stop offset="0.68" stop-color="{sheen}"/>'
            f'<stop offset="1" stop-color="{color}"/></linearGradient>'
            f'<linearGradient id="{base}-satinR" x1="1" y1="0" x2="0" y2="0.4">'
            f'<stop offset="0" stop-color="{shadow}"/>'
            f'<stop offset="0.42" stop-color="{color}"/>'
            f'<stop offset="0.68" stop-color="{sheen}"/>'
            f'<stop offset="1" stop-color="{color}"/></linearGradient>'
            f'<linearGradient id="{base}-satinT" x1="0" y1="0" x2="0.3" y2="1">'
            f'<stop offset="0" stop-color="{color}"/>'
            f'<stop offset="0.55" stop-color="{shadow}"/>'
            f'<stop offset="1" stop-color="{color}"/></linearGradient>')

    folds = (
        f'<path d="M{P(-48, -14)} C{P(-42, -22)} {P(-26, -22)} {P(-14, -11)}" '
        f'fill="none" stroke="{sheen}" stroke-width="{_fmt(1.6 * s)}" '
        f'opacity="0.42" stroke-linecap="round"/>'
        f'<path d="M{P(-40, 2)} C{P(-34, -4)} {P(-22, -3)} {P(-12, 3)}" '
        f'fill="none" stroke="{shadow}" stroke-width="{_fmt(1.3 * s)}" '
        f'opacity="0.45" stroke-linecap="round"/>'
        f'<path d="M{P(20, -13)} C{P(30, -21)} {P(46, -20)} {P(52, -11)}" '
        f'fill="none" stroke="{sheen}" stroke-width="{_fmt(1.5 * s)}" '
        f'opacity="0.38" stroke-linecap="round"/>'
        f'<path d="M{P(16, 3)} C{P(26, -3)} {P(38, -2)} {P(44, 3)}" '
        f'fill="none" stroke="{shadow}" stroke-width="{_fmt(1.2 * s)}" '
        f'opacity="0.42" stroke-linecap="round"/>')

    body = (f'<path d="{tail_l}" fill="url(#{base}-satinT)"/>'
            f'<path d="{tail_r}" fill="url(#{base}-satinT)"/>'
            f'<path d="{loop_l}" fill="url(#{base}-satinL)"/>'
            f'<path d="{loop_r}" fill="url(#{base}-satinR)"/>'
            f'{folds}'
            f'<path d="{knot}" fill="url(#{base}-satinT)"/>'
            f'<path d="M{P(-5, 6)} C{P(-2, 9)} {P(2, 9)} {P(5, 6)}" fill="none" '
            f'stroke="{sheen}" stroke-width="{_fmt(1.4 * s)}" opacity="0.35"/>')
    return (grad + f'<g transform="translate({_fmt(cx)},{_fmt(cy)}) '
            f'rotate({tilt})">{body}</g>')


def leaf_wash(bx, by, length, width, angle, base, *, color="#8FA383",
              vein="#6E8266", seed=3, layers=2, opacity=0.34):
    """Ein Blatt als Farbauftrag mit Mittelrippe statt als Kontur."""
    a = math.radians(angle)
    ca, sa = math.cos(a), math.sin(a)

    def pt(dx, dy):
        return (bx + dx * ca - dy * sa, by + dx * sa + dy * ca)

    L, Wd = length, width / 2
    base_p, tip = pt(0, 0), pt(L, 0)
    d = (f"M{_fmt(base_p[0])},{_fmt(base_p[1])} "
         f"C{_fmt(pt(L * 0.16, -Wd * 1.06)[0])},{_fmt(pt(L * 0.16, -Wd * 1.06)[1])} "
         f"{_fmt(pt(L * 0.66, -Wd * 0.88)[0])},{_fmt(pt(L * 0.66, -Wd * 0.88)[1])} "
         f"{_fmt(tip[0])},{_fmt(tip[1])} "
         f"C{_fmt(pt(L * 0.66, Wd * 0.88)[0])},{_fmt(pt(L * 0.66, Wd * 0.88)[1])} "
         f"{_fmt(pt(L * 0.16, Wd * 1.06)[0])},{_fmt(pt(L * 0.16, Wd * 1.06)[1])} "
         f"{_fmt(base_p[0])},{_fmt(base_p[1])} Z")
    mid = pt(L * 0.78, 0)
    return (washes(d, color, base, layers=layers, opacity=opacity, jitter=1.3,
                   seed=seed, cx=bx, cy=by)
            + f'<path d="M{_fmt(base_p[0])},{_fmt(base_p[1])} '
              f'L{_fmt(mid[0])},{_fmt(mid[1])}" fill="none" stroke="{vein}" '
              f'stroke-width="{_fmt(max(0.6, width * 0.05))}" opacity="0.4"/>')
