# MatriQ: Standardized Culture-Fair Progressive Matrices Assessment

A computerized, open-source psychometric instrument designed to evaluate Fluid Intelligence ($G_f$) and Spearman's general cognitive factor ($g$).

---

## 1. Theoretical Framework and Psychometric Construct

The MatriQ assessment model is grounded in the Cattell-Horn-Carroll (CHC) theory of cognitive abilities, the prevailing consensus taxonomy in contemporary psychometric and differential psychology research.

Within CHC theory, **Fluid Intelligence ($G_f$)** denotes the biologically delimited capacity for inductive and deductive reasoning, novel pattern abstraction, spatial transformations, and rule inference, operating independently of previously acquired declarative or culturally mediated knowledge.

Unlike multi-battery clinical instruments (such as the Wechsler Adult Intelligence Scale, WAIS-IV) that incorporate subtests reliant on lexical breadth and formal education (Verbal Comprehension, $G_c$), MatriQ implements a purely non-verbal **Culture-Fair Progressive Matrices** paradigm. The absence of alphanumeric, linguistic, or cultural stimuli minimizes error variance attributable to native language differences, formal education disparities, and socio-economic variables, enabling statistically valid cross-national comparisons.

---

## 2. Item Taxonomy and Complexity Stratification

The assessment consists of a standardized sequence of **30 progressive 3x3 matrices**, calibrated across an empirical difficulty gradient to eliminate floor and ceiling effects within the general adult population.

Each matrix features 8 visible cells positioned across 3 rows and 3 columns; the missing 9th cell (coordinates [2,2]) must be inferred by identifying horizontal, vertical, and coordinate covarying rules. Response choices (ranging from 6 to 8 candidate options) are engineered with systematically designed distractors targeting documented heuristic errors (e.g., spatial perseveration, phase inversion, incomplete rule application, and parity violations).

### Cognitive Stratification of the 30 Items

| Tier | Items | Primary Cognitive Domain | Underlying Logical Operations |
| :--- | :--- | :--- | :--- |
| **I. Linear Foundations** | 1 – 6 | Quantitative Progression and Continuity | Discrete scalar increments ($\Delta n = +1$), Cartesian translations, topological fill transitions, and 90° rigid planar rotations. |
| **II. Orthogonal Combinatorics** | 7 – 12 | Latin Squares and Attribute Distribution | Bidirectional row/column permutation invariance across 2 and 3 simultaneous orthogonal attributes (shape, hatching pattern, orbital satellites). |
| **III. Direct Graphical Operations** | 13 – 18 | Vector Set Theory and Spatial Dynamics | Direct graphical superposition (Boolean OR), graphical subtraction ($A \setminus B$), modular perimeter orbits ($\mathbb{Z}_8$), and converging kinematic vectors. |
| **IV. Abstract Boolean Logic** | 19 – 24 | Symmetric Difference (XOR) and Lattices | Rigorous XOR gate evaluation on planar segments, radial axes, and 3x3 binary dot matrices: mutual cancellation of overlapping features, preservation of disjoint components. |
| **V. High-Ceiling Composite Integration** | 25 – 30 | Topology, Parity Invariants, and Modular Rules | Conjunction of 3 simultaneous multi-variable transformations: multi-layered XOR with horizontal specular reflection, 2D Cartesian vector addition ($\mathbb{R}^2$), 1D elementary cellular automata (Wolfram Rule 90 neighbor-parity), and invariant dot conservation across counter-rotating concentric notched rings. |

---

## 3. Normative Scoring Model and Statistical Standardization

### 3.1 Wechsler Scale Conversion

Standardized Intelligence Quotient (IQ) estimation conforms to the normal Gaussian distribution with population mean $\mu = 100$ and standard deviation $\sigma = 15$:

$$IQ = 100 + 15 \cdot Z$$

where $Z$ represents the standardized score derived from the empirical calibration of raw correct responses ($R \in [0, 30]$).

### 3.2 Standard Error of Measurement and 95% Confidence Intervals

Assuming an empirical test-retest reliability coefficient for high $g$-loaded progressive matrices of $r_{xx} \approx 0.88$, the Standard Error of Measurement ($SEM$) is formulated as:

$$SEM = \sigma \cdot \sqrt{1 - r_{xx}} \approx 15 \cdot \sqrt{1 - 0.88} \approx 5.20$$

Each final evaluation is accompanied by a standardized two-tailed 95% confidence interval:

$$CI_{95\%} = IQ \pm 1.96 \cdot SEM \approx [IQ - 5, \; IQ + 5]$$

### 3.3 Percentile Rank via Cumulative Distribution Function

The corresponding population percentile rank is calculated using the Standard Normal Cumulative Distribution Function $\Phi(Z)$:

