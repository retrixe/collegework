from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Interactive flight price prediction using saved best model"
    )
    parser.add_argument(
        "--model-path",
        type=Path,
        default=Path("outputs/flight_price/best_model_pipeline.joblib"),
        help="Path to saved sklearn pipeline (.joblib)",
    )
    parser.add_argument(
        "--round-result",
        action="store_true",
        help="Round predicted price to nearest integer",
    )
    return parser.parse_args()


def get_expected_columns(pipeline: object) -> tuple[list[str], list[str]]:
    preprocessor = pipeline.named_steps["preprocessor"]

    numeric_cols: list[str] = []
    categorical_cols: list[str] = []

    for name, _, columns in preprocessor.transformers_:
        if name == "num":
            numeric_cols = list(columns)
        elif name == "cat":
            categorical_cols = list(columns)

    if not numeric_cols and not categorical_cols:
        raise RuntimeError("Could not infer model input columns from preprocessor.")

    return numeric_cols, categorical_cols


def prompt_numeric(column_name: str) -> float:
    while True:
        raw = input(f"Enter {column_name} (number): ").strip()
        try:
            return float(raw)
        except ValueError:
            print("Invalid number. Try again.")


def prompt_categorical(column_name: str) -> str:
    while True:
        raw = input(f"Enter {column_name} (text): ").strip()
        if raw:
            return raw
        print("Value cannot be empty. Try again.")


def collect_user_input(
    numeric_cols: list[str],
    categorical_cols: list[str],
) -> pd.DataFrame:
    row: dict[str, object] = {}

    print("\nProvide flight details for prediction.")

    for col in numeric_cols:
        value = prompt_numeric(col)
        if float(value).is_integer():
            row[col] = int(value)
        else:
            row[col] = value

    for col in categorical_cols:
        row[col] = prompt_categorical(col)

    all_cols = numeric_cols + categorical_cols
    return pd.DataFrame([[row[c] for c in all_cols]], columns=all_cols)


def main() -> None:
    args = parse_args()

    if not args.model_path.exists():
        raise FileNotFoundError(
            f"Model file not found at: {args.model_path}. "
            "Train the model first using flight_price_prediction.py"
        )

    pipeline = joblib.load(args.model_path)
    numeric_cols, categorical_cols = get_expected_columns(pipeline)

    print("Loaded model successfully.")
    print(f"Numeric fields: {numeric_cols}")
    print(f"Categorical fields: {categorical_cols}")

    input_df = collect_user_input(numeric_cols, categorical_cols)
    prediction = pipeline.predict(input_df)
    predicted_price = float(np.asarray(prediction)[0])

    if args.round_result:
        predicted_display = str(int(round(predicted_price)))
    else:
        predicted_display = f"{predicted_price:.2f}"

    print("\nPredicted flight price:", predicted_display)


if __name__ == "__main__":
    main()
