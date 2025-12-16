"""NEPSE Momentum Signal Generator"""

import json
from datetime import datetime
from pathlib import Path

def generate_signals(features_root="data/features"):
    today = datetime.now().strftime("%Y-%m-%d")
    f_file = Path(features_root) / f"{today}.json"
    
    print(f"🎯 Generating signals for {today}")
    print(f"📂 Looking for: {f_file}")
    
    if not f_file.exists():
        print(f"❌ No features file: {f_file}")
        return

    feats = json.loads(f_file.read_text())
    ind = feats.get("indicators", {})
    
    print(f"📊 Indicators found: {ind}")
    
    bs = float(ind.get("buy_sell_ratio", 0.5))
    imb = float(ind.get("order_imbalance", 0.0))

    print(f"💹 buy_sell_ratio: {bs}")
    print(f"⚖️  order_imbalance: {imb}")

    signals = []

    if bs > 0.65 and imb > 0.2:
        sig = {
            "type": "BUY",
            "strategy": "MOMENTUM_DEMAND_SURGE",
            "confidence": round(min(1.0, (bs - 0.65) * 4 + imb), 3),
            "reason": f"buy_sell_ratio={bs:.3f}, order_imbalance={imb:.3f}"
        }
        signals.append(sig)
        print(f"✅ Signal generated: {sig}")
        
    elif bs < 0.35 and imb < -0.2:
        sig = {
            "type": "SELL",
            "strategy": "MOMENTUM_SUPPLY_CRUSH",
            "confidence": round(min(1.0, (0.35 - bs) * 4 + abs(imb)), 3),
            "reason": f"buy_sell_ratio={bs:.3f}, order_imbalance={imb:.3f}"
        }
        signals.append(sig)
        print(f"✅ Signal generated: {sig}")
    else:
        print(f"⚪ No signals (conditions not met)")

    out = {
        "date": today,
        "timestamp": datetime.now().isoformat(),
        "signal_count": len(signals),
        "signals": signals,
    }

    out_dir = Path("data/signals")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{today}.json"
    out_file.write_text(json.dumps(out, indent=2))
    
    print(f"\n💾 Signals saved -> {out_file}")
    print(f"📈 Total signals: {len(signals)}")
    print(f"\n{json.dumps(out, indent=2)}")

if __name__ == "__main__":
    generate_signals()
