# API Usage

Run `uvicorn api.main:app --reload`.

- `GET /health` — health check.
- `POST /recommend` — train a demo demand model and evaluate candidate prices.

Example request:
```json
{
  "product_id": "SKU0001",
  "category": "Home",
  "competitor_price": 49.99,
  "min_price": 35,
  "max_price": 65,
  "promotion": false,
  "day_of_week": 2
}
```
Interactive documentation: `/docs`.
