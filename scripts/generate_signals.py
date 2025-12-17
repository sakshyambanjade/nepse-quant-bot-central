# -*- coding: utf-8 -*-
import sys
import json
from datetime import datetime
from pathlib import Path

def generate_signals(date_str: str):
    print(f"[INFO] Generating signals for {date_str}")

    f_file = Path("data") / "features" / f"{date_str}.json"
    print(f"[INFO] Looking for: {f_file}")

    if not f_file.exists():
        print(f"[ERROR] No features file: {f_file}")
        return None

    feats = json.loads(f_file.read_text(encoding="utf-8"))
    ind = feats.get("indicators", {})

    bs = float(ind.get("buy_sell_ratio", 0.5))
    imb = float(ind.get("order_imbalance", 0.0))

    signals = []

    # simple rules (same idea as before)
    if bs > 0.65 and imb > 0.2:
        signals.append({
            "type": "BUY",
            "strategy": "MOMENTUM_DEMAND_SURGE",
            "confidence": round(min(1.0, (bs - 0.65) * 4 + imb), 3),
            "reason": f"buy_sell_ratio={bs:.3f}, order_imbalance={imb:.3f}"
        })
    elif bs < 0.35 and imb < -0.2:
        signals.append({
            "type": "SELL",
            "strategy": "MOMENTUM_SUPPLY_CRUSH",
            "confidence": round(min(1.0, (0.35 - bs) * 4 + abs(imb)), 3),
            "reason": f"buy_sell_ratio={bs:.3f}, order_imbalance={imb:.3f}"
        })

    out = {
        "date": date_str,
        "timestamp": datetime.now().isoformat(),
        "signal_count": len(signals),
        "signals": signals,
    }

    out_dir = Path("data") / "signals"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{date_str}.json"
    out_file.write_text(json.dumps(out, indent=2), encoding="utf-8")

    print(f"[SAVE] saved signals -> {out_file}")
    print(json.dumps(out, indent=2))
    return out

if __name__ == "__main__":
    date_str = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime("%Y-%m-%d")
    generate_signals(date_str)
