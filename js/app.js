/**
 * MatriQ Application Controller
 * Handles test progression, timers, interactive visual rendering,
 * review navigation, and keyboard shortcuts.
 */

// Application Constants & Timing
const TOTAL_ITEMS = (typeof ITEMS !== 'undefined') ? ITEMS.length : 30;
const TIME_LIMIT_SECONDS = 35 * 60; // 35 minutes

// State
let currentLang = 'it';
let currentTheme = 'dark';
let currentIndex = 0;
let userAnswers = new Array(TOTAL_ITEMS).fill(null);
let flaggedItems = new Set();
let timeRemaining = TIME_LIMIT_SECONDS;
let timerInterval = null;
let testStartTime = null;
let decodedSolutions = null;
let testSubmitted = false;
let currentReviewIndex = 0;

// DOM Elements
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

// Review Mode Elements
const startReviewBtn = document.getElementById('start-review-btn');
const reviewContainer = document.getElementById('review-container');
const reviewPills = document.getElementById('review-pills');
const reviewContent = document.getElementById('review-content');

// Helper: Accessible Screen Reader Announcements
function announceSR(text) {
    if (srAnnouncer) srAnnouncer.textContent = text;
}

// Helper: Safe DOM text & html setters
function setTxt(id, val) {
    const el = document.getElementById(id);
    if (el) el.textContent = val;
}
function setHtml(id, val) {
    const el = document.getElementById(id);
    if (el) el.innerHTML = val;
}

// ----------------------------------------------------
// Theme Management
// ----------------------------------------------------
function applyTheme(theme) {
    currentTheme = theme;
    document.documentElement.setAttribute('data-theme', theme);
    if (themeIcon) {
        themeIcon.textContent = (theme === 'dark') ? '🌙' : '☀️';
    }
    localStorage.setItem('matrix_iq_theme', theme);
}

if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
        const newTheme = (currentTheme === 'dark') ? 'light' : 'dark';
        applyTheme(newTheme);
    });
}

// ----------------------------------------------------
// Internationalization (i18n)
// ----------------------------------------------------
function applyLanguage(lang) {
    if (typeof I18N === 'undefined' || !I18N[lang]) return;
    currentLang = lang;
    document.documentElement.setAttribute('lang', lang);
    localStorage.setItem('matrix_iq_lang', lang);

    const t = I18N[lang];

    // Static Strings
    setHtml('txt-brand-title', 'Matri<span style="color: var(--accent-cyan);">Q</span>');
    setTxt('txt-brand-badge', t.brand_badge);
    setTxt('txt-intro-title', t.intro_title);
    setHtml('txt-intro-desc', t.intro_desc);

    setTxt('txt-rule-1-title', t.rule_1_title);
    setHtml('txt-rule-1-desc', t.rule_1_desc);
    setTxt('txt-rule-2-title', t.rule_2_title);
    setHtml('txt-rule-2-desc', t.rule_2_desc);
    setTxt('txt-rule-3-title', t.rule_3_title);
    setHtml('txt-rule-3-desc', t.rule_3_desc);
    setTxt('txt-rule-4-title', t.rule_4_title);
    setHtml('txt-rule-4-desc', t.rule_4_desc);
    setTxt('start-btn', t.start_btn);

    setTxt('txt-missing-figure-title', t.missing_figure_title);
    if (prevBtn) prevBtn.textContent = t.prev_btn;
    if (submitBtn) submitBtn.textContent = t.submit_btn;
    if (openMapBtn) openMapBtn.textContent = t.map_btn;

    setTxt('map-modal-title', t.map_title);
    setTxt('txt-map-answered', t.map_answered);
    setTxt('txt-map-flagged', t.map_flagged);
    setTxt('txt-map-unanswered', t.map_unanswered);
    if (confirmMapBtn) confirmMapBtn.textContent = t.close_btn;

    setTxt('confirm-modal-title', t.confirm_title);
    if (cancelSubmitBtn) cancelSubmitBtn.textContent = t.cancel_btn;
    if (proceedSubmitBtn) proceedSubmitBtn.textContent = t.proceed_btn;

    setTxt('txt-res-hero-title', t.res_hero_title);
    setTxt('txt-res-raw-score', t.res_raw_score);
    setTxt('txt-res-time-spent', t.res_time_spent);
    setTxt('txt-res-avg-time', t.res_avg_time);
    setTxt('txt-breakdown-title', t.breakdown_title);

    setTxt('txt-export-pdf-btn', t.export_pdf_btn);
    setTxt('txt-home-btn', t.home_btn);
    setTxt('txt-review-panel-title', t.review_panel_title);
    setTxt('txt-review-panel-desc', t.review_panel_desc);
    setTxt('start-review-btn', t.open_review_btn);

    // Re-render active views
    if (testScreen && testScreen.style.display === 'flex') {
        renderQuestion(currentIndex);
    } else if (resultsScreen && resultsScreen.style.display === 'flex') {
        finishTest(true);
    }
}

