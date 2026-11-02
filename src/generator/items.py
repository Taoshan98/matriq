import math
from .primitives import (
    circle, rect, line, polygon, regular_polygon, star, arrow,
    make_dot, validate_svg_snippet
)

items = []

# ==========================================
# ITEM 1: Dot Count Progression (1 -> 5)
# Category: Progressione Quantitativa
# ==========================================
def item_1_dots(count):
    coords_map = {
        1: [(50, 50)],
        2: [(35, 50), (65, 50)],
        3: [(30, 50), (50, 50), (70, 50)],
        4: [(32, 32), (68, 32), (32, 68), (68, 68)],
        5: [(30, 30), (70, 30), (50, 50), (30, 70), (70, 70)],
        6: [(32, 30), (68, 30), (32, 50), (68, 50), (32, 70), (68, 70)],
    }
    return "".join(make_dot(x, y) for x, y in coords_map.get(count, []))

grid_1 = [
    item_1_dots(1), item_1_dots(2), item_1_dots(3),
    item_1_dots(2), item_1_dots(3), item_1_dots(4),
    item_1_dots(3), item_1_dots(4)
]
opts_1 = [
    item_1_dots(3),
    item_1_dots(4),
    item_1_dots(5), # Correct (Index 2)
    item_1_dots(6),
    item_1_dots(2),
    "".join(make_dot(15 + i*17, 50) for i in range(5)) # 5 in a straight line
]
items.append({
    "id": 1,
    "difficulty": 1,
    "category": "Progressione Quantitativa",
    "grid": grid_1,
    "target": item_1_dots(5),
    "options": opts_1,
    "correct_idx": 2,
    "explanation": "Regola orizzontale: il numero di punti aumenta di 1 da sinistra a destra (1→2→3, 2→3→4, 3→4→5). Regola verticale: il numero aumenta di 1 dall'alto in basso. Nella casella mancante servono esattamente 5 punti con la disposizione a quinconce."
})

# ==========================================
# ITEM 2: Fill State Progression (Empty -> Half -> Full)
# ==========================================
def item_2_cell(shape, fill_type):
    # shape: 'circle', 'square', 'triangle'
    # fill_type: 'empty', 'half', 'full'
    res = []
    if shape == 'circle':
        if fill_type == 'empty':
            res.append(circle(50, 50, 28))
        elif fill_type == 'half':
            res.append(circle(50, 50, 28))
            res.append('<path d="M 50,22 A 28,28 0 0,0 50,78 Z" fill="currentColor" stroke="none" />')
        elif fill_type == 'full':
            res.append(circle(50, 50, 28, fill="currentColor"))
    elif shape == 'square':
        if fill_type == 'empty':
            res.append(rect(22, 22, 56, 56))
        elif fill_type == 'half':
            res.append(rect(22, 22, 56, 56))
            res.append(rect(22, 22, 28, 56, fill="currentColor", stroke="none"))
        elif fill_type == 'full':
            res.append(rect(22, 22, 56, 56, fill="currentColor"))
    elif shape == 'triangle':
        pts = [(50, 22), (78, 76), (22, 76)]
        if fill_type == 'empty':
            res.append(polygon(pts))
        elif fill_type == 'half':
            res.append(polygon(pts))
            half_pts = [(50, 22), (50, 76), (22, 76)]
            res.append(polygon(half_pts, fill="currentColor", stroke="none"))
        elif fill_type == 'full':
            res.append(polygon(pts, fill="currentColor"))
    return "".join(res)

grid_2 = [
    item_2_cell('circle', 'empty'), item_2_cell('circle', 'half'), item_2_cell('circle', 'full'),
    item_2_cell('square', 'empty'), item_2_cell('square', 'half'), item_2_cell('square', 'full'),
    item_2_cell('triangle', 'empty'), item_2_cell('triangle', 'half')
]
opts_2 = [
    item_2_cell('triangle', 'empty'),
    item_2_cell('triangle', 'half'),
    item_2_cell('triangle', 'full'), # Correct (Index 2)
    item_2_cell('circle', 'full'),
    regular_polygon(50, 50, 28, 4, rot_deg=45, fill="currentColor"),
    polygon([(50, 76), (78, 22), (22, 22)], fill="currentColor") # inverted triangle
]
items.append({
    "id": 2,
    "difficulty": 1,
    "category": "Progressione Quantitativa",
    "grid": grid_2,
    "target": item_2_cell('triangle', 'full'),
    "options": opts_2,
    "correct_idx": 2,
    "explanation": "Regola orizzontale: lo stato di riempimento evolve da Vuoto → Semipieno (sinistra) → Completamente pieno. Regola verticale: la forma geometrica rimane costante per riga (Cerchio, Quadrato, Triangolo). Nella terza riga serve il Triangolo completamente pieno."
})

# ==========================================
# ITEM 3: 90° Clockwise Arrow Rotation
# ==========================================
def item_3_arrow(deg):
    rad = math.radians(deg)
    # arrow from (50, 50) outward
    r = 30
    x2 = round(50 + r * math.sin(rad), 2)
    y2 = round(50 - r * math.cos(rad), 2)
    x1 = round(50 - r * 0.4 * math.sin(rad), 2)
    y1 = round(50 + r * 0.4 * math.cos(rad), 2)
    return arrow(x1, y1, x2, y2, stroke_width=3, head_len=10)

grid_3 = [
    item_3_arrow(0), item_3_arrow(90), item_3_arrow(180),
    item_3_arrow(90), item_3_arrow(180), item_3_arrow(270),
    item_3_arrow(180), item_3_arrow(270)
]
opts_3 = [
    item_3_arrow(180),
    item_3_arrow(270),
    item_3_arrow(0),   # Correct (Index 2) - pointing Up
    item_3_arrow(90),
    item_3_arrow(45),
    item_3_arrow(225)
]
items.append({
    "id": 3,
    "difficulty": 1,
    "category": "Rotazione Spaziale",
    "grid": grid_3,
    "target": item_3_arrow(0),
    "options": opts_3,
    "correct_idx": 2,
    "explanation": "Regola orizzontale: la freccia ruota in senso orario di 90° ad ogni casella (0°→90°→180°, 90°→180°→270°, 180°→270°→0°). Dopo aver puntato verso sinistra (270°), la rotazione di 90° la riporta verso l'alto (0°)."
})

print(f"Items 1-3 created successfully.")

# ==========================================
# ITEM 4: Side / Segment Count (3 -> 4 -> 5)
# ==========================================
def item_4_spokes(n):
    res = [circle(50, 50, 30)]
    for i in range(n):
        angle = math.radians(i * (360.0 / n) - 90)
        x2 = round(50 + 30 * math.cos(angle), 2)
        y2 = round(50 + 30 * math.sin(angle), 2)
        res.append(line(50, 50, x2, y2, stroke_width=2.5))
    return "".join(res)

grid_4 = [
    regular_polygon(50, 50, 28, 3, -90), regular_polygon(50, 50, 28, 4, 45), regular_polygon(50, 50, 28, 5, -90),
    line(25, 35, 75, 35) + line(25, 50, 75, 50) + line(25, 65, 75, 65),
    line(25, 30, 75, 30) + line(25, 43, 75, 43) + line(25, 57, 75, 57) + line(25, 70, 70, 70),
    line(25, 26, 75, 26) + line(25, 38, 75, 38) + line(25, 50, 75, 50) + line(25, 62, 75, 62) + line(25, 74, 75, 74),
    item_4_spokes(3), item_4_spokes(4)
]
opts_4 = [
    item_4_spokes(4),
    item_4_spokes(6),
    item_4_spokes(5), # Correct (Index 2)
    item_4_spokes(3),
    circle(50, 50, 10) + circle(50, 50, 20) + circle(50, 50, 30),
    regular_polygon(50, 50, 28, 6, 0)
]
items.append({
    "id": 4,
    "difficulty": 1,
    "category": "Progressione Quantitativa",
    "grid": grid_4,
    "target": item_4_spokes(5),
    "options": opts_4,
    "correct_idx": 2,
    "explanation": "Regola orizzontale: il numero di elementi/lati/raggi aumenta di 1 da sinistra a destra (3→4→5). Riga 1: poligoni a 3, 4, 5 lati; Riga 2: 3, 4, 5 linee parallele; Riga 3: cerchio con 3 raggi, 4 raggi, quindi cerchio con 5 raggi."
})

# ==========================================
# ITEM 5: Positional Migration in 3x3 Mini-Grid
# ==========================================
def item_5_grid(r, c):
    # mini grid of 3x3 cells from x=20..80, y=20..80
    res = [rect(20, 20, 60, 60, stroke_width=2)]
    res.append(line(40, 20, 40, 80, stroke_width=1.5))
    res.append(line(60, 20, 60, 80, stroke_width=1.5))
    res.append(line(20, 40, 80, 40, stroke_width=1.5))
    res.append(line(20, 60, 80, 60, stroke_width=1.5))
    cx = 20 + c * 20 + 10
    cy = 20 + r * 20 + 10
    res.append(circle(cx, cy, 6, fill="currentColor", stroke="none"))
    return "".join(res)

grid_5 = [
    item_5_grid(0, 0), item_5_grid(0, 1), item_5_grid(0, 2),
    item_5_grid(1, 0), item_5_grid(1, 1), item_5_grid(1, 2),
    item_5_grid(2, 0), item_5_grid(2, 1)
]
opts_5 = [
    item_5_grid(1, 1),
    item_5_grid(2, 0),
    item_5_grid(0, 2),
    item_5_grid(2, 2), # Correct (Index 3) - bottom right
    item_5_grid(1, 2),
    item_5_grid(2, 1)
]
items.append({
    "id": 5,
    "difficulty": 1,
    "category": "Rotazione Spaziale",
    "grid": grid_5,
    "target": item_5_grid(2, 2),
    "options": opts_5,
    "correct_idx": 3,
    "explanation": "Regola orizzontale: il punto nero scorre verso destra lungo la riga. Regola verticale: la riga attiva scende dall'alto in basso (riga superiore, riga centrale, riga inferiore). Nella casella mancante il punto deve trovarsi in basso a destra (riga 3, colonna 3)."
})

