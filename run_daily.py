import subprocess
import json
import json
from datetime import datetime
from pathlib import Path
import sqlite3

def run_command(cmd, label):
    """Run a shell command and report status."""
    print(f"\n🚀 Running: {cmd}")
    print("=" * 60)
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(f"❌ {label} failed with code {result.returncode}")
            if result.stderr:
                print(f"Error: {result.stderr}")
        else:
            print(f"✅ {label} succeeded")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ {label} error: {e}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(f"❌ {label} failed with code {result.returncode}")
            if result.stderr:
                print(f"Error: {result.stderr}")
        else:
            print(f"✅ {label} succeeded")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ {label} error: {e}")
        return False


def get_latest_data_date():
    """Auto-detect the latest date folder in data/raw/."""
def get_latest_data_date():
    """Auto-detect the latest date folder in data/raw/."""
    raw_root = Path("data") / "raw"
    if not raw_root.exists():
        print(f"⚠ No data/raw folder found. Using today's date.")
        return datetime.now().strftime("%Y-%m-%d")
    
    available = sorted([p.name for p in raw_root.iterdir() if p.is_dir()])
    if not available:
        print(f"⚠ No date folders found in data/raw. Using today's date.")
        return datetime.now().strftime("%Y-%m-%d")
    
    latest_date = available[-1]
    print(f"📅 Auto-detected latest data date: {latest_date}")
    return latest_date


def show_signals(date_str):
    """Display generated signals."""
    sig_path = Path("data") / "signals" / f"{date_str}.json"
    if sig_path.exists():
        content = sig_path.read_text(encoding="utf-8")
        print(content)
    else:
        print(f"⚠ No signals file yet: {sig_path}")
    if not raw_root.exists():
        print(f"⚠ No data/raw folder found. Using today's date.")
        return datetime.now().strftime("%Y-%m-%d")
    
    available = sorted([p.name for p in raw_root.iterdir() if p.is_dir()])
    if not available:
        print(f"⚠ No date folders found in data/raw. Using today's date.")
        return datetime.now().strftime("%Y-%m-%d")
    
    latest_date = available[-1]
    print(f"📅 Auto-detected latest data date: {latest_date}")
    return latest_date


def show_signals(date_str):
    """Display generated signals."""
    sig_path = Path("data") / "signals" / f"{date_str}.json"
    if sig_path.exists():
        content = sig_path.read_text(encoding="utf-8")
        print(content)
    else:
        print(f"⚠ No signals file yet: {sig_path}")


def main():
    print(f"\n📊 NEPSE Daily Pipeline - {datetime.now().isoformat()}")
    
    # Step 1: Pull latest data from GitHub
    print(f"\n1️⃣ Pulling latest data from GitHub...\n")
    print("=" * 60)
    run_command("git pull origin main", "git pull")
    
    # Step 2: Auto-detect latest data date
    data_date = get_latest_data_date()
    
    # Step 3: Scrape index close price
    print(f"\n2️⃣ Scraping NEPSE index close price...\n")
    print("=" * 60)
    run_command(f"python scripts/scrape_index_close.py {data_date}", "scrape_index_close")
    
    # Step 4: Compute features
    print(f"\n3️⃣ Computing features...\n")
    print("=" * 60)
    run_command(f"python scripts/compute_features.py {data_date}", "compute_features")
    
    # Step 5: Generate signals
    print(f"\n4️⃣ Generating signals...\n")
    print("=" * 60)
    run_command(f"python scripts/generate_signals.py {data_date}", "generate_signals")
    
    # Step 6: Show results
    print(f"\n5️⃣ Results from {data_date}:")
    print("=" * 60)
    show_signals(data_date)
    
    # Step 7: Commit and push (optional, comment out if manual)
    print(f"\n6️⃣ Committing results to GitHub...\n")
    print("=" * 60)
    run_command(f'git add data/features/{data_date}.json data/signals/{data_date}.json', "git add")
    run_command(f'git commit -m "Phase 1: Daily pipeline run for {data_date}"', "git commit")
    run_command("git push origin main", "git push")
    
    
    # Step 1: Pull latest data from GitHub
    print(f"\n1️⃣ Pulling latest data from GitHub...\n")
    print("=" * 60)
    run_command("git pull origin main", "git pull")
    
    # Step 2: Auto-detect latest data date
    data_date = get_latest_data_date()
    
    # Step 3: Scrape index close price
    print(f"\n2️⃣ Scraping NEPSE index close price...\n")
    print("=" * 60)
    run_command(f"python scripts/scrape_index_close.py {data_date}", "scrape_index_close")
    
    # Step 4: Compute features
    print(f"\n3️⃣ Computing features...\n")
    print("=" * 60)
    run_command(f"python scripts/compute_features.py {data_date}", "compute_features")
    
    # Step 5: Generate signals
    print(f"\n4️⃣ Generating signals...\n")
    print("=" * 60)
    run_command(f"python scripts/generate_signals.py {data_date}", "generate_signals")
    
    # Step 6: Show results
    print(f"\n5️⃣ Results from {data_date}:")
    print("=" * 60)
    show_signals(data_date)
    
    # Step 7: Commit and push
    print(f"\n6️⃣ Committing results to GitHub...\n")
    print("=" * 60)
    run_command(f'git add data/features/{data_date}.json data/signals/{data_date}.json', "git add")
    run_command(f'git commit -m "Phase 1: Daily pipeline run for {data_date}"', "git commit")
    run_command("git push origin main", "git push")
    
    print(f"\n✅ Pipeline complete! {datetime.now().isoformat()}")


if __name__ == "__main__":
    main()