$$\text{Percentile} = \Phi\left(\frac{IQ - 100}{15}\right) \times 100\% = \frac{1}{\sqrt{2\pi}} \int_{-\infty}^{Z} e^{-\frac{t^2}{2}} \, dt \times 100\%$$

---

## 4. Software Architecture and Technical Specifications

MatriQ is engineered as a zero-dependency, client-side Single-Page Application (SPA) with zero network footprint, ensuring full deterministic execution, offline reliability, and absolute participant privacy.

* **Native SVG Vector Rendering:** All matrix stimuli and distractor options are constructed programmatically via scalar SVG mathematical primitives utilizing `stroke="currentColor"`. This guarantees resolution-independent fidelity on all display densities (Retina, 4K, 8K) and instant contrast-safe theme inversion.
* **Ergonomic Zero-Scroll Split Viewport:** On desktop and laptop displays, the active testing interface employs an adaptive two-column split layout (`max-height: calc(100vh - 80px)`). The stimulus matrix (left column) and the response options with integrated controls (right column) remain simultaneously in the test-taker's foveal visual field. This eliminates vertical displacement, preventing cognitive fatigue and saccadic disruption caused by scrolling.
* **Full Multilingual Internationalization (i18n):** Complete native support for 6 languages: English, Italian, German, Spanish, Portuguese, and French. System language preferences are automatically resolved via RFC 5646 (`navigator.language`) with optional manual persistence in `localStorage`. The translation layer encompasses UI labels, psychometric classifications, and all 30 post-test analytical solutions.
* **Accessibility and WCAG 2.1 AA/AAA Compliance:**
  * Full keyboard navigability: predictable tab order with high-contrast visible focus indicators (`:focus-visible`), arrow-key traversal, rapid selection keys (`1`–`8` / `A`–`H`), and spacebar flag toggling.
  * Screen-reader compliance via WAI-ARIA 1.2 semantics (`role="radiogroup"`, `role="radio"`, `aria-checked`, `aria-live="polite"`).
  * Vestibular and motion-sensitivity compliance via `prefers-reduced-motion`.
* **Standardized ISO 216 (A4) Print Engine:** Through dedicated `@media print` directives, the results screen reconfigures into a clean psychological evaluation report, omitting interactive buttons and rendering vector-sharp typography, statistical confidence bounds, domain breakdowns, and clinical classifications.

---

## 5. Administration Protocol

To ensure construct validity and testing integrity:
1. **Testing Environment:** Administration must occur in a quiet, private setting with adequate lighting and zero auditory or digital interruptions.
2. **Time Constraint:** Total administration duration is strictly capped at **35 minutes** continuous countdown (~70 seconds per item). Pausing the assessment timer is disabled by design.
3. **Hardware Recommendation:** A full-screen desktop or laptop monitor with a minimum display resolution of $1280 \times 720$ is recommended for optimal perceptual discrimination.

---

## 6. Directory Structure

```
matriq/
├── index.html                 # Production-ready compiled standalone application
├── favicon.svg                # Scalable vector favicon
├── logo.svg                   # Full horizontal brand vector mark
├── app_template.html          # Source HTML5/CSS3 application template
├── build_html_template.py     # Deterministic compiler and asset injector
├── items_definition.py        # Mathematical and geometric definitions for all 30 items
├── i18n_data.py               # Multilingual dictionary (EN, IT, DE, ES, PT, FR)
├── translate_explanations.py  # Analytical item solutions across 6 languages
├── generate_test.py           # SVG primitives, geometry generators, and SHA-256 answer hashing
├── validate_all.py            # XML/SVG syntax validation and internal consistency checker
└── README.md                  # Comprehensive scientific and technical documentation
```

---

## 7. Deployment and Static Hosting

The codebase requires no server runtimes, databases, or external build pipelines. To deploy on GitHub Pages:

```bash
cd /Users/nmac/Develop/Taoshan/matriq
git init
git add .
git commit -m "feat: initial standardized release of MatriQ"
git branch -M main
git remote add origin https://github.com/USERNAME/matriq.git
git push -u origin main
```

Navigate to **Settings** > **Pages** within the GitHub repository and select the `main` branch with the `/ (root)` directory. The assessment will be hosted statically at `https://USERNAME.github.io/matriq/`.

---

## 8. References

* **Carroll, J. B. (1993).** *Human cognitive abilities: A survey of factor-analytic studies.* Cambridge University Press.
* **Cattell, R. B. (1971).** *Abilities: Their structure, growth, and action.* Houghton Mifflin.
* **Raven, J., Raven, J. C., & Court, J. H. (1998).** *Manual for Raven's Progressive Matrices and Vocabulary Scales.* Oxford Psychologists Press.
* **Spearman, C. (1904).** *"General Intelligence," objectively determined and measured.* The American Journal of Psychology, 15(2), 201-292.
* **Wechsler, D. (2008).** *Wechsler Adult Intelligence Scale – Fourth Edition (WAIS-IV).* Pearson Assessment.
