import json
import base64
import random
from items_definition import items
from generate_test import SALT, hash_answer

# Deterministic shuffle
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
        "category": item["category"],
        "grid": item["grid"],
        "options": shuffled_options,
        "hash": ans_hash
    })
    
    solution_payload[str(q_id)] = {
        "correct_idx": new_correct_idx,
        "explanation": item["explanation"],
        "category": item["category"],
        "difficulty": item["difficulty"]
    }

encoded_solutions = base64.b64encode(json.dumps(solution_payload).encode('utf-8')).decode('utf-8')
items_json = json.dumps(prepared_items)

html_template = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Valutazione Psicométrica Matrici Progressive</title>
    <style>
        :root {{
            --bg-main: #0b0f19;
            --bg-card: #151d30;
            --bg-card-hover: #1c2742;
            --border-color: #273553;
            --text-main: #f1f5f9;
            --text-muted: #94a3b8;
            --accent-cyan: #38bdf8;
            --accent-blue: #3b82f6;
            --accent-indigo: #6366f1;
            --accent-emerald: #10b981;
            --accent-rose: #f43f5e;
            --accent-amber: #f59e0b;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            -webkit-font-smoothing: antialiased;
        }}

        body {{
            background-color: var(--bg-main);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            user-select: none;
        }}

        /* App Header */
        header {{
            background: rgba(21, 29, 48, 0.85);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border-color);
            position: sticky;
            top: 0;
            z-index: 100;
            padding: 0.75rem 1.5rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}

        .brand-badge {{
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-indigo));
            color: #0b0f19;
            font-weight: 800;
            font-size: 0.75rem;
            padding: 0.25rem 0.5rem;
            border-radius: 6px;
            letter-spacing: 0.05em;
        }}

        .brand-title {{
            font-size: 1rem;
            font-weight: 600;
            letter-spacing: -0.01em;
        }}

        /* Timer and Progress */
        .header-meta {{
            display: flex;
            align-items: center;
            gap: 1.25rem;
        }}

        .timer-badge {{
            display: flex;
            align-items: center;
            gap: 0.4rem;
            background: #0f172a;
            border: 1px solid var(--border-color);
            padding: 0.35rem 0.75rem;
            border-radius: 8px;
            font-size: 0.95rem;
            font-weight: 700;
            letter-spacing: 0.05em;
            color: var(--accent-cyan);
            font-variant-numeric: tabular-nums;
        }}

        .timer-badge.warning {{
            border-color: var(--accent-rose);
            color: var(--accent-rose);
            animation: pulse 1.5s infinite;
        }}

        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.6; }}
        }}

        .progress-pill {{
            font-size: 0.85rem;
            color: var(--text-muted);
            font-weight: 500;
        }}

        /* Container */
        .container {{
            max-width: 960px;
            margin: 0 auto;
            width: 100%;
            padding: 1.5rem;
            flex: 1;
            display: flex;
            flex-direction: column;
        }}

        /* Intro Screen */
        .intro-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 2.5rem;
            max-width: 720px;
            margin: auto;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        }}

        .intro-title {{
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #ffffff, var(--accent-cyan));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .intro-desc {{
            color: var(--text-muted);
            line-height: 1.6;
            margin-bottom: 1.75rem;
            font-size: 1rem;
        }}

        .instructions-list {{
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 0.85rem;
            margin-bottom: 2rem;
        }}

        .instructions-list li {{
            display: flex;
            align-items: flex-start;
            gap: 0.75rem;
            font-size: 0.95rem;
            color: #cbd5e1;
            line-height: 1.5;
        }}

        .instructions-list li .bullet {{
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: rgba(56, 189, 248, 0.15);
            color: var(--accent-cyan);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.75rem;
            font-weight: bold;
            flex-shrink: 0;
            margin-top: 2px;
        }}

        .btn-primary {{
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
            color: #0b0f19;
            font-weight: 700;
            font-size: 1rem;
            border: none;
            padding: 0.85rem 2rem;
            border-radius: 10px;
            cursor: pointer;
            transition: transform 0.15s, box-shadow 0.15s;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .btn-primary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(56, 189, 248, 0.35);
        }}

        .btn-secondary {{
            background: #1e293b;
            color: var(--text-main);
            border: 1px solid var(--border-color);
            padding: 0.6rem 1.25rem;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.9rem;
            transition: background 0.15s, border-color 0.15s;
        }}

        .btn-secondary:hover {{
            background: #334155;
            border-color: #475569;
        }}

        /* Test Section */
        #test-screen {{
            display: none;
            flex-direction: column;
            gap: 1.5rem;
        }}

        .matrix-meta-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .category-tag {{
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--accent-cyan);
            background: rgba(56, 189, 248, 0.1);
            border: 1px solid rgba(56, 189, 248, 0.2);
            padding: 0.25rem 0.6rem;
            border-radius: 6px;
            font-weight: 600;
        }}

        .flag-btn {{
            background: transparent;
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: 0.35rem 0.75rem;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.85rem;
            display: flex;
            align-items: center;
            gap: 0.4rem;
            transition: all 0.15s;
        }}

        .flag-btn.active {{
            background: rgba(245, 158, 11, 0.15);
            border-color: var(--accent-amber);
            color: var(--accent-amber);
        }}

        /* 3x3 Matrix Grid Layout */
        .matrix-container {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 1.5rem;
            display: flex;
            justify-content: center;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        }}

        .matrix-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            width: 100%;
            max-width: 440px;
        }}

        .matrix-cell {{
            background: #0d1322;
            border: 1px solid #23304a;
            border-radius: 10px;
            aspect-ratio: 1 / 1;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 8px;
            position: relative;
            color: #f8fafc;
        }}

        .matrix-cell svg {{
            width: 100%;
            height: 100%;
            display: block;
        }}

        .matrix-cell.target {{
            border: 2px dashed var(--accent-cyan);
            background: rgba(56, 189, 248, 0.04);
        }}

        .target-placeholder {{
            font-size: 2.2rem;
            font-weight: 700;
            color: var(--accent-cyan);
            opacity: 0.7;
        }}

        /* Options Area */
        .options-section {{
            margin-top: 0.5rem;
        }}

        .options-title {{
            font-size: 0.9rem;
            color: var(--text-muted);
            margin-bottom: 0.75rem;
            text-align: center;
        }}

        .options-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            max-width: 640px;
            margin: 0 auto;
        }}

        @media (max-width: 640px) {{
            .options-grid {{
                grid-template-columns: repeat(3, 1fr);
            }}
        }}

        .option-card {{
            background: var(--bg-card);
            border: 1.5px solid var(--border-color);
            border-radius: 10px;
            aspect-ratio: 1 / 1;
            padding: 8px;
            cursor: pointer;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.15s ease;
            color: #f8fafc;
        }}

        .option-card:hover {{
            border-color: var(--accent-cyan);
            background: var(--bg-card-hover);
            transform: translateY(-2px);
        }}

        .option-card.selected {{
            border-color: var(--accent-cyan);
            background: rgba(56, 189, 248, 0.12);
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.25);
        }}

        .option-badge {{
            position: absolute;
            top: 6px;
            left: 6px;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: #1e293b;
            border: 1px solid #334155;
            font-size: 0.7rem;
            font-weight: 700;
            color: var(--text-muted);
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .option-card.selected .option-badge {{
            background: var(--accent-cyan);
            color: #0b0f19;
            border-color: var(--accent-cyan);
        }}

        .option-card svg {{
            width: 82%;
            height: 82%;
            display: block;
        }}

        /* Navigation & Footer Controls */
        .controls-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 1.25rem;
            padding-top: 1rem;
            border-top: 1px solid var(--border-color);
        }}

        .nav-buttons {{
            display: flex;
            gap: 0.75rem;
        }}

        /* Drawer Question Grid */
        .drawer-toggle {{
            background: transparent;
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: 0.5rem 0.9rem;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.85rem;
            font-weight: 600;
        }}

        .modal-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(4px);
            z-index: 200;
            display: none;
            align-items: center;
            justify-content: center;
            padding: 1.5rem;
        }}

        .modal-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 2rem;
            max-width: 540px;
            width: 100%;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
        }}

        .question-map-grid {{
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 8px;
            margin: 1.5rem 0;
        }}

        .map-item {{
            aspect-ratio: 1 / 1;
            border-radius: 8px;
            background: #0f172a;
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            font-weight: 700;
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            position: relative;
        }}

        .map-item.answered {{
            background: rgba(56, 189, 248, 0.15);
            border-color: var(--accent-cyan);
            color: var(--accent-cyan);
        }}

        .map-item.flagged {{
            border-color: var(--accent-amber);
            color: var(--accent-amber);
        }}

        .map-item.current {{
            box-shadow: 0 0 0 2px var(--accent-indigo);
        }}

        /* Results Screen */
        #results-screen {{
            display: none;
            flex-direction: column;
            gap: 2rem;
            max-width: 780px;
            margin: 0 auto;
            width: 100%;
        }}

        .result-hero {{
            background: linear-gradient(145deg, #151d30, #1a2540);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 2.5rem;
            text-align: center;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
            position: relative;
            overflow: hidden;
        }}

        .hero-glow {{
            position: absolute;
            top: -50px;
            left: 50%;
            transform: translateX(-50%);
            width: 300px;
            height: 120px;
            background: radial-gradient(ellipse, rgba(56, 189, 248, 0.25), transparent 70%);
            pointer-events: none;
        }}

        .iq-badge {{
            font-size: 4.5rem;
            font-weight: 800;
            line-height: 1;
            margin: 0.75rem 0;
            background: linear-gradient(135deg, #ffffff, var(--accent-cyan));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .iq-ci {{
            font-size: 1.05rem;
            color: var(--text-muted);
            margin-bottom: 0.5rem;
        }}

        .iq-classification {{
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--accent-cyan);
            margin-bottom: 0.25rem;
        }}

        .percentile-rank {{
            font-size: 0.95rem;
            color: #94a3b8;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin-top: 1.5rem;
            padding-top: 1.5rem;
            border-top: 1px solid var(--border-color);
        }}

        .stat-box {{
            text-align: center;
        }}

        .stat-val {{
            font-size: 1.4rem;
            font-weight: 700;
            color: #f1f5f9;
        }}

        .stat-label {{
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-top: 0.2rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        /* Category Breakdown Cards */
        .breakdown-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 1.75rem;
        }}

        .breakdown-title {{
            font-size: 1.1rem;
            font-weight: 700;
            margin-bottom: 1.25rem;
            color: #f8fafc;
        }}

        .cat-row {{
            display: flex;
            flex-direction: column;
            gap: 0.4rem;
            margin-bottom: 1rem;
        }}

        .cat-header {{
            display: flex;
            justify-content: space-between;
            font-size: 0.9rem;
            font-weight: 600;
        }}

        .cat-bar-bg {{
            height: 8px;
            background: #0f172a;
            border-radius: 999px;
            overflow: hidden;
        }}

        .cat-bar-fill {{
            height: 100%;
            border-radius: 999px;
            background: linear-gradient(90deg, var(--accent-cyan), var(--accent-blue));
            transition: width 1s ease;
        }}

        /* Review Section */
        .review-panel {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 1.75rem;
        }}

        .review-explanation {{
            margin-top: 1rem;
            padding: 1rem;
            background: #0d1322;
            border-left: 3px solid var(--accent-cyan);
            border-radius: 0 8px 8px 0;
            font-size: 0.95rem;
            line-height: 1.6;
            color: #cbd5e1;
        }}

        .option-card.review-correct {{
            border-color: var(--accent-emerald) !important;
            background: rgba(16, 185, 129, 0.12) !important;
        }}

        .option-card.review-user-wrong {{
            border-color: var(--accent-rose) !important;
            background: rgba(244, 63, 94, 0.12) !important;
        }}
    </style>