# ==========================================
# ITEM 6: Scale / Size Progression (Small -> Med -> Large)
# ==========================================
def item_6_shape(shape, size):
    r_map = {'s': 12, 'm': 22, 'l': 34}
    r = r_map[size]
    if shape == 'circle':
        return circle(50, 50, r, stroke_width=2.5)
    elif shape == 'diamond':
        return regular_polygon(50, 50, r, 4, 45, stroke_width=2.5)
    elif shape == 'hexagon':
        return regular_polygon(50, 50, r, 6, 0, stroke_width=2.5)

grid_6 = [
    item_6_shape('circle', 's'), item_6_shape('circle', 'm'), item_6_shape('circle', 'l'),
    item_6_shape('diamond', 's'), item_6_shape('diamond', 'm'), item_6_shape('diamond', 'l'),
    item_6_shape('hexagon', 's'), item_6_shape('hexagon', 'm')
]
opts_6 = [
    item_6_shape('hexagon', 'm'),
    item_6_shape('hexagon', 's'),
    item_6_shape('circle', 'l'),
    item_6_shape('diamond', 'l'),
    item_6_shape('hexagon', 'l'), # Correct (Index 4)
    item_6_shape('hexagon', 'l') + make_dot(50, 50, 4)
]
items.append({
    "id": 6,
    "difficulty": 1,
    "category": "Progressione Quantitativa",
    "grid": grid_6,
    "target": item_6_shape('hexagon', 'l'),
    "options": opts_6,
    "correct_idx": 4,
    "explanation": "Regola orizzontale: la dimensione della figura cresce costantemente da Sinistra a Destra (Piccolo → Medio → Grande). Regola verticale: la forma è identica per ogni riga (Cerchio, Rombo, Esagono). Manca l'Esagono di dimensione Grande."
})

# ==========================================
# ITEM 7: Basic Latin Square of 3 Shapes
# ==========================================
def item_7_shape(s):
    if s == 'circle':
        return circle(50, 50, 26, stroke_width=2.5)
    elif s == 'square':
        return rect(24, 24, 52, 52, stroke_width=2.5)
    elif s == 'cross':
        return line(50, 22, 50, 78, stroke_width=4) + line(22, 50, 78, 50, stroke_width=4)

grid_7 = [
    item_7_shape('circle'), item_7_shape('square'), item_7_shape('cross'),
    item_7_shape('square'), item_7_shape('cross'), item_7_shape('circle'),
    item_7_shape('cross'), item_7_shape('circle')
]
opts_7 = [
    item_7_shape('circle'),
    item_7_shape('cross'),
    item_7_shape('square'), # Correct (Index 2)
    regular_polygon(50, 50, 28, 3, -90),
    regular_polygon(50, 50, 28, 4, 45),
    star(50, 50, 28, 14, 5)
]
items.append({
    "id": 7,
    "difficulty": 2,
    "category": "Permutazione & Distribuzione Attributi",
    "grid": grid_7,
    "target": item_7_shape('square'),
    "options": opts_7,
    "correct_idx": 2,
    "explanation": "Regola del Quadrato Latino: ogni riga e ogni colonna deve contenere esattamente una volta ciascuna delle tre figure (Cerchio, Quadrato, Croce). Nella terza riga mancano solo il Quadrato (e anche nella terza colonna manca il Quadrato)."
})

# ==========================================
# ITEM 8: 2-Attribute Latin Square (Shape + Fill Pattern)
# ==========================================
def item_8_cell(shape, fill_type):
    # Shape: 'triangle', 'circle', 'square'
    # fill_type: 'empty', 'hatch', 'solid'
    res = []
    if fill_type == 'hatch':
        # Add a pattern or simulated diagonal lines
        res.append('<defs><pattern id="hatch8" width="8" height="8" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse"><line x1="0" y1="0" x2="0" y2="8" stroke="currentColor" stroke-width="2.5" /></pattern></defs>')
        fill_val = 'url(#hatch8)'
    elif fill_type == 'solid':
        fill_val = 'currentColor'
    else:
        fill_val = 'none'

    if shape == 'triangle':
        pts = [(50, 20), (80, 78), (20, 78)]
        res.append(polygon(pts, fill=fill_val, stroke="currentColor", stroke_width=2.5))
    elif shape == 'circle':
        res.append(circle(50, 50, 28, fill=fill_val, stroke="currentColor", stroke_width=2.5))
    elif shape == 'square':
        res.append(rect(22, 22, 56, 56, fill=fill_val, stroke="currentColor", stroke_width=2.5))
    return "".join(res)

grid_8 = [
    item_8_cell('triangle', 'empty'), item_8_cell('circle', 'hatch'), item_8_cell('square', 'solid'),
    item_8_cell('circle', 'solid'), item_8_cell('square', 'empty'), item_8_cell('triangle', 'hatch'),
    item_8_cell('square', 'hatch'), item_8_cell('triangle', 'solid')
]
opts_8 = [
    item_8_cell('circle', 'hatch'),
    item_8_cell('circle', 'solid'),
    item_8_cell('triangle', 'empty'),
    item_8_cell('circle', 'empty'), # Correct (Index 3)
    item_8_cell('square', 'empty'),
    item_8_cell('square', 'solid')
]
items.append({
    "id": 8,
    "difficulty": 2,
    "category": "Permutazione & Distribuzione Attributi",
    "grid": grid_8,
    "target": item_8_cell('circle', 'empty'),
    "options": opts_8,
    "correct_idx": 3,
    "explanation": "Distribuzione a due dimensioni indipendenti (Quadrato Latino 3x3): 1) Ogni riga e colonna contiene un Triangolo, un Cerchio e un Quadrato; 2) Ogni riga e colonna contiene una figura Vuota, una Tratteggiata e una Piena. Nella terza riga mancano il Cerchio e la proprietà Vuota, quindi serve il Cerchio Vuoto."
})

# ==========================================
# ITEM 9: Outer Shape + Inner Marker Latin Square
# ==========================================
def item_9_cell(outer, inner):
    # outer: 'hex', 'circle', 'square'
    # inner: 'plus', 'dot', 'minus'
    res = []
    if outer == 'hex':
        res.append(regular_polygon(50, 50, 30, 6, 0))
    elif outer == 'circle':
        res.append(circle(50, 50, 30))
    elif outer == 'square':
        res.append(rect(20, 20, 60, 60))

    if inner == 'plus':
        res.append(line(50, 38, 50, 62, stroke_width=3))
        res.append(line(38, 50, 62, 50, stroke_width=3))
    elif inner == 'dot':
        res.append(circle(50, 50, 6, fill="currentColor", stroke="none"))
    elif inner == 'minus':
        res.append(line(36, 50, 64, 50, stroke_width=3))
    return "".join(res)

grid_9 = [
    item_9_cell('hex', 'plus'), item_9_cell('circle', 'dot'), item_9_cell('square', 'minus'),
    item_9_cell('circle', 'minus'), item_9_cell('square', 'plus'), item_9_cell('hex', 'dot'),
    item_9_cell('square', 'dot'), item_9_cell('hex', 'minus')
]
opts_9 = [
    item_9_cell('circle', 'minus'),
    item_9_cell('circle', 'dot'),
    item_9_cell('circle', 'plus'), # Correct (Index 2)
    item_9_cell('square', 'plus'),
    item_9_cell('hex', 'plus'),
    item_9_cell('circle', 'none')
]
items.append({
    "id": 9,
    "difficulty": 2,
    "category": "Permutazione & Distribuzione Attributi",
    "grid": grid_9,
    "target": item_9_cell('circle', 'plus'),
    "options": opts_9,
    "correct_idx": 2,
    "explanation": "Quadrato Latino congiunto: 1) Forma esterna: ogni riga e colonna ha Esagono, Cerchio, Quadrato (manca il Cerchio); 2) Simbolo interno: ogni riga e colonna ha Più (+), Punto (•), Meno (-) (manca il Più). La figura corretta è il Cerchio con il Più interno."
})

# ==========================================
# ITEM 10: Clock Face Hand Rotation (45° per step)
# ==========================================
def item_10_clock(deg):
    res = [circle(50, 50, 34, stroke_width=2)]
    # center pivot
    res.append(circle(50, 50, 4, fill="currentColor", stroke="none"))
    rad = math.radians(deg)
    x2 = round(50 + 26 * math.sin(rad), 2)
    y2 = round(50 - 26 * math.cos(rad), 2)
    res.append(line(50, 50, x2, y2, stroke_width=3.5))
    return "".join(res)

grid_10 = [
    item_10_clock(0), item_10_clock(45), item_10_clock(90),
    item_10_clock(90), item_10_clock(135), item_10_clock(180),
    item_10_clock(180), item_10_clock(225)
]
opts_10 = [
    item_10_clock(225),
    item_10_clock(270), # Correct (Index 1) - pointing left (9:00)
    item_10_clock(315),
    item_10_clock(0),
    item_10_clock(180),
    item_10_clock(135)
]
items.append({
    "id": 10,
    "difficulty": 2,
    "category": "Rotazione Spaziale",
    "grid": grid_10,
    "target": item_10_clock(270),
    "options": opts_10,
    "correct_idx": 1,
    "explanation": "Regola orizzontale: la lancetta ruota in senso orario di 45° ad ogni passaggio (0°→45°→90°, 90°→135°→180°, 180°→225°→270°). Regola verticale: la lancetta ruota in senso orario di 90° ad ogni riga. Aggiungendo 45° a 225° si ottiene 270° (lancetta orizzontale che punta a sinistra)."
})

# ==========================================
# ITEM 11: Dual Independent Movements (Outer CW, Inner Corner CCW)
# ==========================================
def item_11_cell(rot_deg, corner):
    # outer triangle pointing: rot_deg
    # corner: 0: TL, 1: BL, 2: BR, 3: TR
    res = [regular_polygon(50, 50, 32, 3, rot_deg)]
    corner_coords = {
        0: (30, 30),
        1: (30, 70),
        2: (70, 70),
        3: (70, 30)
    }
    cx, cy = corner_coords[corner]
    res.append(make_dot(cx, cy, 4.5))
    return "".join(res)

