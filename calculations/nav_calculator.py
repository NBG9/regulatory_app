import pandas as pd
import numpy as np


def calculate_nav(df: pd.DataFrame) -> dict:
    """
    Calculates NAV from normalized dataset (USD only).
    Returns NAV + breakdown with auditability.
    """

    df = df.copy()

    # Validations
    if "price_usd" not in df.columns:
        raise ValueError("price_usd column missing. Run normalization first.")

    if "quantity" not in df.columns:
        raise ValueError("quantity column missing.")

    # -----------------------------
    # Position classification
    # -----------------------------
    df["position_type"] = np.where(df["quantity"] < 0, "SHORT", "LONG")

    df["notes"] = np.where(
        df["quantity"] < 0,
        "SHORT POSITION",
        "LONG POSITION"
    )

    # -----------------------------
    # Position value (IMPORTANT FIX)
    # -----------------------------
    df["position_value"] = df["quantity"] * df["price_usd"]        # NAV impact (signed)
    df["gross_exposure"] = abs(df["quantity"]) * df["price_usd"]   # risk view (unsigned)

    # NAV (IMPORTANT: do NOT flip sign for shorts in accounting view)
    nav = df["position_value"].sum()

    # -----------------------------
    # Breakdown for auditability
    # -----------------------------
    breakdown = df[[
        "symbol",
        "quantity",
        "price_usd",
        "position_type",
        "position_value",
        "gross_exposure",
        "notes"
    ]].to_dict(orient="records")

    result = {
        "nav": nav,
        "currency": "USD",
        "breakdown": breakdown
    }

    print(f"[NAV CALCULATED] NAV = {nav}")

    return result