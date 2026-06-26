import pandas as pd
import json
import os
from typing import Union, List, Dict, Any


def load_dataset(data: Union[str, List[Dict[str, Any]]]):
    """
    Loads dataset from:
    - file path (CSV/JSON) OR
    - raw JSON list (from API)
    """

    # -------------------------
    # CASE 1: API input (list[dict])
    # -------------------------
    if isinstance(data, list):
        df = pd.DataFrame(data)

    # -------------------------
    # CASE 2: file path input (legacy support)
    # -------------------------
    elif isinstance(data, str):

        file_extension = data.split(".")[-1].lower()

        if file_extension == "csv":
            df = pd.read_csv(data)

        elif file_extension == "json":
            with open(data, "r") as f:
                raw = json.load(f)

            if isinstance(raw, list):
                df = pd.DataFrame(raw)
            else:
                df = pd.json_normalize(raw)

        else:
            raise ValueError("Unsupported file format. Use CSV or JSON.")

    else:
        raise TypeError("Unsupported input type for dataset")

    print(f"[DATA LOADED] rows={len(df)} cols={len(df.columns)}")
    return df