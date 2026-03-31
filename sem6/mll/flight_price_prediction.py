from __future__ import annotations

import argparse
import importlib
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import (
    BaggingRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeRegressor


@dataclass
class RunConfig:
    data_path: Path
    output_dir: Path
    test_size: float
    random_state: int
    use_log_target: bool
    max_rows: int | None
    cv_folds: int


def parse_args() -> RunConfig:
    parser = argparse.ArgumentParser(
        description="Flight price prediction model comparison"
    )
    parser.add_argument(
        "--data",
        type=Path,
        default=Path("datasets/miniproject/Clean_Dataset.csv"),
        help="Path to the input CSV dataset",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/flight_price"),
        help="Directory to store metrics and model artifacts",
    )
    parser.add_argument(
        "--test-size",
        type=float,
        default=0.2,
        help="Test set fraction",
    )
    parser.add_argument(
        "--random-state",
        type=int,
        default=42,
        help="Random seed",
    )
    parser.add_argument(
        "--use-log-target",
        action="store_true",
        help="Train on log1p(price) and evaluate after inverse transform",
    )
    parser.add_argument(
        "--max-rows",
        type=int,
        default=80_000,
        help="Optional random sample size for faster iteration",
    )
    parser.add_argument(
        "--cv-folds",
        type=int,
        default=3,
        help="Number of cross-validation folds (set 0 or 1 to skip CV)",
    )

    args = parser.parse_args()
    return RunConfig(
        data_path=args.data,
        output_dir=args.output_dir,
        test_size=args.test_size,
        random_state=args.random_state,
        use_log_target=args.use_log_target,
        max_rows=args.max_rows,
        cv_folds=args.cv_folds,
    )


def load_and_prepare_data(
    data_path: Path,
    random_state: int,
    max_rows: int | None,
) -> tuple[pd.DataFrame, pd.Series]:
    df = pd.read_csv(data_path)

    if max_rows is not None and len(df) > max_rows:
        df = df.sample(n=max_rows, random_state=random_state)

    unnamed_cols = [
        col for col in df.columns if col.lower().startswith("unnamed")
    ]
    if unnamed_cols:
        df = df.drop(columns=unnamed_cols)

    if "stops" in df.columns:
        stop_map = {"zero": 0, "one": 1, "two_or_more": 2}
        mapped_stops = df["stops"].map(stop_map)
        if mapped_stops.notna().all():
            df["stops"] = mapped_stops.astype(int)

    if "price" not in df.columns:
        raise ValueError("Dataset must contain a 'price' column.")

    y = df["price"].astype(float)
    X = df.drop(columns=["price"])

    constant_cols = [
        col for col in X.columns if X[col].nunique(dropna=False) <= 1
    ]
    if constant_cols:
        X = X.drop(columns=constant_cols)

    return X, y


def build_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    categorical_columns = X.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()
    numeric_columns = [
        col for col in X.columns if col not in categorical_columns
    ]

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_columns),
            ("cat", categorical_transformer, categorical_columns),
        ]
    )


def build_models(random_state: int) -> dict[str, object]:
    models: dict[str, object] = {
        "dummy_mean": DummyRegressor(strategy="mean"),
        "ridge": Ridge(alpha=1.0),
        "linear_regression": LinearRegression(),
        "lasso": Lasso(alpha=0.001, max_iter=10_000),
        "decision_tree": DecisionTreeRegressor(
            random_state=random_state,
            max_depth=10,
            min_samples_leaf=5,
        ),
        "bagging": BaggingRegressor(
            estimator=DecisionTreeRegressor(
                random_state=random_state,
                max_depth=10,
                min_samples_leaf=5,
            ),
            n_estimators=60,
            max_samples=0.7,
            bootstrap=True,
            n_jobs=-1,
            random_state=random_state,
        ),
        "random_forest": RandomForestRegressor(
            n_estimators=120,
            random_state=random_state,
            n_jobs=-1,
        ),
        "gradient_boosting": GradientBoostingRegressor(
            random_state=random_state
        ),
    }

    try:
        xgboost_module = importlib.import_module("xgboost")
        xgb_regressor = getattr(xgboost_module, "XGBRegressor")

        models["xgboost"] = xgb_regressor(
            n_estimators=180,
            learning_rate=0.05,
            max_depth=5,
            subsample=0.9,
            colsample_bytree=0.9,
            random_state=random_state,
            objective="reg:squarederror",
            n_jobs=-1,
        )
    except ImportError:
        pass

    try:
        lightgbm_module = importlib.import_module("lightgbm")
        lgbm_regressor = getattr(lightgbm_module, "LGBMRegressor")

        models["lightgbm"] = lgbm_regressor(
            n_estimators=200,
            learning_rate=0.05,
            random_state=random_state,
        )
    except ImportError:
        pass

    return models


