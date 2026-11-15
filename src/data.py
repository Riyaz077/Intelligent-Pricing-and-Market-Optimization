import numpy as np
import pandas as pd

def generate_data(n=3600, seed=42):
    rng = np.random.default_rng(seed)
    products = [f"SKU{i:04d}" for i in range(1, 61)]
    categories = ["Electronics", "Home", "Fashion", "Beauty", "Sports"]
    product_category = {p: rng.choice(categories) for p in products}
    base = {p: float(rng.uniform(12, 250)) for p in products}
    rows = []
    for i in range(n):
        p = rng.choice(products)
        price = max(2, base[p] * rng.uniform(.78, 1.25))
        comp = max(2, base[p] * rng.uniform(.75, 1.28))
        promo = int(rng.random() < .22)
        dow = int(rng.integers(0, 7))
        # Synthetic demand mechanism with noise and product-level variation.
        relative = price / max(comp, 1)
        demand = 32 * (base[p] / price) ** 0.8 * (1.18 if promo else 1) * (1.08 if dow in [5,6] else 1)
        demand *= np.exp(-0.35 * (relative - 1))
        units = max(0, int(rng.poisson(max(demand, .2))))
        rows.append((f"SALE{i:07d}", p, product_category[p], round(price,2),
                     round(comp,2), promo, dow, units))
    return pd.DataFrame(rows, columns=["record_id","product_id","category","our_price",
        "competitor_price","promotion","day_of_week","units_sold"])

REQUIRED = ["product_id","category","our_price","competitor_price","promotion","day_of_week","units_sold"]

def validate_data(df):
    missing = sorted(set(REQUIRED)-set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    out = df.copy()
    for c in ["our_price","competitor_price","promotion","day_of_week","units_sold"]:
        out[c] = pd.to_numeric(out[c], errors="coerce")
    out = out.dropna(subset=REQUIRED)
    out = out[(out.our_price > 0) & (out.competitor_price > 0) &
              out.day_of_week.between(0,6) & (out.units_sold >= 0)]
    return out.reset_index(drop=True)
