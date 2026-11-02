import math
import hashlib
import xml.etree.ElementTree as ET

SALT = "ANTIGRAVITY_PSYCHOMETRICS_2026_MATRIX_TEST"

def hash_answer(item_id, correct_idx):
    raw = f"{SALT}_{item_id}_{correct_idx}"
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()

def validate_svg_snippet(snippet):
    full = f"<svg xmlns='http://www.w3.org/2000/svg'>{snippet}</svg>"
    try:
        ET.fromstring(full)
        return True
    except Exception as e:
        print(f"XML Error in snippet: {e}\nSnippet:\n{snippet}")
        return False

# Base SVG Primitives
def circle(cx, cy, r, fill="none", stroke="currentColor", stroke_width=2.5):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}" />'

def rect(x, y, w, h, fill="none", stroke="currentColor", stroke_width=2.5, rx=0):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}" />'

def line(x1, y1, x2, y2, stroke="currentColor", stroke_width=2.5, dashed=False):
    dash = ' stroke-dasharray="4,4"' if dashed else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{stroke_width}" stroke-linecap="round"{dash} />'

def polygon(points, fill="none", stroke="currentColor", stroke_width=2.5):
    pts = " ".join(f"{x},{y}" for x, y in points)
    return f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}" stroke-linejoin="round" />'

def regular_polygon(cx, cy, r, sides, rot_deg=0, fill="none", stroke="currentColor", stroke_width=2.5):
    points = []
    for i in range(sides):
        angle = math.radians(rot_deg + i * (360.0 / sides))
        px = round(cx + r * math.cos(angle), 2)
        py = round(cy + r * math.sin(angle), 2)
        points.append((px, py))
    return polygon(points, fill, stroke, stroke_width)

def star(cx, cy, r_outer, r_inner, points, rot_deg=0, fill="none", stroke="currentColor", stroke_width=2.5):
    pts = []
    step = 360.0 / (points * 2)
    for i in range(points * 2):
        angle = math.radians(rot_deg + i * step)
        r = r_outer if i % 2 == 0 else r_inner
        px = round(cx + r * math.cos(angle), 2)
        py = round(cy + r * math.sin(angle), 2)
        pts.append((px, py))
    return polygon(pts, fill, stroke, stroke_width)

def arrow(x1, y1, x2, y2, stroke="currentColor", stroke_width=2.5, head_len=8):
    dx = x2 - x1
    dy = y2 - y1
    angle = math.atan2(dy, dx)
    l1_x = round(x2 - head_len * math.cos(angle - math.pi / 6), 2)
    l1_y = round(y2 - head_len * math.sin(angle - math.pi / 6), 2)
    l2_x = round(x2 - head_len * math.cos(angle + math.pi / 6), 2)
    l2_y = round(y2 - head_len * math.sin(angle + math.pi / 6), 2)
    return (line(x1, y1, x2, y2, stroke, stroke_width) +
            line(x2, y2, l1_x, l1_y, stroke, stroke_width) +
            line(x2, y2, l2_x, l2_y, stroke, stroke_width))

def make_dot(cx, cy, r=4.5, fill="currentColor"):
    return circle(cx, cy, r, fill=fill, stroke="none")