if (langSelect) {
    langSelect.addEventListener('change', (e) => {
        applyLanguage(e.target.value);
    });
}

function initThemeAndLang() {
    // Language detection
    const savedLang = localStorage.getItem('matrix_iq_lang');
    if (savedLang && typeof I18N !== 'undefined' && I18N[savedLang]) {
        currentLang = savedLang;
    } else {
        const browserLang = (navigator.language || navigator.userLanguage || 'en').slice(0, 2).toLowerCase();
        if (typeof I18N !== 'undefined' && I18N[browserLang]) {
            currentLang = browserLang;
        } else {
            currentLang = 'en';
        }
    }
    if (langSelect) langSelect.value = currentLang;

    // Theme detection
    const savedTheme = localStorage.getItem('matrix_iq_theme');
    if (savedTheme) {
        currentTheme = savedTheme;
    } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
        currentTheme = 'light';
    } else {
        currentTheme = 'dark';
    }

    applyTheme(currentTheme);
    applyLanguage(currentLang);
}

// ----------------------------------------------------
// Test Progression & Timers
// ----------------------------------------------------
const startBtn = document.getElementById('start-btn');
if (startBtn) {
    startBtn.addEventListener('click', () => {
        if (introScreen) introScreen.style.display = 'none';
        if (testScreen) testScreen.style.display = 'flex';
        if (headerMeta) headerMeta.style.display = 'flex';
        testStartTime = Date.now();
        renderQuestion(currentIndex);
        startTimer();
        announceSR("Assessment started. Question 1 of 30.");
    });
}

function startTimer() {
    timerInterval = setInterval(() => {
        timeRemaining--;
        const mins = Math.floor(timeRemaining / 60);
        const secs = timeRemaining % 60;
        if (timerDisplay) {
            timerDisplay.textContent = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
            if (timeRemaining <= 300) {
                timerDisplay.classList.add('warning');
            }
        }

        if (timeRemaining <= 0) {
            clearInterval(timerInterval);
            finishTest();
        }
    }, 1000);
}

