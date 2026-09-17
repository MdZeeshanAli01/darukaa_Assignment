from __future__ import annotations

from fastapi import APIRouter

from darukaa_assignment.reasoning.recommender import build_recommendation
from darukaa_assignment.reasoning.slot_filler import ask_clarifying_question
from darukaa_assignment.schemas.request_models import ChatRequest

router = APIRouter()


@router.post("/chat")
def chat_endpoint(payload: ChatRequest) -> dict[str, object]:
    metrics = payload.metrics.model_dump() if payload.metrics else {}
    question = ask_clarifying_question(metrics)

    if question:
        return {
            "session_id": payload.session_id or "demo-session",
            "status": "needs_more_context",
            "clarifying_question": question,
            "message": payload.message,
        }

    recommendation, grouped_sources = build_recommendation(payload.message, metrics)

    return {
        "session_id": payload.session_id or "demo-session",
        "status": "ok",
        "clarifying_question": None,
        "message": payload.message,
        "recommendation": recommendation.model_dump(),
        "evidence": [
            {
                "title": source["title"],
                "source_org": source["source_org"],
                "url": source["url"],
                "year": source["year"],
                "domain": source["domain"],
                "match_count": len(source["matches"]),
                "matches": source["matches"][:2],
            }
            for source in grouped_sources
        ],
    }
