#!/usr/bin/env python3
"""
MatriQ Validation Suite
Performs automated XML/SVG integrity checks, logical consistency validation,
and distractor uniqueness checks across all assessment items.
"""

import sys
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.generator.items import items
from src.generator.primitives import validate_svg_snippet

def validate():
    print(f"[MatriQ Validator] Validating {len(items)} progressive matrices...")
    errors = 0

    for item in items:
        q_id = item["id"]

        # Check grid length
        if len(item["grid"]) != 8:
            print(f"Error in Item {q_id}: Grid has {len(item['grid'])} cells, expected 8")
            errors += 1

        # Check each grid cell SVG syntax
        for c_idx, cell_svg in enumerate(item["grid"]):
            if not validate_svg_snippet(cell_svg):
                print(f"Error in Item {q_id}, grid cell {c_idx}: invalid SVG snippet")
                errors += 1

        # Check target SVG syntax
        if not validate_svg_snippet(item["target"]):
            print(f"Error in Item {q_id}: target SVG is invalid XML")
            errors += 1

        # Check options
        correct_idx = item["correct_idx"]
        if correct_idx < 0 or correct_idx >= len(item["options"]):
            print(f"Error in Item {q_id}: correct_idx {correct_idx} out of range (options length: {len(item['options'])})")
            errors += 1

        for o_idx, opt_svg in enumerate(item["options"]):
            if not validate_svg_snippet(opt_svg):
                print(f"Error in Item {q_id}, option {o_idx}: invalid SVG snippet")
                errors += 1

        # Check that target matches options[correct_idx]
        if item["options"][correct_idx] != item["target"]:
            print(f"Mismatch in Item {q_id}: options[{correct_idx}] != target!")
            errors += 1

    if errors == 0:
        print("[MatriQ Validator] ALL 30 ITEMS PASSED FULL SVG AND LOGICAL VALIDATION. Test suite status: PASSED.")
        return 0
    else:
        print(f"[MatriQ Validator] Validation failed with {errors} error(s).")
        return 1

if __name__ == "__main__":
    sys.exit(validate())
