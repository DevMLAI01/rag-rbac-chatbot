from __future__ import annotations
import sqlite3
import threading
from pathlib import Path
from config.settings import settings

_lock = threading.Lock()


def _conn() -> sqlite3.Connection:
    Path(settings.metrics_db_path).parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(settings.metrics_db_path, check_same_thread=False)


def init_db():
    with _lock, _conn() as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS request_costs (
            request_id TEXT PRIMARY KEY,
            user_id TEXT, role TEXT, timestamp TEXT,
            prompt_tokens INTEGER, completion_tokens INTEGER, total_tokens INTEGER,
            model TEXT, estimated_cost_usd REAL, cost_alert_triggered INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS ragas_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id TEXT, user_id TEXT, role TEXT, timestamp TEXT,
            faithfulness REAL, answer_relevancy REAL, context_precision REAL, overall_score REAL
        );
        CREATE TABLE IF NOT EXISTS guardrail_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id TEXT, user_id TEXT, role TEXT, timestamp TEXT,
            guard_type TEXT, action TEXT, reason TEXT
        );
        """)


def insert_cost(row: dict):
    with _lock, _conn() as con:
        con.execute("""
        INSERT OR REPLACE INTO request_costs
        (request_id,user_id,role,timestamp,prompt_tokens,completion_tokens,total_tokens,model,estimated_cost_usd,cost_alert_triggered)
        VALUES (:request_id,:user_id,:role,:timestamp,:prompt_tokens,:completion_tokens,:total_tokens,:model,:estimated_cost_usd,:cost_alert_triggered)
        """, row)


def insert_ragas(row: dict):
    with _lock, _conn() as con:
        con.execute("""
        INSERT INTO ragas_scores
        (request_id,user_id,role,timestamp,faithfulness,answer_relevancy,context_precision,overall_score)
        VALUES (:request_id,:user_id,:role,:timestamp,:faithfulness,:answer_relevancy,:context_precision,:overall_score)
        """, row)


def insert_guardrail_event(row: dict):
    with _lock, _conn() as con:
        con.execute("""
        INSERT INTO guardrail_events (request_id,user_id,role,timestamp,guard_type,action,reason)
        VALUES (:request_id,:user_id,:role,:timestamp,:guard_type,:action,:reason)
        """, row)


def get_cost_summary() -> list[dict]:
    with _lock, _conn() as con:
        con.row_factory = sqlite3.Row
        rows = con.execute("""
        SELECT role, COUNT(*) as requests,
               SUM(total_tokens) as total_tokens,
               SUM(estimated_cost_usd) as total_cost,
               SUM(cost_alert_triggered) as alerts
        FROM request_costs GROUP BY role
        """).fetchall()
        return [dict(r) for r in rows]


def get_recent_guardrail_events(limit: int = 50) -> list[dict]:
    with _lock, _conn() as con:
        con.row_factory = sqlite3.Row
        rows = con.execute(
            "SELECT * FROM guardrail_events ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]


def get_ragas_summary() -> list[dict]:
    with _lock, _conn() as con:
        con.row_factory = sqlite3.Row
        rows = con.execute("""
        SELECT role, COUNT(*) as evals,
               AVG(faithfulness) as avg_faithfulness,
               AVG(answer_relevancy) as avg_relevancy,
               AVG(context_precision) as avg_precision,
               AVG(overall_score) as avg_overall
        FROM ragas_scores GROUP BY role
        """).fetchall()
        return [dict(r) for r in rows]
