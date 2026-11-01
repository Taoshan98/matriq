import json
import xml.etree.ElementTree as ET
import hashlib

def validate_svg(svg_str):
    try:
        ET.fromstring(f"<svg xmlns='http://www.w3.org/2000/svg'>{svg_str}</svg>")
        return True
    except Exception as e:
        print("SVG XML Error:", e)
        print("String was:", svg_str)
        return False

print("Script template ready.")
