"""Streamlit dashboard for flight price predictions."""

# pyright: reportMissingImports=false

from __future__ import annotations

from pathlib import Path
from typing import Any, cast

import joblib  # type: ignore[import-untyped]
import numpy as np
import pandas as pd  # type: ignore[import-untyped]
import pydeck as pdk  # type: ignore[import-untyped]
import streamlit as st


MODEL_PATH = Path("outputs/flight_price/best_model_pipeline.joblib")
METRICS_PATH = Path("outputs/flight_price/model_comparison.csv")
BEST_MODEL_NAME_PATH = Path("outputs/flight_price/best_model.txt")
DATASET_PATH = Path("datasets/miniproject/Clean_Dataset.csv")

CITY_COORDS: dict[str, tuple[float, float]] = {
    "Bangalore": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707),
    "Delhi": (28.6139, 77.2090),
    "Hyderabad": (17.3850, 78.4867),
    "Kolkata": (22.5726, 88.3639),
    "Mumbai": (19.0760, 72.8777),
}

MONTH_COLUMNS = ["month", "journey_month", "travel_month"]
DATE_COLUMNS = ["date", "journey_date", "flight_date"]


@st.cache_data
def load_dataset(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    unnamed = [c for c in df.columns if c.lower().startswith("unnamed")]
    if unnamed:
        df = df.drop(columns=unnamed)
    return df


@st.cache_data
def load_metrics(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


@st.cache_data
def estimate_model_rmse(path: Path) -> float | None:
    if not path.exists():
        return None
    metrics = pd.read_csv(path)
    if "test_rmse" not in metrics.columns or len(metrics) == 0:
        return None
    return float(metrics.iloc[0]["test_rmse"])


@st.cache_resource
def load_model(path: Path) -> Any:
    return joblib.load(path)


def get_expected_columns(pipeline: Any) -> tuple[list[str], list[str]]:
    preprocessor = pipeline.named_steps["preprocessor"]
    numeric_cols: list[str] = []
    categorical_cols: list[str] = []

    for name, _, cols in preprocessor.transformers_:
        if name == "num":
            numeric_cols = list(cols)
        elif name == "cat":
            categorical_cols = list(cols)

    if not (numeric_cols or categorical_cols):
        raise RuntimeError("Unable to infer model input columns.")

    return numeric_cols, categorical_cols


def get_default_from_mode(series: pd.Series, fallback: object) -> object:
    mode = series.mode(dropna=True)
    if len(mode) == 0:
        return fallback
    return mode.iloc[0]


def infer_defaults_from_flight(
    df: pd.DataFrame,
    flight_code: str,
) -> dict[str, object]:
    if "flight" not in df.columns:
        return {}

    flight_rows = df[df["flight"].astype(str) == str(flight_code)]
    if len(flight_rows) == 0:
        return {}

    inferred: dict[str, object] = {}
    for col in flight_rows.columns:
        if col == "price":
            continue

        col_data = flight_rows[col].dropna()
        if len(col_data) == 0:
            continue

        if pd.api.types.is_numeric_dtype(flight_rows[col]):
            inferred[col] = float(pd.to_numeric(col_data).median())
        else:
            mode = col_data.astype(str).mode(dropna=True)
            if len(mode):
                inferred[col] = str(mode.iloc[0])

    return inferred


def create_input_row(
    numeric_cols: list[str],
    categorical_cols: list[str],
    df: pd.DataFrame,
) -> pd.DataFrame:
    with st.sidebar:
        st.header("Flight Inputs")

        values: dict[str, object] = {}

        quick_fields = {
            "flight",
            "source_city",
            "destination_city",
            "class",
            "days_left",
        }
        input_mode = st.radio(
            "Input mode",
            ["Quick", "Detailed"],
            horizontal=True,
            help="Quick mode hides advanced fields and auto-fills them.",
        )

        inferred_defaults: dict[str, object] = {}
        auto_fill_enabled = False
        flight_available = (
            "flight" in categorical_cols and "flight" in df.columns
        )

        if flight_available:
            flight_options = sorted(
                df["flight"].dropna().astype(str).unique().tolist()
            )
            default_flight = str(
                get_default_from_mode(
                    df["flight"].astype(str),
                    flight_options[0],
                )
            )
            default_flight_index = (
                flight_options.index(default_flight)
                if default_flight in flight_options
                else 0
            )
            values["flight"] = st.selectbox(
                "flight",
                options=flight_options,
                index=default_flight_index,
            )
            auto_fill_enabled = st.toggle(
                "Auto-fill from selected flight code",
                value=True,
                help=(
                    "Populate source/destination/departure/arrival and "
                    "other fields using historical rows for this flight code."
                ),
            )
            if auto_fill_enabled:
                inferred_defaults = infer_defaults_from_flight(
                    df,
                    str(values["flight"]),
                )
                if inferred_defaults:
                    st.caption(
                        "Applied defaults from historical records "
                        "of this flight."
                    )

        hidden_count = 0

        for col in categorical_cols:
            if col in values:
                continue

            is_quick_visible = input_mode == "Detailed" or col in quick_fields

            if col in df.columns:
                options = sorted(
                    df[col].dropna().astype(str).unique().tolist()
                )
                fallback_default_cat = str(
                    get_default_from_mode(df[col].astype(str), options[0])
                )
                inferred_default = inferred_defaults.get(
                    col,
                    fallback_default_cat,
                )
                default = str(inferred_default)
                if default not in options:
                    default = fallback_default_cat
                default_index = (
                    options.index(default) if default in options else 0
                )
                if is_quick_visible:
                    values[col] = st.selectbox(
                        col,
                        options=options,
                        index=default_index,
                    )
                else:
                    values[col] = default
                    hidden_count += 1
            else:
                if is_quick_visible:
                    values[col] = st.text_input(col, value="")
                else:
                    values[col] = ""
                    hidden_count += 1

        for col in numeric_cols:
            is_quick_visible = input_mode == "Detailed" or col in quick_fields

            if col in df.columns:
                col_data = pd.to_numeric(df[col], errors="coerce").dropna()
                min_v = float(col_data.min()) if len(col_data) else 0.0
                max_v = float(col_data.max()) if len(col_data) else 100.0
                fallback_default_num = (
                    float(col_data.median()) if len(col_data) else min_v
                )
                inferred_value = inferred_defaults.get(
                    col,
                    fallback_default_num,
                )
                inferred_default = float(
                    pd.to_numeric(pd.Series([inferred_value]), errors="coerce")
                    .fillna(fallback_default_num)
                    .iloc[0]
                )
                default_v = min(max(inferred_default, min_v), max_v)

                if np.allclose(col_data % 1, 0):
                    if is_quick_visible:
                        values[col] = int(
                            st.number_input(
                                col,
                                min_value=int(min_v),
                                max_value=int(max_v),
                                value=int(default_v),
                                step=1,
                            )
                        )
                    else:
                        values[col] = int(default_v)
                        hidden_count += 1
                else:
                    if is_quick_visible:
                        values[col] = float(
                            st.number_input(
                                col,
                                min_value=min_v,
                                max_value=max_v,
                                value=default_v,
                                step=0.1,
                                format="%.2f",
                            )
                        )
                    else:
                        values[col] = float(default_v)
                        hidden_count += 1
            else:
                if is_quick_visible:
                    values[col] = float(
                        st.number_input(col, value=0.0, step=0.1)
                    )
                else:
                    values[col] = 0.0
                    hidden_count += 1

        if input_mode == "Quick" and hidden_count > 0:
            st.caption(
                f"Quick mode auto-filled {hidden_count} advanced fields. "
                "Switch to Detailed to edit everything."
            )

    all_cols = numeric_cols + categorical_cols
    return pd.DataFrame([[values[c] for c in all_cols]], columns=all_cols)


def add_price_band(
    predicted_price: float,
    df: pd.DataFrame,
) -> tuple[str, str]:
    route_match = df[
        (df["source_city"] == st.session_state.get("source_city", ""))
        & (
            df["destination_city"]
            == st.session_state.get("destination_city", "")
        )
    ]

    benchmark = (
        float(route_match["price"].median())
        if len(route_match) > 20
        else float(df["price"].median())
    )

    ratio = predicted_price / benchmark if benchmark > 0 else 1.0
    if ratio <= 0.9:
        return "Cheap", "green"
    if ratio <= 1.1:
        return "Fair", "orange"
    return "Expensive", "red"


def get_nearest_flights(
    input_df: pd.DataFrame,
    df: pd.DataFrame,
    top_k: int,
) -> pd.DataFrame:
    work_df = df.copy()
    selected = input_df.iloc[0]

    for col in ["source_city", "destination_city", "class"]:
        if col in input_df.columns and col in work_df.columns:
            work_df = work_df[work_df[col].astype(str) == str(selected[col])]

    if len(work_df) < top_k:
        work_df = df.copy()

    score = pd.Series(np.zeros(len(work_df)), index=work_df.index)

    numeric_keys = ["duration", "days_left", "stops"]
    for key in numeric_keys:
        if key in input_df.columns and key in work_df.columns:
            col_numeric = pd.to_numeric(work_df[key], errors="coerce")
            target = float(pd.to_numeric(pd.Series([selected[key]]))[0])
            spread = float(col_numeric.std()) if col_numeric.std() > 0 else 1.0
            score += ((col_numeric - target).abs() / spread).fillna(1.0)

    work_df = work_df.assign(similarity_score=score)
    return work_df.sort_values("similarity_score").head(top_k)


def render_confidence_range(
    predicted_price: float,
    input_df: pd.DataFrame,
    df: pd.DataFrame,
) -> None:
    mode = st.radio(
        "Confidence method",
        ["RMSE-based", "Empirical (nearest flights)"],
        horizontal=True,
        key="confidence_method",
    )
    st.caption(
        "RMSE-based is more stable when similar historical "
        "samples are sparse. Empirical is more realistic "
        "when many close matches exist for the selected "
        "route and conditions."
    )

    if mode == "Empirical (nearest flights)":
        nearest = get_nearest_flights(input_df, df, top_k=120)
        if "price" in nearest.columns and len(nearest) >= 20:
            prices = pd.to_numeric(nearest["price"], errors="coerce").dropna()
            q16, q84 = np.quantile(prices, [0.16, 0.84])
            q025, q975 = np.quantile(prices, [0.025, 0.975])
            st.markdown(
                "Estimated uncertainty (from nearest-flight quantiles)"
            )
            c1, c2, c3 = st.columns(3)
            c1.metric("Nearest samples", f"{len(prices)}")
            c2.metric("Approx 68% range", f"INR {q16:,.0f} - INR {q84:,.0f}")
            c3.metric(
                "Approx 95% range",
                f"INR {q025:,.0f} - INR {q975:,.0f}",
            )
            return
        st.info("Not enough similar historical flights; using RMSE fallback.")

    rmse = estimate_model_rmse(METRICS_PATH)
    if rmse is None:
        st.info(
            "Confidence range unavailable until model metrics are present."
        )
        return

    low_68 = max(0.0, predicted_price - rmse)
    high_68 = predicted_price + rmse
    low_95 = max(0.0, predicted_price - 1.96 * rmse)
    high_95 = predicted_price + 1.96 * rmse

    st.markdown("Estimated uncertainty (from validation RMSE)")
    c1, c2 = st.columns(2)
    c1.metric("Approx 68% range", f"INR {low_68:,.0f} - INR {high_68:,.0f}")
    c2.metric("Approx 95% range", f"INR {low_95:,.0f} - INR {high_95:,.0f}")


def render_nearest_flights_table(
    input_df: pd.DataFrame,
    df: pd.DataFrame,
    top_k: int = 8,
) -> None:
    st.markdown("Nearest historical flights")
    nearest = get_nearest_flights(input_df, df, top_k=top_k)

    display_cols = [
        c
        for c in [
            "airline",
            "source_city",
            "destination_city",
            "class",
            "stops",
            "duration",
            "days_left",
            "price",
            "similarity_score",
        ]
        if c in nearest.columns
    ]

    st.dataframe(
        nearest[display_cols].round(3),
        width="stretch",
        hide_index=True,
    )


def render_seasonality_view(df: pd.DataFrame) -> None:
    st.subheader("Seasonality")

    if "selected_input" not in st.session_state:
        st.info("Pick a flight in Predict tab to see route seasonality.")
        return

    selected: dict[str, Any] = st.session_state["selected_input"]
    work_df = df.copy()
    for col in ["source_city", "destination_city", "class"]:
        if col in work_df.columns and col in selected:
            work_df = work_df[work_df[col].astype(str) == str(selected[col])]

    if len(work_df) < 20:
        st.info("Not enough route history for seasonality; showing all data.")
        work_df = df.copy()

    month_col = next((c for c in MONTH_COLUMNS if c in work_df.columns), None)
    if month_col is not None:
        seasonal = (
            work_df.groupby(month_col, as_index=False)["price"]
            .median()
            .sort_values(month_col)
        )
        st.markdown("Median price by month")
        st.bar_chart(seasonal.set_index(month_col)["price"])
        return

    date_col = next((c for c in DATE_COLUMNS if c in work_df.columns), None)
    if date_col is not None:
        parsed = pd.to_datetime(work_df[date_col], errors="coerce")
        seasonal = work_df.loc[parsed.notna(), ["price"]].copy()
        seasonal["month"] = parsed[parsed.notna()].dt.month
        seasonal = (
            seasonal.groupby("month", as_index=False)["price"]
            .median()
            .sort_values("month")
        )
        if len(seasonal):
            st.markdown("Median price by month")
            st.bar_chart(seasonal.set_index("month")["price"])
            return

    st.info(
        "Monthly fields are not available in this dataset. "
        "Showing departure-time pattern instead."
    )
    if "departure_time" in work_df.columns:
        dep_curve = (
            work_df.groupby("departure_time", as_index=False)["price"]
            .median()
            .sort_values("price", ascending=False)
        )
        st.bar_chart(dep_curve.set_index("departure_time")["price"])


def render_selected_flight_chart(
    pipeline: Any,
    input_df: pd.DataFrame,
    df: pd.DataFrame,
) -> None:
    if "days_left" not in input_df.columns:
        st.info("No days_left feature found, skipping prediction trend chart.")
        return

    st.markdown("Prediction trend for this selected flight")

    days_min = int(pd.to_numeric(df["days_left"], errors="coerce").min())
    days_max = int(pd.to_numeric(df["days_left"], errors="coerce").max())
    day_points = list(range(days_min, days_max + 1))

    simulated = pd.concat([input_df] * len(day_points), ignore_index=True)
    simulated["days_left"] = day_points
    simulated_pred = cast(Any, pipeline).predict(simulated)

    chart_df = pd.DataFrame(
        {
            "days_left": day_points,
            "Predicted price": simulated_pred,
        }
    )

    if {
        "source_city",
        "destination_city",
        "class",
    }.issubset(input_df.columns):
        route_hist = df[
            (df["source_city"] == input_df.iloc[0]["source_city"])
            & (df["destination_city"] == input_df.iloc[0]["destination_city"])
            & (df["class"] == input_df.iloc[0]["class"])
        ]
        if len(route_hist) >= 30:
            hist_curve = (
                route_hist.groupby("days_left", as_index=False)["price"]
                .median()
                .rename(columns={"price": "Historical median"})
            )
            chart_df = chart_df.merge(hist_curve, on="days_left", how="left")

    st.line_chart(chart_df.set_index("days_left"), width="stretch")


def render_route_map(input_df: pd.DataFrame) -> None:
    required_cols = {"source_city", "destination_city"}
    if not required_cols.issubset(input_df.columns):
        st.info("Route map is unavailable for this model input schema.")
        return

    source_city = str(input_df.iloc[0]["source_city"])
    destination_city = str(input_df.iloc[0]["destination_city"])

    if source_city not in CITY_COORDS or destination_city not in CITY_COORDS:
        st.info("Missing coordinates for one or more selected cities.")
        return

    src_lat, src_lon = CITY_COORDS[source_city]
    dst_lat, dst_lon = CITY_COORDS[destination_city]

    st.markdown("Selected route map")

    city_points = pd.DataFrame(
        [
            {"city": source_city, "lat": src_lat, "lon": src_lon},
            {"city": destination_city, "lat": dst_lat, "lon": dst_lon},
        ]
    )
    path_data = [
        {
            "path": [[src_lon, src_lat], [dst_lon, dst_lat]],
            "name": f"{source_city} -> {destination_city}",
        }
    ]

    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=city_points,
        get_position="[lon, lat]",
        get_radius=25000,
        get_fill_color=[255, 99, 71, 180],
        pickable=True,
    )
    path_layer = pdk.Layer(
        "PathLayer",
        data=path_data,
        get_path="path",
        get_width=5000,
        get_color=[25, 102, 255],
        width_min_pixels=2,
    )

    view_state = pdk.ViewState(
        latitude=(src_lat + dst_lat) / 2,
        longitude=(src_lon + dst_lon) / 2,
        zoom=4.4,
        pitch=0,
    )

    st.pydeck_chart(
        pdk.Deck(
            map_style=(
                "https://basemaps.cartocdn.com/gl/positron-gl-style/"
                "style.json"
            ),
            initial_view_state=view_state,
            layers=[path_layer, scatter_layer],
            tooltip={"text": "{name}"},
        ),
        width="stretch",
    )


def render_prediction_section(pipeline: Any, df: pd.DataFrame) -> None:
    st.subheader("Prediction Console")

    numeric_cols, categorical_cols = get_expected_columns(pipeline)
    input_df = create_input_row(numeric_cols, categorical_cols, df)

    for col in ["source_city", "destination_city"]:
        if col in input_df.columns:
            st.session_state[col] = input_df.iloc[0][col]

    predicted_price = float(cast(Any, pipeline).predict(input_df)[0])
    label, color = add_price_band(predicted_price, df)

    c1, c2 = st.columns(2)
    c1.metric("Predicted Price", f"INR {predicted_price:,.0f}")
    c2.markdown(
        (
            f"**Fare Signal:** <span style='color:{color};"
            f"font-weight:700'>{label}</span>"
        ),
        unsafe_allow_html=True,
    )

    st.session_state["selected_input"] = input_df.iloc[0].to_dict()

    st.dataframe(input_df, width="stretch")
    render_confidence_range(predicted_price, input_df, df)
    render_selected_flight_chart(pipeline, input_df, df)
    render_route_map(input_df)
    render_nearest_flights_table(input_df, df)


def render_route_insights(df: pd.DataFrame) -> None:
    st.subheader("Route Insights")

    route_price = df.groupby(
        ["source_city", "destination_city"],
        as_index=False,
    )["price"].median().sort_values("price", ascending=False)
    route_price["route"] = (
        route_price["source_city"] + " -> " + route_price["destination_city"]
    )

    c1, c2 = st.columns(2)
    c1.markdown("Top expensive routes")
    c1.dataframe(
        route_price[["route", "price"]].head(10),
        width="stretch",
    )

    c2.markdown("Top cheapest routes")
    c2.dataframe(
        route_price[["route", "price"]].sort_values("price").head(10),
        width="stretch",
    )

    booking_curve = (
        df.groupby("days_left", as_index=False)["price"]
        .median()
        .sort_values("days_left")
    )
    st.markdown("Median price by booking window")
    st.line_chart(booking_curve.set_index("days_left")["price"])
    render_seasonality_view(df)


def render_model_performance() -> None:
    st.subheader("Model Performance")
    if not METRICS_PATH.exists():
        st.info("No model metrics found yet. Run training first.")
        return

    metrics = load_metrics(METRICS_PATH)
    st.dataframe(metrics.round(4), width="stretch")

    best_name = "Unknown"
    if BEST_MODEL_NAME_PATH.exists():
        best_name = BEST_MODEL_NAME_PATH.read_text(encoding="utf-8").strip()

    top = metrics.iloc[0]
    c1, c2, c3 = st.columns(3)
    c1.metric("Best Model", best_name)
    c2.metric("Best RMSE", f"{float(top['test_rmse']):,.2f}")
    c3.metric("Best R2", f"{float(top['test_r2']):.4f}")


def main() -> None:
    st.set_page_config(page_title="Flight Price Dashboard", layout="wide")
    st.title("Flight Price Intelligence Dashboard")

    if not MODEL_PATH.exists():
        st.error(
            "Model artifact not found. Run flight_price_prediction.py first "
            "to generate best_model_pipeline.joblib"
        )
        st.stop()

    if not DATASET_PATH.exists():
        st.error("Dataset not found at datasets/miniproject/Clean_Dataset.csv")
        st.stop()

    pipeline = load_model(MODEL_PATH)
    df = load_dataset(DATASET_PATH)

    tab_predict, tab_insights, tab_perf = st.tabs(
        ["Predict", "Route Insights", "Model Performance"]
    )

    with tab_predict:
        render_prediction_section(pipeline, df)

    with tab_insights:
        render_route_insights(df)

    with tab_perf:
        render_model_performance()


if __name__ == "__main__":
    main()
