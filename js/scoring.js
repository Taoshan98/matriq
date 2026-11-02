/**
 * MatriQ Psychometric Scoring Module
 * Evaluates Wechsler-standardized IQ, Gaussian percentile rank,
 * and standard error bounds (SEM).
 */

const IQ_TABLE = [
    68, 72, 75, 78, 81, 84, 87, 90, 93, 96, 98,
    100, 102, 105, 108, 110, 113, 115, 118, 120, 123,
    125, 128, 131, 133, 136, 138, 140, 142, 144, 145
];

function calculateIQ(rawScore, lang = 'it') {
    const clampedRaw = Math.max(0, Math.min(30, rawScore));
    const iq = IQ_TABLE[clampedRaw];

    // Standard score: Z = (IQ - 100) / 15
    const z = (iq - 100) / 15.0;

    // Standard normal CDF approximation (Abramowitz & Stegun formula)
    const t = 1.0 / (1.0 + 0.2316419 * Math.abs(z));
    const d = 0.3989423 * Math.exp(-z * z / 2.0);
    let p = d * t * (0.3193815 + t * (-0.3565638 + t * (1.781478 + t * (-1.821256 + t * 1.330274))));
    let percentile = (z > 0) ? (1.0 - p) * 100 : p * 100;
    percentile = Math.max(0.1, Math.min(99.9, percentile)).toFixed(1);

    const sem = 5; // Standard error of measurement (95% CI: +/- 5)
    const ciLow = Math.max(65, iq - sem);
    const ciHigh = Math.min(150, iq + sem);

    const t_lang = (typeof I18N !== 'undefined' && I18N[lang]) ? I18N[lang] : {};
    let classification = t_lang.class_avg || "Nella Media";
    if (iq >= 135) classification = t_lang.class_exceptional || "Eccezionale / Alto Potenziale (Top 1%)";
    else if (iq >= 130) classification = t_lang.class_very_superior || "Molto Superiore (Top 2%)";
    else if (iq >= 120) classification = t_lang.class_superior || "Superiore (Top 10%)";
    else if (iq >= 110) classification = t_lang.class_high_avg || "Media Superiore";
    else if (iq >= 90) classification = t_lang.class_avg || "Nella Media Tipica";
    else if (iq >= 80) classification = t_lang.class_low_avg || "Media Inferiore";
    else classification = t_lang.class_below_avg || "Al di sotto della Media";

    return {
        iq,
        percentile,
        classification,
        ciLow,
        ciHigh
    };
}
