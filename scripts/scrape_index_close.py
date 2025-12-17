# -*- coding: utf-8 -*-
import requests
import json
from datetime import datetime
from pathlib import Path
import sqlite3

def scrape_index_close(date_str: str = None):
    """
    Scrape NEPSE index close price for a given date.
    Falls back to today's date if not provided.
    """
    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    print(f"\n[INFO] Scraping NEPSE index close for {date_str}")
    
    try:
        # Try ShareSansar API first
        url = f"https://api.sharesansar.com/api/index/nepse?date={date_str}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data and len(data) > 0:
            close_price = float(data[0].get("close", 0))
            high_price = float(data[0].get("high", 0))
            low_price = float(data[0].get("low", 0))
            open_price = float(data[0].get("open", 0))
            
            print(f"[OK] Index close: {close_price}")
            print(f"     Open: {open_price}, High: {high_price}, Low: {low_price}")
            
            # Save to JSON
            close_data = {
                "date": date_str,
                "timestamp": datetime.now().isoformat(),
                "close": close_price,
                "open": open_price,
                "high": high_price,
                "low": low_price
            }
            
            data_dir = Path("data") / "close"
            data_dir.mkdir(parents=True, exist_ok=True)
            
            close_file = data_dir / f"{date_str}.json"
            close_file.write_text(json.dumps(close_data, indent=2), encoding="utf-8")
            print(f"[SAVE] Saved close price -> {close_file}")
            
            # Also store in database
            store_close_in_db(date_str, close_price, open_price, high_price, low_price)
            
            return close_data
        else:
            print(f"[WARN] No data found for {date_str}")
            return None
            
    except Exception as e:
        print(f"[ERROR] Error scraping close price: {e}")
        return None


def store_close_in_db(date_str: str, close: float, open_p: float, high: float, low: float):
    """Store close price in SQLite database."""
    try:
        conn = sqlite3.connect("nepse_trading.db")
        cursor = conn.cursor()
        
        # Create table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS index_close (
                date TEXT PRIMARY KEY,
                close REAL,
                open REAL,
                high REAL,
                low REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insert or update
        cursor.execute("""
            INSERT OR REPLACE INTO index_close (date, close, open, high, low)
            VALUES (?, ?, ?, ?, ?)
        """, (date_str, close, open_p, high, low))
        
        conn.commit()
        conn.close()
        print(f"[SAVE] Stored in database: index_close")
        
    except Exception as e:
        print(f"[ERROR] Database error: {e}")


if __name__ == "__main__":
    import sys
    date = sys.argv[1] if len(sys.argv) > 1 else None
    scrape_index_close(date)