function renderQuestion(index) {
    currentIndex = index;
    if (typeof ITEMS === 'undefined' || !ITEMS[index]) return;
    const item = ITEMS[index];
    const t = (typeof I18N !== 'undefined' && I18N[currentLang]) ? I18N[currentLang] : {};

    if (progressIndicator) {
        progressIndicator.textContent = (t.q_progress || "Domanda {current} di {total}")
            .replace('{current}', index + 1)
            .replace('{total}', TOTAL_ITEMS);
    }

    // Category
    const translatedCat = (t.categories && t.categories[item.category_key]) || item.category_key;
    if (qCategory) qCategory.textContent = translatedCat;

    // Flagging
    if (flagBtn) {
        if (flaggedItems.has(index)) {
            flagBtn.classList.add('active');
            flagBtn.setAttribute('aria-pressed', 'true');
            if (txtFlagLabel) txtFlagLabel.textContent = t.flagged_btn || "Segnata per revisione";
        } else {
            flagBtn.classList.remove('active');
            flagBtn.setAttribute('aria-pressed', 'false');
            if (txtFlagLabel) txtFlagLabel.textContent = t.flag_btn || "Segna per dopo";
        }
    }

    // Render 3x3 Matrix
    if (matrixGrid) {
        matrixGrid.innerHTML = '';
        for (let i = 0; i < 8; i++) {
            const cell = document.createElement('div');
            cell.className = 'matrix-cell';
            cell.setAttribute('aria-label', `Row ${Math.floor(i/3)+1}, Column ${(i%3)+1}`);
            cell.innerHTML = `<svg viewBox="0 0 100 100">${item.grid[i]}</svg>`;
            matrixGrid.appendChild(cell);
        }

        // 9th target cell
        const targetCell = document.createElement('div');
        targetCell.className = 'matrix-cell target';
        targetCell.setAttribute('aria-label', 'Missing target cell');
        if (userAnswers[index] !== null) {
            const chosenSvg = item.options[userAnswers[index]];
            targetCell.innerHTML = `<svg viewBox="0 0 100 100">${chosenSvg}</svg>`;
        } else {
            targetCell.innerHTML = `<span class="target-placeholder">?</span>`;
        }
        matrixGrid.appendChild(targetCell);
    }

    // Render Candidate Options
    if (optionsGrid) {
        optionsGrid.innerHTML = '';
        item.options.forEach((optSvg, optIdx) => {
            const optCard = document.createElement('div');
            optCard.className = 'option-card';
            optCard.setAttribute('role', 'radio');
            optCard.setAttribute('tabindex', '0');
            const isSelected = (userAnswers[index] === optIdx);
            optCard.setAttribute('aria-checked', isSelected ? 'true' : 'false');

            const letter = String.fromCharCode(65 + optIdx);
            optCard.setAttribute('aria-label', `Option ${letter}`);

            if (isSelected) {
                optCard.classList.add('selected');
            }

            optCard.innerHTML = `
                <div class="option-badge" aria-hidden="true">${letter}</div>
                <svg viewBox="0 0 100 100">${optSvg}</svg>
            `;

            optCard.addEventListener('click', () => selectOption(optIdx));
            optCard.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    selectOption(optIdx);
                }
            });

            optionsGrid.appendChild(optCard);
        });
    }

    // Navigation buttons state
    if (prevBtn) {
        prevBtn.disabled = (index === 0);
        prevBtn.style.opacity = (index === 0) ? '0.4' : '1';
    }
    if (nextBtn) {
        nextBtn.textContent = (index === TOTAL_ITEMS - 1) ? (t.summary_btn || "Riepilogo") : (t.next_btn || "Successiva →");
    }
}

function selectOption(optIdx) {
    userAnswers[currentIndex] = optIdx;
    renderQuestion(currentIndex);
    const letter = String.fromCharCode(65 + optIdx);
    announceSR(`Selected option ${letter} for item ${currentIndex + 1}`);
}

if (flagBtn) {
    flagBtn.addEventListener('click', () => {
        if (flaggedItems.has(currentIndex)) {
            flaggedItems.delete(currentIndex);
        } else {
            flaggedItems.add(currentIndex);
        }
        renderQuestion(currentIndex);
    });
}

if (prevBtn) {
    prevBtn.addEventListener('click', () => {
        if (currentIndex > 0) renderQuestion(currentIndex - 1);
    });
}

if (nextBtn) {
    nextBtn.addEventListener('click', () => {
        if (currentIndex < TOTAL_ITEMS - 1) {
            renderQuestion(currentIndex + 1);
        } else {
            openQuestionMap();
        }
    });
}

// ----------------------------------------------------
// Question Map Modal
// ----------------------------------------------------
function openQuestionMap() {
    if (!questionMapGrid || !mapModal) return;
    questionMapGrid.innerHTML = '';
    for (let i = 0; i < TOTAL_ITEMS; i++) {
        const mapBtn = document.createElement('button');
        mapBtn.className = 'map-item';
        mapBtn.textContent = i + 1;
        mapBtn.setAttribute('aria-label', `Navigate to item ${i+1}`);

        if (userAnswers[i] !== null) mapBtn.classList.add('answered');
        if (flaggedItems.has(i)) mapBtn.classList.add('flagged');
        if (i === currentIndex) mapBtn.classList.add('current');

        mapBtn.addEventListener('click', () => {
            mapModal.style.display = 'none';
            renderQuestion(i);
        });

        questionMapGrid.appendChild(mapBtn);
    }
    mapModal.style.display = 'flex';
}

