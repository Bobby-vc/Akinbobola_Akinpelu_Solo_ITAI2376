import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent / "trading.db"


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS crew_runs (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                run_at      TEXT NOT NULL,
                question    TEXT,
                ticker      TEXT,
                experience  TEXT,
                threshold   REAL,
                analysis    TEXT,
                trade_signal TEXT,
                raw_output  TEXT
            );

            CREATE TABLE IF NOT EXISTS trade_history (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                traded_at   TEXT NOT NULL,
                ticker      TEXT NOT NULL,
                qty         INTEGER NOT NULL,
                side        TEXT NOT NULL,
                order_id    TEXT,
                status      TEXT,
                crew_run_id INTEGER REFERENCES crew_runs(id)
            );

            CREATE TABLE IF NOT EXISTS portfolio_snapshots (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                snapped_at      TEXT NOT NULL,
                cash            REAL,
                portfolio_value REAL,
                buying_power    REAL,
                positions_json  TEXT
            );

            CREATE TABLE IF NOT EXISTS stock_cache (
                ticker      TEXT NOT NULL,
                cached_at   TEXT NOT NULL,
                data_json   TEXT NOT NULL,
                PRIMARY KEY (ticker)
            );
        """)


# --- crew runs ---

def log_crew_run(question: str, ticker: str, experience: str, threshold: float,
                 analysis: str, trade_signal: str, raw_output: str) -> int:
    with get_conn() as conn:
        cur = conn.execute(
            """INSERT INTO crew_runs (run_at, question, ticker, experience, threshold,
               analysis, trade_signal, raw_output) VALUES (?,?,?,?,?,?,?,?)""",
            (datetime.utcnow().isoformat(), question, ticker, experience,
             threshold, analysis, trade_signal, raw_output),
        )
        return cur.lastrowid


def get_crew_runs(limit: int = 50):
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM crew_runs ORDER BY run_at DESC LIMIT ?", (limit,)
        ).fetchall()


# --- trades ---

def log_trade(ticker: str, qty: int, side: str, order_id: str,
              status: str, crew_run_id: int | None = None):
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO trade_history (traded_at, ticker, qty, side, order_id, status, crew_run_id)
               VALUES (?,?,?,?,?,?,?)""",
            (datetime.utcnow().isoformat(), ticker, qty, side, order_id, status, crew_run_id),
        )


def get_trades(limit: int = 100):
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM trade_history ORDER BY traded_at DESC LIMIT ?", (limit,)
        ).fetchall()


# --- portfolio snapshots ---

def log_portfolio_snapshot(cash: float, portfolio_value: float,
                           buying_power: float, positions: list[dict]):
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO portfolio_snapshots (snapped_at, cash, portfolio_value, buying_power, positions_json)
               VALUES (?,?,?,?,?)""",
            (datetime.utcnow().isoformat(), cash, portfolio_value,
             buying_power, json.dumps(positions)),
        )


def get_portfolio_snapshots(limit: int = 100):
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM portfolio_snapshots ORDER BY snapped_at DESC LIMIT ?", (limit,)
        ).fetchall()


# --- stock cache ---

def cache_stock_data(ticker: str, data: dict):
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO stock_cache (ticker, cached_at, data_json)
               VALUES (?,?,?)
               ON CONFLICT(ticker) DO UPDATE SET cached_at=excluded.cached_at, data_json=excluded.data_json""",
            (ticker.upper(), datetime.utcnow().isoformat(), json.dumps(data)),
        )


def get_cached_stock(ticker: str, max_age_minutes: int = 15) -> dict | None:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM stock_cache WHERE ticker=?", (ticker.upper(),)
        ).fetchone()
    if not row:
        return None
    cached_at = datetime.fromisoformat(row["cached_at"])
    age = (datetime.utcnow() - cached_at).total_seconds() / 60
    if age > max_age_minutes:
        return None
    return json.loads(row["data_json"])


init_db()
