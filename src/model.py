import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
from pathlib import Path

FEATURES = ["product_id","category","our_price","competitor_price","promotion","day_of_week"]
CAT = ["product_id","category"]
NUM = ["our_price","competitor_price","promotion","day_of_week"]

def build_pipeline():
    prep = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), CAT),
        ("num", StandardScaler(), NUM)
    ])
    return Pipeline([("prep", prep), ("model", RandomForestRegressor(
        n_estimators=180, max_depth=14, min_samples_leaf=2, random_state=42, n_jobs=-1))])

def train_model(df, artifact_dir="artifacts", report_dir="reports"):
    X, y = df[FEATURES], df["units_sold"]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=.22, random_state=42)
    model = build_pipeline()
    model.fit(Xtr, ytr)
    pred = np.maximum(model.predict(Xte), 0)
    metrics = {"mae": float(mean_absolute_error(yte,pred)),
               "rmse": float(np.sqrt(mean_squared_error(yte,pred))),
               "r2": float(r2_score(yte,pred))}
    Path(artifact_dir).mkdir(parents=True, exist_ok=True)
    Path(report_dir).mkdir(parents=True, exist_ok=True)
    joblib.dump(model, Path(artifact_dir)/"demand_model.joblib")
    import json
    (Path(report_dir)/"metrics.json").write_text(json.dumps(metrics, indent=2))
    return model, metrics

def predict_demand(model, product_id, category, price, competitor_price, promotion=0, day_of_week=2):
    import pandas as pd
    row = pd.DataFrame([{"product_id":product_id, "category":category,
        "our_price":float(price), "competitor_price":float(competitor_price),
        "promotion":int(promotion), "day_of_week":int(day_of_week)}])
    return max(0.0, float(model.predict(row)[0]))
