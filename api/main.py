from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from src.data import generate_data
from src.model import train_model
from src.pricing import estimate_price_response, recommend_price

app = FastAPI(title="PriceSense AI API", version="1.0.0")
class PriceRequest(BaseModel):
    product_id: str
    category: str
    competitor_price: float = Field(gt=0)
    min_price: float = Field(gt=0)
    max_price: float = Field(gt=0)
    promotion: bool = False
    day_of_week: int = Field(default=2, ge=0, le=6)

@app.get("/health")
def health():
    return {"status":"ok","project":"PriceSense AI"}

@app.post("/recommend")
def recommend(req: PriceRequest):
    if req.max_price <= req.min_price:
        raise HTTPException(status_code=400, detail="max_price must exceed min_price")
    try:
        model, metrics = train_model(generate_data(2200, seed=17),
            artifact_dir="/tmp/pricesense_artifacts", report_dir="/tmp/pricesense_reports")
        curve = estimate_price_response(model, req.product_id, req.category,
            req.competitor_price, req.min_price, req.max_price,
            int(req.promotion), req.day_of_week)
        return {"recommendation":recommend_price(curve), "model_metrics":metrics,
                "note":"Synthetic-data demo recommendation."}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
