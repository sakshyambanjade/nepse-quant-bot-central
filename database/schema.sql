-- Close price history table
CREATE TABLE IF NOT EXISTS index_close (
    date TEXT PRIMARY KEY,
    close REAL NOT NULL,
    open REAL,
    high REAL,
    low REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Raw demand/supply snapshots
CREATE TABLE IF NOT EXISTS demand_supply_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_buy_quantity REAL,
    total_sell_quantity REAL,
    buy_sell_ratio REAL,
    snapshot_json TEXT
);

-- Raw sector transaction snapshots
CREATE TABLE IF NOT EXISTS sector_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sector_name TEXT,
    turnover_value REAL,
    turnover_volume REAL,
    transaction_count INTEGER,
    snapshot_json TEXT
);

-- Raw stock transaction snapshots
CREATE TABLE IF NOT EXISTS stock_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    symbol TEXT,
    traded_volume INTEGER,
    traded_value REAL,
    transaction_count INTEGER,
    snapshot_json TEXT
);

-- Computed features per date
CREATE TABLE IF NOT EXISTS features (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    buy_sell_ratio REAL,
    order_imbalance REAL,
    sector_momentum TEXT,
    top_gainers TEXT,
    features_json TEXT
);

-- Trading signals
CREATE TABLE IF NOT EXISTS signals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    signal_type TEXT,
    confidence REAL,
    action TEXT,
    reason TEXT,
    signals_json TEXT
);

-- Create indices for faster queries
CREATE INDEX IF NOT EXISTS idx_close_date ON index_close(date);
CREATE INDEX IF NOT EXISTS idx_demand_date ON demand_supply_snapshots(date);
CREATE INDEX IF NOT EXISTS idx_sector_date ON sector_snapshots(date);
CREATE INDEX IF NOT EXISTS idx_stock_date ON stock_snapshots(date);
CREATE INDEX IF NOT EXISTS idx_features_date ON features(date);
CREATE INDEX IF NOT EXISTS idx_signals_date ON signals(date);
