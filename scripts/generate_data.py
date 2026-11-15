from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.data import generate_data
out = Path(__file__).resolve().parents[1]/"data"/"pricing_data.csv"
generate_data().to_csv(out, index=False)
print(f"Saved {out}")
