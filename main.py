from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any

from ingestion.parser import load_dataset
from normalization.currency_normalizer import normalize_currencies
from calculations.nav_calculator import calculate_nav
from validation.rule_engine import validate_dataset
from lineage.tracker import build_lineage
from exporter.report_exporter import generate_report
from risk.risk_engine import compute_risk_metrics
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PipelineRequest(BaseModel):
    dataset: list[dict[str, Any]]


@app.get("/")
def root():
    return {"message": "Backend is running"}


@app.post("/run-pipeline")
def run_pipeline(req: PipelineRequest):

    df = load_dataset(req.dataset)

    df = normalize_currencies(df)
    nav_result = calculate_nav(df)
    validation_result = validate_dataset(df, nav_result)
    lineage = build_lineage(df, nav_result)

    risk_metrics = compute_risk_metrics(df, nav_result["nav"])

    report = generate_report(
        df,
        nav_result,
        validation_result,
        lineage,
        risk_metrics
    )

    return report