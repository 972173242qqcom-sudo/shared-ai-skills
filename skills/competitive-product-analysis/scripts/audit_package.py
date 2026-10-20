#!/usr/bin/env python3
"""Audit competitor, source, and image coverage before analysis."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path


ALIASES = {
    "id": ("competitor_id", "id", "序号"),
    "brand": ("brand", "品牌"),
    "product": ("product", "offering_name", "solution", "service", "产品", "方案名称", "服务名称", "name", "名称"),
    "status": ("market_status", "status", "市场状态"),
    "price": ("reference_price", "price", "参考价格"),
    "source": ("primary_source", "source_url", "官方/主来源", "来源"),
    "asset_id": ("competitor_id", "id"),
    "asset_product": ("product", "产品", "name"),
    "asset_file": ("file", "path", "文件"),
    "asset_source": ("source_url", "source_page", "来源"),
    "asset_decision": ("decision", "状态"),
}


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def find_column(rows, names):
    if not rows:
        return None
    keys = set(rows[0])
    return next((name for name in names if name in keys), None)


def normalize(value):
    return re.sub(r"[^0-9a-z\u4e00-\u9fff]+", "", (value or "").casefold())


def asset_matches(comp, asset, fields):
    cid = comp.get(fields["id"], "") if fields["id"] else ""
    aid = asset.get(fields["asset_id"], "") if fields["asset_id"] else ""
    if fields["id"] == "competitor_id" and cid and aid and normalize(cid) == normalize(aid):
        return True

    product = normalize(comp.get(fields["product"], ""))
    brand = comp.get(fields["brand"], "") if fields["brand"] else ""
    brand_product = normalize(brand + comp.get(fields["product"], ""))
    asset_product = normalize(asset.get(fields["asset_product"], "")) if fields["asset_product"] else ""
    if not product or not asset_product:
        return False
    if product in asset_product or asset_product in product or brand_product in asset_product or asset_product in brand_product:
        return True
    similarity = max(
        SequenceMatcher(None, product, asset_product).ratio(),
        SequenceMatcher(None, brand_product, asset_product).ratio(),
    )
    # Without stable IDs, prefer false negatives over assigning the wrong image.
    return similarity >= 0.84


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("competitors", type=Path, help="Competitor CSV")
    parser.add_argument("--assets", type=Path, help="Asset manifest CSV")
    parser.add_argument("--json", type=Path, dest="json_out", help="Optional JSON report")
    parser.add_argument(
        "--require",
        default="status,price,source",
        help="Comma-separated required field groups: status, price, source (default: status,price,source)",
    )
    args = parser.parse_args()

    competitors = read_csv(args.competitors)
    assets = read_csv(args.assets) if args.assets else []
    fields = {}
    for key, names in ALIASES.items():
        fields[key] = find_column(assets if key.startswith("asset_") else competitors, names)
    if not fields["product"]:
        print("ERROR: competitor product/name column not found", file=sys.stderr)
        return 2

    selected_assets = []
    rejected = {"rejected", "discarded", "skip", "skipped"}
    for asset in assets:
        decision = asset.get(fields["asset_decision"], "") if fields["asset_decision"] else ""
        if normalize(decision) not in rejected:
            selected_assets.append(asset)

    missing_images = []
    missing_fields = []
    labels = []
    required_groups = [item.strip() for item in args.require.split(",") if item.strip()]
    unknown_groups = sorted(set(required_groups) - {"status", "price", "source"})
    if unknown_groups:
        print(f"ERROR: unknown --require groups: {', '.join(unknown_groups)}", file=sys.stderr)
        return 2

    for comp in competitors:
        brand = comp.get(fields["brand"], "") if fields["brand"] else ""
        label = " ".join(x for x in (brand, comp.get(fields["product"], "")) if x).strip()
        labels.append(label)
        if assets and not any(asset_matches(comp, asset, fields) for asset in selected_assets):
            missing_images.append(label)
        absent = []
        for key in required_groups:
            field = fields[key]
            if not field or not comp.get(field, "").strip():
                absent.append(key)
        if absent:
            missing_fields.append({"product": label, "fields": absent})

    duplicates = sorted({label for label in labels if labels.count(label) > 1})
    covered = len(competitors) - len(missing_images)
    report = {
        "competitor_count": len(competitors),
        "selected_asset_count": len(selected_assets),
        "image_coverage_count": covered if assets else None,
        "image_coverage_percent": round(100 * covered / len(competitors), 1) if competitors and assets else None,
        "missing_images": missing_images,
        "missing_required_fields": missing_fields,
        "duplicate_products": duplicates,
        "stable_competitor_id_present": fields["id"] == "competitor_id",
    }

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
