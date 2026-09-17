from __future__ import annotations

from typing import Any

from darukaa_assignment.knowledge.retriever import MultiDocumentRetriever
from darukaa_assignment.reasoning.rules import RULES, build_reasoning_context
from darukaa_assignment.schemas.recommendation import Recommendation


def _active_effects(context: dict[str, object]) -> list[str]:
    effects: list[str] = []
    for rule in RULES.values():
        if context.get(rule["condition"]):
            effects.extend(rule["linked_effects"])
    return effects


def build_recommendation(
    message: str,
    metrics: dict[str, object],
    retriever: MultiDocumentRetriever | None = None,
) -> tuple[Recommendation, list[dict[str, Any]]]:
    context = build_reasoning_context(metrics)
    active_effects = _active_effects(context)
    query = " ".join(
        [
            message,
            f"soil organic carbon {metrics.get('soc', '')}",
            f"rainfall {metrics.get('rainfall', '')}",
            f"land use {metrics.get('land_use', '')}",
            "biodiversity habitat restoration",
        ]
    )
    retriever = retriever or MultiDocumentRetriever()
    chunks = retriever.retrieve(query, top_k=8)
    grouped = retriever.aggregate_sources(chunks)
    if not grouped:
        raise ValueError("No grounded sources were retrieved for this request.")

    primary = grouped[0]
    supporting = grouped[1:4]
    impacted_metrics = ["soc", "species_richness"]
    recommendation = "Increase soil organic carbon with cover crops, retained organic matter, and habitat-supporting land management."
    mechanism = "Improving soil carbon supports soil structure and nutrient cycling; combined with habitat connectivity, this can improve conditions for soil organisms and wider biodiversity."
    if context["low_rainfall_or_moisture"]:
        recommendation += " Prioritize moisture-retaining practices because rainfall or soil moisture is limited."
        impacted_metrics.append("moisture")
    if context["monoculture_or_fragmented_land"]:
        recommendation += " Add diverse vegetation corridors or mixed planting to reduce fragmentation pressure."
        impacted_metrics.append("land_use")

    confidence = "high" if len(active_effects) >= 2 else "moderate"
    source_fields = ("title", "source_org", "url", "year", "domain")
    result = Recommendation(
        recommendation=recommendation,
        mechanism=mechanism,
        impacted_metrics=impacted_metrics,
        expected_change="Improved soil carbon, moisture resilience, and habitat conditions; measure against the submitted baseline.",
        time_horizon="medium-term (1-3 years)",
        confidence=confidence,
        source={key: primary[key] or None for key in source_fields},
        supporting_sources=[
            {key: source[key] or None for key in source_fields}
            for source in supporting
        ],
    )
    return result, grouped