from __future__ import annotations

from pydantic import BaseModel, Field


class LandMetrics(BaseModel):
    soc: float | None = Field(default=None, description="Soil organic carbon (%)")
    ph: float | None = Field(default=None, description="Soil pH")
    rainfall: float | None = Field(default=None, description="Annual rainfall (mm)")
    temperature: float | None = Field(default=None, description="Average temperature (C)")
    land_use: str | None = Field(default=None, description="Current land use")
    species_richness: float | None = Field(default=None, description="Species richness indicator")
    moisture: float | None = Field(default=None, description="Soil moisture or moisture index")
    pollution: float | None = Field(default=None, description="Pollution level")
    deforestation_rate: float | None = Field(default=None, description="Deforestation rate")
    region: str | None = Field(default=None, description="Region or location name")
    geo_coords: str | None = Field(default=None, description="Latitude/longitude string or coordinate pair")


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None
    metrics: LandMetrics | None = None
