"""
R129 Driver UI -- R129 Wireframe Model
3D line-segment data for a stylized Mercedes-Benz R129 SL.
Retro arcade vector graphics style: edges only, no faces.

Coordinate system: X = right, Y = up, Z = forward (toward nose).
Origin at center of wheelbase, ground plane at Y=0.
Units are arbitrary (~1 unit = ~50mm real scale).
"""

# Each entry is ((x0,y0,z0), (x1,y1,z1))
# The car is roughly 9 units long, 3.6 units wide, 2.5 units tall.

_W = 1.8   # half-width
_WB = 4.5  # half-wheelbase (nose at +Z, tail at -Z)

def _mirror_x(edges):
    """Mirror edges across the X=0 center plane to get the other side."""
    mirrored = []
    for (x0, y0, z0), (x1, y1, z1) in edges:
        mirrored.append(((x0, y0, z0), (x1, y1, z1)))
        if abs(x0) > 0.01 or abs(x1) > 0.01:
            mirrored.append(((-x0, y0, z0), (-x1, y1, z1)))
    return mirrored


def _build_model():
    right_side = []

    # ── Body profile (right side) ────────────────────────────────────
    # Front bumper -> hood -> windshield -> roof/soft-top -> rear deck -> tail
    profile = [
        (_W, 0.6, 4.5),    # front bumper lower
        (_W, 0.7, 4.6),    # bumper top
        (_W, 0.8, 4.4),    # hood front edge
        (_W, 0.85, 3.0),   # hood mid
        (_W, 0.9, 1.5),    # hood rear / cowl
        (_W, 1.4, 0.8),    # windshield base (A-pillar)
        (_W, 2.1, 0.0),    # windshield top / roof front
        (_W, 2.2, -0.5),   # roof peak
        (_W, 2.1, -1.2),   # soft-top rear curve
        (_W, 1.6, -2.0),   # rear window / deck transition
        (_W, 1.2, -2.8),   # deck
        (_W, 1.0, -3.5),   # trunk
        (_W, 0.8, -4.0),   # tail panel top
        (_W, 0.5, -4.2),   # tail panel lower
        (_W, 0.3, -4.3),   # rear bumper
    ]
    for i in range(len(profile) - 1):
        right_side.append((profile[i], profile[i + 1]))

    # ── Rocker panel / sill line ─────────────────────────────────────
    sill = [
        (_W, 0.3, 4.0),
        (_W, 0.3, 2.0),
        (_W, 0.3, 0.0),
        (_W, 0.3, -2.0),
        (_W, 0.3, -3.8),
    ]
    for i in range(len(sill) - 1):
        right_side.append((sill[i], sill[i + 1]))

    # ── Door line ────────────────────────────────────────────────────
    right_side.append(((_W, 0.3, 0.2), (_W, 1.3, 0.2)))
    right_side.append(((_W, 1.3, 0.2), (_W, 1.4, 0.8)))

    # ── Wheel arches ─────────────────────────────────────────────────
    import math
    # Front wheel (center at Z=3.0, radius=0.55)
    wc_f = 3.0
    wr = 0.55
    for j in range(12):
        a0 = math.pi * j / 12
        a1 = math.pi * (j + 1) / 12
        right_side.append((
            (_W, wr * math.sin(a0), wc_f + wr * math.cos(a0)),
            (_W, wr * math.sin(a1), wc_f + wr * math.cos(a1)),
        ))

    # Rear wheel (center at Z=-2.5)
    wc_r = -2.5
    for j in range(12):
        a0 = math.pi * j / 12
        a1 = math.pi * (j + 1) / 12
        right_side.append((
            (_W, wr * math.sin(a0), wc_r + wr * math.cos(a0)),
            (_W, wr * math.sin(a1), wc_r + wr * math.cos(a1)),
        ))

    # ── Wheels (circles, visible from the side as spokes/rims) ───────
    rim_r = 0.42
    for wc in [wc_f, wc_r]:
        for j in range(16):
            a0 = 2 * math.pi * j / 16
            a1 = 2 * math.pi * (j + 1) / 16
            right_side.append((
                (_W + 0.01, rim_r * math.sin(a0), wc + rim_r * math.cos(a0)),
                (_W + 0.01, rim_r * math.sin(a1), wc + rim_r * math.cos(a1)),
            ))
        # Spokes
        for s in range(5):
            a = 2 * math.pi * s / 5
            right_side.append((
                (_W + 0.01, 0.0, wc),
                (_W + 0.01, rim_r * 0.85 * math.sin(a), wc + rim_r * 0.85 * math.cos(a)),
            ))

    # ── Cross-sections (top view structure) ──────────────────────────
    cross_z = [4.4, 3.0, 1.5, 0.0, -1.5, -3.0, -4.0]
    cross_y_top = [0.8, 0.85, 0.9, 2.2, 2.0, 1.2, 0.8]
    centerline = []
    for z, yt in zip(cross_z, cross_y_top):
        centerline.append((
            (_W, yt, z),
            (-_W, yt, z),
        ))

    # ── Front face ───────────────────────────────────────────────────
    front = []
    # Grille outline
    front.append(((-0.8, 0.6, 4.55), (0.8, 0.6, 4.55)))
    front.append(((-0.8, 0.6, 4.55), (-0.8, 0.3, 4.55)))
    front.append(((0.8, 0.6, 4.55), (0.8, 0.3, 4.55)))
    front.append(((-0.8, 0.3, 4.55), (0.8, 0.3, 4.55)))
    # Grille vertical bars
    for gx in [-0.5, -0.2, 0.0, 0.2, 0.5]:
        front.append(((gx, 0.6, 4.55), (gx, 0.3, 4.55)))
    # Star emblem (simple cross)
    front.append(((0.0, 0.65, 4.56), (0.0, 0.78, 4.56)))
    front.append(((-0.06, 0.71, 4.56), (0.06, 0.71, 4.56)))
    # Headlights
    for sign in [1, -1]:
        lx = sign * 1.4
        front.append(((lx - 0.3, 0.65, 4.5), (lx + 0.3, 0.65, 4.5)))
        front.append(((lx - 0.3, 0.55, 4.5), (lx + 0.3, 0.55, 4.5)))
        front.append(((lx - 0.3, 0.65, 4.5), (lx - 0.3, 0.55, 4.5)))
        front.append(((lx + 0.3, 0.65, 4.5), (lx + 0.3, 0.55, 4.5)))

    # ── Rear face ────────────────────────────────────────────────────
    rear = []
    rear.append(((-_W, 0.5, -4.2), (_W, 0.5, -4.2)))
    rear.append(((-_W, 0.8, -4.0), (_W, 0.8, -4.0)))
    rear.append(((-_W, 0.5, -4.2), (-_W, 0.8, -4.0)))
    rear.append(((_W, 0.5, -4.2), (_W, 0.8, -4.0)))
    # Taillights
    for sign in [1, -1]:
        tx = sign * 1.2
        rear.append(((tx - 0.4, 0.75, -4.15), (tx + 0.4, 0.75, -4.15)))
        rear.append(((tx - 0.4, 0.6, -4.15), (tx + 0.4, 0.6, -4.15)))
        rear.append(((tx - 0.4, 0.75, -4.15), (tx - 0.4, 0.6, -4.15)))
        rear.append(((tx + 0.4, 0.75, -4.15), (tx + 0.4, 0.6, -4.15)))
    # License plate
    rear.append(((-0.3, 0.55, -4.22), (0.3, 0.55, -4.22)))
    rear.append(((-0.3, 0.4, -4.22), (0.3, 0.4, -4.22)))
    rear.append(((-0.3, 0.55, -4.22), (-0.3, 0.4, -4.22)))
    rear.append(((0.3, 0.55, -4.22), (0.3, 0.4, -4.22)))

    # ── Soft-top arches (visible frame structure) ────────────────────
    top_arches = []
    for z in [-0.2, -0.7, -1.2]:
        top_arches.append(((-_W * 0.85, 2.15, z), (0.0, 2.25, z)))
        top_arches.append(((0.0, 2.25, z), (_W * 0.85, 2.15, z)))

    # ── Windshield frame ─────────────────────────────────────────────
    windshield = [
        ((-_W * 0.9, 1.4, 0.8), (_W * 0.9, 1.4, 0.8)),     # base
        ((-_W * 0.8, 2.1, 0.0), (_W * 0.8, 2.1, 0.0)),     # top
        ((-_W * 0.9, 1.4, 0.8), (-_W * 0.8, 2.1, 0.0)),    # left A-pillar
        ((_W * 0.9, 1.4, 0.8), (_W * 0.8, 2.1, 0.0)),      # right A-pillar
    ]

    # ── Hood lines ───────────────────────────────────────────────────
    hood = [
        ((0.0, 0.88, 3.0), (0.0, 0.92, 1.5)),  # center crease
        ((-0.6, 0.86, 3.0), (-0.6, 0.90, 1.5)),
        ((0.6, 0.86, 3.0), (0.6, 0.90, 1.5)),
    ]

    # Assemble
    all_edges = []
    all_edges.extend(_mirror_x(right_side))
    all_edges.extend(centerline)
    all_edges.extend(front)
    all_edges.extend(rear)
    all_edges.extend(top_arches)
    all_edges.extend(windshield)
    all_edges.extend(hood)

    return all_edges


EDGES = _build_model()