if (openMapBtn) openMapBtn.addEventListener('click', openQuestionMap);
if (closeMapBtn) closeMapBtn.addEventListener('click', () => { if (mapModal) mapModal.style.display = 'none'; });
if (confirmMapBtn) confirmMapBtn.addEventListener('click', () => { if (mapModal) mapModal.style.display = 'none'; });

// ----------------------------------------------------
// Submission & Scoring Evaluation
// ----------------------------------------------------
if (submitBtn) {
    submitBtn.addEventListener('click', () => {
        const t = (typeof I18N !== 'undefined' && I18N[currentLang]) ? I18N[currentLang] : {};
        const unanswered = userAnswers.filter(a => a === null).length;
        const flagged = flaggedItems.size;

        let msg = t.confirm_default || "Confermare la consegna?";
        if (unanswered > 0) {
            msg = (t.confirm_unanswered || "Attenzione: {count} quesiti senza risposta.").replace('{count}', unanswered);
        } else if (flagged > 0) {
            msg = (t.confirm_flagged || "Hai {count} quesiti contrassegnati.").replace('{count}', flagged);
        }

        if (confirmModalText) confirmModalText.innerHTML = msg;
        if (confirmModal) confirmModal.style.display = 'flex';
    });
}

if (cancelSubmitBtn) cancelSubmitBtn.addEventListener('click', () => { if (confirmModal) confirmModal.style.display = 'none'; });
if (proceedSubmitBtn) proceedSubmitBtn.addEventListener('click', () => {
    if (confirmModal) confirmModal.style.display = 'none';
    finishTest();
});

function finishTest(isRecompute = false) {
    if (!isRecompute) {
        testSubmitted = true;
        clearInterval(timerInterval);
    }

    if (typeof ENCODED_SOLUTIONS !== 'undefined') {
        decodedSolutions = JSON.parse(atob(ENCODED_SOLUTIONS));
    }
    const t = (typeof I18N !== 'undefined' && I18N[currentLang]) ? I18N[currentLang] : {};

    const timeSpentSeconds = Math.max(1, Math.round(((testStartTime ? Date.now() : 0) - (testStartTime || 0)) / 1000) || (TIME_LIMIT_SECONDS - timeRemaining));
    const minsSpent = Math.floor(timeSpentSeconds / 60);
    const secsSpent = timeSpentSeconds % 60;
    const avgSecondsPerItem = Math.round(timeSpentSeconds / TOTAL_ITEMS);

    let rawScore = 0;
    const categoryScores = {};

    for (let i = 0; i < TOTAL_ITEMS; i++) {
        if (!ITEMS || !ITEMS[i] || !decodedSolutions) continue;
        const qId = String(ITEMS[i].id);
        const sol = decodedSolutions[qId];
        const catKey = sol.category_key;

        if (!categoryScores[catKey]) {
            categoryScores[catKey] = { correct: 0, total: 0 };
        }
        categoryScores[catKey].total++;

        if (userAnswers[i] !== null && userAnswers[i] === sol.correct_idx) {
            rawScore++;
            categoryScores[catKey].correct++;
        }
    }

    // Call modular scoring engine
    const psych = calculateIQ(rawScore, currentLang);

    // Populate Results Screen
    setTxt('res-iq', psych.iq);
    setTxt('res-ci', (t.res_ci || "95% CI: [{low} - {high}]").replace('{low}', psych.ciLow).replace('{high}', psych.ciHigh));
    setTxt('res-classification', psych.classification);
    setTxt('res-percentile', (t.res_percentile || "{p}° percentile").replace(/\{p\}/g, psych.percentile));

    setTxt('res-raw-score', `${rawScore} / ${TOTAL_ITEMS}`);
    setTxt('res-time-spent', `${minsSpent}m ${secsSpent}s`);
    setTxt('res-avg-time', `${avgSecondsPerItem}s`);

    // Category breakdown bars
    const breakdownContainer = document.getElementById('categories-breakdown');
    if (breakdownContainer) {
        breakdownContainer.innerHTML = '';
        for (const [catKey, score] of Object.entries(categoryScores)) {
            const pct = Math.round((score.correct / score.total) * 100);
            const translatedCat = (t.categories && t.categories[catKey]) || catKey;
            const row = document.createElement('div');
            row.className = 'cat-row';
            row.innerHTML = `
                <div class="cat-header">
                    <span>${translatedCat}</span>
                    <span>${score.correct}/${score.total} (${pct}%)</span>
                </div>
                <div class="cat-bar-bg">
                    <div class="cat-bar-fill" style="width: ${pct}%;"></div>
                </div>
            `;
            breakdownContainer.appendChild(row);
        }
    }

    if (testScreen) testScreen.style.display = 'none';
    if (headerMeta) headerMeta.style.display = 'none';
    if (resultsScreen) resultsScreen.style.display = 'flex';
    window.scrollTo({ top: 0, behavior: 'smooth' });

    // If review was active, re-render in new language
    if (reviewContainer && reviewContainer.style.display === 'block') {
        renderReviewNavigator();
        renderReviewItem(currentReviewIndex || 0);
    }
}

