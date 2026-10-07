"""Minimal reproducible AI-search visibility aggregation.

Input observations must be manually or programmatically collected with evidence.
This script does not fabricate model responses.
"""
from pathlib import Path
import csv
from collections import defaultdict

INPUT = Path("data/ai-search/observations.csv")

def pct(n, d):
    return round(100*n/d, 1) if d else 0.0

def main():
    if not INPUT.exists():
        print("No observations.csv yet; collect evidence before scoring.")
        return
    rows = list(csv.DictReader(INPUT.open(encoding="utf-8")))
    by_brand = defaultdict(list)
    for row in rows:
        by_brand[row["brand"]].append(row)
    for brand, items in sorted(by_brand.items()):
        n=len(items)
        mentions=sum(r["mentioned"].lower()=="true" for r in items)
        citations=sum(r["cited"].lower()=="true" for r in items)
        recommended=sum(r["recommended"].lower()=="true" for r in items)
        print(f"{brand}: mention={pct(mentions,n)}% citation={pct(citations,n)}% recommendation={pct(recommended,n)}% n={n}")

if __name__ == "__main__":
    main()
