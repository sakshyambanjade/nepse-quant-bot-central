"""NEPSE Feature Engineering Script"""

import json
from datetime import datetime
from pathlib import Path

def compute_features(raw_data_root="data/raw"):
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"\n🔧 Computing features for {today}")
    day_dir = Path(raw_data_root) / today

    if not day_dir.exists():
        print(f"❌ No raw data directory: {day_dir}")
        return

    demand_file = day_dir / "demand_supply.json"
    sector_file = day_dir / "sectortransaction.json"
    stock_file = day_dir / "stocktransaction.json"

    features = {
        "date": today,
        "timestamp": datetime.now().isoformat(),
        "indicators": {}
    }

    # demand/supply
    try:
        if demand_file.exists():
            data = json.loads(demand_file.read_text())
            if isinstance(data, list) and data:
                latest = data[-1]
                top_buy = latest.get("top_buy", [])
                top_sell = latest.get("top_sell", [])

                def s_int(x): 
                    return int(str(x).replace(",", "") or "0")

                buy_qty = sum(s_int(r.get("quantity", 0)) for r in top_buy)
                sell_qty = sum(s_int(r.get("quantity", 0)) for r in top_sell)
                total = buy_qty + sell_qty or 1
                bs_ratio = buy_qty / total

                buy_orders = int(latest.get("buy_orders", 0) or 0)
                sell_orders = int(latest.get("sell_orders", 0) or 0)
                o_total = buy_orders + sell_orders or 1
                order_imb = (buy_orders - sell_orders) / o_total

                features["indicators"].update({
                    "buy_sell_ratio": round(bs_ratio, 4),
                    "order_imbalance": round(order_imb, 4),
                    "total_buy_quantity": buy_qty,
                    "total_sell_quantity": sell_qty,
                    "buy_orders": buy_orders,
                    "sell_orders": sell_orders
                })

                if bs_ratio > 0.65:
                    features["indicators"]["momentum_signal"] = "BUY_DEMAND_SURGE"
                elif bs_ratio < 0.35:
                    features["indicators"]["momentum_signal"] = "SELL_PRESSURE"
                else:
                    features["indicators"]["momentum_signal"] = "NEUTRAL"

                print(f"✅ demand_supply snapshots: {len(data)}")
    except Exception as e:
        print("⚠ demand_supply error:", e)

    # sectors
    try:
        if sector_file.exists():
            data = json.loads(sector_file.read_text())
            if isinstance(data, list) and data:
                latest = data[-1]
                sectors = latest.get("sectors", [])
                if sectors:
                    def s_float(x): 
                        return float(str(x).replace(",", "") or 0)

                    top_sector = max(sectors, key=lambda s: s_float(s.get("turnover", 0)))
                    features["indicators"].update({
                        "top_sector": top_sector.get("sector", "N/A"),
                        "sector_count": len(sectors)
                    })
                print(f"✅ sector snapshots: {len(data)}")
    except Exception as e:
        print("⚠ sector error:", e)

    # stock
    try:
        if stock_file.exists():
            data = json.loads(stock_file.read_text())
            if isinstance(data, list) and data:
                latest = data[-1]
                tx = latest.get("transactions", [])
                features["indicators"]["transaction_count"] = len(tx)
                print(f"✅ stock snapshots: {len(data)}")
    except Exception as e:
        print("⚠ stock error:", e)

    out_dir = Path("data/features")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{today}.json"
    out_file.write_text(json.dumps(features, indent=2))
    print(f"💾 saved features -> {out_file}")

if __name__ == "__main__":
    compute_features()