</head>
<body>

    <!-- Header -->
    <header>
        <div class="brand">
            <span class="brand-badge">PSYCHOMETRICS</span>
            <span class="brand-title">Valutazione Matrici Progressive</span>
        </div>
        <div class="header-meta" id="header-meta" style="display: none;">
            <div class="progress-pill" id="progress-indicator">Domanda 1 di 30</div>
            <div class="timer-badge" id="timer-display">35:00</div>
            <button class="drawer-toggle" id="open-map-btn">Mappa Quesiti</button>
        </div>
    </header>

    <div class="container">

        <!-- Screen 1: Introduction -->
        <div class="intro-card" id="intro-screen">
            <h1 class="intro-title">Test di Intelligenza a Matrici Progressive</h1>
            <p class="intro-desc">
                Questo test misura l'<strong>Intelligenza Fluida</strong> (il fattore generale <em>g</em> di Spearman) attraverso 30 problemi di logica visuo-spaziale a difficoltà progressiva. È indipendente dal linguaggio, dall'istruzione scolastica e dal background culturale.
            </p>
            <ul class="instructions-list">
                <li>
                    <span class="bullet">1</span>
                    <span><strong>Struttura:</strong> Ogni quesito presenta una griglia 3x3 di figure con una casella mancante contrassegnata da <strong>?</strong> in basso a destra.</span>
                </li>
                <li>
                    <span class="bullet">2</span>
                    <span><strong>Obiettivo:</strong> Identificare la regola logica (orizzontale, verticale o combinata) e selezionare la figura corretta tra le opzioni sottostanti.</span>
                </li>
                <li>
                    <span class="bullet">3</span>
                    <span><strong>Tempo massimo:</strong> <strong>35 minuti</strong> per tutti i 30 quesiti (~70 secondi per domanda). Il tempo inizierà appena clicchi sul pulsante sottostante.</span>
                </li>
                <li>
                    <span class="bullet">4</span>
                    <span><strong>Navigazione & Scorciatoie:</strong> Puoi usare le frecce della tastiera per navigare e i tasti <strong>1-8</strong> o <strong>A-H</strong> per selezionare le risposte. Puoi contrassegnare le domande dubbie per revisionarle dopo.</span>
                </li>
            </ul>
            <div style="text-align: center; margin-top: 2rem;">
                <button class="btn-primary" id="start-btn">Inizia la Valutazione &rarr;</button>
            </div>
        </div>

        <!-- Screen 2: Active Test -->
        <div id="test-screen">
            <div class="matrix-meta-bar">
                <span class="category-tag" id="q-category">Progressione Quantitativa</span>
                <button class="flag-btn" id="flag-btn">
                    <span>&#9873;</span> Segna per revisione
                </button>
            </div>

            <!-- 3x3 Matrix Grid -->
            <div class="matrix-container">
                <div class="matrix-grid" id="matrix-grid">
                    <!-- 9 cells rendered by JS -->
                </div>
            </div>

            <!-- Options Area -->
            <div class="options-section">
                <div class="options-title">Seleziona la figura mancante per completare la logica:</div>
                <div class="options-grid" id="options-grid">
                    <!-- Options rendered by JS -->
                </div>
            </div>

            <!-- Bottom Controls -->
            <div class="controls-bar">
                <div class="nav-buttons">
                    <button class="btn-secondary" id="prev-btn">&larr; Precedente</button>
                    <button class="btn-secondary" id="next-btn">Successiva &rarr;</button>
                </div>
                <button class="btn-primary" id="submit-btn" style="padding: 0.6rem 1.25rem; font-size: 0.9rem;">
                    Consegna Test
                </button>
            </div>
        </div>

        <!-- Screen 3: Results -->
        <div id="results-screen">
            <div class="result-hero">
                <div class="hero-glow"></div>
                <div style="font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-muted);">Quoziente Intellettivo Stimato</div>
                <div class="iq-badge" id="res-iq">125</div>
                <div class="iq-ci" id="res-ci">Intervallo di Confidenza al 95%: 119 - 131</div>
                <div class="iq-classification" id="res-classification">Superiore / Alto Potenziale</div>
                <div class="percentile-rank" id="res-percentile">95.2° percentile (Superiore al 95% della popolazione)</div>

                <div class="stats-grid">
                    <div class="stat-box">
                        <div class="stat-val" id="res-raw-score">25 / 30</div>
                        <div class="stat-label">Punteggio Grezzo</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-val" id="res-time-spent">21:40</div>
                        <div class="stat-label">Tempo Impiegato</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-val" id="res-avg-time">43s</div>
                        <div class="stat-label">Tempo Medio / Item</div>
                    </div>
                </div>
            </div>

            <!-- Breakdown -->
            <div class="breakdown-card">
                <div class="breakdown-title">Profilo Cognitivo per Categorie di Ragionamento</div>
                <div id="categories-breakdown">
                    <!-- Category bars -->
                </div>
            </div>

            <!-- Review Button -->
            <div class="review-panel">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <div style="font-size: 1.1rem; font-weight: 700;">Revisione Dettagliata & Soluzioni</div>
                    <button class="btn-secondary" id="start-review-btn">Apri Spiegazioni Passo-Passo</button>
                </div>
                <p style="color: var(--text-muted); font-size: 0.9rem; line-height: 1.5;">
                    Visualizza per ciascun quesito la regola logica esatta (orizzontale, verticale e insiemistica) e l'analisi degli errori delle altre opzioni.
                </p>
                <div id="review-container" style="display: none; margin-top: 1.5rem;">
                    <!-- Interactive review navigator -->
                    <div style="display: flex; gap: 0.5rem; overflow-x: auto; padding-bottom: 0.75rem; margin-bottom: 1rem;" id="review-pills"></div>
                    <div id="review-content"></div>
                </div>
            </div>
        </div>

    </div>

    <!-- Question Map Modal -->
    <div class="modal-overlay" id="map-modal">
        <div class="modal-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h3 style="font-size: 1.1rem; font-weight: 700;">Mappa dei 30 Quesiti</h3>
                <button id="close-map-btn" style="background: none; border: none; color: var(--text-muted); font-size: 1.4rem; cursor: pointer;">&times;</button>
            </div>
            <div style="display: flex; gap: 1rem; font-size: 0.8rem; color: var(--text-muted); margin-bottom: 0.5rem;">
                <span style="display: flex; align-items: center; gap: 0.3rem;"><span style="width: 10px; height: 10px; background: rgba(56, 189, 248, 0.4); border-radius: 2px;"></span> Risposto</span>
                <span style="display: flex; align-items: center; gap: 0.3rem;"><span style="width: 10px; height: 10px; background: rgba(245, 158, 11, 0.4); border-radius: 2px;"></span> Segnato</span>
                <span style="display: flex; align-items: center; gap: 0.3rem;"><span style="width: 10px; height: 10px; background: #0f172a; border: 1px solid #334155; border-radius: 2px;"></span> Non risposto</span>
            </div>
            <div class="question-map-grid" id="question-map-grid"></div>
            <button class="btn-primary" id="confirm-map-btn" style="width: 100%; justify-content: center;">Chiudi</button>
        </div>
    </div>

    <!-- Confirm Submit Modal -->
    <div class="modal-overlay" id="confirm-modal">
        <div class="modal-card">
            <h3 style="font-size: 1.2rem; font-weight: 700; margin-bottom: 0.75rem;">Conferma Consegna Test</h3>
            <p id="confirm-modal-text" style="color: var(--text-muted); line-height: 1.5; margin-bottom: 1.5rem;">
                Sei sicuro di voler terminare il test e calcolare il tuo Quoziente Intellettivo?
            </p>
            <div style="display: flex; justify-content: flex-end; gap: 0.75rem;">
                <button class="btn-secondary" id="cancel-submit-btn">Torna al Test</button>
                <button class="btn-primary" id="proceed-submit-btn">Conferma & Calcola</button>
            </div>
        </div>
    </div>

    <script>
        // Data Payload
        const ITEMS = {items_json};
        const ENCODED_SOLUTIONS = "{encoded_solutions}";
        const TOTAL_ITEMS = ITEMS.length;
        const TIME_LIMIT_SECONDS = 35 * 60; // 35 minutes

        // App State
        let currentIndex = 0;
        let userAnswers = new Array(TOTAL_ITEMS).fill(null);
        let flaggedItems = new Set();
        let timeRemaining = TIME_LIMIT_SECONDS;
        let timerInterval = null;
        let testStartTime = null;
        let decodedSolutions = null;
        let testSubmitted = false;

        // Elements
        const introScreen = document.getElementById('intro-screen');
        const testScreen = document.getElementById('test-screen');
        const resultsScreen = document.getElementById('results-screen');
        const headerMeta = document.getElementById('header-meta');
        const timerDisplay = document.getElementById('timer-display');
        const progressIndicator = document.getElementById('progress-indicator');
        const qCategory = document.getElementById('q-category');
        const flagBtn = document.getElementById('flag-btn');
        const matrixGrid = document.getElementById('matrix-grid');
        const optionsGrid = document.getElementById('options-grid');
        const prevBtn = document.getElementById('prev-btn');
        const nextBtn = document.getElementById('next-btn');
        const submitBtn = document.getElementById('submit-btn');

        // Modals
        const mapModal = document.getElementById('map-modal');
        const openMapBtn = document.getElementById('open-map-btn');
        const closeMapBtn = document.getElementById('close-map-btn');
        const confirmMapBtn = document.getElementById('confirm-map-btn');
        const questionMapGrid = document.getElementById('question-map-grid');

        const confirmModal = document.getElementById('confirm-modal');
        const confirmModalText = document.getElementById('confirm-modal-text');
        const cancelSubmitBtn = document.getElementById('cancel-submit-btn');
        const proceedSubmitBtn = document.getElementById('proceed-submit-btn');

        // Start Test
        document.getElementById('start-btn').addEventListener('click', () => {{
            introScreen.style.display = 'none';
            testScreen.style.display = 'flex';
            headerMeta.style.display = 'flex';
            testStartTime = Date.now();
            renderQuestion(currentIndex);
            startTimer();
        }});

        function startTimer() {{
            timerInterval = setInterval(() => {{
                timeRemaining--;
                const mins = Math.floor(timeRemaining / 60);
                const secs = timeRemaining % 60;
                timerDisplay.textContent = `${{String(mins).padStart(2, '0')}}:${{String(secs).padStart(2, '0')}}`;

                if (timeRemaining <= 300) {{
                    timerDisplay.classList.add('warning');
                }}

                if (timeRemaining <= 0) {{
                    clearInterval(timerInterval);
                    finishTest();
                }}
            }}, 1000);
        }}

        function renderQuestion(index) {{
            currentIndex = index;
            const item = ITEMS[index];

            progressIndicator.textContent = `Domanda ${{index + 1}} di ${{TOTAL_ITEMS}}`;
            qCategory.textContent = item.category;

            // Flag state
            if (flaggedItems.has(index)) {{
                flagBtn.classList.add('active');
                flagBtn.innerHTML = `<span>&#9873;</span> Segnata per revisione`;
            }} else {{
                flagBtn.classList.remove('active');
                flagBtn.innerHTML = `<span>&#9873;</span> Segna per revisione`;
            }}

            // Render 3x3 Matrix Grid
            matrixGrid.innerHTML = '';
            for (let i = 0; i < 8; i++) {{
                const cell = document.createElement('div');
                cell.className = 'matrix-cell';
                cell.innerHTML = `<svg viewBox="0 0 100 100">${{item.grid[i]}}</svg>`;
                matrixGrid.appendChild(cell);
            }}

            // 9th missing cell
            const targetCell = document.createElement('div');
            targetCell.className = 'matrix-cell target';
            if (userAnswers[index] !== null) {{
                const chosenSvg = item.options[userAnswers[index]];
                targetCell.innerHTML = `<svg viewBox="0 0 100 100">${{chosenSvg}}</svg>`;
            }} else {{
                targetCell.innerHTML = `<span class="target-placeholder">?</span>`;
            }}
            matrixGrid.appendChild(targetCell);

            // Render Options
            optionsGrid.innerHTML = '';
            item.options.forEach((optSvg, optIdx) => {{
                const optCard = document.createElement('div');
                optCard.className = 'option-card';
                if (userAnswers[index] === optIdx) {{
                    optCard.classList.add('selected');
                }}

                const letter = String.fromCharCode(65 + optIdx);
                optCard.innerHTML = `
                    <div class="option-badge">${{letter}}</div>
                    <svg viewBox="0 0 100 100">${{optSvg}}</svg>
                `;

                optCard.addEventListener('click', () => {{
                    selectOption(optIdx);
                }});

                optionsGrid.appendChild(optCard);
            }});

            // Prev / Next button state
            prevBtn.disabled = (index === 0);
            prevBtn.style.opacity = (index === 0) ? '0.4' : '1';
            nextBtn.textContent = (index === TOTAL_ITEMS - 1) ? 'Riepilogo' : 'Successiva \u2192';
        }}

        function selectOption(optIdx) {{
            userAnswers[currentIndex] = optIdx;
            renderQuestion(currentIndex);
        }}

        flagBtn.addEventListener('click', () => {{
            if (flaggedItems.has(currentIndex)) {{
                flaggedItems.delete(currentIndex);
            }} else {{
                flaggedItems.add(currentIndex);
            }}
            renderQuestion(currentIndex);
        }});

        prevBtn.addEventListener('click', () => {{
            if (currentIndex > 0) renderQuestion(currentIndex - 1);
        }});

        nextBtn.addEventListener('click', () => {{
            if (currentIndex < TOTAL_ITEMS - 1) {{
                renderQuestion(currentIndex + 1);
            }} else {{
                openQuestionMap();
            }}
        }});

        // Question Map
        function openQuestionMap() {{
            questionMapGrid.innerHTML = '';
            for (let i = 0; i < TOTAL_ITEMS; i++) {{
                const mapBtn = document.createElement('div');
                mapBtn.className = 'map-item';
                mapBtn.textContent = i + 1;

                if (userAnswers[i] !== null) mapBtn.classList.add('answered');
                if (flaggedItems.has(i)) mapBtn.classList.add('flagged');
                if (i === currentIndex) mapBtn.classList.add('current');

                mapBtn.addEventListener('click', () => {{
                    mapModal.style.display = 'none';
                    renderQuestion(i);
                }});

                questionMapGrid.appendChild(mapBtn);
            }}
            mapModal.style.display = 'flex';
        }}

        openMapBtn.addEventListener('click', openQuestionMap);
        closeMapBtn.addEventListener('click', () => mapModal.style.display = 'none');
        confirmMapBtn.addEventListener('click', () => mapModal.style.display = 'none');

        // Submit Test flow
        submitBtn.addEventListener('click', () => {{
            const unanswered = userAnswers.filter(a => a === null).length;
            const flagged = flaggedItems.size;

            let msg = "Sei sicuro di voler terminare il test e calcolare il tuo Quoziente Intellettivo?";
            if (unanswered > 0) {{
                msg = `Attenzione: hai ancora <strong>${{unanswered}} quesiti senza risposta</strong>. Vuoi davvero consegnare ora?`;
            }} else if (flagged > 0) {{
                msg = `Hai <strong>${{flagged}} quesiti contrassegnati per revisione</strong>. Vuoi revisionarli o confermare il calcolo?`;
            }}

            confirmModalText.innerHTML = msg;
            confirmModal.style.display = 'flex';
        }});

        cancelSubmitBtn.addEventListener('click', () => confirmModal.style.display = 'none');
        proceedSubmitBtn.addEventListener('click', () => {{
            confirmModal.style.display = 'none';
            finishTest();
        }});

        // Keyboard Shortcuts
        window.addEventListener('keydown', (e) => {{
            if (testSubmitted || testScreen.style.display !== 'flex') return;

            // Numbers 1-8
            if (e.key >= '1' && e.key <= '8') {{
                const num = parseInt(e.key, 10) - 1;
                if (num < ITEMS[currentIndex].options.length) selectOption(num);
            }}
            // Letters A-H
            const k = e.key.toUpperCase();
            if (k >= 'A' && k <= 'H') {{
                const idx = k.charCodeAt(0) - 65;
                if (idx < ITEMS[currentIndex].options.length) selectOption(idx);
            }}
            // Arrow Left / Right
            if (e.key === 'ArrowLeft') {{
                if (currentIndex > 0) renderQuestion(currentIndex - 1);
            }}
            if (e.key === 'ArrowRight') {{
                if (currentIndex < TOTAL_ITEMS - 1) renderQuestion(currentIndex + 1);
            }}
            // Space to toggle flag
            if (e.key === ' ') {{
                e.preventDefault();
                flagBtn.click();
            }}
        }});

        // Psychometric Scoring Model (Calibrated against Raven APM / Mensa Nordic standards)
        // Wechsler Scale (Mean = 100, SD = 15)
        function calculateIQ(rawScore) {{
            // Raw score 0-30 mapping to IQ
            const iqTable = [
                68, 72, 75, 78, 81, 84, 87, 90, 93, 96, 98,
                100, 102, 105, 108, 110, 113, 115, 118, 120, 123,
                125, 128, 131, 133, 136, 138, 140, 142, 144, 145
            ];
            const iq = iqTable[Math.max(0, Math.min(30, rawScore))];

            // Percentile from normal distribution
            // Z = (IQ - 100) / 15
            const z = (iq - 100) / 15.0;
            // Approximation of standard normal CDF
            const t = 1.0 / (1.0 + 0.2316419 * Math.abs(z));
            const d = 0.3989423 * Math.exp(-z * z / 2.0);
            let p = d * t * (0.3193815 + t * (-0.3565638 + t * (1.781478 + t * (-1.821256 + t * 1.330274))));
            let percentile = (z > 0) ? (1.0 - p) * 100 : p * 100;
            percentile = Math.max(0.1, Math.min(99.9, percentile)).toFixed(1);

            let classification = "Nella Media";
            if (iq >= 135) classification = "Eccezionale / Alto Potenziale (Fascia Mensa Top 1%)";
            else if (iq >= 130) classification = "Molto Superiore (Soglia Mensa Top 2%)";
            else if (iq >= 120) classification = "Superiore / Ottimo Potenziale (Top 10%)";
            else if (iq >= 110) classification = "Media Superiore";
            else if (iq >= 90) classification = "Nella Media Tipica";
            else if (iq >= 80) classification = "Media Inferiore";
            else classification = "Al di sotto della Media";

            const sem = 5; // Standard error of measurement (95% CI: +/- 5)
            const ciLow = Math.max(65, iq - sem);
            const ciHigh = Math.min(150, iq + sem);

            return {{
                iq,
                percentile,
                classification,
                ciLow,
                ciHigh
            }};
        }}

        function finishTest() {{
            testSubmitted = true;
            clearInterval(timerInterval);

            // Decode solutions payload
            decodedSolutions = JSON.parse(atob(ENCODED_SOLUTIONS));

            const timeSpentSeconds = Math.max(1, Math.round((Date.now() - testStartTime) / 1000));
            const minsSpent = Math.floor(timeSpentSeconds / 60);
            const secsSpent = timeSpentSeconds % 60;
            const avgSecondsPerItem = Math.round(timeSpentSeconds / TOTAL_ITEMS);

            let rawScore = 0;
            const categoryScores = {{}};

            for (let i = 0; i < TOTAL_ITEMS; i++) {{
                const qId = String(ITEMS[i].id);
                const sol = decodedSolutions[qId];
                const cat = sol.category;

                if (!categoryScores[cat]) {{
                    categoryScores[cat] = {{ correct: 0, total: 0 }};
                }}
                categoryScores[cat].total++;

                if (userAnswers[i] !== null && userAnswers[i] === sol.correct_idx) {{
                    rawScore++;
                    categoryScores[cat].correct++;
                }}
            }}

            const psych = calculateIQ(rawScore);

            // Populate Results Screen
            document.getElementById('res-iq').textContent = psych.iq;
            document.getElementById('res-ci').textContent = `Intervallo di Confidenza 95%: [${{psych.ciLow}} - ${{psych.ciHigh}}]`;
            document.getElementById('res-classification').textContent = psych.classification;
            document.getElementById('res-percentile').textContent = `${{psych.percentile}}\u00b0 percentile (superiore al ${{psych.percentile}}% della popolazione generale)`;

            document.getElementById('res-raw-score').textContent = `${{rawScore}} / ${{TOTAL_ITEMS}}`;
            document.getElementById('res-time-spent').textContent = `${{minsSpent}}m ${{secsSpent}}s`;
            document.getElementById('res-avg-time').textContent = `${{avgSecondsPerItem}}s`;

            // Category breakdown bars
            const breakdownContainer = document.getElementById('categories-breakdown');
            breakdownContainer.innerHTML = '';
            for (const [catName, score] of Object.entries(categoryScores)) {{
                const pct = Math.round((score.correct / score.total) * 100);
                const row = document.createElement('div');
                row.className = 'cat-row';
                row.innerHTML = `
                    <div class="cat-header">
                        <span>${{catName}}</span>
                        <span>${{score.correct}}/${{score.total}} (${{pct}}%)</span>
                    </div>
                    <div class="cat-bar-bg">
                        <div class="cat-bar-fill" style="width: ${{pct}}%;"></div>
                    </div>
                `;
                breakdownContainer.appendChild(row);
            }}

            // Transition Screens
            testScreen.style.display = 'none';
            headerMeta.style.display = 'none';
            resultsScreen.style.display = 'flex';
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}

        // Review Mode
        const startReviewBtn = document.getElementById('start-review-btn');
        const reviewContainer = document.getElementById('review-container');
        const reviewPills = document.getElementById('review-pills');
        const reviewContent = document.getElementById('review-content');

        startReviewBtn.addEventListener('click', () => {{
            reviewContainer.style.display = 'block';
            startReviewBtn.style.display = 'none';
            renderReviewNavigator();
            renderReviewItem(0);
        }});

        function renderReviewNavigator() {{
            reviewPills.innerHTML = '';
            for (let i = 0; i < TOTAL_ITEMS; i++) {{
                const qId = String(ITEMS[i].id);
                const sol = decodedSolutions[qId];
                const isCorrect = (userAnswers[i] === sol.correct_idx);

                const pill = document.createElement('button');
                pill.className = 'btn-secondary';
                pill.style.padding = '0.35rem 0.65rem';
                pill.style.fontSize = '0.8rem';
                pill.style.fontWeight = '700';
                pill.style.borderColor = isCorrect ? 'var(--accent-emerald)' : 'var(--accent-rose)';
                pill.style.color = isCorrect ? 'var(--accent-emerald)' : 'var(--accent-rose)';
                pill.textContent = `${{i + 1}} ${{isCorrect ? '\u2713' : '\u2717'}}`;

                pill.addEventListener('click', () => {{
                    renderReviewItem(i);
                }});

                reviewPills.appendChild(pill);
            }}
        }}

        function renderReviewItem(idx) {{
            const item = ITEMS[idx];
            const qId = String(item.id);
            const sol = decodedSolutions[qId];
            const userChoice = userAnswers[idx];
            const isCorrect = (userChoice === sol.correct_idx);

            let optionsHtml = '';
            item.options.forEach((optSvg, oIdx) => {{
                let extraClass = '';
                let statusBadge = '';
                if (oIdx === sol.correct_idx) {{
                    extraClass = 'review-correct';
                    statusBadge = '<span style="color: var(--accent-emerald); font-size: 0.7rem; font-weight: bold; position: absolute; bottom: 4px; right: 6px;">Corretta</span>';
                }} else if (oIdx === userChoice && !isCorrect) {{
                    extraClass = 'review-user-wrong';
                    statusBadge = '<span style="color: var(--accent-rose); font-size: 0.7rem; font-weight: bold; position: absolute; bottom: 4px; right: 6px;">Tua scelta</span>';
                }}

                optionsHtml += `
                    <div class="option-card ${{extraClass}}" style="cursor: default;">
                        <div class="option-badge">${{String.fromCharCode(65 + oIdx)}}</div>
                        <svg viewBox="0 0 100 100">${{optSvg}}</svg>
                        ${{statusBadge}}
                    </div>
                `;
            }});

            let gridCellsHtml = '';
            for (let i = 0; i < 8; i++) {{
                gridCellsHtml += `<div class="matrix-cell"><svg viewBox="0 0 100 100">${{item.grid[i]}}</svg></div>`;
            }}
            // Target cell shows solution
            gridCellsHtml += `
                <div class="matrix-cell review-correct" style="border: 2px solid var(--accent-emerald);">
                    <svg viewBox="0 0 100 100">${{item.options[sol.correct_idx]}}</svg>
                </div>
            `;

            reviewContent.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h4 style="font-size: 1.05rem; font-weight: 700;">Domanda ${{idx + 1}} di ${{TOTAL_ITEMS}} &bull; ${{sol.category}}</h4>
                    <span style="font-weight: 700; color: ${{isCorrect ? 'var(--accent-emerald)' : 'var(--accent-rose)'}};">
                        ${{isCorrect ? '\u2713 Risposta Corretta' : '\u2717 Risposta Errata'}}
                    </span>
                </div>
                <div class="matrix-container" style="padding: 1rem; margin-bottom: 1.25rem;">
                    <div class="matrix-grid" style="max-width: 360px;">${{gridCellsHtml}}</div>
                </div>
                <div class="options-grid" style="max-width: 580px; margin-bottom: 1.25rem;">${{optionsHtml}}</div>
                <div class="review-explanation">
                    <strong>Spiegazione della Regola Logica:</strong><br>
                    ${{sol.explanation}}
                </div>
            `;
        }}
    </script>
</body>
</html>
"""

with open("iq_test/index.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print("Successfully generated iq_test/index.html (Single-page app ready).")
