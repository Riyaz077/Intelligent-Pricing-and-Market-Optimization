from src.data import generate_data, validate_data
from src.pricing import competitor_position, recommend_price
import pandas as pd

def test_generated_data():
    df = validate_data(generate_data(150, 5))
    assert len(df) == 150
    assert (df.our_price > 0).all()

def test_competitor_position():
    assert competitor_position(90,100) == "Below competitor"
    assert competitor_position(100,100) == "Price aligned"

def test_recommendation_selects_maximum():
    curve = pd.DataFrame({"price":[10,20,30],"predicted_units":[10,8,4],
                          "estimated_revenue":[100,160,120]})
    rec = recommend_price(curve)
    assert rec["recommended_price"] == 20
