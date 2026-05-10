# 📈 Hedge Fund — Panel Time-Series Forecasting

> A diagnostic-driven forecasting study on anonymised hedge-fund panel data, comparing classical, deep-learning, and gradient-boosted quantile models under a weighted skill metric.

<p align="center">
  <strong>Applied Forecasting Methods · Group 8</strong>
</p>

---

## 👥 Team

| Name | Roll Number |
|------|-------------|
| Kaushal Nandaniya | 202303036 |
| Jeetrajsinh Gohil | 202303017 |
| Dhyey Patel | 202301415 |
| Manthan Gajera | 202301488 |

**Instructor:** Prof. Pritam Anand  
**Institution:** Dhirubhai Ambani Institute of Information and Communication Technology (DA-IICT)

---

## 📋 Table of Contents

- [Abstract](#abstract)
- [Problem Statement](#problem-statement)
- [Dataset](#dataset)
- [Methodology](#methodology)
  - [Exploratory Data Analysis](#1-exploratory-data-analysis)
  - [Classical Forecasting Models](#2-classical-forecasting-models)
  - [Deep Sequence Models](#3-deep-sequence-models)
  - [Quantile Regression Forecasts](#4-quantile-regression-forecasts)
  - [Two-Model Approach with Time-Based K-Fold](#5-two-model-approach-with-time-based-k-fold)
- [Key Results](#key-results)
- [Converting Forecasts into Actions](#converting-forecasts-into-actions)
- [Project Structure](#project-structure)
- [Installation & Usage](#installation--usage)
- [Future Work](#future-work)
- [References](#references)

---

## Abstract

This project tackles a large-scale panel time-series forecasting problem derived from anonymised hedge-fund data ([Kaggle Competition](https://www.kaggle.com/competitions/ts-forecasting)). The objective is to predict future values of a target variable across **36,923 heterogeneous series** under a **weighted evaluation metric** where the top 1% of rows carry **64.2%** of the total weight.

The study adopts a **diagnostic-driven approach**:

1. **Extensive EDA** to understand missingness, distributional properties, weight imbalance, and multi-horizon coupling.
2. **Classical models** (SES, Holt, AR, MA, ARMA, ARIMA, SARIMA) applied to four representative series spanning the panel's stress dimensions.
3. **Deep recurrent models** (RNN, GRU, LSTM) fit under adaptive chronological splits.
4. **LightGBM quantile regression** with calibrated 80% prediction intervals via rolling 70/20/20 chronological backtests.
5. **Two-model approach** with time-based K-fold cross-validation and engineered features.

**Key finding:** No single model universally dominates — model choice matters most where the data has structure to exploit. The deployable artefact is a **calibrated prediction interval**, not a single point estimate.

---

## Problem Statement

Given a panel of ~5.3M training rows organised by anonymised financial instruments across **4 forecasting horizons** (H = 1, 3, 10, 25), predict future target values while:

- Handling **heavy-tailed distributions** (target range: −2202 to +2314)
- Optimising for **extreme weight concentration** (top 1% of rows carry 64% of total weight)
- Respecting **strict chronological constraints** (no future leakage)
- Managing **varying series lengths** (most series are short; only ~5% have ≥120 training rows)

### Weighted Skill Score

All models are evaluated using the competition's **weighted skill score**:

$$\text{score}(\mathbf{y}, \hat{\mathbf{y}}; \mathbf{w}) = \sqrt{1 - \text{clip}_{[0,1]} \left( \frac{\sum_i w_i (y_i - \hat{y}_i)^2}{\sum_i w_i y_i^2} \right)}$$

- **1.0** = perfect prediction
- **0.0** = no better than predicting zero
- **~0.95** = strong, near the practical ceiling

---

## Dataset

| Property | Value |
|----------|-------|
| **Source** | [Kaggle: Hedge Fund Time-Series Forecasting](https://www.kaggle.com/competitions/ts-forecasting) |
| **Format** | Parquet (~1 GB) |
| **Training rows** | 5,337,414 |
| **Test rows** | 1,447,107 |
| **Distinct series** | 36,923 |
| **Codes** | 23 |
| **Sub-codes** | 180 (train), 47 (test) |
| **Horizons** | 4 (H = 1, 3, 10, 25) |
| **Features** | 86 anonymised |
| **Time index range** | Train: [1, 3601], Test: [3602, 4376] |

### Key Data Properties

- **Heavy tails:** Median target ≈ −0.0006, but extremes reach ±2200
- **Extreme weight skew:** Median weight ~1,699 vs max ~1.39 × 10¹³
- **Multi-horizon coupling:** Targets at H ∈ {3, 10, 25} ≈ rolling cumulative sums of H=1 (Pearson ρ = 0.96, 0.94, 0.91)
- **Missingness:** Max missing rate ~12.5% — within-fold median imputation suffices

---

## Methodology

### Representative Series

All per-series analyses use **four representative series** spanning distinct stress regimes:

| Label | Regime | Horizon | Length |
|-------|--------|---------|--------|
| Longest History | Long data, moderate signal | H=1 | 212 |
| Highest Total Weight | Economically critical | H=25 | 156 |
| Most Volatile | High variance, cyclical | H=25 | 162 |
| Most Stable | Near-zero signal / noise | H=1 | 170 |

---

### 1. Exploratory Data Analysis

**Notebook:** [`01_eda.ipynb`](01_eda.ipynb)

- Schema validation and train–test comparability checks
- Missing value analysis (48/86 features have some missingness, max ~12.5%)
- Target and weight distribution analysis
- Stationarity testing (ADF & KPSS tests on 200 sampled series)
- Rolling statistics for visual stationarity assessment
- ACF/PACF correlograms and panel-level aggregation
- STL decomposition with ACF-based period selection
- Feature importance audit
- Multi-horizon coupling verification
- Per-horizon weight dominance analysis

---

### 2. Classical Forecasting Models

**Notebook:** [`02_classical_models.ipynb`](02_classical_models.ipynb)

**Models evaluated:**
- Simple Exponential Smoothing (SES)
- Holt's Linear Trend
- Rolling Mean
- AR(1), AR(2), AR(3)
- MA(1), MA(2), MA(3)
- ARMA(1,1), ARMA(2,1)
- ARIMA(1,1,0), ARIMA(1,1,1)
- SARIMA

**Protocols:**
- **Fixed cutoff** at `tsindex = 2880` (baseline comparison)
- **Adaptive 80/20 chronological split** (full-history utilisation)

**Key findings:**
- Smoothing models dominate on stable, low-variance series
- ARIMA(1,1,1) and AR(1) take over with sufficient training data
- Moving from fixed to adaptive splits changes which model family wins

---

### 3. Deep Sequence Models

**Notebook:** [`03_deep_sequence_models.ipynb`](03_deep_sequence_models.ipynb)

**Architectures:**
- Vanilla RNN (hidden size 32, 1 layer)
- GRU (hidden size 32, 1 layer)
- LSTM (hidden size 32, 1 layer)

All models use **univariate inputs** (lagged target only) with **recursive multi-step forecasting**.

**Key findings:**
- RNN achieves 0.9235 skill on the Most Volatile series
- LSTM achieves 0.6264 on the Highest Total Weight series
- Recursive error compounding limits multi-step performance on long horizons

---

### 4. Quantile Regression Forecasts

**Notebooks:** [`03_af.ipynb`](03_af.ipynb), [`04_quantile_regression.ipynb`](04_quantile_regression.ipynb)

**Method:** LightGBM with quantile loss (`objective="quantile"`)
- Three separate boosters per series at τ_low, τ_mid (0.5), τ_high
- Per-series interval pair (τ_lo, τ_hi) selection on calibration slice
- Conformal post-calibration for coverage guarantee

**Configuration:** 400 trees · lr=0.04 · depth=5 · 31 leaves · subsample=0.85

**Evaluation:** Rolling 70/20/20 chronological backtest (2–5 folds per series)

**Key findings:**
- Best single point forecast on Highest Total Weight: **skill = 0.865**
- Calibrated 80% prediction intervals with wPICP between 0.762 and 0.862
- Non-recursive protocol avoids the error compounding that limits deep models

---

### 5. Two-Model Approach with Time-Based K-Fold

**Notebooks:** [`05_two-model-approach-with-time-based-k-fold.ipynb`](05_two-model-approach-with-time-based-k-fold.ipynb), [`two-model-approach-with-time-based-k-fold.ipynb`](two-model-approach-with-time-based-k-fold.ipynb)

Splits the problem into two specialised models and validates with time-based K-fold cross-validation and engineered features. This approach outperforms quantile regression on the headline score by targeting the point-forecast and interval objectives separately.

---

## Key Results

### Cross-Method Comparison (Best Weighted Skill per Series)

| Series | Classical (Best) | Deep (Best) | Quantile (Median) |
|--------|-----------------|-------------|-------------------|
| Longest History | SARIMA 0.0617 | GRU 0.0686 | 0.000 |
| **Highest Total Weight** | ARIMA(1,1,1) 0.4667 | LSTM 0.6264 | **0.865** |
| **Most Volatile** | AR(1) 0.8277 | RNN **0.9235** | 0.859 |
| Most Stable | AR(1) 0.0000 | all 0.0000 | 0.000 |

### Calibrated 80% Prediction Interval Coverage

| Series | wPICP | PICP | wMPIW | Folds |
|--------|-------|------|-------|-------|
| Longest History | 0.862 | 0.860 | 6.437 | 5 |
| Highest Total Weight | 0.792 | 0.800 | 0.0005 | 2 |
| Most Volatile | 0.774 | 0.767 | 192.1 | 5 |
| Most Stable | 0.762 | 0.767 | 0.0004 | 3 |

### Headline Findings

1. **Model choice matters most where data has exploitable structure.** On the two informative series (Highest Total Weight, Most Volatile), moving from classical → deep → quantile produces real lifts. On near-zero-signal series, no model beats the floor.

2. **The non-recursive protocol wins on long horizons.** LightGBM quantile-median (0.865) beats recursive LSTM (0.6264) on Highest Total Weight because it avoids error compounding.

3. **Calibrated 80% prediction intervals are achievable** on every representative series (wPICP: 0.762–0.862). This is the deployable artefact.

4. **Data quantity changes model selection.** With 7 training points, only smoothing is fittable; with 120+, ARIMA takes over — a methodological not cosmetic distinction.

---

## Converting Forecasts into Actions

The report includes a practical framework for translating model outputs into **tradeable positions**:

- **Position sizing:** $\pi_i = K \cdot \hat{y}^{(0.5)}_i / \sigma^2_i$ (Kelly-style, scaled by inverse variance)
- **Risk controls:** Per-code hard caps, interval-crossing scaling, noise-floor filters
- **Live monitoring:** Rolling wPICP, per-code skill tracking, interval width ratios
- **Decision tree:** 8-step production checklist (filter → size → cap → execute)

---

## Project Structure

```
HedgeFund_TimeSeriesForcasting/
├── 01_eda.ipynb                                          # Exploratory Data Analysis
├── 02_classical_models.ipynb                             # Classical forecasting models
├── 03_deep_sequence_models.ipynb                         # RNN, GRU, LSTM models
├── 03_af.ipynb                                           # Applied forecasting notebook
├── 04_quantile_regression.ipynb                          # LightGBM quantile regression
├── 05_two-model-approach-with-time-based-k-fold.ipynb    # Two-model approach (config)
├── two-model-approach-with-time-based-k-fold.ipynb       # Two-model approach (full)
├── data/
│   ├── ts-forecasting/                                   # Raw Kaggle data (parquet)
│   ├── processed/                                        # Processed data artifacts
│   └── quantile_outputs/                                 # Quantile model outputs
├── report/
│   ├── main.tex                                          # LaTeX source
│   ├── sections/                                         # LaTeX section files
│   └── figures/                                          # Report figures
├── Report.pdf                                            # Final compiled report (63 pages)
├── Final_presentation.pdf                                # Final presentation slides
├── Mid_presentation.pdf                                  # Mid-term presentation slides
├── requirement.txt                                       # Python dependencies
└── README.md                                             # This file
```

---

## Installation & Usage

### Prerequisites

- Python 3.8+
- ~1 GB disk space for the dataset

### Setup

```bash
# Clone the repository
git clone https://github.com/your-username/HedgeFund_TimeSeriesForcasting.git
cd HedgeFund_TimeSeriesForcasting

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirement.txt
```

### Additional Dependencies

Some notebooks require packages beyond `requirement.txt`:

```bash
pip install lightgbm scikit-learn torch PyPDF2
```

### Data

Download the dataset from the [Kaggle competition page](https://www.kaggle.com/competitions/ts-forecasting) and place the parquet files in `data/ts-forecasting/`.

### Running the Notebooks

Execute the notebooks **in order** for the full reproducible pipeline:

```
01_eda.ipynb                    → Data exploration & diagnostics
02_classical_models.ipynb       → Classical model fitting & evaluation
03_deep_sequence_models.ipynb   → Deep sequence model training
04_quantile_regression.ipynb    → Quantile regression & interval calibration
05_two-model-approach-*.ipynb   → Two-model ensemble approach
```

---

## Future Work

1. **Scale per-series studies to the full panel** (all 1,930 eligible series)
2. **Per-horizon LightGBM calibration** — fit one booster per horizon on the full panel
3. **Feature-aware deep models** — concatenate top-k features into LSTM/GRU inputs
4. **Hyperparameter sweep** — Optuna tuning on the quantile model (20–50 trials)
5. **Ensemble across model families** — ridge-stacking on the reserved meta slice
6. **Multi-horizon coupling** — multi-output model with soft cumulation constraint
7. **Cross-series transfer** — multi-task learning across sub-codes within a code
8. **Real-money risk overlay** — portfolio construction with transaction costs and live monitoring
9. **Tube Loss** — single-stage prediction interval estimation as an alternative to conformal quantile regression

---

## References

1. Hyndman, R. J. & Athanasopoulos, G. — *Forecasting: Principles and Practice*, 3rd ed., OTexts, 2021.
2. Ke, G. et al. — *LightGBM: A Highly Efficient Gradient Boosting Decision Tree*, NeurIPS 2017.
3. Hochreiter, S. & Schmidhuber, J. — *Long Short-Term Memory*, Neural Computation, 1997.
4. Romano, Y. et al. — *Conformalized Quantile Regression*, NeurIPS 2019.
5. Kaggle — [Hedge Fund Time-Series Forecasting Competition](https://www.kaggle.com/competitions/ts-forecasting).
6. Anand, P. et al. — *Tube Loss: A Novel Approach for Prediction Interval Estimation*, arXiv:2412.06853, 2024.

---

<p align="center">
  <em>Applied Forecasting Methods · Semester 6 · DA-IICT</em>
</p>