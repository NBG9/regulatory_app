import numpy as np
import pandas as pd


def compute_risk_metrics(df: pd.DataFrame, nav: float) -> dict:
    df = df.copy()

    # -------------------------
    # Ensure required columns exist
    # -------------------------
    if "gross_exposure" not in df.columns:
        df["gross_exposure"] = abs(df["quantity"]) * df["price_usd"]

    if "position_value" not in df.columns:
        df["position_value"] = df["quantity"] * df["price_usd"]

    # -------------------------
    # Exposure calculations
    # -------------------------
    df["weight"] = df["gross_exposure"] / df["gross_exposure"].sum()

    top_concentration = df["weight"].max()

    long_exposure = df[df["position_type"] == "LONG"]["position_value"].sum()
    short_exposure = abs(df[df["position_type"] == "SHORT"]["position_value"].sum())

    return {
        "nav": nav,
        "gross_exposure": float(long_exposure + short_exposure),
        "net_exposure": float(long_exposure - short_exposure),
        "long_exposure": float(long_exposure),
        "short_exposure": float(short_exposure),
        "concentration_risk": {
            "top_single_asset_weight": float(top_concentration)
        }
    }