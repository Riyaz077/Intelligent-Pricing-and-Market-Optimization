import numpy as np
import pandas as pd
from src.model import predict_demand

def estimate_price_response(model, product_id, category, competitor_price,
                            min_price, max_price, promotion=0, day_of_week=2, points=25):
    if min_price <= 0 or max_price <= min_price:
        raise ValueError("Require 0 < min_price < max_price.")
    prices = np.linspace(min_price, max_price, points)
    rows = []
    for price in prices:
        demand = predict_demand(model, product_id, category, price, competitor_price,
                                promotion, day_of_week)
        rows.append({"price":float(price), "predicted_units":demand,
                     "estimated_revenue":float(price*demand)})
    return pd.DataFrame(rows)

def recommend_price(curve, objective="revenue"):
    col = "estimated_revenue" if objective == "revenue" else "estimated_profit_proxy"
    if col not in curve.columns:
        curve = curve.copy()
        # A simple contribution-margin proxy; not a full cost model.
        curve["estimated_profit_proxy"] = curve["estimated_revenue"] * 0.30
        col = "estimated_profit_proxy"
    best = curve.loc[curve[col].idxmax()]
    return {"recommended_price":float(best.price),
            "predicted_units":float(best.predicted_units),
            "estimated_revenue":float(best.estimated_revenue),
            "objective":objective}

def competitor_position(price, competitor_price):
    ratio = float(price) / max(float(competitor_price), 1e-9)
    if ratio < .97: return "Below competitor"
    if ratio > 1.03: return "Above competitor"
    return "Price aligned"
