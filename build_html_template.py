import json
import base64
import random
from items_definition import items
from generate_test import hash_answer
from i18n_data import TRANSLATIONS
from translate_explanations import EXPLANATIONS

rng = random.Random(1337)

prepared_items = []
solution_payload = {}

for item in items:
    q_id = item["id"]
    orig_options = list(item["options"])
    correct_opt = orig_options[item["correct_idx"]]
    
    indices = list(range(len(orig_options)))
    rng.shuffle(indices)
    shuffled_options = [orig_options[i] for i in indices]
    new_correct_idx = shuffled_options.index(correct_opt)
    
    ans_hash = hash_answer(q_id, new_correct_idx)
    
    prepared_items.append({
        "id": q_id,
        "difficulty": item["difficulty"],
        "category_key": item["category"],
        "grid": item["grid"],
        "options": shuffled_options,
        "hash": ans_hash
    })
    
    multilingual_expl = EXPLANATIONS.get(q_id, {
        "it": item["explanation"],
        "en": item["explanation"],
        "de": item["explanation"],
        "es": item["explanation"],
        "pt": item["explanation"],
        "fr": item["explanation"]
    })
    
    solution_payload[str(q_id)] = {
        "correct_idx": new_correct_idx,
        "category_key": item["category"],
        "difficulty": item["difficulty"],
        "explanations": multilingual_expl
    }

encoded_solutions = base64.b64encode(json.dumps(solution_payload).encode('utf-8')).decode('utf-8')
items_json = json.dumps(prepared_items)
translations_json = json.dumps(TRANSLATIONS)

with open("app_template.html", "r", encoding="utf-8") as f:
    template = f.read()

final_html = template.replace("__ITEMS_JSON__", items_json)
final_html = final_html.replace("__ENCODED_SOLUTIONS__", encoded_solutions)
final_html = final_html.replace("__TRANSLATIONS_JSON__", translations_json)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(final_html)

print("Advanced multilingual index.html generated successfully via template!")