# Row 1: rot: -90 (Up), 0 (Right), 90 (Down) | dot corner: 0 (TL) -> 1 (BL) -> 2 (BR)
# Row 2: rot: 0 (Right), 90 (Down), 180 (Left) | dot corner: 1 (BL) -> 2 (BR) -> 3 (TR)
# Row 3: rot: 90 (Down), 180 (Left), -90 (Up) | dot corner: 2 (BR) -> 3 (TR) -> 0 (TL)
grid_11 = [
    item_11_cell(-90, 0), item_11_cell(0, 1), item_11_cell(90, 2),
    item_11_cell(0, 1), item_11_cell(90, 2), item_11_cell(180, 3),
    item_11_cell(90, 2), item_11_cell(180, 3)
]
opts_11 = [
    item_11_cell(-90, 2),
    item_11_cell(90, 0),
    item_11_cell(-90, 0), # Correct (Index 2) - Triangle Up, Dot TL
    item_11_cell(-90, 3),
    item_11_cell(180, 1),
    item_11_cell(0, 0)
]
items.append({
    "id": 11,
    "difficulty": 2,
    "category": "Rotazione Spaziale",
    "grid": grid_11,
    "target": item_11_cell(-90, 0),
    "options": opts_11,
    "correct_idx": 2,
    "explanation": "Due movimenti simultanei e indipendenti: 1) Il triangolo esterno ruota di 90° in senso orario (in riga 3 passa da Giù → Sinistra → Su); 2) Il punto interno orbita tra i quattro angoli in senso antiorario (in riga 3 passa da Basso-Destra → Alto-Destra → Alto-Sinistra). Il bersaglio ha il triangolo rivolto verso l'alto con il punto in Alto-Sinistra."
})

# ==========================================
# ITEM 12: Line Orientation & End Caps Latin Square
# ==========================================
def item_12_bar(orient, cap):
    # orient: 'h', 'v', 'd' (diagonal 45)
    # cap: 'dots', 'arrows', 'bars'
    res = []
    if orient == 'h':
        p1, p2 = (22, 50), (78, 50)
    elif orient == 'v':
        p1, p2 = (50, 22), (50, 78)
    elif orient == 'd':
        p1, p2 = (24, 76), (76, 24)

    res.append(line(p1[0], p1[1], p2[0], p2[1], stroke_width=3))
    if cap == 'dots':
        res.append(make_dot(p1[0], p1[1], 5))
        res.append(make_dot(p2[0], p2[1], 5))
    elif cap == 'bars':
        if orient == 'h':
            res.append(line(p1[0], 40, p1[0], 60, stroke_width=3))
            res.append(line(p2[0], 40, p2[0], 60, stroke_width=3))
        elif orient == 'v':
            res.append(line(40, p1[1], 60, p1[1], stroke_width=3))
            res.append(line(40, p2[1], 60, p2[1], stroke_width=3))
        elif orient == 'd':
            res.append(line(p1[0]-7, p1[1]-7, p1[0]+7, p1[1]+7, stroke_width=3))
            res.append(line(p2[0]-7, p2[1]-7, p2[0]+7, p2[1]+7, stroke_width=3))
    elif cap == 'arrows':
        # two arrow heads
        if orient == 'h':
            res.append(polygon([(p1[0], p1[1]), (p1[0]+10, p1[1]-6), (p1[0]+10, p1[1]+6)], fill="currentColor"))
            res.append(polygon([(p2[0], p2[1]), (p2[0]-10, p2[1]-6), (p2[0]-10, p2[1]+6)], fill="currentColor"))
        elif orient == 'v':
            res.append(polygon([(p1[0], p1[1]), (p1[0]-6, p1[1]+10), (p1[0]+6, p1[1]+10)], fill="currentColor"))
            res.append(polygon([(p2[0], p2[1]), (p2[0]-6, p2[1]-10), (p2[0]+6, p2[1]-10)], fill="currentColor"))
        elif orient == 'd':
            res.append(polygon([(p1[0], p1[1]), (p1[0]+11, p1[1]), (p1[0], p1[1]-11)], fill="currentColor"))
            res.append(polygon([(p2[0], p2[1]), (p2[0]-11, p2[1]), (p2[0], p2[1]+11)], fill="currentColor"))
    return "".join(res)

grid_12 = [
    item_12_bar('h', 'dots'), item_12_bar('v', 'arrows'), item_12_bar('d', 'bars'),
    item_12_bar('v', 'bars'), item_12_bar('d', 'dots'), item_12_bar('h', 'arrows'),
    item_12_bar('d', 'arrows'), item_12_bar('h', 'bars')
]
opts_12 = [
    item_12_bar('v', 'arrows'),
    item_12_bar('v', 'bars'),
    item_12_bar('v', 'dots'), # Correct (Index 2)
    item_12_bar('h', 'dots'),
    item_12_bar('d', 'dots'),
    item_12_bar('v', 'none')
]
items.append({
    "id": 12,
    "difficulty": 2,
    "category": "Permutazione & Distribuzione Attributi",
    "grid": grid_12,
    "target": item_12_bar('v', 'dots'),
    "options": opts_12,
    "correct_idx": 2,
    "explanation": "Quadrato Latino incrociato: 1) Orientamento linea: Orizzontale, Verticale, Diagonale (nella terza riga manca la Verticale); 2) Terminazioni: Pallini, Frecce, Trattini a T (nella terza riga mancano i Pallini). La figura corretta è la barra verticale con pallini alle estremità."
})

print(f"Items 1-12 created successfully. Total items: {len(items)}")

# ==========================================
# ITEM 13: Direct Graphic Union (Col 1 + Col 2 = Col 3)
# 8 Options
# ==========================================
grid_13 = [
    line(50, 20, 50, 80, stroke_width=3), line(20, 50, 80, 50, stroke_width=3), line(50, 20, 50, 80, stroke_width=3) + line(20, 50, 80, 50, stroke_width=3),
    line(22, 22, 78, 78, stroke_width=3), line(22, 78, 78, 22, stroke_width=3), line(22, 22, 78, 78, stroke_width=3) + line(22, 78, 78, 22, stroke_width=3),
    circle(50, 50, 26, stroke_width=3), rect(24, 24, 52, 52, stroke_width=3)
]
target_13 = rect(24, 24, 52, 52, stroke_width=3) + circle(50, 50, 26, stroke_width=3)
opts_13 = [
    circle(50, 50, 26, stroke_width=3),
    rect(24, 24, 52, 52, stroke_width=3),
    rect(24, 24, 52, 52, stroke_width=3) + line(24, 24, 76, 76, stroke_width=3),
    target_13, # Correct (Index 3) - Square with inscribed circle
    circle(50, 50, 26, stroke_width=3) + line(50, 24, 50, 76, stroke_width=3),
    rect(24, 24, 52, 52, stroke_width=3) + regular_polygon(50, 50, 26, 3, -90, stroke_width=3),
    circle(50, 50, 16, stroke_width=3) + circle(50, 50, 28, stroke_width=3),
    rect(34, 34, 32, 32, stroke_width=3) + circle(50, 50, 32, stroke_width=3)
]
items.append({
    "id": 13,
    "difficulty": 3,
    "category": "Operazioni Grafiche & Coordinate",
    "grid": grid_13,
    "target": target_13,
    "options": opts_13,
    "correct_idx": 3,
    "explanation": "Regola di unione grafica diretta: gli elementi della colonna 1 e della colonna 2 vengono sovrapposti per generare la colonna 3 (Col 1 + Col 2 = Col 3). Riga 1: linea verticale + linea orizzontale = croce. Riga 2: diagonale discendente + diagonale ascendente = X. Riga 3: cerchio + quadrato = quadrato con cerchio inscritto."
})

# ==========================================
# ITEM 14: Quantitative Segment Addition across Rows (C1 + C2 = C3)
# ==========================================
def item_14_bars(orient, count):
    # orient: 'h', 'v', 'd'
    res = []
    gap = 60.0 / (count + 1)
    for i in range(1, count + 1):
        pos = round(20 + i * gap, 2)
        if orient == 'h':
            res.append(line(24, pos, 76, pos, stroke_width=2.5))
        elif orient == 'v':
            res.append(line(pos, 24, pos, 76, stroke_width=2.5))
        elif orient == 'd':
            offset = (i - (count + 1) / 2.0) * (50.0 / max(count, 1))
            res.append(line(round(25 + offset, 2), 75, round(75 + offset, 2), 25, stroke_width=2.5))
    return "".join(res)

grid_14 = [
    item_14_bars('h', 2), item_14_bars('h', 3), item_14_bars('h', 5),
    item_14_bars('v', 1), item_14_bars('v', 3), item_14_bars('v', 4),
    item_14_bars('d', 3), item_14_bars('d', 3)
]
target_14 = item_14_bars('d', 6)
opts_14 = [
    item_14_bars('d', 5),
    item_14_bars('d', 7),
    target_14, # Correct (Index 2) - 6 diagonal bars
    item_14_bars('d', 4),
    item_14_bars('h', 6),
    item_14_bars('v', 6),
    item_14_bars('d', 3),
    item_14_bars('d', 2)
]
items.append({
    "id": 14,
    "difficulty": 3,
    "category": "Progressione Quantitativa",
    "grid": grid_14,
    "target": target_14,
    "options": opts_14,
    "correct_idx": 2,
    "explanation": "Regola additiva orizzontale: il numero di segmenti nella colonna 3 è la somma algebrica dei segmenti della colonna 1 e della colonna 2 (Col 1 + Col 2 = Col 3). Riga 1: 2 + 3 = 5 linee orizzontali. Riga 2: 1 + 3 = 4 linee verticali. Riga 3: 3 + 3 = 6 linee diagonali."
})

