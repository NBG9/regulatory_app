import pandas as pd
import numpy as np


def build_lineage(df: pd.DataFrame, nav_result: dict) -> dict:
    """
    Builds explainability / audit trail for NAV computation,
    including LONG/SHORT classification.
    """

    df = df.copy()

    # -------------------------
    # Ensure position value exists
    # -------------------------
    if "position_value" not in df.columns:
        df["position_value"] = df["quantity"] * df["price_usd"]        # NAV impact (signed)
        df["gross_exposure"] = abs(df["quantity"]) * df["price_usd"]   # risk view (unsigned)

    # -------------------------
    # Classify positions (IMPORTANT ADDITION)
    # -------------------------
    df["position_type"] = np.where(df["quantity"] < 0, "SHORT", "LONG")

    total_nav = nav_result.get("nav", 0)

    # -------------------------
    # Asset-level lineage
    # -------------------------
    asset_breakdown = []

    for _, row in df.iterrows():

        asset_lineage = {
            "symbol": row["symbol"],
            "position_type": row["position_type"],
            "computation": {
                "formula": "quantity * price_usd",
                "quantity": float(row["quantity"]),
                "price_usd": float(row["price_usd"]),
                "position_value": float(row["position_value"]),
                "gross_exposure": float(row["gross_exposure"]),
            }
        }

        # FX annotation
        if "currency" in row and row["currency"] != "USD":
            asset_lineage["computation"]["note"] = "includes FX conversion to USD"

        # Add semantic explanation for shorts
        if row["position_type"] == "SHORT":
            asset_lineage["computation"]["interpretation"] = (
                "Short position (negative exposure contributes negatively to NAV)"
            )
        else:
            asset_lineage["computation"]["interpretation"] = (
                "Long position (positive exposure contributes positively to NAV)"
            )

        asset_breakdown.append(asset_lineage)

    # -------------------------
    # NAV-level lineage
    # -------------------------
    nav_lineage = {
        "formula": "sum(position_values)",
        "final_nav": float(total_nav),
        "components": [
            {
                "symbol": row["symbol"],
                "type": row["position_type"],
                "value": float(row["position_value"])
            }
            for _, row in df.iterrows()
        ],
        "interpretation": {
            "note": "NAV includes both long and short exposures",
            "rule": "Short positions reduce NAV; long positions increase NAV"
        }
    }

    result = {
        "nav_lineage": nav_lineage,
        "asset_lineage": asset_breakdown
    }

    print("[LINEAGE] built successfully (short-aware)")

    return result