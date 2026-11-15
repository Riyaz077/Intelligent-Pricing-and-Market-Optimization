from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import streamlit as st
import pandas as pd
import plotly.express as px
from src.data import generate_data, validate_data
from src.model import train_model
from src.pricing import estimate_price_response, recommend_price, competitor_position

st.set_page_config(page_title="PriceSense AI", page_icon="💹", layout="wide")
st.title("💹 PriceSense AI")
st.caption("Dynamic Pricing and Competitor Intelligence | Synthetic-data demo")
upload = st.sidebar.file_uploader("Upload pricing CSV", type=["csv"])
if upload:
    df = validate_data(pd.read_csv(upload))
else:
    path = Path(__file__).resolve().parents[1]/"data"/"pricing_data.csv"
    df = validate_data(pd.read_csv(path)) if path.exists() else generate_data()
a,b,c = st.columns(3)
a.metric("Pricing records", f"{len(df):,}")
b.metric("Products", f"{df.product_id.nunique():,}")
c.metric("Average selling price", f"{df.our_price.mean():.2f}")
l,r = st.columns(2)
with l:
    st.subheader("Price vs demand")
    st.plotly_chart(px.scatter(df, x="our_price", y="units_sold", color="category",
                               hover_data=["product_id","competitor_price"]), use_container_width=True)
with r:
    st.subheader("Competitor price positioning")
    pos = df.assign(position=[competitor_position(x,y) for x,y in zip(df.our_price,df.competitor_price)])
    st.plotly_chart(px.histogram(pos, x="position", color="category"), use_container_width=True)
st.subheader("Product pricing simulator")
product = st.selectbox("Product", sorted(df.product_id.unique()))
sample = df[df.product_id == product].iloc[0]
minp,maxp = st.slider("Allowed price range", 1.0, max(300.0,float(sample.our_price)*2), 
                      (max(1.0,float(sample.our_price)*.75), float(sample.our_price)*1.25))
comp = st.number_input("Competitor price", min_value=1.0, value=float(sample.competitor_price))
promo = st.checkbox("Promotion active")
if st.button("Generate price recommendation", type="primary"):
    with st.spinner("Training demand model and evaluating price range..."):
        model, metrics = train_model(df)
        curve = estimate_price_response(model, product, str(sample.category), comp,
                                        minp, maxp, int(promo))
        rec = recommend_price(curve)
    st.metric("Suggested price (revenue objective)", f"{rec['recommended_price']:.2f}")
    st.write(f"Predicted units: {rec['predicted_units']:.1f} | Estimated revenue: {rec['estimated_revenue']:.2f}")
    st.plotly_chart(px.line(curve, x="price", y="estimated_revenue", markers=True,
                            title="Modelled revenue across allowed prices"), use_container_width=True)
    st.caption(f"Holdout model metrics: MAE {metrics['mae']:.2f} | RMSE {metrics['rmse']:.2f} | R² {metrics['r2']:.3f}")
st.dataframe(df.head(100), use_container_width=True)
st.info("Synthetic data and simplified price-response estimates. Recommendations are illustrative, not guaranteed optimal prices.")