# ==========================================
# ITEM 15: Graphic Subtraction (Col 1 - Col 2 = Col 3)
# ==========================================
grid_15 = [
    make_dot(30, 30) + make_dot(70, 30) + make_dot(30, 70) + make_dot(70, 70),
    make_dot(30, 30) + make_dot(70, 30),
    make_dot(30, 70) + make_dot(70, 70),

    rect(24, 24, 52, 52) + line(24, 24, 76, 76) + line(24, 76, 76, 24),
    line(24, 76, 76, 24),
    rect(24, 24, 52, 52) + line(24, 24, 76, 76),

    circle(50, 50, 28) + line(50, 22, 50, 78) + line(22, 50, 78, 50),
    line(50, 22, 50, 78)
]
target_15 = circle(50, 50, 28) + line(22, 50, 78, 50) # Circle with horizontal line
opts_15 = [
    circle(50, 50, 28) + line(50, 22, 50, 78), # vertical
    circle(50, 50, 28) + line(50, 22, 50, 78) + line(22, 50, 78, 50), # cross
    target_15, # Correct (Index 2) - Circle with horizontal line
    circle(50, 50, 28), # empty circle
    rect(24, 24, 52, 52) + line(22, 50, 78, 50),
    circle(50, 50, 28) + line(30, 30, 70, 70),
    line(22, 50, 78, 50),
    circle(50, 50, 28) + make_dot(50, 50)
]
items.append({
    "id": 15,
    "difficulty": 3,
    "category": "Operazioni Grafiche & Coordinate",
    "grid": grid_15,
    "target": target_15,
    "options": opts_15,
    "correct_idx": 2,
    "explanation": "Regola di sottrazione grafica (Col 1 - Col 2 = Col 3): dalla figura della colonna 1 vengono rimossi gli elementi presenti nella colonna 2. Riga 1: 4 vertici meno i 2 superiori = 2 inferiori. Riga 2: quadrato con X meno la diagonale ascendente = quadrato con la diagonale discendente. Riga 3: cerchio con croce interna meno la linea verticale = cerchio con la sola linea orizzontale."
})

# ==========================================
# ITEM 16: Perimeter Orbital Movement (+2 CW steps on 8-perimeter)
# ==========================================
def item_16_pos(idx):
    # 8 points around a square 30..70
    # 0: TL(30,30), 1: TM(50,30), 2: TR(70,30), 3: RM(70,50),
    # 4: BR(70,70), 5: BM(50,70), 6: BL(30,70), 7: LM(30,50)
    coords = [
        (30, 30), (50, 30), (70, 30), (70, 50),
        (70, 70), (50, 70), (30, 70), (30, 50)
    ]
    res = [rect(24, 24, 52, 52, stroke_width=1.5, stroke="#64748b")]
    cx, cy = coords[idx % 8]
    res.append(make_dot(cx, cy, 6))
    return "".join(res)

grid_16 = [
    item_16_pos(0), item_16_pos(2), item_16_pos(4),
    item_16_pos(1), item_16_pos(3), item_16_pos(5),
    item_16_pos(2), item_16_pos(4)
]
target_16 = item_16_pos(6) # BL corner (Index 6)
opts_16 = [
    item_16_pos(5), # BM
    item_16_pos(7), # LM
    item_16_pos(6), # Correct (Index 2) - BL corner
    item_16_pos(0), # TL
    item_16_pos(4), # BR
    rect(24, 24, 52, 52, stroke_width=1.5, stroke="#64748b") + make_dot(50, 50, 6), # Center
    item_16_pos(1), # TM
    item_16_pos(3)  # RM
]
items.append({
    "id": 16,
    "difficulty": 3,
    "category": "Rotazione Spaziale",
    "grid": grid_16,
    "target": target_16,
    "options": opts_16,
    "correct_idx": 2,
    "explanation": "Regola di salto orbitale perimetrale: il punto nero si muove in senso orario lungo gli 8 nodi perimetrali del quadrato compiendo esattamente 2 passi ad ogni casella (+2 mod 8). Riga 3: posizione 2 (Alto-Destra) → posizione 4 (Basso-Destra) → posizione 6 (Basso-Sinistra)."
})

# ==========================================
# ITEM 17: Overlap Inversion (Venn Symmetric Difference / Intersection fill)
# ==========================================
def item_17_diamonds(fill_mode):
    # fill_mode: 'left', 'right', 'intersect', 'union', 'empty'
    d_left = regular_polygon(42, 50, 22, 4, 45)
    d_right = regular_polygon(58, 50, 22, 4, 45)
    res = []
    if fill_mode == 'left':
        res.append(regular_polygon(42, 50, 22, 4, 45, fill="currentColor"))
        res.append(regular_polygon(58, 50, 22, 4, 45))
    elif fill_mode == 'right':
        res.append(regular_polygon(42, 50, 22, 4, 45))
        res.append(regular_polygon(58, 50, 22, 4, 45, fill="currentColor"))
    elif fill_mode == 'intersect':
        # both diamonds outlines + filled intersection polygon
        res.append(regular_polygon(42, 50, 22, 4, 45))
        res.append(regular_polygon(58, 50, 22, 4, 45))
        # intersection of (42,50) and (58,50) diamond: x in [36, 64]
        # vertices at (50, 42), (58-16=42?, top is at (50, 42), bottom at (50, 58))
        res.append(polygon([(50, 42), (58, 50), (50, 58), (42, 50)], fill="currentColor"))
    elif fill_mode == 'union':
        res.append(regular_polygon(42, 50, 22, 4, 45, fill="currentColor"))
        res.append(regular_polygon(58, 50, 22, 4, 45, fill="currentColor"))
    elif fill_mode == 'empty':
        res.append(regular_polygon(42, 50, 22, 4, 45))
        res.append(regular_polygon(58, 50, 22, 4, 45))
    return "".join(res)

def item_17_circles(fill_mode):
    res = [circle(42, 50, 20), circle(58, 50, 20)]
    if fill_mode == 'left':
        res[0] = circle(42, 50, 20, fill="currentColor")
    elif fill_mode == 'right':
        res[1] = circle(58, 50, 20, fill="currentColor")
    elif fill_mode == 'intersect':
        # lens path intersection
        res.append('<path d="M 50,37 A 20,20 0 0,1 50,63 A 20,20 0 0,1 50,37 Z" fill="currentColor" />')
    return "".join(res)

def item_17_squares(fill_mode):
    res = [rect(30, 26, 40, 30), rect(30, 44, 40, 30)]
    if fill_mode == 'top':
        res[0] = rect(30, 26, 40, 30, fill="currentColor")
    elif fill_mode == 'bottom':
        res[1] = rect(30, 44, 40, 30, fill="currentColor")
    elif fill_mode == 'intersect':
        res.append(rect(30, 44, 40, 12, fill="currentColor"))
    return "".join(res)

grid_17 = [
    item_17_circles('left'), item_17_circles('right'), item_17_circles('intersect'),
    item_17_squares('top'), item_17_squares('bottom'), item_17_squares('intersect'),
    item_17_diamonds('left'), item_17_diamonds('right')
]
target_17 = item_17_diamonds('intersect')
opts_17 = [
    item_17_diamonds('left'),
    item_17_diamonds('right'),
    item_17_diamonds('union'),
    target_17, # Correct (Index 3) - Only intersection filled
    item_17_diamonds('empty'),
    regular_polygon(50, 50, 22, 4, 45, fill="currentColor"),
    item_17_circles('intersect'),
    circle(50, 50, 25, fill="currentColor")
]
items.append({
    "id": 17,
    "difficulty": 3,
    "category": "Operazioni Grafiche & Coordinate",
    "grid": grid_17,
    "target": target_17,
    "options": opts_17,
    "correct_idx": 3,
    "explanation": "Regola di intersezione Booleana (Colonna 1 AND Colonna 2 = Colonna 3): solo le regioni geometriche che sono colorate in entrambe le prime due figure rimangono piene nella terza casella (intersezione insiemistica). Nella terza riga si intersecano i due rombi, quindi deve essere riempita solo la lente centrale."
})

# ==========================================
# ITEM 18: Counter-Directional Movement (Vector Intersection)
# ==========================================
def item_18_cell(dot_x, sq_y):
    res = [
        line(20, 50, 80, 50, stroke="#64748b", stroke_width=1.5, dashed=True),
        line(50, 20, 50, 80, stroke="#64748b", stroke_width=1.5, dashed=True),
        circle(dot_x, 50, 6, fill="currentColor", stroke="none"),
        rect(50 - 6, sq_y - 6, 12, 12, fill="none", stroke="currentColor", stroke_width=2.5)
    ]
    return "".join(res)

grid_18 = [
    item_18_cell(25, 25), item_18_cell(50, 50), item_18_cell(75, 75),
    item_18_cell(75, 25), item_18_cell(50, 50), item_18_cell(25, 75),
    item_18_cell(25, 75), item_18_cell(50, 50)
]
target_18 = item_18_cell(75, 25) # Dot at right (75), Square at top (25)
opts_18 = [
    item_18_cell(50, 50),
    item_18_cell(75, 75),
    item_18_cell(25, 25),
    target_18, # Correct (Index 3)
    item_18_cell(25, 50),
    item_18_cell(75, 50),
    item_18_cell(50, 25),
    item_18_cell(50, 75)
]
items.append({
    "id": 18,
    "difficulty": 3,
    "category": "Operazioni Grafiche & Coordinate",
    "grid": grid_18,
    "target": target_18,
    "options": opts_18,
    "correct_idx": 3,
    "explanation": "Due traiettorie lineari continue: 1) Il pallino nero solido si muove orizzontalmente da sinistra verso destra (25 → 50 → 75); 2) Il quadratino cavo nella riga 3 parte dal basso e sale verso l'alto (75 → 50 → 25). Al terzo step il pallino è a destra (x=75) e il quadrato è in alto (y=25)."
})

# ==========================================
# ITEM 19: Pure Horizontal Line XOR (Col 1 XOR Col 2 = Col 3)
# ==========================================
def item_19_lines(top=False, mid=False, bot=False):
    res = []
    if top: res.append(line(24, 30, 76, 30, stroke_width=3.5))
    if mid: res.append(line(24, 50, 76, 50, stroke_width=3.5))
    if bot: res.append(line(24, 70, 76, 70, stroke_width=3.5))
    if not res:
        res.append(circle(50, 50, 2, fill="#64748b", stroke="none")) # blank indicator
    return "".join(res)