def evaluate_models(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    preprocessor: ColumnTransformer,
    models: dict[str, object],
    random_state: int,
    cv_folds: int,
    use_log_target: bool,
) -> tuple[pd.DataFrame, Pipeline]:
    rows: list[dict[str, float | str]] = []
    best_rmse = float("inf")
    best_model_pipeline: Pipeline | None = None

    scoring = {
        "rmse": "neg_root_mean_squared_error",
        "mae": "neg_mean_absolute_error",
        "r2": "r2",
    }

    y_train_fit = np.log1p(y_train) if use_log_target else y_train
    total_models = len(models)

    for idx, (model_name, estimator) in enumerate(models.items(), start=1):
        model_start = perf_counter()
        print(f"[{idx}/{total_models}] Training model: {model_name}")
        pipe = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("model", estimator),
            ]
        )

        if cv_folds >= 2:
            cv = KFold(
                n_splits=cv_folds,
                shuffle=True,
                random_state=random_state,
            )
            cv_results = cross_validate(
                pipe,
                X_train,
                y_train_fit,
                cv=cv,
                scoring=scoring,
                n_jobs=1,
            )
            cv_rmse_mean = float(-cv_results["test_rmse"].mean())
            cv_rmse_std = float(cv_results["test_rmse"].std())
            cv_mae_mean = float(-cv_results["test_mae"].mean())
            cv_r2_mean = float(cv_results["test_r2"].mean())
        else:
            cv_rmse_mean = float("nan")
            cv_rmse_std = float("nan")
            cv_mae_mean = float("nan")
            cv_r2_mean = float("nan")

        pipe.fit(X_train, y_train_fit)
        pred_test = pipe.predict(X_test)

        if use_log_target:
            pred_test = np.expm1(pred_test)

        test_rmse = float(np.sqrt(mean_squared_error(y_test, pred_test)))
        test_mae = float(mean_absolute_error(y_test, pred_test))
        test_r2 = float(r2_score(y_test, pred_test))

        rows.append(
            {
                "model": model_name,
                "cv_rmse_mean": cv_rmse_mean,
                "cv_rmse_std": cv_rmse_std,
                "cv_mae_mean": cv_mae_mean,
                "cv_r2_mean": cv_r2_mean,
                "test_rmse": test_rmse,
                "test_mae": test_mae,
                "test_r2": test_r2,
            }
        )

        if test_rmse < best_rmse:
            best_rmse = test_rmse
            best_model_pipeline = pipe

        elapsed = perf_counter() - model_start
        print(
            f"    Done {model_name} in {elapsed:.2f}s | "
            f"test_rmse={test_rmse:.4f}, test_r2={test_r2:.4f}"
        )

    if best_model_pipeline is None:
        raise RuntimeError("No model was successfully trained.")

    result_df = pd.DataFrame(rows)
    result_df = result_df.sort_values("test_rmse").reset_index(drop=True)
    return result_df, best_model_pipeline


def main() -> None:
    config = parse_args()
    config.output_dir.mkdir(parents=True, exist_ok=True)

    X, y = load_and_prepare_data(
        data_path=config.data_path,
        random_state=config.random_state,
        max_rows=config.max_rows,
    )
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=config.test_size,
        random_state=config.random_state,
    )

    preprocessor = build_preprocessor(X)
    models = build_models(config.random_state)
    results, best_pipeline = evaluate_models(
        X_train=X_train,
        X_test=X_test,
        y_train=y_train,
        y_test=y_test,
        preprocessor=preprocessor,
        models=models,
        random_state=config.random_state,
        cv_folds=config.cv_folds,
        use_log_target=config.use_log_target,
    )

    results_path = config.output_dir / "model_comparison.csv"
    results.to_csv(results_path, index=False)

    try:
        import joblib

        best_model_name = results.iloc[0]["model"]
        model_file = config.output_dir / "best_model_pipeline.joblib"
        joblib.dump(best_pipeline, model_file)
        with (config.output_dir / "best_model.txt").open(
            "w", encoding="utf-8"
        ) as file:
            file.write(str(best_model_name))
    except ImportError:
        pass

    print("\nModel comparison (sorted by test RMSE):")
    print(results.round(4).to_string(index=False))
    print(f"\nSaved metrics to: {results_path}")
    print(f"Saved artifacts in: {config.output_dir}")


if __name__ == "__main__":
    main()
