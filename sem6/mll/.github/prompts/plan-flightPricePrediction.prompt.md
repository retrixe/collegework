## Plan: Flight Price Prediction Notebook

Build a regression workflow in a new section of your existing notebook style: clean/encode features, train a baseline and stronger models, compare with regression metrics, and present explainable conclusions. This mirrors your Assignment1–6 structure while adapting evaluation from classification to regression.

**Steps**
1. **Phase 1 — Problem framing & data audit**
   - Define target as `price` and prediction task as supervised regression.
   - Load `datasets/miniproject/Clean_Dataset.csv` and validate schema/types.
   - Check duplicates, missing values, and constant/near-constant features (especially `class`, `days_left`).
   - Decide removable ID-like columns (`Unnamed: 0` index column, possibly `flight` if overly high-cardinality/noisy).

2. **Phase 2 — Preprocessing design**
   - Separate numeric (`duration`, `days_left`) and categorical features.
   - Map `stops` to ordinal integers (`zero`→0, `one`→1, `two_or_more`→2).
   - Keep nominal features (`airline`, `source_city`, `destination_city`, `departure_time`, `arrival_time`, optionally `flight`) for encoding.
   - Add optional target transform branch (`log1p(price)`) if price distribution is strongly right-skewed.
   - Build preprocessing with a `ColumnTransformer` + `Pipeline` to avoid leakage and keep models comparable.

3. **Phase 3 — Split strategy & baselines** (*depends on 1–2*)
   - Train/test split 80/20 with `random_state=42`.
   - Add baseline predictors:
     - Dummy baseline (mean prediction).
     - Linear Regression baseline.
   - Evaluate with MAE, RMSE, R² on the same split.

4. **Phase 4 — Core model comparison** (*depends on 3*)
   - Train assignment-friendly explainable set:
     - Ridge/Lasso (regularized linear models).
     - Decision Tree Regressor.
     - Random Forest Regressor.
     - Gradient Boosting Regressor.
   - If extra libs allowed/installed: add XGBoost or LightGBM as advanced candidate.
   - Use consistent cross-validation (e.g., 5-fold) on training set for fair comparison before final test-set report.

5. **Phase 5 — Tuning & diagnostics** (*depends on 4; parallelizable by model*)
   - Tune top 1–2 models with small, controlled search spaces (depth, estimators, learning rate, min samples).
   - Run residual diagnostics: residual histogram + predicted-vs-actual scatter.
   - Extract explainability artifacts:
     - Linear coefficients (for linear family).
     - Feature importances (tree/boosting models).

6. **Phase 6 — Final selection & report-ready outputs** (*depends on 5*)
   - Select final model using test RMSE/MAE plus interpretability.
   - Produce compact comparison table and ranking chart.
   - Write conclusions in assignment style:
     - Best model and why.
     - Top price drivers.
     - Error behavior (where model under/over-predicts).
     - Short limitations + future improvements.

7. **Phase 7 — Optional deployment-ready extras** (*parallel with 6 if needed*)
   - Persist model + preprocessing pipeline with `joblib`.
   - Add small inference cell for one custom itinerary.

**Relevant files**
- `/home/ibu/Documents/collegework/sem6/mll/datasets/miniproject/Clean_Dataset.csv` — main training data and feature schema.
- `/home/ibu/Documents/collegework/sem6/mll/Assignment6.ipynb` — reuse notebook organization/style conventions for sections and visuals.
- `/home/ibu/Documents/collegework/sem6/mll/pyproject.toml` — dependency boundary check (scikit-learn/pandas/seaborn and optional xgboost/lightgbm).

**Verification**
1. Data checks pass: no unresolved missing values; expected dtypes after preprocessing.
2. Pipeline integrity check: same preprocessing is applied through cross-validation and test inference (no manual leakage-prone transforms).
3. Metrics check: baseline RMSE > at least one trained model RMSE; test MAE/RMSE/R² reported for all compared models.
4. Diagnostic check: residuals are roughly centered around zero; no severe systematic pattern in predicted-vs-actual plot.
5. Reproducibility check: rerun with same seed yields same split and nearly identical metrics.

**Decisions**
- Included: explainable model-comparison workflow with optional boosted model.
- Excluded: deep learning sequence models and external APIs/pricing features (outside dataset scope).
- Primary objective: assignment-friendly interpretability first, then performance.

**Further Considerations**
1. Keep or drop `flight` feature: test both; retain only if cross-validated RMSE improves materially.
2. Use log-target only if residual plots improve and metric gains are stable on original-price inverse transform.
3. If compute budget is limited, prioritize Random Forest + Gradient Boosting + one linear model.
