import subprocess
import sys
from datetime import datetime

def run_command(cmd, name):
    print(f"\n{'='*60}")
    print(f"🚀 Running: {name}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(cmd, shell=True, check=True)
        print(f"✅ {name} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {name} failed with code {e.returncode}")
        return False

def main():
    print(f"\n📊 NEPSE Daily Pipeline - {datetime.now().isoformat()}")
    
    # 1. Pull latest data
    print("\n1️⃣ Pulling latest data from GitHub...")
    if not run_command("git pull origin main", "git pull"):
        sys.exit(1)
    
    # 2. Compute features
    print("\n2️⃣ Computing features...")
    if not run_command("python scripts/compute_features.py", "compute_features"):
        sys.exit(1)
    
    # 3. Generate signals
    print("\n3️⃣ Generating signals...")
    if not run_command("python scripts/generate_signals.py", "generate_signals"):
        sys.exit(1)
    
    # 4. Show results
    print("\n4️⃣ Results:")
    run_command("cat data/signals/$(date +%Y-%m-%d).json", "show signals")
    
    print(f"\n✅ Pipeline complete! {datetime.now().isoformat()}")

if __name__ == "__main__":
    main()
