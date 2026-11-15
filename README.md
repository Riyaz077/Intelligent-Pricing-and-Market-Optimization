# PriceSense AI
## Dynamic Pricing and Competitor Intelligence Platform

PriceSense AI is a portfolio-ready pricing analytics prototype that combines demand modelling, price-response analysis and competitor benchmarking to recommend prices under configurable business constraints.

### Features
- Synthetic product, sales and competitor-price dataset.
- Demand prediction using Random Forest regression.
- Price elasticity estimates from historical-like observations.
- Constrained price recommendations with configurable minimum/maximum prices.
- Competitor price positioning and product-level comparison.
- Streamlit dashboard and FastAPI endpoints.
- Evaluation metrics, tests, notebook and documentation.

### Quick start
Python 3.10+ recommended.

```bash
pip install -r requirements.txt
python scripts/generate_data.py
python scripts/train.py
streamlit run app/streamlit_app.py
```

Run the API:
```bash
uvicorn api.main:app --reload
```

### Input data
CSV columns: `product_id`, `category`, `our_price`, `competitor_price`, `promotion`, `day_of_week`, `units_sold`.

### Project structure
```text
PriceSenseAI/
├── api/              # FastAPI service
├── app/              # Streamlit dashboard
├── data/             # Synthetic sample data
├── docs/             # Data dictionary and model notes
├── notebooks/        # Exploratory walkthrough
├── scripts/          # Data generation and model training
├── src/              # Features, modelling and pricing engine
├── tests/            # Unit tests
├── requirements.txt
└── README.md
```

### Limitations
This is an educational decision-support prototype. Included data is synthetic, competitor prices are simulated rather than collected from live retailers, and price recommendations rely on simplified observational relationships. The project does not guarantee revenue or profit improvements and should not be deployed for production pricing without real data, causal validation, legal review and human oversight.