// ----------------------------------------------------
// PDF Export & Home Reset
// ----------------------------------------------------
const exportPdfBtn = document.getElementById('export-pdf-btn');
if (exportPdfBtn) {
    exportPdfBtn.addEventListener('click', () => window.print());
}

const homeBtn = document.getElementById('home-btn');
if (homeBtn) {
    homeBtn.addEventListener('click', () => {
        const t = (typeof I18N !== 'undefined' && I18N[currentLang]) ? I18N[currentLang] : {};
        if (confirm(t.home_confirm || "Ricominciare il test?")) {
            resetTest();
        }
    });
}

function resetTest() {
    testSubmitted = false;
    clearInterval(timerInterval);
    timeRemaining = TIME_LIMIT_SECONDS;
    if (timerDisplay) {
        timerDisplay.textContent = "35:00";
        timerDisplay.classList.remove('warning');
    }
    currentIndex = 0;
    userAnswers = new Array(TOTAL_ITEMS).fill(null);
    flaggedItems.clear();
    testStartTime = null;

    if (resultsScreen) resultsScreen.style.display = 'none';
    if (testScreen) testScreen.style.display = 'none';
    if (headerMeta) headerMeta.style.display = 'none';
    if (introScreen) introScreen.style.display = 'block';

    if (reviewContainer) reviewContainer.style.display = 'none';
    if (startReviewBtn) startReviewBtn.style.display = 'inline-flex';
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ----------------------------------------------------
// Review Mode & Solutions
// ----------------------------------------------------
if (startReviewBtn) {
    startReviewBtn.addEventListener('click', () => {
        if (reviewContainer) reviewContainer.style.display = 'block';
        startReviewBtn.style.display = 'none';
        renderReviewNavigator();
        renderReviewItem(0);
    });
}

function renderReviewNavigator() {
    if (!reviewPills || !decodedSolutions) return;
    reviewPills.innerHTML = '';
    for (let i = 0; i < TOTAL_ITEMS; i++) {
        if (!ITEMS[i]) continue;
        const qId = String(ITEMS[i].id);
        const sol = decodedSolutions[qId];
        const isCorrect = (userAnswers[i] === sol.correct_idx);

        const pill = document.createElement('button');
        pill.className = 'btn-secondary';
        pill.style.padding = '0.3rem 0.55rem';
        pill.style.fontSize = '0.78rem';
        pill.style.fontWeight = '700';
        pill.style.borderColor = isCorrect ? 'var(--accent-emerald)' : 'var(--accent-rose)';
        pill.style.color = isCorrect ? 'var(--accent-emerald)' : 'var(--accent-rose)';
        pill.textContent = `${i + 1} ${isCorrect ? '✓' : '✗'}`;

        pill.addEventListener('click', () => renderReviewItem(i));
        reviewPills.appendChild(pill);
    }
}

function renderReviewItem(idx) {
    currentReviewIndex = idx;
    if (!ITEMS[idx] || !decodedSolutions || !reviewContent) return;
    const item = ITEMS[idx];
    const qId = String(item.id);
    const sol = decodedSolutions[qId];
    const userChoice = userAnswers[idx];
    const isCorrect = (userChoice === sol.correct_idx);
    const t = (typeof I18N !== 'undefined' && I18N[currentLang]) ? I18N[currentLang] : {};

    const expl = (sol.explanations && sol.explanations[currentLang]) || sol.explanations['en'] || "";
    const translatedCat = (t.categories && t.categories[sol.category_key]) || sol.category_key;

    let optionsHtml = '';
    item.options.forEach((optSvg, oIdx) => {
        let extraClass = '';
        let statusBadge = '';
        if (oIdx === sol.correct_idx) {
            extraClass = 'review-correct';
            statusBadge = `<span style="color: var(--accent-emerald); font-size: 0.65rem; font-weight: bold; position: absolute; bottom: 3px; right: 5px;">${t.correct_badge || 'Corretta'}</span>`;
        } else if (oIdx === userChoice && !isCorrect) {
            extraClass = 'review-user-wrong';
            statusBadge = `<span style="color: var(--accent-rose); font-size: 0.65rem; font-weight: bold; position: absolute; bottom: 3px; right: 5px;">${t.your_choice_badge || 'Tua scelta'}</span>`;
        }

        optionsHtml += `
            <div class="option-card ${extraClass}" style="cursor: default;">
                <div class="option-badge">${String.fromCharCode(65 + oIdx)}</div>
                <svg viewBox="0 0 100 100">${optSvg}</svg>
                ${statusBadge}
            </div>
        `;
    });

    let gridCellsHtml = '';
    for (let i = 0; i < 8; i++) {
        gridCellsHtml += `<div class="matrix-cell"><svg viewBox="0 0 100 100">${item.grid[i]}</svg></div>`;
    }
    gridCellsHtml += `
        <div class="matrix-cell review-correct" style="border: 2px solid var(--accent-emerald);">
            <svg viewBox="0 0 100 100">${item.options[sol.correct_idx]}</svg>
        </div>
    `;

    reviewContent.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; flex-wrap: wrap; gap: 0.5rem;">
            <h4 style="font-size: 1rem; font-weight: 700;">Domanda ${idx + 1} di ${TOTAL_ITEMS} • ${translatedCat}</h4>
            <span style="font-weight: 700; font-size: 0.9rem; color: ${isCorrect ? 'var(--accent-emerald)' : 'var(--accent-rose)'};">
                ${isCorrect ? (t.review_correct_label || '✓ Risposta Corretta') : (t.review_wrong_label || '✗ Risposta Errata')}
            </span>
        </div>
        <div class="review-split">
            <div class="matrix-container" style="padding: 0.75rem; max-width: 320px; margin: auto;">
                <div class="matrix-grid" style="gap: 6px;">${gridCellsHtml}</div>
            </div>
            <div class="options-grid" style="max-width: 440px; margin: auto;">${optionsHtml}</div>
        </div>
        <div class="review-explanation">
            <strong>${t.explanation_title || 'Spiegazione della Regola Logica:'}</strong><br>
            ${expl}
        </div>
    `;
}

// ----------------------------------------------------
// Global Keyboard Shortcuts
// ----------------------------------------------------
window.addEventListener('keydown', (e) => {
    if (testSubmitted || !testScreen || testScreen.style.display !== 'flex') return;

    // Keys 1-8
    if (e.key >= '1' && e.key <= '8') {
        const num = parseInt(e.key, 10) - 1;
        if (ITEMS && ITEMS[currentIndex] && num < ITEMS[currentIndex].options.length) selectOption(num);
    }
    // Keys A-H
    const k = e.key.toUpperCase();
    if (k >= 'A' && k <= 'H') {
        const idx = k.charCodeAt(0) - 65;
        if (ITEMS && ITEMS[currentIndex] && idx < ITEMS[currentIndex].options.length) selectOption(idx);
    }
    // Arrow Left / Right
    if (e.key === 'ArrowLeft') {
        if (currentIndex > 0) renderQuestion(currentIndex - 1);
    }
    if (e.key === 'ArrowRight') {
        if (currentIndex < TOTAL_ITEMS - 1) renderQuestion(currentIndex + 1);
    }
    // Space to toggle flag
    if (e.key === ' ' && e.target.tagName !== 'BUTTON') {
        e.preventDefault();
        if (flagBtn) flagBtn.click();
    }
});

// App Startup
window.addEventListener('DOMContentLoaded', initThemeAndLang);
