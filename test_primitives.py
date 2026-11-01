import math
import xml.etree.ElementTree as ET

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

# Verify regular polygon generator
poly = regular_polygon(50, 50, 30, 3, -90)
print("Triangle polygon:", poly)
ET.fromstring(f"<svg xmlns='http://www.w3.org/2000/svg'>{poly}</svg>")
print("XML validation passed!")
