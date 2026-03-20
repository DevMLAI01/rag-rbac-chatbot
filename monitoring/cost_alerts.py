from __future__ import annotations
import logging
from datetime import datetime, timezone
from config.settings import settings
from monitoring.metrics_store import _conn, _lock
import sqlite3

logger = logging.getLogger(__name__)


def check_alerts(user_id: str, role: str, request_cost: float) -> list[str]:
    """Check all cost thresholds. Return list of alert messages (empty = no alerts)."""
    alerts = []

    if request_cost > settings.cost_alert_per_request:
        msg = f"Per-request cost ${request_cost:.4f} exceeds threshold ${settings.cost_alert_per_request}"
        logger.warning("COST_ALERT | %s", msg)
        alerts.append(msg)

    today = datetime.now(timezone.utc).date().isoformat()
    with _lock, _conn() as con:
        row = con.execute(
            "SELECT SUM(estimated_cost_usd) FROM request_costs WHERE user_id=? AND timestamp LIKE ?",
            (user_id, f"{today}%"),
        ).fetchone()
    user_daily = (row[0] or 0.0) + request_cost
    if user_daily > settings.cost_alert_per_user_daily:
        msg = f"User {user_id} daily spend ${user_daily:.4f} exceeds ${settings.cost_alert_per_user_daily}"
        logger.warning("COST_ALERT | %s", msg)
        alerts.append(msg)

    with _lock, _conn() as con:
        row = con.execute(
            "SELECT SUM(estimated_cost_usd) FROM request_costs WHERE timestamp LIKE ?",
            (f"{today}%",),
        ).fetchone()
    system_daily = (row[0] or 0.0) + request_cost
    if system_daily > settings.cost_alert_system_daily:
        msg = f"System daily spend ${system_daily:.4f} exceeds ${settings.cost_alert_system_daily}"
        logger.critical("COST_ALERT | %s", msg)
        alerts.append(msg)

    return alerts