# Row 1: {T, M} XOR {M, B} = {T, B}
# Row 2: {T, B} XOR {T, M, B} = {M}
# Row 3: {T, M} XOR {T} = {M}
grid_19 = [
    item_19_lines(True, True, False), item_19_lines(False, True, True), item_19_lines(True, False, True),
    item_19_lines(True, False, True), item_19_lines(True, True, True), item_19_lines(False, True, False),
    item_19_lines(True, True, False), item_19_lines(True, False, False)
]
target_19 = item_19_lines(False, True, False) # Middle only
opts_19 = [
    item_19_lines(True, False, False), # Top only
    item_19_lines(False, False, True), # Bottom only
    target_19, # Correct (Index 2) - Middle only
    item_19_lines(True, True, False),  # Top + Mid
    item_19_lines(False, True, True),  # Mid + Bot
    item_19_lines(True, False, True),  # Top + Bot
    item_19_lines(True, True, True),   # All 3
    item_19_lines(False, False, False) # Empty
]
items.append({
    "id": 19,
    "difficulty": 4,
    "category": "Logica Booleana & Set-Theory (XOR)",
    "grid": grid_19,
    "target": target_19,
    "options": opts_19,
    "correct_idx": 2,
    "explanation": "Operazione logica XOR (Disgiunzione esclusiva): le linee presenti in ENTRAMBE le colonne 1 e 2 si cancellano; le linee presenti in UNA SOLA colonna rimangono nella colonna 3. Riga 3: [Superiore + Centrale] XOR [Superiore] = la linea superiore è presente in entrambe e si cancella, resta solo la linea Centrale."
})

# ==========================================
# ITEM 20: 4-Spoke Cross XOR (Top, Right, Bottom, Left)
# ==========================================
def item_20_cross(n=False, e=False, s=False, w=False):
    res = [circle(50, 50, 3, fill="currentColor", stroke="none")]
    if n: res.append(line(50, 50, 50, 22, stroke_width=3.5))
    if e: res.append(line(50, 50, 78, 50, stroke_width=3.5))
    if s: res.append(line(50, 50, 50, 78, stroke_width=3.5))
    if w: res.append(line(50, 50, 22, 50, stroke_width=3.5))
    return "".join(res)

# Row 1: {N, E} XOR {E, S} = {N, S}
# Row 2: {N, S, W} XOR {S, W} = {N}
# Row 3: {N, E, W} XOR {E, S, W} = {N, S} (E and W appear in both -> cancel! N and S appear once -> keep!)
grid_20 = [
    item_20_cross(True, True, False, False), item_20_cross(False, True, True, False), item_20_cross(True, False, True, False),
    item_20_cross(True, False, True, True), item_20_cross(False, False, True, True), item_20_cross(True, False, False, False),
    item_20_cross(True, True, False, True), item_20_cross(False, True, True, True)
]
target_20 = item_20_cross(True, False, True, False) # N and S (vertical line)
opts_20 = [
    item_20_cross(False, True, False, True), # Horizontal (E, W)
    target_20, # Correct (Index 1) - Vertical line (N, S)
    item_20_cross(True, True, True, True),   # Full cross
    item_20_cross(True, False, False, False), # N only
    item_20_cross(False, False, True, False), # S only
    item_20_cross(True, True, False, False),  # N, E
    item_20_cross(False, True, True, False),  # E, S
    item_20_cross(False, False, False, False) # Center dot only
]
items.append({
    "id": 20,
    "difficulty": 4,
    "category": "Logica Booleana & Set-Theory (XOR)",
    "grid": grid_20,
    "target": target_20,
    "options": opts_20,
    "correct_idx": 1,
    "explanation": "Operazione XOR sui quattro bracci della croce: ogni braccio presente sia nella prima che nella seconda colonna viene annullato; i bracci presenti una sola volta rimangono nella terza colonna. Riga 3: [Nord, Est, Ovest] XOR [Est, Sud, Ovest] = Est e Ovest si cancellano a vicenda, lasciando i bracci Nord e Sud (linea verticale)."
})

print(f"Items 1-20 created successfully. Total items: {len(items)}")

# ==========================================
# ITEM 21: Dual Rule: XOR of Diagonal Cross + Latin Square Core Shape
# ==========================================
def item_21_cell(slash=False, backslash=False, core='star'):
    # slash: / from (22,78) to (78,22)
    # backslash: \ from (22,22) to (78,78)
    res = []
    if slash: res.append(line(24, 76, 76, 24, stroke_width=3))
    if backslash: res.append(line(24, 24, 76, 76, stroke_width=3))

    # Core shape with white background mask to look crisp
    res.append(circle(50, 50, 12, fill="#0f172a", stroke="none"))
    if core == 'star':
        res.append(star(50, 50, 10, 5, 4, 45, fill="currentColor"))
    elif core == 'circle':
        res.append(circle(50, 50, 8, fill="currentColor"))
    elif core == 'triangle':
        res.append(regular_polygon(50, 50, 9, 3, -90, fill="currentColor"))
    return "".join(res)

# Diagonals XOR:
# R1: / XOR \ = X
# R2: X XOR / = \
# R3: \ XOR X = / (Slash / remains, backslash cancels!)
# Core Latin Square:
# R1: star, circle, triangle
# R2: triangle, star, circle
# R3: circle, star, [triangle]
grid_21 = [
    item_21_cell(True, False, 'star'), item_21_cell(False, True, 'circle'), item_21_cell(True, True, 'triangle'),
    item_21_cell(True, True, 'triangle'), item_21_cell(True, False, 'star'), item_21_cell(False, True, 'circle'),
    item_21_cell(False, True, 'circle'), item_21_cell(True, True, 'star')
]
target_21 = item_21_cell(True, False, 'triangle') # Slash (/) + Triangle
opts_21 = [
    item_21_cell(False, True, 'triangle'), # Backslash + Triangle
    item_21_cell(True, False, 'star'),     # Slash + Star
    target_21, # Correct (Index 2) - Slash + Triangle
    item_21_cell(True, True, 'triangle'),  # X + Triangle
    item_21_cell(True, False, 'circle'),   # Slash + Circle
    item_21_cell(False, True, 'star'),     # Backslash + Star
    item_21_cell(True, True, 'circle'),    # X + Circle
    item_21_cell(False, False, 'triangle') # Triangle alone
]
items.append({
    "id": 21,
    "difficulty": 4,
    "category": "Logica Booleana & Set-Theory (XOR)",
    "grid": grid_21,
    "target": target_21,
    "options": opts_21,
    "correct_idx": 2,
    "explanation": "Due regole indipendenti congiunte: 1) Le diagonali seguono la regola XOR (Col 1 XOR Col 2 = Col 3). In riga 3: Backslash (\\) XOR X = la diagonale discendente è comune e si cancella, lasciando solo la diagonale ascendente Slash (/); 2) Il nucleo centrale segue un Quadrato Latino (Stella, Cerchio, Triangolo): in riga 3 mancano Cerchio e Stella, quindi serve il Triangolo. La risposta corretta è Slash (/) con Triangolo al centro."
})

# ==========================================
# ITEM 22: Progressive 90° CW Rotation + Segment Count Loss
# ==========================================
def item_22_wheel(n_spokes, rot_deg):
    res = [regular_polygon(50, 50, 30, 6, 0, stroke_width=2)]
    # spokes from center
    for i in range(n_spokes):
        angle = math.radians(rot_deg + i * (360.0 / 6))
        x2 = round(50 + 26 * math.cos(angle), 2)
        y2 = round(50 + 26 * math.sin(angle), 2)
        res.append(line(50, 50, x2, y2, stroke_width=2.5))
    res.append(circle(50, 50, 3.5, fill="currentColor", stroke="none"))
    return "".join(res)

# Row 1: 4 spokes (0°), 3 spokes (90°), 2 spokes (180°)
# Row 2: 5 spokes (90°), 4 spokes (180°), 3 spokes (270°)
# Row 3: 6 spokes (180°), 5 spokes (270°), [4 spokes (0°)]
grid_22 = [
    item_22_wheel(4, 0), item_22_wheel(3, 90), item_22_wheel(2, 180),
    item_22_wheel(5, 90), item_22_wheel(4, 180), item_22_wheel(3, 270),
    item_22_wheel(6, 180), item_22_wheel(5, 270)
]
target_22 = item_22_wheel(4, 0) # 4 spokes starting at 0°
opts_22 = [
    item_22_wheel(5, 0),
    item_22_wheel(3, 0),
    target_22, # Correct (Index 2) - 4 spokes, rot 0
    item_22_wheel(4, 90),
    item_22_wheel(4, 180),
    item_22_wheel(4, 270),
    item_22_wheel(2, 0),
    regular_polygon(50, 50, 30, 6, 0, stroke_width=2) + make_dot(50, 50)
]
items.append({
    "id": 22,
    "difficulty": 4,
    "category": "Rotazione Spaziale",
    "grid": grid_22,
    "target": target_22,
    "options": opts_22,
    "correct_idx": 2,
    "explanation": "Due trasformazioni simultanee: 1) Rotazione: la figura ruota in senso orario di 90° ad ogni casella (Riga 3: 180° → 270° → 0°/360°); 2) Perdita di segmenti: il numero di raggi interni si riduce di 1 ad ogni passaggio (Riga 3: 6 → 5 → 4 raggi). La risposta è l'esagono con 4 raggi interni con orientamento di partenza a 0°."
})

# ==========================================
# ITEM 23: 3x3 Dot Grid XOR (Classic Mensa Hard Matrix)
# ==========================================
def item_23_grid(active_bits):
    # active_bits: list of 9 booleans (TL, TM, TR, ML, MM, MR, BL, BM, BR)
    coords = [
        (30, 30), (50, 30), (70, 30),
        (30, 50), (50, 50), (70, 50),
        (30, 70), (50, 70), (70, 70)
    ]
    res = [rect(20, 20, 60, 60, stroke_width=1.5, stroke="#475569")]
    for idx, active in enumerate(active_bits):
        cx, cy = coords[idx]
        if active:
            res.append(circle(cx, cy, 5.5, fill="currentColor", stroke="none"))
        else:
            res.append(circle(cx, cy, 2, fill="#334155", stroke="none"))
    return "".join(res)

