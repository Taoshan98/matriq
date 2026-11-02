#!/usr/bin/env python3
"""
MatriQ Build Pipeline
Compiles modular source templates, mathematical item definitions, and multilingual
dictionaries into the standalone production runtime: index.html
"""

import os
import sys
import json
from pathlib import Path

# Set up project root in python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.generator.items import items
from src.generator.encoder import prepare_dataset
from src.i18n.ui import TRANSLATIONS
from src.i18n.explanations import EXPLANATIONS

def build():
    print(f"[MatriQ Builder] Compiling {len(items)} progressive matrices...")
    
    # Encode items & solutions
    items_json, encoded_solutions = prepare_dataset(items, EXPLANATIONS)
    translations_json = json.dumps(TRANSLATIONS)
    
    template_path = ROOT_DIR / "src" / "templates" / "app_template.html"
    output_path = ROOT_DIR / "index.html"
    
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()
    
    # Inject compiled assets
    compiled = template.replace("__ITEMS_JSON__", items_json)
    compiled = compiled.replace("__ENCODED_SOLUTIONS__", encoded_solutions)
    compiled = compiled.replace("__TRANSLATIONS_JSON__", translations_json)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(compiled)
        
    print(f"[MatriQ Builder] Successfully compiled standalone SPA: {output_path} ({os.path.getsize(output_path):,} bytes)")

if __name__ == "__main__":
    build()
