from __future__ import annotations

from fastapi import APIRouter

from darukaa_assignment.db.database import (
    save_land_metrics,
    save_recommendation,
    save_session,
)
from darukaa_assignment.reasoning.recommender import build_recommendation
from darukaa_assignment.reasoning.slot_filler import ask_clarifying_question
from darukaa_assignment.schemas.request_models import ChatRequest

router = APIRouter()


@router.post("/chat")
def chat_endpoint(payload: ChatRequest) -> dict[str, object]:
    session_id = payload.session_id or "demo-session"
    metrics = payload.metrics.model_dump() if payload.metrics else {}

    if metrics and any(value is not None for value in metrics.values()):
        save_land_metrics(metrics)

    question = ask_clarifying_question(metrics)

    if question:
        save_session(session_id, context=f"Clarification asked: {question}")
        return {
            "session_id": session_id,
            "status": "needs_more_context",
            "clarifying_question": question,
            "message": payload.message,
        }

    recommendation, grouped_sources = build_recommendation(payload.message, metrics)

    save_session(session_id, context=f"Generated recommendation: {recommendation.recommendation[:100]}")
    save_recommendation(
        session_id=session_id,
        recommendation_text=recommendation.recommendation,
        source_title=recommendation.source.title if recommendation.source else None,
        source_url=recommendation.source.url if recommendation.source else None,
    )

    return {
        "session_id": session_id,
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
