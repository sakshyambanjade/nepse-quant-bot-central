# -*- coding: utf-8 -*-
import sys
import json
from datetime import datetime
from pathlib import Path

def compute_features(date_str: str):
    print(f"\n[INFO] Computing features for {date_str}")

    raw_dir = Path("data") / "raw" / date_str
    if not raw_dir.exists():
        print(f"[ERROR] No raw data directory: {raw_dir}")
        return None

    # load raw files if present
    demand_file = raw_dir / "demand_supply.json"
    sector_file = raw_dir / "sectortransaction.json"
    stock_file  = raw_dir / "stocktransaction.json"

    demand = json.loads(demand_file.read_text(encoding="utf-8")) if demand_file.exists() else []
    sector = json.loads(sector_file.read_text(encoding="utf-8")) if sector_file.exists() else []
    stock  = json.loads(stock_file.read_text(encoding="utf-8")) if stock_file.exists() else []

    print(f"[OK] demand_supply snapshots: {len(demand)}")
    print(f"[OK] sector snapshots: {len(sector)}")
    print(f"[OK] stock snapshots: {len(stock)}")

    # ---- simple indicators (safe defaults) ----
    buy_qty = 0.0
    sell_qty = 0.0

    if demand:
        last = demand[-1]
        for r in last.get("top_buy", []):
            try:
                buy_qty += float(str(r.get("quantity", "0")).replace(",", ""))
            except:
                pass
        for r in last.get("top_sell", []):
            try:
                sell_qty += float(str(r.get("quantity", "0")).replace(",", ""))
            except:
                pass

    buy_sell_ratio = buy_qty / (buy_qty + sell_qty) if (buy_qty + sell_qty) > 0 else 0.5
    order_imbalance = (buy_qty - sell_qty) / (buy_qty + sell_qty) if (buy_qty + sell_qty) > 0 else 0.0

    features = {
        "date": date_str,
        "timestamp": datetime.now().isoformat(),
        "indicators": {
            "buy_sell_ratio": round(buy_sell_ratio, 6),
            "order_imbalance": round(order_imbalance, 6),
        },
        "counts": {
            "demand_snapshots": len(demand),
            "sector_snapshots": len(sector),
            "stock_snapshots": len(stock),
        },
    }

    out_dir = Path("data") / "features"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{date_str}.json"
    out_file.write_text(json.dumps(features, indent=2), encoding="utf-8")

    print(f"[SAVE] saved features -> {out_file}")
    return features

if __name__ == "__main__":
    date_str = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime("%Y-%m-%d")
    compute_features(date_str)
