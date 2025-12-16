import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_command(cmd, name):
    print(f"\n{'=' * 60}")
    print(f"🚀 Running: {name}")
    print(f"{'=' * 60}")
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"✅ {name} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {name} failed with code {e.returncode}")
        return False


def get_latest_available_date():
    """
    Pick latest folder inside data/raw/YYYY-MM-DD
    Fallback to today if none exists
    """
    raw_root = Path("data") / "raw"

    if raw_root.exists():
        available = sorted(
            p.name for p in raw_root.iterdir() if p.is_dir()
        )
        if available:
            return available[-1]

    return datetime.now().strftime("%Y-%m-%d")


def main():
    print(f"\n📊 NEPSE Daily Pipeline - {datetime.now().isoformat()}")

    # Use latest available date
    data_date = get_latest_available_date()
    print(f"📅 Using data date: {data_date}")

    # 1. Pull latest data
    print("\n1️⃣ Pulling latest data from GitHub...")
    if not run_command("git pull origin main", "git pull"):
        sys.exit(1)

    # 2. Compute features (PASS DATE)
    print("\n2️⃣ Computing features...")
    if not run_command(
        f"python scripts/compute_features.py {data_date}",
        "compute_features",
    ):
        sys.exit(1)

    # 3. Generate signals (PASS DATE)
    print("\n3️⃣ Generating signals...")
    if not run_command(
        f"python scripts/generate_signals.py {data_date}",
        "generate_signals",
    ):
        sys.exit(1)

    # 4. Show results
    print("\n4️⃣ Results:")
    sig_path = Path("data") / "signals" / f"{data_date}.json"

    if sig_path.exists():
        print(sig_path.read_text(encoding="utf-8"))
    else:
        print(f"⚠ No signals file yet: {sig_path}")

    print(f"\n✅ Pipeline complete! {datetime.now().isoformat()}")


if __name__ == "__main__":
    main()
