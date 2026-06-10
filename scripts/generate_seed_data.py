"""
Generate the raw seed CSVs for the coffee-shop pipeline.

Reproducible: a fixed random seed means re-running produces identical data,
so the committed CSVs and anyone who regenerates them always match.

Run from the repo root:
    python scripts/generate_seed_data.py
"""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)  # fixed seed -> deterministic output

SEEDS_DIR = Path(__file__).resolve().parent.parent / "data_pipeline" / "seeds"

# --- Products (the menu) -----------------------------------------------------
PRODUCTS = [
    ("Espresso", "coffee", 3.00),
    ("Americano", "coffee", 3.25),
    ("Latte", "coffee", 4.50),
    ("Cappuccino", "coffee", 4.25),
    ("Mocha", "coffee", 4.75),
    ("Cold Brew", "coffee", 4.75),
    ("Green Tea", "tea", 3.50),
    ("Earl Grey", "tea", 3.50),
    ("Chai Latte", "tea", 4.25),
    ("Matcha Latte", "tea", 4.95),
    ("Croissant", "pastry", 3.25),
    ("Blueberry Muffin", "pastry", 3.00),
    ("Bagel", "pastry", 2.75),
    ("Cinnamon Roll", "pastry", 3.75),
    ("Chocolate Chip Cookie", "pastry", 2.50),
]

FIRST_NAMES = [
    "Ava", "Liam", "Noah", "Emma", "Olivia", "William", "Sophia", "James",
    "Isabella", "Benjamin", "Mia", "Lucas", "Charlotte", "Henry", "Amelia",
    "Alexander", "Harper", "Daniel", "Evelyn", "Michael", "Abigail", "Ethan",
    "Emily", "Jacob", "Elizabeth", "Logan", "Sofia", "Jackson", "Ella", "Aiden",
]
LAST_NAMES = [
    "Martinez", "Chen", "Patel", "Johnson", "Brown", "Lee", "Garcia", "Wilson",
    "Nguyen", "Kim", "Davis", "Lopez", "Smith", "Jones", "Williams", "Rivera",
]
CITIES = ["Austin", "Dallas", "Houston", "San Antonio"]

NUM_CUSTOMERS = 50
NUM_ORDERS = 600
START_DATE = date(2024, 1, 1)
END_DATE = date(2024, 6, 30)


def daterange_pick():
    """A random date in the window, lightly weighted toward weekends."""
    span = (END_DATE - START_DATE).days
    d = START_DATE + timedelta(days=random.randint(0, span))
    # 30% chance to nudge onto the nearest weekend -> busier Sat/Sun
    if random.random() < 0.30 and d.weekday() < 5:
        d += timedelta(days=(5 - d.weekday()))
    return d


def write_csv(name, header, rows):
    path = SEEDS_DIR / name
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"wrote {len(rows):>4} rows -> {path.relative_to(SEEDS_DIR.parent.parent)}")


def main():
    # Customers
    customers = []
    for cid in range(1, NUM_CUSTOMERS + 1):
        name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        signup = START_DATE - timedelta(days=random.randint(0, 365))
        customers.append((cid, name, signup.isoformat(), random.choice(CITIES)))
    write_csv("raw_customers.csv",
              ["customer_id", "customer_name", "signup_date", "city"], customers)

    # Products
    products = [(101 + i, n, c, f"{p:.2f}") for i, (n, c, p) in enumerate(PRODUCTS)]
    write_csv("raw_products.csv",
              ["product_id", "product_name", "category", "price"], products)

    # Orders. Grain = one row per LINE ITEM. A single ticket (order_id) can have
    # several lines, each numbered 1..N -> (order_id, line_number) is unique.
    orders = []
    order_id = 1001
    while len(orders) < NUM_ORDERS:
        cust = random.randint(1, NUM_CUSTOMERS)
        d = daterange_pick().isoformat()
        items_on_ticket = random.choices([1, 2, 3], weights=[60, 30, 10])[0]
        line_number = 0
        for _ in range(items_on_ticket):
            if len(orders) >= NUM_ORDERS:
                break
            line_number += 1
            prod = 101 + random.randint(0, len(PRODUCTS) - 1)
            qty = random.choices([1, 2, 3], weights=[80, 15, 5])[0]
            orders.append((order_id, line_number, cust, prod, d, qty))
        order_id += 1
    write_csv("raw_orders.csv",
              ["order_id", "line_number", "customer_id", "product_id", "order_date", "quantity"],
              orders)


if __name__ == "__main__":
    main()
