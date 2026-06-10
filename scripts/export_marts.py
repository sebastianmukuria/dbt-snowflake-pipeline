"""
Export the dbt marts from Snowflake to CSV for the Evidence dashboard.

Evidence reads these CSVs (via its csv connector), so the dashboard is fully
self-contained and keeps building even after the Snowflake trial expires.

Run from the repo root:
    python scripts/export_marts.py
"""
import csv
import json
import subprocess
from pathlib import Path

MARTS = ["daily_sales", "fct_orders", "dim_customers"]
OUT_DIR = Path(__file__).resolve().parent.parent / "reports" / "sources" / "coffee_shop"
DBT_DIR = Path(__file__).resolve().parent.parent / "data_pipeline"


def fetch(model: str) -> list[dict]:
    """Run `dbt show` for a model and return its rows as a list of dicts."""
    cmd = [
        "dbt", "--quiet", "show",
        "--inline", f"select * from {{{{ ref('{model}') }}}}",
        "--output", "json", "--limit", "100000",
    ]
    raw = subprocess.run(cmd, cwd=DBT_DIR, capture_output=True, text=True, check=True).stdout
    payload = json.loads(raw)
    # dbt returns {"<node>": [ {row}, ... ]}; grab the first list value.
    rows = next(v for v in payload.values() if isinstance(v, list))
    return rows


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for model in MARTS:
        rows = fetch(model)
        path = OUT_DIR / f"{model}.csv"
        with path.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=[c.lower() for c in rows[0].keys()])
            writer.writeheader()
            for r in rows:
                writer.writerow({k.lower(): v for k, v in r.items()})
        print(f"wrote {len(rows):>4} rows -> {path.relative_to(OUT_DIR.parent.parent.parent)}")


if __name__ == "__main__":
    main()
