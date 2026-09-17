from __future__ import annotations

from pydantic import BaseModel, Field


class SourceInfo(BaseModel):
    title: str
    source_org: str = Field(default="unknown")
    url: str
    year: str | None = None
    domain: str | None = None


class Recommendation(BaseModel):
    recommendation: str
    mechanism: str
    impacted_metrics: list[str]
    expected_change: str
    time_horizon: str
    confidence: str
    source: SourceInfo
    supporting_sources: list[SourceInfo] = Field(default_factory=list)
