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

html_content = f"""<!DOCTYPE html>
<html lang="it" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Progressive Matrices IQ Assessment</title>
    <meta name="description" content="Culture-fair Progressive Matrices IQ Assessment based on fluid intelligence and standardized psychometrics.">
    
    <style>
        /* CSS Variables - Dual Theme (Dark / Light) */
        :root[data-theme="dark"] {{
            --bg-main: #090d16;
            --bg-card: #131b2e;
            --bg-card-hover: #1c2742;
            --bg-cell: #0b111f;
            --border-color: #24324f;
            --border-cell: #1e2c47;
            --text-main: #f1f5f9;
            --text-muted: #94a3b8;
            --accent-cyan: #38bdf8;
            --accent-blue: #3b82f6;
            --accent-indigo: #6366f1;
            --accent-emerald: #10b981;
            --accent-rose: #f43f5e;
            --accent-amber: #f59e0b;
            --shadow-subtle: 0 10px 25px rgba(0, 0, 0, 0.4);
            --cell-target-bg: rgba(56, 189, 248, 0.05);
            --header-bg: rgba(19, 27, 46, 0.88);
        }}

        :root[data-theme="light"] {{
            --bg-main: #f8fafc;
            --bg-card: #ffffff;
            --bg-card-hover: #f1f5f9;
            --bg-cell: #f8fafc;
            --border-color: #cbd5e1;
            --border-cell: #94a3b8;
            --text-main: #0f172a;
            --text-muted: #475569;
            --accent-cyan: #0284c7;
            --accent-blue: #2563eb;
            --accent-indigo: #4f46e5;
            --accent-emerald: #059669;
            --accent-rose: #e11d48;
            --accent-amber: #d97706;
            --shadow-subtle: 0 10px 25px rgba(0, 0, 0, 0.06);
            --cell-target-bg: rgba(2, 132, 199, 0.05);
            --header-bg: rgba(255, 255, 255, 0.92);
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
            transition: background-color 0.25s ease, color 0.25s ease;
        }}

        /* Accessibility: skip link & focus ring */
        .skip-link {{
            position: absolute;
            top: -40px;
            left: 0;
            background: var(--accent-cyan);
            color: #000;
            padding: 8px;
            z-index: 1000;
            text-decoration: none;
            font-weight: bold;
        }}
        .skip-link:focus {{
            top: 0;
        }}

        :focus-visible {{
            outline: 2px solid var(--accent-cyan);
            outline-offset: 2px;
        }}

        @media (prefers-reduced-motion: reduce) {{
            *, *::before, *::after {{
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
                scroll-behavior: auto !important;
            }}
        }}

        /* App Header */
        header {{
            background: var(--header-bg);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border-color);
            position: sticky;
            top: 0;
            z-index: 100;
            padding: 0.65rem 1.5rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 0.65rem;
            text-decoration: none;
            color: var(--text-main);
        }}

        .brand-badge {{
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-indigo));
            color: #ffffff;
            font-weight: 800;
            font-size: 0.72rem;
            padding: 0.25rem 0.5rem;
            border-radius: 6px;
            letter-spacing: 0.05em;
        }}

        .brand-title {{
            font-size: 0.95rem;
            font-weight: 700;
            letter-spacing: -0.01em;
        }}

        /* Header Controls */
        .header-actions {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}

        .lang-select {{
            background: var(--bg-card);
            color: var(--text-main);
            border: 1px solid var(--border-color);
            padding: 0.35rem 0.6rem;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            transition: border-color 0.15s;
        }}

        .theme-toggle-btn {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            color: var(--text-main);
            padding: 0.35rem 0.6rem;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1rem;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.15s;
        }}
        .theme-toggle-btn:hover {{
            background: var(--bg-card-hover);
            border-color: var(--accent-cyan);
        }}

        /* Timer and Progress */
        .header-meta {{
            display: flex;
            align-items: center;
            gap: 1rem;
        }}

        .timer-badge {{
            display: flex;
            align-items: center;
            gap: 0.35rem;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            padding: 0.35rem 0.75rem;
            border-radius: 8px;
            font-size: 0.95rem;
            font-weight: 700;
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
            50% {{ opacity: 0.55; }}
        }}

        .progress-pill {{
            font-size: 0.85rem;
            color: var(--text-muted);
            font-weight: 600;
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
            border-radius: 18px;
            padding: 2.5rem;
            max-width: 740px;
            margin: auto;
            box-shadow: var(--shadow-subtle);
        }}

        .intro-title {{
            font-size: 1.85rem;
            font-weight: 800;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, var(--text-main), var(--accent-cyan));
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
            color: var(--text-main);
            line-height: 1.5;
        }}

        .instructions-list li .bullet {{
            width: 22px;
            height: 22px;
            border-radius: 50%;
            background: rgba(56, 189, 248, 0.15);
            color: var(--accent-cyan);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.75rem;
            font-weight: 800;
            flex-shrink: 0;
            margin-top: 1px;
        }}

        .btn-primary {{
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
            color: #ffffff;
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
            background: var(--bg-card);
            color: var(--text-main);
            border: 1px solid var(--border-color);
            padding: 0.6rem 1.25rem;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.9rem;
            transition: background 0.15s, border-color 0.15s, transform 0.1s;
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
        }}

        .btn-secondary:hover {{
            background: var(--bg-card-hover);
            border-color: var(--accent-cyan);
        }}

        /* Test Section */
        #test-screen {{
            display: none;
            flex-direction: column;
            gap: 1.25rem;
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
            font-weight: 700;
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
            box-shadow: var(--shadow-subtle);
        }}

        .matrix-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            width: 100%;
            max-width: 440px;
        }}

        .matrix-cell {{
            background: var(--bg-cell);
            border: 1px solid var(--border-cell);
            border-radius: 10px;
            aspect-ratio: 1 / 1;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 8px;
            position: relative;
            color: var(--text-main);
        }}

        .matrix-cell svg {{
            width: 100%;
            height: 100%;
            display: block;
        }}

        .matrix-cell.target {{
            border: 2px dashed var(--accent-cyan);
            background: var(--cell-target-bg);
        }}

        .target-placeholder {{
            font-size: 2.2rem;
            font-weight: 800;
            color: var(--accent-cyan);
            opacity: 0.75;
        }}

        /* Options Area */
        .options-section {{
            margin-top: 0.25rem;
        }}

        .options-title {{
            font-size: 0.9rem;
            color: var(--text-muted);
            margin-bottom: 0.75rem;
            text-align: center;
            font-weight: 500;
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
            color: var(--text-main);
        }}

        .option-card:hover {{
            border-color: var(--accent-cyan);
            background: var(--bg-card-hover);
            transform: translateY(-2px);
        }}

        .option-card.selected {{
            border-color: var(--accent-cyan);
            background: rgba(56, 189, 248, 0.12);
            box-shadow: 0 0 14px rgba(56, 189, 248, 0.3);
        }}

        .option-badge {{
            position: absolute;
            top: 6px;
            left: 6px;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: var(--bg-cell);
            border: 1px solid var(--border-color);
            font-size: 0.7rem;
            font-weight: 700;
            color: var(--text-muted);
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .option-card.selected .option-badge {{
            background: var(--accent-cyan);
            color: #ffffff;
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
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid var(--border-color);
        }}

        .nav-buttons {{
            display: flex;
            gap: 0.75rem;
        }}

        /* Drawer / Modals */
        .modal-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.75);
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
            background: var(--bg-cell);
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            font-weight: 700;
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.15s;
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
            gap: 1.75rem;
            max-width: 800px;
            margin: 0 auto;
            width: 100%;
        }}

        .result-hero {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 2.5rem;
            text-align: center;
            box-shadow: var(--shadow-subtle);
            position: relative;
            overflow: hidden;
        }}

        .hero-glow {{
            position: absolute;
            top: -50px;
            left: 50%;
            transform: translateX(-50%);
            width: 320px;
            height: 120px;
            background: radial-gradient(ellipse, rgba(56, 189, 248, 0.2), transparent 70%);
            pointer-events: none;
        }}

        .iq-badge {{
            font-size: 4.8rem;
            font-weight: 900;
            line-height: 1;
            margin: 0.75rem 0;
            background: linear-gradient(135deg, var(--text-main), var(--accent-cyan));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .iq-ci {{
            font-size: 1.05rem;
            color: var(--text-muted);
            margin-bottom: 0.5rem;
            font-weight: 600;
        }}

        .iq-classification {{
            font-size: 1.35rem;
            font-weight: 800;
            color: var(--accent-cyan);
            margin-bottom: 0.25rem;
        }}

        .percentile-rank {{
            font-size: 0.95rem;
            color: var(--text-muted);
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
            color: var(--text-main);
        }}

        .stat-label {{
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-top: 0.2rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        /* Actions on Results (PDF & Home) */
        .results-actions-bar {{
            display: flex;
            justify-content: center;
            gap: 1rem;
            flex-wrap: wrap;
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
            color: var(--text-main);
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
            height: 9px;
            background: var(--bg-cell);
            border: 1px solid var(--border-color);
            border-radius: 999px;
            overflow: hidden;
        }}

        .cat-bar-fill {{
            height: 100%;
            border-radius: 999px;
            background: linear-gradient(90deg, var(--accent-cyan), var(--accent-blue));
            transition: width 0.8s ease;
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
            padding: 1.1rem;
            background: var(--bg-cell);
            border-left: 3px solid var(--accent-cyan);
            border-radius: 0 8px 8px 0;
            font-size: 0.95rem;
            line-height: 1.6;
            color: var(--text-main);
        }}

        .option-card.review-correct {{
            border-color: var(--accent-emerald) !important;
            background: rgba(16, 185, 129, 0.12) !important;
        }}

        .option-card.review-user-wrong {{
            border-color: var(--accent-rose) !important;
            background: rgba(244, 63, 94, 0.12) !important;
        }}

        /* Live Region for Screen Readers */
        .sr-only {{
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0, 0, 0, 0);
            white-space: nowrap;
            border-width: 0;
        }}

        /* ========================================================
           PRINT STYLESHEET FOR CRISP A4 PDF EXPORT
           ======================================================== */
        @media print {{
            header,
            .results-actions-bar,
            .review-panel,
            .controls-bar,
            .modal-overlay,
            #test-screen,
            #intro-screen {{
                display: none !important;
            }}

            body {{
                background: #ffffff !important;
                color: #0f172a !important;
                font-size: 11pt !important;
            }}

            .container {{
                max-width: 100% !important;
                padding: 0 !important;
            }}

            #results-screen {{
                display: block !important;
            }}

            .result-hero {{
                background: #ffffff !important;
                border: 2px solid #0f172a !important;
                box-shadow: none !important;
                padding: 1.5rem !important;
                page-break-inside: avoid;
            }}

            .hero-glow {{
                display: none !important;
            }}

            .iq-badge {{
                color: #0f172a !important;
                -webkit-text-fill-color: #0f172a !important;
                font-size: 3.5rem !important;
            }}

            .iq-classification {{
                color: #0284c7 !important;
            }}

            .breakdown-card {{
                background: #ffffff !important;
                border: 1px solid #cbd5e1 !important;
                box-shadow: none !important;
                margin-top: 1.5rem !important;
                page-break-inside: avoid;
            }}

            .cat-bar-bg {{
                border: 1px solid #94a3b8 !important;
            }}

            .cat-bar-fill {{
                background: #0284c7 !important;
                print-color-adjust: exact;
                -webkit-print-color-adjust: exact;
            }}

            .print-footer-notice {{
                display: block !important;
                margin-top: 2rem;
                text-align: center;
                font-size: 8pt;
                color: #64748b;
                border-top: 1px solid #e2e8f0;
                padding-top: 0.5rem;
            }}
        }}

        .print-footer-notice {{
            display: none;
        }}
    </style>
</head>
<body>

    <a href="#main-content" class="skip-link">Passa al contenuto principale</a>
    <div id="sr-announcer" class="sr-only" aria-live="polite"></div>

    <!-- Header -->
    <header role="banner">
        <div class="brand">
            <span class="brand-badge" id="txt-brand-badge">PSICOMETRIA</span>
            <span class="brand-title" id="txt-brand-title">Valutazione Matrici Progressive</span>
        </div>

        <div class="header-meta" id="header-meta" style="display: none;">
            <div class="progress-pill" id="progress-indicator">Domanda 1 di 30</div>
            <div class="timer-badge" id="timer-display" aria-label="Tempo rimanente">35:00</div>
            <button class="btn-secondary" id="open-map-btn" style="padding: 0.35rem 0.75rem; font-size: 0.85rem;" id="txt-map-btn">
                Mappa Quesiti
            </button>
        </div>

        <div class="header-actions">
            <!-- Language Selector -->
            <select class="lang-select" id="lang-select" aria-label="Seleziona Lingua">
                <option value="it">🇮🇹 Italiano</option>
                <option value="en">🇬🇧 English</option>
                <option value="de">🇩🇪 Deutsch</option>
                <option value="es">🇪🇸 Español</option>
                <option value="pt">🇧🇷 Português</option>
                <option value="fr">🇫🇷 Français</option>
            </select>

            <!-- Theme Toggle -->
            <button class="theme-toggle-btn" id="theme-toggle-btn" aria-label="Cambia tema chiaro/scuro">
                <span id="theme-icon">🌙</span>
            </button>
        </div>
    </header>

    <main class="container" id="main-content" role="main">

        <!-- Screen 1: Introduction -->
        <section class="intro-card" id="intro-screen">
            <h1 class="intro-title" id="txt-intro-title">Test di Intelligenza a Matrici Progressive</h1>
            <p class="intro-desc" id="txt-intro-desc">
                Questo test misura l'<strong>Intelligenza Fluida</strong> (il fattore generale <em>g</em> di Spearman) attraverso 30 problemi di logica visuo-spaziale a difficoltà progressiva. È indipendente dal linguaggio, dall'istruzione scolastica e dal background culturale.
            </p>
            <ul class="instructions-list">
                <li>
                    <span class="bullet" aria-hidden="true">1</span>
                    <span><strong id="txt-rule-1-title">Struttura:</strong> <span id="txt-rule-1-desc">Ogni quesito presenta una griglia 3x3 di figure con una casella mancante contrassegnata da <strong>?</strong> in basso a destra.</span></span>
                </li>
                <li>
                    <span class="bullet" aria-hidden="true">2</span>
                    <span><strong id="txt-rule-2-title">Obiettivo:</strong> <span id="txt-rule-2-desc">Identificare la regola logica (orizzontale, verticale o combinata) e selezionare la figura corretta tra le opzioni sottostanti.</span></span>
                </li>
                <li>
                    <span class="bullet" aria-hidden="true">3</span>
                    <span><strong id="txt-rule-3-title">Tempo limite:</strong> <span id="txt-rule-3-desc"><strong>35 minuti</strong> per tutti i 30 quesiti (~70 secondi per domanda). Il timer si avvia cliccando sul pulsante sottostante.</span></span>
                </li>
                <li>
                    <span class="bullet" aria-hidden="true">4</span>
                    <span><strong id="txt-rule-4-title">Accessibilità & Scorciatoie:</strong> <span id="txt-rule-4-desc">Usa le <strong>Frecce</strong> per navigare, i tasti <strong>1-8</strong> o <strong>A-H</strong> per selezionare, e <strong>Spazio</strong> per contrassegnare i dubbi.</span></span>
                </li>
            </ul>
            <div style="text-align: center; margin-top: 2rem;">
                <button class="btn-primary" id="start-btn">Inizia la Valutazione &rarr;</button>
            </div>
        </section>

        <!-- Screen 2: Active Test -->
        <section id="test-screen">
            <div class="matrix-meta-bar">
                <span class="category-tag" id="q-category">Progressione Quantitativa</span>
                <button class="flag-btn" id="flag-btn" aria-pressed="false">
                    <span aria-hidden="true">&#9873;</span> <span id="txt-flag-label">Segna per dopo</span>
                </button>
            </div>

            <!-- 3x3 Matrix Grid -->
            <div class="matrix-container">
                <div class="matrix-grid" id="matrix-grid" role="region" aria-label="Matrice logica 3x3 del quesito">
                    <!-- 9 cells rendered by JS -->
                </div>
            </div>

            <!-- Options Area -->
            <div class="options-section">
                <div class="options-title" id="txt-missing-figure-title">Seleziona la figura mancante per completare la logica:</div>
                <div class="options-grid" id="options-grid" role="radiogroup" aria-label="Opzioni di risposta">
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
        </section>

        <!-- Screen 3: Results -->
        <section id="results-screen">
            <div class="result-hero">
                <div class="hero-glow"></div>
                <div style="font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-muted);" id="txt-res-hero-title">Quoziente Intellettivo Stimato</div>
                <div class="iq-badge" id="res-iq" aria-label="QI calcolato">125</div>
                <div class="iq-ci" id="res-ci">Intervallo di Confidenza al 95%: [119 - 131]</div>
                <div class="iq-classification" id="res-classification">Superiore / Alto Potenziale</div>
                <div class="percentile-rank" id="res-percentile">95.2° percentile</div>

                <div class="stats-grid">
                    <div class="stat-box">
                        <div class="stat-val" id="res-raw-score">25 / 30</div>
                        <div class="stat-label" id="txt-res-raw-score">Punteggio Grezzo</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-val" id="res-time-spent">21:40</div>
                        <div class="stat-label" id="txt-res-time-spent">Tempo Impiegato</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-val" id="res-avg-time">43s</div>
                        <div class="stat-label" id="txt-res-avg-time">Tempo Medio / Item</div>
                    </div>
                </div>
            </div>

            <!-- Action buttons: PDF & Home -->
            <div class="results-actions-bar">
                <button class="btn-primary" id="export-pdf-btn">
                    <span>&#128424;</span> <span id="txt-export-pdf-btn">Esporta Report in PDF</span>
                </button>
                <button class="btn-secondary" id="home-btn">
                    <span>&#8634;</span> <span id="txt-home-btn">Torna alla Home / Ricomincia</span>
                </button>
            </div>

            <!-- Breakdown -->
            <div class="breakdown-card">
                <div class="breakdown-title" id="txt-breakdown-title">Profilo Cognitivo per Categorie di Ragionamento</div>
                <div id="categories-breakdown">
                    <!-- Category bars -->
                </div>
            </div>

            <!-- Review Button & Panel -->
            <div class="review-panel">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; flex-wrap: wrap; gap: 0.5rem;">
                    <div style="font-size: 1.1rem; font-weight: 700;" id="txt-review-panel-title">Revisione Dettagliata & Soluzioni</div>
                    <button class="btn-secondary" id="start-review-btn">Apri Spiegazioni Passo-Passo</button>
                </div>
                <p style="color: var(--text-muted); font-size: 0.9rem; line-height: 1.5;" id="txt-review-panel-desc">
                    Visualizza per ciascun quesito la regola logica esatta (orizzontale, verticale e insiemistica) e l'analisi degli errori delle altre opzioni.
                </p>
                <div id="review-container" style="display: none; margin-top: 1.5rem;">
                    <!-- Interactive review pills -->
                    <div style="display: flex; gap: 0.5rem; overflow-x: auto; padding-bottom: 0.75rem; margin-bottom: 1rem;" id="review-pills"></div>
                    <div id="review-content"></div>
                </div>
            </div>

            <div class="print-footer-notice">
                Report psicométrico generato automaticamente &bull; Valutazione Matrici Progressive Culture-Fair &bull; Basato su scala standard Wechsler (&mu;=100, &sigma;=15)
            </div>
        </section>

    </main>

    <!-- Question Map Modal -->
    <div class="modal-overlay" id="map-modal" role="dialog" aria-modal="true" aria-labelledby="map-modal-title">
        <div class="modal-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h3 style="font-size: 1.1rem; font-weight: 700;" id="map-modal-title">Mappa dei 30 Quesiti</h3>
                <button id="close-map-btn" style="background: none; border: none; color: var(--text-muted); font-size: 1.4rem; cursor: pointer;" aria-label="Chiudi finestra mappa">&times;</button>
            </div>
            <div style="display: flex; gap: 1rem; font-size: 0.8rem; color: var(--text-muted); margin-bottom: 0.5rem;">
                <span style="display: flex; align-items: center; gap: 0.3rem;"><span style="width: 10px; height: 10px; background: rgba(56, 189, 248, 0.4); border-radius: 2px;"></span> <span id="txt-map-answered">Risposto</span></span>
                <span style="display: flex; align-items: center; gap: 0.3rem;"><span style="width: 10px; height: 10px; background: rgba(245, 158, 11, 0.4); border-radius: 2px;"></span> <span id="txt-map-flagged">Segnato</span></span>
                <span style="display: flex; align-items: center; gap: 0.3rem;"><span style="width: 10px; height: 10px; background: var(--bg-cell); border: 1px solid var(--border-color); border-radius: 2px;"></span> <span id="txt-map-unanswered">Non risposto</span></span>
            </div>
            <div class="question-map-grid" id="question-map-grid"></div>
            <button class="btn-primary" id="confirm-map-btn" style="width: 100%; justify-content: center;">Chiudi</button>
        </div>
    </div>

    <!-- Confirm Submit Modal -->
    <div class="modal-overlay" id="confirm-modal" role="dialog" aria-modal="true" aria-labelledby="confirm-modal-title">
        <div class="modal-card">
            <h3 style="font-size: 1.2rem; font-weight: 700; margin-bottom: 0.75rem;" id="confirm-modal-title">Conferma Consegna Test</h3>
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
        const I18N = {translations_json};
        const TOTAL_ITEMS = ITEMS.length;
        const TIME_LIMIT_SECONDS = 35 * 60; // 35 minutes

        // Language & Theme State
        let currentLang = 'it';
        let currentTheme = 'dark';

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
        const txtFlagLabel = document.getElementById('txt-flag-label');
        const matrixGrid = document.getElementById('matrix-grid');
        const optionsGrid = document.getElementById('options-grid');
        const prevBtn = document.getElementById('prev-btn');
        const nextBtn = document.getElementById('next-btn');
        const submitBtn = document.getElementById('submit-btn');
        const langSelect = document.getElementById('lang-select');
        const themeToggleBtn = document.getElementById('theme-toggle-btn');
        const themeIcon = document.getElementById('theme-icon');
        const srAnnouncer = document.getElementById('sr-announcer');

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

        // Initial setup for Theme & Language detection
        function initThemeAndLang() {{
            // Language
            const savedLang = localStorage.getItem('matrix_iq_lang');
            if (savedLang && I18N[savedLang]) {{
                currentLang = savedLang;
            }} else {{
                // Auto detect browser language
                const browserLang = (navigator.language || navigator.userLanguage || 'en').slice(0, 2).toLowerCase();
                if (I18N[browserLang]) {{
                    currentLang = browserLang;
                }} else {{
                    currentLang = 'en';
                }}
            }}
            langSelect.value = currentLang;

            // Theme
            const savedTheme = localStorage.getItem('matrix_iq_theme');
            if (savedTheme) {{
                currentTheme = savedTheme;
            }} else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {{
                currentTheme = 'light';
            }} else {{
                currentTheme = 'dark';
            }}
            applyTheme(currentTheme);
            applyLanguage(currentLang);
        }}

        function applyTheme(theme) {{
            currentTheme = theme;
            document.documentElement.setAttribute('data-theme', theme);
            themeIcon.textContent = (theme === 'dark') ? '🌙' : '☀️';
            localStorage.setItem('matrix_iq_theme', theme);
        }}

        themeToggleBtn.addEventListener('click', () => {{
            const newTheme = (currentTheme === 'dark') ? 'light' : 'dark';
            applyTheme(newTheme);
        }});

        function applyLanguage(lang) {{
            if (!I18N[lang]) return;
            currentLang = lang;
            document.documentElement.setAttribute('lang', lang);
            localStorage.setItem('matrix_iq_lang', lang);

            const t = I18N[lang];
            // Update static strings
            document.getElementById('txt-brand-title').textContent = t.brand_title;
            document.getElementById('txt-brand-badge').textContent = t.brand_badge;
            document.getElementById('txt-intro-title').textContent = t.intro_title;
            document.getElementById('txt-intro-desc').innerHTML = t.intro_desc;

            document.getElementById('txt-rule-1-title').textContent = t.rule_1_title;
            document.getElementById('txt-rule-1-desc').innerHTML = t.rule_1_desc;
            document.getElementById('txt-rule-2-title').textContent = t.rule_2_title;
            document.getElementById('txt-rule-2-desc').innerHTML = t.rule_2_desc;
            document.getElementById('txt-rule-3-title').textContent = t.rule_3_title;
            document.getElementById('txt-rule-3-desc').innerHTML = t.rule_3_desc;
            document.getElementById('txt-rule-4-title').textContent = t.rule_4_title;
            document.getElementById('txt-rule-4-desc').innerHTML = t.rule_4_desc;
            document.getElementById('start-btn').textContent = t.start_btn;

            document.getElementById('txt-missing-figure-title').textContent = t.missing_figure_title;
            prevBtn.textContent = t.prev_btn;
            submitBtn.textContent = t.submit_btn;
            openMapBtn.textContent = t.map_btn;

            document.getElementById('map-modal-title').textContent = t.map_title;
            document.getElementById('txt-map-answered').textContent = t.map_answered;
            document.getElementById('txt-map-flagged').textContent = t.map_flagged;
            document.getElementById('txt-map-unanswered').textContent = t.map_unanswered;
            confirmMapBtn.textContent = t.close_btn;

            document.getElementById('confirm-modal-title').textContent = t.confirm_title;
            cancelSubmitBtn.textContent = t.cancel_btn;
            proceedSubmitBtn.textContent = t.proceed_btn;

            document.getElementById('txt-res-hero-title').textContent = t.res_hero_title;
            document.getElementById('txt-res-raw-score').textContent = t.res_raw_score;
            document.getElementById('txt-res-time-spent').textContent = t.res_time_spent;
            document.getElementById('txt-res-avg-time').textContent = t.res_avg_time;
            document.getElementById('txt-breakdown-title').textContent = t.breakdown_title;

            document.getElementById('txt-export-pdf-btn').textContent = t.export_pdf_btn;
            document.getElementById('txt-home-btn').textContent = t.home_btn;
            document.getElementById('txt-review-panel-title').textContent = t.review_panel_title;
            document.getElementById('txt-review-panel-desc').textContent = t.review_panel_desc;
            document.getElementById('start-review-btn').textContent = t.open_review_btn;

            // Re-render current question if in test
            if (testScreen.style.display === 'flex') {{
                renderQuestion(currentIndex);
            }} else if (resultsScreen.style.display === 'flex') {{
                // Re-evaluate results labels in new language
                finishTest(true);
            }}
        }}

        langSelect.addEventListener('change', (e) => {{
            applyLanguage(e.target.value);
        }});

        // Start Test
        document.getElementById('start-btn').addEventListener('click', () => {{
            introScreen.style.display = 'none';
            testScreen.style.display = 'flex';
            headerMeta.style.display = 'flex';
            testStartTime = Date.now();
            renderQuestion(currentIndex);
            startTimer();
            announceSR("Test iniziato. Domanda 1 di 30.");
        }});

        function announceSR(text) {{
            srAnnouncer.textContent = text;
        }}

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
            const t = I18N[currentLang];

            progressIndicator.textContent = t.q_progress.replace('{current}', index + 1).replace('{total}', TOTAL_ITEMS);

            // Translate category name
            const translatedCat = (t.categories && t.categories[item.category_key]) || item.category_key;
            qCategory.textContent = translatedCat;

            // Flag state
            if (flaggedItems.has(index)) {{
                flagBtn.classList.add('active');
                flagBtn.setAttribute('aria-pressed', 'true');
                txtFlagLabel.textContent = t.flagged_btn;
            }} else {{
                flagBtn.classList.remove('active');
                flagBtn.setAttribute('aria-pressed', 'false');
                txtFlagLabel.textContent = t.flag_btn;
            }}

            // Render 3x3 Matrix Grid
            matrixGrid.innerHTML = '';
            for (let i = 0; i < 8; i++) {{
                const cell = document.createElement('div');
                cell.className = 'matrix-cell';
                cell.setAttribute('aria-label', `Cella riga ${{Math.floor(i/3)+1}}, colonna ${{(i%3)+1}}`);
                cell.innerHTML = `<svg viewBox="0 0 100 100">${{item.grid[i]}}</svg>`;
                matrixGrid.appendChild(cell);
            }}

            // 9th missing cell
            const targetCell = document.createElement('div');
            targetCell.className = 'matrix-cell target';
            targetCell.setAttribute('aria-label', `Cella bersaglio mancante`);
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
                optCard.setAttribute('role', 'radio');
                optCard.setAttribute('tabindex', '0');
                const isSelected = (userAnswers[index] === optIdx);
                optCard.setAttribute('aria-checked', isSelected ? 'true' : 'false');

                const letter = String.fromCharCode(65 + optIdx);
                optCard.setAttribute('aria-label', `Opzione ${{letter}}`);

                if (isSelected) {{
                    optCard.classList.add('selected');
                }}

                optCard.innerHTML = `
                    <div class="option-badge" aria-hidden="true">${{letter}}</div>
                    <svg viewBox="0 0 100 100">${{optSvg}}</svg>
                `;

                optCard.addEventListener('click', () => {{
                    selectOption(optIdx);
                }});

                optCard.addEventListener('keydown', (e) => {{
                    if (e.key === 'Enter' || e.key === ' ') {{
                        e.preventDefault();
                        selectOption(optIdx);
                    }}
                }});

                optionsGrid.appendChild(optCard);
            }});

            // Prev / Next button state
            prevBtn.disabled = (index === 0);
            prevBtn.style.opacity = (index === 0) ? '0.4' : '1';
            nextBtn.textContent = (index === TOTAL_ITEMS - 1) ? t.summary_btn : t.next_btn;
        }}

        function selectOption(optIdx) {{
            userAnswers[currentIndex] = optIdx;
            renderQuestion(currentIndex);
            const letter = String.fromCharCode(65 + optIdx);
            announceSR(`Selezionata opzione ${{letter}} per la domanda ${{currentIndex + 1}}`);
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
                const mapBtn = document.createElement('button');
                mapBtn.className = 'map-item';
                mapBtn.textContent = i + 1;
                mapBtn.setAttribute('aria-label', `Vai alla domanda ${{i+1}}`);

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
            const t = I18N[currentLang];
            const unanswered = userAnswers.filter(a => a === null).length;
            const flagged = flaggedItems.size;

            let msg = t.confirm_default;
            if (unanswered > 0) {{
                msg = t.confirm_unanswered.replace('{count}', unanswered);
            }} else if (flagged > 0) {{
                msg = t.confirm_flagged.replace('{count}', flagged);
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
            // Space to toggle flag (when not on a button)
            if (e.key === ' ' && e.target.tagName !== 'BUTTON') {{
                e.preventDefault();
                flagBtn.click();
            }}
        }});

        // Psychometric Scoring Model (Calibrated against Raven APM / Mensa Nordic standards)
        // Wechsler Scale (Mean = 100, SD = 15)
        function calculateIQ(rawScore) {{
            const iqTable = [
                68, 72, 75, 78, 81, 84, 87, 90, 93, 96, 98,
                100, 102, 105, 108, 110, 113, 115, 118, 120, 123,
                125, 128, 131, 133, 136, 138, 140, 142, 144, 145
            ];
            const iq = iqTable[Math.max(0, Math.min(30, rawScore))];

            const z = (iq - 100) / 15.0;
            const t = 1.0 / (1.0 + 0.2316419 * Math.abs(z));
            const d = 0.3989423 * Math.exp(-z * z / 2.0);
            let p = d * t * (0.3193815 + t * (-0.3565638 + t * (1.781478 + t * (-1.821256 + t * 1.330274))));
            let percentile = (z > 0) ? (1.0 - p) * 100 : p * 100;
            percentile = Math.max(0.1, Math.min(99.9, percentile)).toFixed(1);

            const sem = 5;
            const ciLow = Math.max(65, iq - sem);
            const ciHigh = Math.min(150, iq + sem);

            const t_lang = I18N[currentLang];
            let classification = t_lang.class_avg;
            if (iq >= 135) classification = t_lang.class_exceptional;
            else if (iq >= 130) classification = t_lang.class_very_superior;
            else if (iq >= 120) classification = t_lang.class_superior;
            else if (iq >= 110) classification = t_lang.class_high_avg;
            else if (iq >= 90) classification = t_lang.class_avg;
            else if (iq >= 80) classification = t_lang.class_low_avg;
            else classification = t_lang.class_below_avg;

            return {{
                iq,
                percentile,
                classification,
                ciLow,
                ciHigh
            }};
        }}

        function finishTest(isRecompute = false) {{
            if (!isRecompute) {{
                testSubmitted = true;
                clearInterval(timerInterval);
            }}

            decodedSolutions = JSON.parse(atob(ENCODED_SOLUTIONS));
            const t = I18N[currentLang];

            const timeSpentSeconds = Math.max(1, Math.round(((testStartTime ? Date.now() : 0) - (testStartTime || 0)) / 1000) || (TIME_LIMIT_SECONDS - timeRemaining));
            const minsSpent = Math.floor(timeSpentSeconds / 60);
            const secsSpent = timeSpentSeconds % 60;
            const avgSecondsPerItem = Math.round(timeSpentSeconds / TOTAL_ITEMS);

            let rawScore = 0;
            const categoryScores = {{}};

            for (let i = 0; i < TOTAL_ITEMS; i++) {{
                const qId = String(ITEMS[i].id);
                const sol = decodedSolutions[qId];
                const catKey = sol.category_key;

                if (!categoryScores[catKey]) {{
                    categoryScores[catKey] = {{ correct: 0, total: 0 }};
                }}
                categoryScores[catKey].total++;

                if (userAnswers[i] !== null && userAnswers[i] === sol.correct_idx) {{
                    rawScore++;
                    categoryScores[catKey].correct++;
                }}
            }}

            const psych = calculateIQ(rawScore);

            // Populate Results Screen
            document.getElementById('res-iq').textContent = psych.iq;
            document.getElementById('res-ci').textContent = t.res_ci.replace('{low}', psych.ciLow).replace('{high}', psych.ciHigh);
            document.getElementById('res-classification').textContent = psych.classification;
            document.getElementById('res-percentile').textContent = t.res_percentile.replace(/\{p\}/g, psych.percentile);

            document.getElementById('res-raw-score').textContent = `${{rawScore}} / ${{TOTAL_ITEMS}}`;
            document.getElementById('res-time-spent').textContent = `${{minsSpent}}m ${{secsSpent}}s`;
            document.getElementById('res-avg-time').textContent = `${{avgSecondsPerItem}}s`;

            // Category breakdown bars
            const breakdownContainer = document.getElementById('categories-breakdown');
            breakdownContainer.innerHTML = '';
            for (const [catKey, score] of Object.entries(categoryScores)) {{
                const pct = Math.round((score.correct / score.total) * 100);
                const translatedCat = (t.categories && t.categories[catKey]) || catKey;
                const row = document.createElement('div');
                row.className = 'cat-row';
                row.innerHTML = `
                    <div class="cat-header">
                        <span>${{translatedCat}}</span>
                        <span>${{score.correct}}/${{score.total}} (${{pct}}%)</span>
                    </div>
                    <div class="cat-bar-bg">
                        <div class="cat-bar-fill" style="width: ${{pct}}%;"></div>
                    </div>
                `;
                breakdownContainer.appendChild(row);
            }}

            testScreen.style.display = 'none';
            headerMeta.style.display = 'none';
            resultsScreen.style.display = 'flex';
            window.scrollTo({{ top: 0, behavior: 'smooth' }});

            // If review was open, re-render it
            if (reviewContainer.style.display === 'block') {{
                renderReviewNavigator();
                renderReviewItem(currentReviewIndex || 0);
            }}
        }}

        // PDF Export Feature
        document.getElementById('export-pdf-btn').addEventListener('click', () => {{
            window.print();
        }});

        // Home / Restart Feature
        document.getElementById('home-btn').addEventListener('click', () => {{
            const t = I18N[currentLang];
            if (confirm(t.home_confirm)) {{
                resetTest();
            }}
        }});

        function resetTest() {{
            testSubmitted = false;
            clearInterval(timerInterval);
            timeRemaining = TIME_LIMIT_SECONDS;
            timerDisplay.textContent = "35:00";
            timerDisplay.classList.remove('warning');
            currentIndex = 0;
            userAnswers = new Array(TOTAL_ITEMS).fill(null);
            flaggedItems.clear();
            testStartTime = null;

            resultsScreen.style.display = 'none';
            testScreen.style.display = 'none';
            headerMeta.style.display = 'none';
            introScreen.style.display = 'block';

            reviewContainer.style.display = 'none';
            startReviewBtn.style.display = 'inline-flex';
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}

        // Review Mode
        let currentReviewIndex = 0;
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
            currentReviewIndex = idx;
            const item = ITEMS[idx];
            const qId = String(item.id);
            const sol = decodedSolutions[qId];
            const userChoice = userAnswers[idx];
            const isCorrect = (userChoice === sol.correct_idx);
            const t = I18N[currentLang];

            // Get explanation in current language
            const expl = (sol.explanations && sol.explanations[currentLang]) || sol.explanations['en'] || "";
            const translatedCat = (t.categories && t.categories[sol.category_key]) || sol.category_key;

            let optionsHtml = '';
            item.options.forEach((optSvg, oIdx) => {{
                let extraClass = '';
                let statusBadge = '';
                if (oIdx === sol.correct_idx) {{
                    extraClass = 'review-correct';
                    statusBadge = `<span style="color: var(--accent-emerald); font-size: 0.7rem; font-weight: bold; position: absolute; bottom: 4px; right: 6px;">${{t.correct_badge}}</span>`;
                }} else if (oIdx === userChoice && !isCorrect) {{
                    extraClass = 'review-user-wrong';
                    statusBadge = `<span style="color: var(--accent-rose); font-size: 0.7rem; font-weight: bold; position: absolute; bottom: 4px; right: 6px;">${{t.your_choice_badge}}</span>`;
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
            gridCellsHtml += `
                <div class="matrix-cell review-correct" style="border: 2px solid var(--accent-emerald);">
                    <svg viewBox="0 0 100 100">${{item.options[sol.correct_idx]}}</svg>
                </div>
            `;

            reviewContent.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; flex-wrap: wrap; gap: 0.5rem;">
                    <h4 style="font-size: 1.05rem; font-weight: 700;">Domanda ${{idx + 1}} di ${{TOTAL_ITEMS}} &bull; ${{translatedCat}}</h4>
                    <span style="font-weight: 700; color: ${{isCorrect ? 'var(--accent-emerald)' : 'var(--accent-rose)'}};">
                        ${{isCorrect ? t.review_correct_label : t.review_wrong_label}}
                    </span>
                </div>
                <div class="matrix-container" style="padding: 1rem; margin-bottom: 1.25rem;">
                    <div class="matrix-grid" style="max-width: 360px;">${{gridCellsHtml}}</div>
                </div>
                <div class="options-grid" style="max-width: 580px; margin-bottom: 1.25rem;">${{optionsHtml}}</div>
                <div class="review-explanation">
                    <strong>${{t.explanation_title}}</strong><br>
                    ${{expl}}
                </div>
            `;
        }}

        // Initialize on load
        window.addEventListener('DOMContentLoaded', initThemeAndLang);
    </script>
</body>
</html>
"""

with open("iq_test/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Advanced multilingual index.html generated successfully!")
