import pandas as pd


def validate_dataset(df: pd.DataFrame, nav_result: dict) -> dict:
    """
    Runs validation rules on normalized dataset + computed NAV.
    Returns structured validation report.
    """

    errors = []
    warnings = []

    # -------------------------
    # Rule 1: Required columns
    # -------------------------
    required_cols = ["symbol", "quantity", "price_usd"]
    for col in required_cols:
        if col not in df.columns:
            errors.append({
                "rule": "REQUIRED_COLUMN_MISSING",
                "message": f"Missing required column: {col}"
            })

    # -------------------------
    # Rule 2: Position type validation (SHORT aware)
    # -------------------------
    if "quantity" in df.columns:
        df["position_type"] = df["quantity"].apply(
            lambda x: "SHORT" if x < 0 else "LONG"
        )

        short_count = (df["position_type"] == "SHORT").sum()

        if short_count > 0:
            warnings.append({
                "rule": "SHORT_POSITION_DETECTED",
                "message": f"{short_count} SHORT positions found"
            })

    # -------------------------
    # Rule 3: No missing prices
    # -------------------------
    if "price_usd" in df.columns:
        if (df["price_usd"] <= 0).any():
            errors.append({
                "rule": "INVALID_PRICE",
                "message": "Price must be greater than 0"
        })
        if df["price_usd"].isnull().any():
            errors.append({
                "rule": "MISSING_PRICE",
                "message": "Null values found in price_usd"
            })

    # -------------------------
    # Rule 4: NAV sanity check
    # -------------------------
    if "price_usd" in df.columns and "quantity" in df.columns:
        computed_nav = (df["price_usd"] * df["quantity"]).sum()

        reported_nav = nav_result.get("nav", None)

        if reported_nav is not None:
            diff = abs(computed_nav - reported_nav)

            if diff > 0.01:  # tolerance
                errors.append({
                    "rule": "NAV_MISMATCH",
                    "message": f"NAV mismatch detected (diff={diff})"
                })

    # -------------------------
    # Final result
    # -------------------------
    status = "FAILED" if len(errors) > 0 else "PASSED"

    result = {
        "status": status,
        "errors": errors,
        "warnings": warnings
    }

    print(f"[VALIDATION] status={status} errors={len(errors)}")

    return result