from items_definition import items, validate_svg_snippet
import sys

print(f"Validating {len(items)} items...")

for item in items:
    q_id = item["id"]
    # Check grid (8 cells)
    if len(item["grid"]) != 8:
        print(f"Error in Item {q_id}: Grid has {len(item['grid'])} cells, expected 8")
        sys.exit(1)
    for c_idx, cell_svg in enumerate(item["grid"]):
        if not validate_svg_snippet(cell_svg):
            print(f"Error in Item {q_id}, grid cell {c_idx}")
            sys.exit(1)

    # Check target
    if not validate_svg_snippet(item["target"]):
        print(f"Error in Item {q_id}, target SVG invalid")
        sys.exit(1)

    # Check options
    correct_idx = item["correct_idx"]
    if correct_idx < 0 or correct_idx >= len(item["options"]):
        print(f"Error in Item {q_id}: correct_idx {correct_idx} out of range (options len: {len(item['options'])})")
        sys.exit(1)

    for o_idx, opt_svg in enumerate(item["options"]):
        if not validate_svg_snippet(opt_svg):
            print(f"Error in Item {q_id}, option {o_idx} SVG invalid")
            sys.exit(1)

    # Check target matches options[correct_idx]
    if item["options"][correct_idx] != item["target"]:
        print(f"Mismatch in Item {q_id}: options[{correct_idx}] != target!")
        sys.exit(1)

print("ALL 30 ITEMS PASSED FULL SVG AND LOGICAL VALIDATION! Perfect.")
