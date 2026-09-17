from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class SourceInfo(BaseModel):
    title: str
    url: str


class Recommendation(BaseModel):
    recommendation: str
    mechanism: str
    impacted_metrics: List[str]
    expected_change: str
    time_horizon: str
    confidence: str
    source: SourceInfo
