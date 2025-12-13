from fastapi import FastAPI, Query
from typing import Optional, List
from datetime import datetime, timedelta
from uuid import uuid4
import random

app = FastAPI(title="Dashboard API - Telemetry Service Mock")

# Helper to generate timestamps
def now_iso():
    return datetime.utcnow().isoformat() + "Z"

# -------------------------------
# /api/health
# -------------------------------
@app.get("/api/health")
def get_health():
    return {
        "status": "connected",
        "last_update": now_iso()
    }

# -------------------------------
# /api/test
# -------------------------------
@app.get("/api/test")
def get_tests(
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    test_name: Optional[str] = None,
    state: Optional[str] = None
):
    data = [
        {
            "test_id": str(uuid4()),
            "test_name": test_name or "strategy_alpha",
            "started_at": (datetime.utcnow() - timedelta(minutes=45)).isoformat() + "Z",
            "ended_at": datetime.utcnow().isoformat() + "Z",
            "pnl": round(random.uniform(-5000, 5000), 2),
            "drawdown": round(random.uniform(-500, 0), 2),
            "duration_sec": 2700,
            "return": round(random.uniform(-0.1, 0.1), 4),
            "link_status": "OK",
            "state": state or "COMPLETED"
        }
        for _ in range(3)
    ]
    return {
        "meta": {"rows": len(data), "generated_at": now_iso()},
        "data": data
    }

# -------------------------------
# /api/submissions
# -------------------------------
@app.get("/api/submissions")
def get_submissions(
    test_id: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None
):
    data = [
        {
            "submission_id": str(uuid4()),
            "test_id": test_id or str(uuid4()),
            "score": round(random.uniform(0, 1), 2)
        }
        for _ in range(5)
    ]
    return {
        "meta": {"rows": len(data), "generated_at": now_iso()},
        "data": data
    }

# -------------------------------
# /api/portfolio
# -------------------------------
@app.get("/api/portfolio")
def get_portfolio(
    test_id: Optional[str] = None,
    portfolio_id: Optional[str] = None
):
    data = [
        {
            "portfolio_id": portfolio_id or str(uuid4()),
            "test_id": test_id or str(uuid4()),
            "state": "ACTIVE",
            "cash_balance": round(random.uniform(1000, 50000), 2),
            "positions": [
                {"asset_id": "AAPL", "quantity": 50, "avg_price": 178.3},
                {"asset_id": "GOOGL", "quantity": 10, "avg_price": 1450.2},
            ]
        }
    ]
    return {
        "meta": {"rows": len(data), "generated_at": now_iso()},
        "data": data
    }

# -------------------------------
# /api/performance
# -------------------------------
@app.get("/api/performance")
def get_performance(
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    interval: Optional[str] = "5m",
    module: Optional[str] = None,
    test_id: Optional[str] = None,
    host: Optional[str] = None,
    asset: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 500
):
    data = [
        {
            "timestamp": (datetime.utcnow() - timedelta(minutes=i*5)).isoformat() + "Z",
            "module": module or random.choice(["ingestion_module", "scoring_module", "portfolio_building_module","execution_module"]),
            "test_id": test_id or str(uuid4()),
            "host": host or f"node-{i%5+1:02d}",
            "throughput": random.randint(10000, 20000),
            "latency_ms_p95": random.randint(50, 200),
            "cpu_usage": round(random.uniform(0, 1), 2),
            "memory_usage_mb": random.randint(1000, 4000),
            "errors": random.randint(0, 5)
        }
        for i in range(min(limit, 10))
    ]
    return {
        "meta": {"interval": interval, "rows": len(data), "generated_at": now_iso()},
        "data": data
    }

# -------------------------------
# /api/alerts
# -------------------------------
@app.get("/api/alerts")
def get_alerts(
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    module: Optional[str] = None,
    test_id: Optional[str] = None,
    status: Optional[str] = None
):
    data = [
        {
            "timestamp": (datetime.utcnow() - timedelta(minutes=i)).isoformat() + "Z",
            "module": module or random.choice(["ingestion_module", "scoring_module", "portfolio_building_module","execution_module"]),
            "test_id": test_id or str(uuid4()),
            "host": f"node-{i%5+1:02d}",
            "metric": "latency_ms_p95",
            "value": random.randint(150, 300),
            "threshold": 150,
            "status": status or "CRITICAL"
        }
        for i in range(3)
    ]
    return {
        "meta": {"rows": len(data), "generated_at": now_iso()},
        "data": data
    }

# -------------------------------
# Run with:
# uvicorn mock_server:app --reload --port 8000
# -------------------------------
