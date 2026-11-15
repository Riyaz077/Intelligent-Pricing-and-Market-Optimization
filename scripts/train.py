from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.data import generate_data, validate_data
from src.model import train_model
path = Path("data/pricing_data.csv")
df = validate_data(__import__("pandas").read_csv(path)) if path.exists() else generate_data()
model, metrics = train_model(df)
print("Holdout metrics:", metrics)
