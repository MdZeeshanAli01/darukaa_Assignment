from __future__ import annotations

from fastapi import APIRouter

from darukaa_assignment.reasoning.slot_filler import ask_clarifying_question
from darukaa_assignment.schemas.request_models import ChatRequest

router = APIRouter()


@router.post("/chat")
def chat_endpoint(payload: ChatRequest) -> dict[str, object]:
    metrics = payload.metrics.model_dump() if payload.metrics else {}
    question = ask_clarifying_question(metrics)

    return {
        "session_id": payload.session_id or "demo-session",
        "status": "ok",
        "clarifying_question": question,
        "message": payload.message,
    }