def xor_bits(b1, b2):
    return [x ^ y for x, y in zip(b1, b2)]

# R1:
b_r1_c1 = [1, 0, 1,  0, 1, 0,  1, 0, 0]
b_r1_c2 = [0, 0, 1,  0, 1, 1,  0, 0, 1]
b_r1_c3 = xor_bits(b_r1_c1, b_r1_c2) # [1, 0, 0, 0, 0, 1, 1, 0, 1]

# R2:
b_r2_c1 = [0, 1, 0,  1, 1, 0,  0, 1, 0]
b_r2_c2 = [1, 1, 0,  0, 1, 0,  0, 0, 1]
b_r2_c3 = xor_bits(b_r2_c1, b_r2_c2) # [1, 0, 0, 1, 0, 0, 0, 1, 1]

# R3:
# Col 1: TL, TR, C, BR
b_r3_c1 = [1, 0, 1,  0, 1, 0,  0, 0, 1]
# Col 2: TR, C, BL
b_r3_c2 = [0, 0, 1,  0, 1, 0,  1, 0, 0]
# Col 3 = XOR: TR and C cancel out! Remaining: TL, BL, BR
b_r3_c3 = xor_bits(b_r3_c1, b_r3_c2) # [1, 0, 0, 0, 0, 0, 1, 0, 1]

grid_23 = [
    item_23_grid(b_r1_c1), item_23_grid(b_r1_c2), item_23_grid(b_r1_c3),
    item_23_grid(b_r2_c1), item_23_grid(b_r2_c2), item_23_grid(b_r2_c3),
    item_23_grid(b_r3_c1), item_23_grid(b_r3_c2)
]
target_23 = item_23_grid(b_r3_c3) # TL, BL, BR (3 dots)
opts_23 = [
    item_23_grid([1, 0, 1,  0, 1, 0,  1, 0, 1]), # Union (all 5 dots)
    item_23_grid([0, 0, 1,  0, 1, 0,  0, 0, 0]), # Intersection (TR, C)
    target_23, # Correct (Index 2) - TL, BL, BR
    item_23_grid([0, 0, 1,  0, 0, 0,  1, 0, 1]), # TR, BL, BR (inverted)
    item_23_grid([1, 0, 0,  0, 0, 0,  0, 0, 1]), # TL, BR only
    item_23_grid([1, 0, 1,  0, 0, 0,  1, 0, 0]), # TL, TR, BL
    item_23_grid([0, 1, 0,  1, 0, 1,  0, 1, 0]), # Cross
    item_23_grid([0]*9) # All empty
]
items.append({
    "id": 23,
    "difficulty": 4,
    "category": "Logica Booleana & Set-Theory (XOR)",
    "grid": grid_23,
    "target": target_23,
    "options": opts_23,
    "correct_idx": 2,
    "explanation": "Operazione XOR applicata a una matrice 3x3 di 9 punti binari: i punti presenti in entrambe le celle si annullano, quelli presenti in una sola rimangono. Riga 3: [Alto-Sx, Alto-Dx, Centro, Basso-Dx] XOR [Alto-Dx, Centro, Basso-Sx]. I punti Alto-Dx e Centro sono comuni e scompaiono; rimangono Alto-Sx, Basso-Sx e Basso-Dx (esattamente 3 punti che formano una L)."
})

# ==========================================
# ITEM 24: Geometric Intersection Nodes (N H-lines x M V-lines -> N*M dots)
# ==========================================
def item_24_mesh(n_h, n_v):
    res = []
    h_coords = []
    v_coords = []
    gap_h = 56.0 / (n_h + 1)
    for i in range(1, n_h + 1):
        y = round(22 + i * gap_h, 2)
        h_coords.append(y)
        res.append(line(22, y, 78, y, stroke_width=2.5))
    gap_v = 56.0 / (n_v + 1)
    for j in range(1, n_v + 1):
        x = round(22 + j * gap_v, 2)
        v_coords.append(x)
        res.append(line(x, 22, x, 78, stroke_width=2.5))
    # Nodes at all intersections
    for y in h_coords:
        for x in v_coords:
            res.append(circle(x, y, 4.5, fill="currentColor", stroke="none"))
    return "".join(res)

grid_24 = [
    item_24_mesh(1, 2), item_24_mesh(1, 3), item_24_mesh(1, 4), # 2 dots, 3 dots, 4 dots
    item_24_mesh(2, 1), item_24_mesh(2, 2), item_24_mesh(2, 3), # 2 dots, 4 dots, 6 dots
    item_24_mesh(3, 1), item_24_mesh(3, 2)                      # 3 dots, 6 dots, [9 dots]
]
target_24 = item_24_mesh(3, 3) # 3 H-lines, 3 V-lines = 9 dots
opts_24 = [
    item_24_mesh(3, 2), # 6 dots
    item_24_mesh(2, 3), # 6 dots inverted
    target_24, # Correct (Index 2) - 3x3 mesh with 9 intersection dots
    item_24_mesh(3, 4), # 12 dots
    item_24_mesh(2, 2), # 4 dots
    item_24_mesh(4, 3), # 12 dots
    line(22, 50, 78, 50, stroke_width=2.5) + line(50, 22, 50, 78, stroke_width=2.5) + make_dot(50, 50),
    rect(22, 22, 56, 56, stroke_width=2.5)
]
items.append({
    "id": 24,
    "difficulty": 4,
    "category": "Progressione Quantitativa",
    "grid": grid_24,
    "target": target_24,
    "options": opts_24,
    "correct_idx": 2,
    "explanation": "Relazione combinatoria bidimensionale: il numero di linee orizzontali corrisponde all'indice di riga (Riga 1: 1 linea, Riga 2: 2 linee, Riga 3: 3 linee), mentre le linee verticali aumentano da sinistra a destra (Col 1: 1 linea, Col 2: 2 linee, Col 3: 3 linee). Ad ogni incrocio tra una linea orizzontale e una verticale si forma un nodo nero. Nella cella (3,3) si intersecano 3 linee orizzontali e 3 verticali, generando una griglia di 3×3 = 9 punti nodali."
})

# ==========================================
# ITEM 25: Triple Variable Latin Cube (Polygon, Hatching, Orbiting Satellite)
# ==========================================
def item_25_cell(poly, hatch, sat_pos):
    # poly: 'oct', 'hex', 'diamond'
    # hatch: 'h', 'd', 'v'
    # sat_pos: 'top', 'br', 'bl'
    res = []
    # Hatch pattern inside polygon
    if hatch == 'h':
        p_id = "hatch_25_h"
        res.append(f'<defs><pattern id="{p_id}" width="6" height="6" patternUnits="userSpaceOnUse"><line x1="0" y1="3" x2="6" y2="3" stroke="currentColor" stroke-width="2" /></pattern></defs>')
    elif hatch == 'v':
        p_id = "hatch_25_v"
        res.append(f'<defs><pattern id="{p_id}" width="6" height="6" patternUnits="userSpaceOnUse"><line x1="3" y1="0" x2="3" y2="6" stroke="currentColor" stroke-width="2" /></pattern></defs>')
    elif hatch == 'd':
        p_id = "hatch_25_d"
        res.append(f'<defs><pattern id="{p_id}" width="8" height="8" patternTransform="rotate(45)" patternUnits="userSpaceOnUse"><line x1="0" y1="0" x2="0" y2="8" stroke="currentColor" stroke-width="2" /></pattern></defs>')

    fill_val = f'url(#{p_id})'
    if poly == 'oct':
        res.append(regular_polygon(50, 50, 26, 8, 22.5, fill=fill_val, stroke_width=2.5))
    elif poly == 'hex':
        res.append(regular_polygon(50, 50, 26, 6, 0, fill=fill_val, stroke_width=2.5))
    elif poly == 'diamond':
        res.append(regular_polygon(50, 50, 26, 4, 45, fill=fill_val, stroke_width=2.5))

    sat_map = {'top': (50, 14), 'br': (78, 76), 'bl': (22, 76)}
    sx, sy = sat_map[sat_pos]
    res.append(circle(sx, sy, 5, fill="currentColor", stroke="none"))
    return "".join(res)

# Variables:
# Poly: Oct, Hex, Diamond
# Hatch: H, D, V
# Sat: Top, BR, BL
# R1: (Oct, H, Top), (Hex, D, BR), (Diamond, V, BL)
# R2: (Hex, V, BR), (Diamond, H, BL), (Oct, D, Top)
# R3: (Diamond, D, BL), (Oct, V, Top), [(Hex, H, BR)]
grid_25 = [
    item_25_cell('oct', 'h', 'top'), item_25_cell('hex', 'd', 'br'), item_25_cell('diamond', 'v', 'bl'),
    item_25_cell('hex', 'v', 'br'), item_25_cell('diamond', 'h', 'bl'), item_25_cell('oct', 'd', 'top'),
    item_25_cell('diamond', 'd', 'bl'), item_25_cell('oct', 'v', 'top')
]
target_25 = item_25_cell('hex', 'h', 'br') # Hexagon, Horizontal hatch, Satellite BR
opts_25 = [
    item_25_cell('hex', 'v', 'br'),
    item_25_cell('oct', 'h', 'br'),
    target_25, # Correct (Index 2)
    item_25_cell('hex', 'd', 'br'),
    item_25_cell('diamond', 'h', 'br'),
    item_25_cell('hex', 'h', 'top'),
    item_25_cell('hex', 'h', 'bl'),
    item_25_cell('oct', 'd', 'top')
]
items.append({
    "id": 25,
    "difficulty": 5,
    "category": "Integrazione Astratta Multi-Variabile",
    "grid": grid_25,
    "target": target_25,
    "options": opts_25,
    "correct_idx": 2,
    "explanation": "Triplo Quadrato Latino simultaneo (tre variabili indipendenti): 1) Poligono esterno: ogni riga e colonna contiene Ottagono, Esagono, Rombo (in riga 3 manca l'Esagono); 2) Orientamento tratteggio: ogni riga e colonna contiene Orizzontale, Diagonale, Verticale (in riga 3 manca l'Orizzontale); 3) Posizione del satellite orbitale: ogni riga e colonna contiene Alto, Basso-Destra, Basso-Sinistra (in riga 3 manca Basso-Destra). La figura unica che soddisfa tutti e tre i vincoli è l'Esagono con tratteggio orizzontale e punto in Basso-Destra."
})

