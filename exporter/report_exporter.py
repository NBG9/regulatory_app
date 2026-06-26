import json
from datetime import datetime


def generate_report(df, nav_result, validation_result, lineage, risk_metrics):
    """
    Combines all pipeline outputs into a final regulatory report.
    """

    report = {
        "meta": {
            "generated_at": datetime.utcnow().isoformat(),
            "report_type": "AIFMD_LITE_SIMULATION",
            "version": "1.0"
        },

        "metrics": {
            "nav": nav_result.get("nav"),
            "currency": nav_result.get("currency", "USD")
        },

        "risk": risk_metrics,

        "validation": validation_result,

        "lineage": lineage,

        "positions": nav_result.get("breakdown", []),

        "dataset_summary": {
            "rows": len(df),
            "columns": list(df.columns)
        }
    }

    print("[EXPORTER] Report generated successfully")

    return report


def export_to_json(report, filename="regulatory_report.json"):
    """
    Saves the report to disk as a JSON file.
    """

    with open(filename, "w") as f:
        json.dump(report, f, indent=4)

    print(f"[EXPORTER] Saved to {filename}")