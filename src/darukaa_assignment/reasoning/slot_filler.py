from __future__ import annotations

REQUIRED_FIELDS = [
    "soc",
    "ph",
    "rainfall",
    "land_use",
    "region",
]


def missing_required_fields(metrics: dict[str, object]) -> list[str]:
    missing: list[str] = []
    for field in REQUIRED_FIELDS:
        value = metrics.get(field)
        if value is None or value == "":
            missing.append(field)
    return missing


def ask_clarifying_question(metrics: dict[str, object]) -> str | None:
    missing = missing_required_fields(metrics)
    if not missing:
        return None

    if "soc" in missing or "land_use" in missing or "rainfall" in missing:
        return "Could you share the soil organic carbon, current land use, and annual rainfall for the site so I can tailor the recommendation?"

    return "I need a few more land and climate details before I can give a grounded recommendation."
