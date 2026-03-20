from fastapi import APIRouter
from monitoring.metrics_store import get_cost_summary, get_recent_guardrail_events, get_ragas_summary

router = APIRouter(prefix="/monitoring", tags=["monitoring"])


@router.get("/costs/summary")
async def costs_summary():
    return {"summary": get_cost_summary()}


@router.get("/ragas/summary")
async def ragas_summary():
    return {"summary": get_ragas_summary()}


@router.get("/guardrails/events")
async def guardrail_events():
    return {"events": get_recent_guardrail_events()}
