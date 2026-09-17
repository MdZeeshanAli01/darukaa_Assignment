from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional


class LandMetrics(BaseModel):
    soc: Optional[float] = Field(default=None, description="Soil organic carbon (%)")
    ph: Optional[float] = Field(default=None, description="Soil pH")
    rainfall: Optional[float] = Field(default=None, description="Annual rainfall (mm)")
    temperature: Optional[float] = Field(default=None, description="Average temperature (C)")
    land_use: Optional[str] = Field(default=None, description="Current land use")
    species_richness: Optional[float] = Field(default=None, description="Species richness indicator")
    moisture: Optional[float] = Field(default=None, description="Soil moisture or moisture index")
    pollution: Optional[float] = Field(default=None, description="Pollution level")
    deforestation_rate: Optional[float] = Field(default=None, description="Deforestation rate")
    region: Optional[str] = Field(default=None, description="Region or location name")
    geo_coords: Optional[str] = Field(default=None, description="Latitude/longitude string or coordinate pair")


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    metrics: Optional[LandMetrics] = None
