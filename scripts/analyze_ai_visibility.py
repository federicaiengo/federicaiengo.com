"""Reproducible aggregation for the AI Search Competitive Intelligence study.

The script only scores collected evidence. It never generates or imputes observations.
"""
from pathlib import Path
import csv
from collections import defaultdict

INPUT = Path("data/ai-search/observations.csv")

def yes(row, key):
    return row.get(key, "").strip().lower() == "true"

def pct(n, d):
    return round(100 * n / d, 1) if d else 0.0

def main():
    if not INPUT.exists():
        print("No observations.csv yet; collect evidence before scoring.")
        return
    rows = list(csv.DictReader(INPUT.open(encoding="utf-8")))
    if not rows:
        print("No observations available.")
        return
    by_brand = defaultdict(list)
    by_brand_family = defaultdict(list)
    for row in rows:
        by_brand[row["brand"]].append(row)
        by_brand_family[(row["brand"], row["prompt_family"])].append(row)

    print("OVERALL")
    for brand, items in sorted(by_brand.items()):
        n = len(items)
        rec_items = [r for r in items if r["prompt_family"] == "recommendation"]
        positions = [int(r["position"]) for r in items if r.get("position", "").isdigit()]
        mean_position = round(sum(positions)/len(positions), 2) if positions else "n/a"
        print(f"{brand}: mention={pct(sum(yes(r,'mentioned') for r in items),n)}% "
              f"citation={pct(sum(yes(r,'cited') for r in items),n)}% "
              f"recommendation={pct(sum(yes(r,'recommended') for r in rec_items),len(rec_items))}% "
              f"ordered_mean_position={mean_position} n={n}")

    print("\nBY INTENT FAMILY")
    for (brand, family), items in sorted(by_brand_family.items()):
        print(f"{brand} | {family}: mention={pct(sum(yes(r,'mentioned') for r in items),len(items))}% "
              f"citation={pct(sum(yes(r,'cited') for r in items),len(items))}% n={len(items)}")

if __name__ == "__main__":
    main()