# ==========================================
# ITEM 26: Modular Angle & Branch Arithmetic
# ==========================================
def item_26_cell(rot_deg, branches):
    # branches: 1 to 5 radial lines
    res = [circle(50, 50, 32, stroke_width=2)]
    for i in range(branches):
        angle = math.radians(rot_deg + i * (360.0 / 5))
        x2 = round(50 + 26 * math.cos(angle), 2)
        y2 = round(50 + 26 * math.sin(angle), 2)
        res.append(line(50, 50, x2, y2, stroke_width=2.5))
        # Arrowhead or dot at branch tip
        res.append(circle(x2, y2, 3.5, fill="currentColor", stroke="none"))
    res.append(circle(50, 50, 4, fill="currentColor", stroke="none"))
    return "".join(res)

# Across row: rot increases by 45° in C1, 90° in C2, 135° in C3 (cumulative)
# Branches count:
# R1: 5 branches (rot 0) -> 4 branches (rot 45) -> 3 branches (rot 90)
# R2: 4 branches (rot 90) -> 3 branches (rot 135) -> 2 branches (rot 180)
# R3: 3 branches (rot 180) -> 2 branches (rot 225) -> [1 branch (rot 270)]
grid_26 = [
    item_26_cell(0, 5), item_26_cell(45, 4), item_26_cell(90, 3),
    item_26_cell(90, 4), item_26_cell(135, 3), item_26_cell(180, 2),
    item_26_cell(180, 3), item_26_cell(225, 2)
]
target_26 = item_26_cell(270, 1) # 1 branch pointing left (270°)
opts_26 = [
    item_26_cell(225, 1),
    item_26_cell(270, 2),
    target_26, # Correct (Index 2) - 1 branch at 270°
    item_26_cell(315, 1),
    item_26_cell(270, 3),
    item_26_cell(0, 1),
    item_26_cell(180, 1),
    circle(50, 50, 32, stroke_width=2) + make_dot(50, 50)
]
items.append({
    "id": 26,
    "difficulty": 5,
    "category": "Integrazione Astratta Multi-Variabile",
    "grid": grid_26,
    "target": target_26,
    "options": opts_26,
    "correct_idx": 2,
    "explanation": "Due leggi matematiche sincronizzate: 1) Rotazione: la base dei rami ruota di +45° in senso orario ad ogni passaggio orizzontale (in riga 3: 180° → 225° → 270°); 2) Conteggio dei rami: il numero di rami diminuisce di 1 per ogni passo (in riga 3: 3 rami → 2 rami → 1 singolo ramo). L'unico elemento corretto ha un singolo ramo puntato a 270° (verso sinistra)."
})

# ==========================================
# ITEM 27: Multi-Layer XOR with Horizontal Reflection (C3 = H_Flip(C1 XOR C2))
# ==========================================
def item_27_pattern(bars_left, bars_right, top_shape):
    # bars_left: list of booleans [L1, L2, L3] (horizontal bars in left half)
    # bars_right: list of booleans [R1, R2, R3] (horizontal bars in right half)
    # top_shape: 'triangle', 'circle'
    res = [rect(20, 20, 60, 60, stroke_width=2.5)]
    res.append(line(50, 20, 50, 80, stroke_width=1.5, dashed=True)) # dividing line
    y_coords = [35, 50, 65]
    for idx, act in enumerate(bars_left):
        if act:
            res.append(line(24, y_coords[idx], 46, y_coords[idx], stroke_width=3))
    for idx, act in enumerate(bars_right):
        if act:
            res.append(line(54, y_coords[idx], 76, y_coords[idx], stroke_width=3))

    if top_shape == 'triangle':
        res.append(polygon([(50, 24), (56, 34), (44, 34)], fill="currentColor"))
    elif top_shape == 'circle':
        res.append(circle(50, 28, 4, fill="currentColor"))
    return "".join(res)

# Left and right bars follow XOR, then horizontally flipped (Left becomes Right, Right becomes Left)
# Let b = [L1,L2,L3, R1,R2,R3]
def step_27(b1, b2, top):
    xored = [x ^ y for x, y in zip(b1, b2)]
    # Horizontal flip: swap left (0..2) and right (3..5)
    flipped = xored[3:6] + xored[0:3]
    return item_27_pattern(flipped[0:3], flipped[3:6], top)

# R1:
b1_1 = [1, 1, 0,  0, 1, 1]
b1_2 = [0, 1, 1,  0, 1, 0]
# XOR: [1, 0, 1,  0, 0, 1] -> Flip: [0, 0, 1,  1, 0, 1]

# R2:
b2_1 = [0, 1, 1,  1, 0, 0]
b2_2 = [1, 1, 0,  1, 1, 0]
# XOR: [1, 0, 1,  0, 1, 0] -> Flip: [0, 1, 0,  1, 0, 1]

# R3:
b3_1 = [1, 0, 1,  1, 1, 0]
b3_2 = [1, 1, 0,  0, 1, 1]
# XOR: [0, 1, 1,  1, 0, 1] -> Flip: [1, 0, 1,  0, 1, 1]
c3_target = [1, 0, 1,  0, 1, 1]

grid_27 = [
    item_27_pattern(b1_1[0:3], b1_1[3:6], 'triangle'),
    item_27_pattern(b1_2[0:3], b1_2[3:6], 'triangle'),
    step_27(b1_1, b1_2, 'triangle'),

    item_27_pattern(b2_1[0:3], b2_1[3:6], 'circle'),
    item_27_pattern(b2_2[0:3], b2_2[3:6], 'circle'),
    step_27(b2_1, b2_2, 'circle'),

    item_27_pattern(b3_1[0:3], b3_1[3:6], 'triangle'),
    item_27_pattern(b3_2[0:3], b3_2[3:6], 'triangle')
]
target_27 = item_27_pattern(c3_target[0:3], c3_target[3:6], 'triangle')
opts_27 = [
    item_27_pattern([0, 1, 1], [1, 0, 1], 'triangle'), # Unflipped XOR (classic distractor!)
    item_27_pattern(c3_target[0:3], c3_target[3:6], 'circle'), # Wrong top shape
    target_27, # Correct (Index 2) - Flipped XOR with triangle
    item_27_pattern([1, 1, 1], [0, 1, 1], 'triangle'),
    item_27_pattern([1, 0, 1], [1, 1, 1], 'triangle'),
    item_27_pattern([0, 1, 0], [1, 0, 1], 'triangle'),
    item_27_pattern([1, 0, 1], [0, 0, 0], 'triangle'),
    rect(20, 20, 60, 60, stroke_width=2.5)
]
items.append({
    "id": 27,
    "difficulty": 5,
    "category": "Integrazione Astratta Multi-Variabile",
    "grid": grid_27,
    "target": target_27,
    "options": opts_27,
    "correct_idx": 2,
    "explanation": "Operazione composta: 1) Le barre orizzontali nelle due metà seguono l'operazione Booleana XOR (Col 1 XOR Col 2); 2) Il pattern risultante viene RIFLESSO SPECULARMENTE lungo l'asse verticale nella colonna 3 (la metà sinistra scambia posizione con la metà destra); 3) L'indicatore in alto mantiene la forma della riga (Triangolo in riga 3). Applicando prima lo XOR e poi la riflessione speculare si ottiene la figura opzione C."
})

# ==========================================
# ITEM 28: 2D Vector Addition on a Grid (C3 = Vector A + Vector B)
# ==========================================
def item_28_vector(vx, vy):
    # origin at (50, 50). Unit = 24 px
    res = [
        rect(20, 20, 60, 60, stroke_width=1.5, stroke="#334155"),
        line(50, 20, 50, 80, stroke="#475569", stroke_width=1, dashed=True),
        line(20, 50, 80, 50, stroke="#475569", stroke_width=1, dashed=True),
        circle(50, 50, 3.5, fill="#94a3b8", stroke="none")
    ]
    if vx == 0 and vy == 0:
        res.append(circle(50, 50, 6, fill="currentColor", stroke="none"))
    else:
        tx = 50 + vx * 24
        ty = 50 + vy * 24
        res.append(arrow(50, 50, tx, ty, stroke="currentColor", stroke_width=3.5, head_len=8))
    return "".join(res)

# R1: (1, 0) [Right] + (0, -1) [Up] = (1, -1) [Diag Up-Right]
# R2: (-1, 0) [Left] + (0, 1) [Down] = (-1, 1) [Diag Down-Left]
# R3: (-1, 0) [Left] + (1, 1) [Diag Down-Right] = (0, 1) [Pure Downward]
grid_28 = [
    item_28_vector(1, 0), item_28_vector(0, -1), item_28_vector(1, -1),
    item_28_vector(-1, 0), item_28_vector(0, 1), item_28_vector(-1, 1),
    item_28_vector(-1, 0), item_28_vector(1, 1)
]
target_28 = item_28_vector(0, 1) # Down arrow (0, 1)
opts_28 = [
    item_28_vector(0, -1), # Up arrow
    item_28_vector(1, 0),  # Right arrow
    target_28, # Correct (Index 2) - Pure Downward
    item_28_vector(-1, 1), # Diag Down-Left
    item_28_vector(1, 1),  # Diag Down-Right
    item_28_vector(0, 0),  # Null vector
    item_28_vector(-1, -1), # Diag Up-Left
    item_28_vector(1, -1)  # Diag Up-Right
]
items.append({
    "id": 28,
    "difficulty": 5,
    "category": "Integrazione Astratta Multi-Variabile",
    "grid": grid_28,
    "target": target_28,
    "options": opts_28,
    "correct_idx": 2,
    "explanation": "Composizione algebrica di vettori nel piano bidimensionale: il vettore nella colonna 3 è la risultante vettoriale esatta (regola del parallelogramma) dei vettori delle colonne 1 e 2: V3 = V1 + V2. In riga 3: Vettore (-1, 0) verso Sinistra + Vettore (1, 1) Diagonale Basso-Destra = la componente orizzontale (-1 + 1 = 0) si annulla, mentre rimane la componente verticale (0 + 1 = 1) verso il Basso. La risultante è una freccia diretta verso il basso."
})

