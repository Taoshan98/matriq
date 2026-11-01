import random
import json
import base64
from items_definition import items; from generate_test import SALT, hash_answer

# Deterministic shuffle seed
rng = random.Random(1337)

prepared_items = []
solution_payload = {}

for item in items:
    q_id = item["id"]
    orig_options = list(item["options"])
    correct_opt = orig_options[item["correct_idx"]]
    
    # Shuffle options deterministically
    indices = list(range(len(orig_options)))
    rng.shuffle(indices)
    shuffled_options = [orig_options[i] for i in indices]
    new_correct_idx = shuffled_options.index(correct_opt)
    
    # Verify
    assert shuffled_options[new_correct_idx] == item["target"]
    
    # Answer hash for instant client verification without leaking plain index
    ans_hash = hash_answer(q_id, new_correct_idx)
    
    prepared_items.append({
        "id": q_id,
        "difficulty": item["difficulty"],
        "category": item["category"],
        "grid": item["grid"],
        "options": shuffled_options,
        "hash": ans_hash
    })
    
    solution_payload[str(q_id)] = {
        "correct_idx": new_correct_idx,
        "explanation": item["explanation"]
    }

# Encode solutions in base64 string
encoded_solutions = base64.b64encode(json.dumps(solution_payload).encode('utf-8')).decode('utf-8')

print(f"Prepared {len(prepared_items)} items.")
print("Distribution of correct answer positions:")
counts = {}
for q_id, data in solution_payload.items():
    idx = data["correct_idx"]
    counts[idx] = counts.get(idx, 0) + 1
for idx in sorted(counts.keys()):
    letter = chr(65 + idx)
    print(f"  Option {letter} (index {idx}): {counts[idx]} times")

