from __future__ import annotations

RULES = {
    "soil_biodiversity": {
        "condition": "low_soc",
        "linked_effects": [
            "reduced microbial diversity",
            "weaker nutrient cycling",
            "lower plant diversity",
        ],
    },
    "water_species": {
        "condition": "low_rainfall_or_moisture",
        "linked_effects": [
            "reduced habitat moisture refugia",
            "species range contraction",
            "lower pollinator stability",
        ],
    },
    "land_fragmentation": {
        "condition": "monoculture_or_fragmented_land",
        "linked_effects": [
            "reduced habitat connectivity",
            "isolated populations",
            "lower genetic diversity",
        ],
    },
}


def build_reasoning_context(metrics: dict[str, object]) -> dict[str, object]:
    soc = float(metrics.get("soc", 0.0) or 0.0)
    rainfall = float(metrics.get("rainfall", 0.0) or 0.0)
    land_use = str(metrics.get("land_use", "") or "")

    context = {
        "low_soc": soc < 1.0,
        "low_rainfall_or_moisture": rainfall < 600 or float(metrics.get("moisture", 0.0) or 0.0) < 20,
        "monoculture_or_fragmented_land": "monoculture" in land_use.lower() or "fragmented" in land_use.lower(),
    }
    return context