# ==========================================
# ITEM 29: 1D Cellular Automaton Parity (Wolfram Rule 90 / Neighbor XOR)
# ==========================================
def item_29_strip(bits):
    # 5 blocks along x: x=20..80, w=12, gap=2.4
    res = []
    for i, b in enumerate(bits):
        bx = 21 + i * 12
        fill = "currentColor" if b else "none"
        res.append(rect(bx, 40, 10, 20, fill=fill, stroke="currentColor", stroke_width=2))
    return "".join(res)

def rule_90_step(b):
    # b is length 5. Next state at index i is b[i-1] XOR b[i+1] with zero boundary
    n = len(b)
    res = []
    for i in range(n):
        left = b[i-1] if i > 0 else 0
        right = b[i+1] if i < n-1 else 0
        res.append(left ^ right)
    return res

# Row 1:
b1_0 = [0, 1, 0, 1, 0]
b1_1 = rule_90_step(b1_0) # [1, 0, 0, 0, 1]
b1_2 = rule_90_step(b1_1) # [0, 1, 0, 1, 0]

# Row 2:
b2_0 = [0, 0, 1, 0, 0]
b2_1 = rule_90_step(b2_0) # [0, 1, 0, 1, 0]
b2_2 = rule_90_step(b2_1) # [1, 0, 0, 0, 1]

# Row 3:
b3_0 = [1, 0, 1, 0, 1]
b3_1 = rule_90_step(b3_0) # [0, 0, 0, 0, 0] (since 0^1=1? wait: left^right:
# for [1,0,1,0,1]:
# i=0: 0^0 = 0
# i=1: 1^1 = 0
# i=2: 0^0 = 0
# i=3: 1^1 = 0
# i=4: 0^0 = 0
# Next from [0,0,0,0,0] is all 0s! Let's choose a richer pattern:
b3_0 = [1, 1, 0, 0, 1]
# i=0: 0^1 = 1
# i=1: 1^0 = 1
# i=2: 1^0 = 1
# i=3: 0^1 = 1
# i=4: 0^0 = 0
b3_1 = rule_90_step(b3_0) # [1, 1, 1, 1, 0]
# Next step from [1, 1, 1, 1, 0]:
# i=0: 0^1 = 1
# i=1: 1^1 = 0
# i=2: 1^1 = 0
# i=3: 1^0 = 1
# i=4: 1^0 = 1
b3_2 = rule_90_step(b3_1) # [1, 0, 0, 1, 1]

grid_29 = [
    item_29_strip(b1_0), item_29_strip(b1_1), item_29_strip(b1_2),
    item_29_strip(b2_0), item_29_strip(b2_1), item_29_strip(b2_2),
    item_29_strip(b3_0), item_29_strip(b3_1)
]
target_29 = item_29_strip(b3_2) # [1, 0, 0, 1, 1]
opts_29 = [
    item_29_strip([1, 1, 1, 1, 0]), # Previous state
    item_29_strip([0, 1, 1, 0, 0]),
    target_29, # Correct (Index 2) - [1, 0, 0, 1, 1]
    item_29_strip([1, 1, 0, 0, 1]), # Initial state
    item_29_strip([0, 0, 0, 0, 0]), # All empty
    item_29_strip([1, 1, 1, 1, 1]), # All full
    item_29_strip([0, 1, 0, 1, 0]),
    item_29_strip([1, 0, 1, 0, 1])
]
items.append({
    "id": 29,
    "difficulty": 5,
    "category": "Integrazione Astratta Multi-Variabile",
    "grid": grid_29,
    "target": target_29,
    "options": opts_29,
    "correct_idx": 2,
    "explanation": "Regola di evoluzione deterministica locale (Automa Cellulare 1D / Regola di Parità): ciascuna casella al passo successivo è attiva (piena) se e solo se esattamente UNO dei suoi due vicini immediati (sinistra e destra) era attivo al passo precedente (XOR dei vicini). Applicando la trasformazione alla seconda casella [1, 1, 1, 1, 0], il nuovo stato calcolato è [1, 0, 0, 1, 1]."
})

# ==========================================
# ITEM 30: The Master Matrix (Concentric Notched Rings + Regional Parity)
# High ceiling item (IQ 140+ differentiator)
# ==========================================
def item_30_rings(rot_out, rot_mid, rot_in, n_out_dots, n_in_dots):
    # 3 concentric rings: Outer (r=36), Middle (r=26), Inner (r=16)
    # Each ring has a 30° notch/opening at its rotation angle
    res = []
    # Ring notches paths
    for r, rot in [(36, rot_out), (26, rot_mid), (16, rot_in)]:
        # Arc with a gap of 40 degrees centered at rot
        start_a = math.radians(rot + 25)
        end_a = math.radians(rot + 335)
        sx = round(50 + r * math.cos(start_a), 2)
        sy = round(50 + r * math.sin(start_a), 2)
        ex = round(50 + r * math.cos(end_a), 2)
        ey = round(50 + r * math.sin(end_a), 2)
        res.append(f'<path d="M {sx},{sy} A {r},{r} 0 1,1 {ex},{ey}" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" />')

    # Outer dots distributed between mid and out ring (r=31)
    for i in range(n_out_dots):
        a = math.radians(rot_out + 180 + i * (360.0 / max(n_out_dots, 1)))
        dx = round(50 + 31 * math.cos(a), 2)
        dy = round(50 + 31 * math.sin(a), 2)
        res.append(circle(dx, dy, 3.5, fill="currentColor", stroke="none"))

    # Inner dots inside innermost ring (r=9)
    for i in range(n_in_dots):
        a = math.radians(rot_in + 90 + i * (360.0 / max(n_in_dots, 1)))
        dx = round(50 + 9 * math.cos(a), 2)
        dy = round(50 + 9 * math.sin(a), 2)
        res.append(circle(dx, dy, 3.5, fill="currentColor", stroke="none"))

    res.append(circle(50, 50, 2.5, fill="currentColor", stroke="none"))
    return "".join(res)

# Laws:
# 1. Outer ring rotates +90° CW per step (0° -> 90° -> 180°)
# 2. Middle ring rotates -90° CCW per step (0° -> 270° -> 180°)
# 3. Inner ring rotates 180° per step (0° -> 180° -> 0°)
# 4. Parity and Dot conservation: Total dots in system = 6 in all cells
#    Row 3: Outer dots = 4, Inner dots = 2.
# R1: out_rot: 0, 90, 180 | mid_rot: 0, 270, 180 | in_rot: 0, 180, 0 | dots: (2,4), (3,3), (4,2)
# R2: out_rot: 90, 180, 270 | mid_rot: 270, 180, 90 | in_rot: 180, 0, 180 | dots: (3,3), (4,2), (5,1)
# R3: out_rot: 180, 270, 0 | mid_rot: 180, 90, 0 | in_rot: 0, 180, 0 | dots: (4,2), (5,1), [(6,0) or (3,3)? Wait, let's look at progression:
# In R1: (2,4) -> (3,3) -> (4,2) [Outer dots: 2 -> 3 -> 4]
# In R2: (3,3) -> (4,2) -> (5,1) [Outer dots: 3 -> 4 -> 5]
# In R3: (4,2) -> (5,1) -> [(6,0)]! Total dots = 6, outer = 6, inner = 0!
grid_30 = [
    item_30_rings(0, 0, 0, 2, 4), item_30_rings(90, 270, 180, 3, 3), item_30_rings(180, 180, 0, 4, 2),
    item_30_rings(90, 270, 180, 3, 3), item_30_rings(180, 180, 0, 4, 2), item_30_rings(270, 90, 180, 5, 1),
    item_30_rings(180, 180, 0, 4, 2), item_30_rings(270, 90, 180, 5, 1)
]
target_30 = item_30_rings(0, 0, 0, 6, 0) # Outer=0°, Mid=0°, Inner=0°, 6 outer dots, 0 inner dots
opts_30 = [
    item_30_rings(0, 180, 0, 6, 0), # Wrong mid ring rot
    item_30_rings(0, 0, 180, 5, 1), # Wrong dot count
    target_30, # Correct (Index 2)
    item_30_rings(90, 0, 0, 6, 0),  # Wrong outer ring rot
    item_30_rings(0, 0, 0, 5, 1),   # 5 dots outer, 1 inner (failed transfer)
    item_30_rings(180, 0, 0, 6, 0),
    item_30_rings(0, 0, 0, 4, 2),
    circle(50, 50, 36) + circle(50, 50, 26) + circle(50, 50, 16)
]
items.append({
    "id": 30,
    "difficulty": 5,
    "category": "Integrazione Astratta Multi-Variabile",
    "grid": grid_30,
    "target": target_30,
    "options": opts_30,
    "correct_idx": 2,
    "explanation": "Il problema sommo combina tre rotazioni contro-fase e un principio di conservazione dell'invariante: 1) L'anello esterno ruota di +90° in senso orario (in riga 3: 180° → 270° → 0°); 2) L'anello intermedio ruota di 90° in senso antiorario (in riga 3: 180° → 90° → 0°); 3) L'anello interno compie inversioni a 180° (0° → 180° → 0°); 4) Conservazione dei nodi: la somma dei punti è costante (=6), con un trasferimento netto di 1 punto dall'anello interno a quello esterno ad ogni casella (in riga 3: [4 esterni, 2 interni] → [5 esterni, 1 interno] → [6 esterni, 0 interni]). La figura finale ha tutte e tre le tacche allineate a 0° con 6 punti esterni e 0 punti interni."
})

print(f"ALL 30 ITEMS CREATED SUCCESSFULLY! Total items in list: {len(items)}")
