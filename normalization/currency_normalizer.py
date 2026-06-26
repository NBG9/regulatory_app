import pandas as pd

# Temporary FX rates (we can replace later)
FX_RATES = {
    "USD": 1.0,
    "EUR": 1.09,
    "GBP": 1.27
}


def normalize_currencies(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts all prices into USD and standardizes schema.
    """

    df = df.copy()

    # Ensure required columns exist
    required_cols = ["symbol", "quantity", "price", "currency"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Normalize numeric types (important for finance systems)
    df["quantity"] = df["quantity"].astype(float)
    df["price"] = df["price"].astype(float)

    # Convert to USD
    price_usd = []

    for _, row in df.iterrows():
        currency = row["currency"]

        if currency not in FX_RATES:
            raise ValueError(f"Unsupported currency: {currency}")

        fx = FX_RATES[currency]
        converted = row["price"] * fx
        price_usd.append(converted)

    df["price_usd"] = price_usd

    # Optional: keep original price for auditability
    df["original_price"] = df["price"]

    print(f"[NORMALIZED] rows={len(df)} currencies={df['currency'].unique().tolist()}")

    return df