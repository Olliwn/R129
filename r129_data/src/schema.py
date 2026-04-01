"""Pydantic models for all R129 data structures."""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Confidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class SourceType(str, Enum):
    OWNER_MANUAL = "owner_manual"
    WORKSHOP_MANUAL = "workshop_manual"
    ETM = "etm"
    EPC = "epc"
    COMMUNITY = "community"
    ENGINEERING_DIARY = "engineering_diary"
    WIKIPEDIA = "wikipedia"
    STARFINDER = "starfinder"
    MEASURED = "measured"


class Source(BaseModel):
    type: SourceType
    ref: str
    confidence: Confidence = Confidence.MEDIUM


class AppliesTo(BaseModel):
    """Year range [from, to] inclusive, plus optional chassis filter."""
    years: Optional[list[int]] = None
    chassis: Optional[list[str] | str] = "all"
    engines: Optional[list[str]] = None
    options: Optional[list[int]] = None


# --- Vehicle identity ---

class OptionCode(BaseModel):
    code: int
    description: str


class VehicleIdentity(BaseModel):
    vin: str
    model: str
    model_year: int
    chassis_code: str
    engine_code: str
    engine_description: str
    transmission_code: str
    transmission_description: str
    fuel_system: str
    paint_code: str
    paint_name: str
    interior_code: str
    interior_name: str
    gvwr_kg: int
    front_axle_kg: int
    rear_axle_kg: int
    option_codes: list[OptionCode]
    source: Source


# --- Variants ---

class ProductionChange(BaseModel):
    year: int
    description: str
    source: Source


class R129Variant(BaseModel):
    model_name: str
    chassis_code: str
    engine_code: str
    engine_description: str
    transmission_codes: list[str]
    years_from: int
    years_to: int
    notes: Optional[str] = None
    source: Source


class VariantsFile(BaseModel):
    variants: list[R129Variant]
    production_changes: list[ProductionChange]


# --- Fuses ---

class Fuse(BaseModel):
    id: str
    rating_amps: int
    location: str
    protects: list[str]
    notes: Optional[str] = None
    applies_to: Optional[AppliesTo] = None
    source: Source


class FuseBoxFile(BaseModel):
    description: str
    fuses: list[Fuse]


# --- Relays ---

class Relay(BaseModel):
    id: str
    designation: str
    function: str
    location: str
    part_number: Optional[str] = None
    notes: Optional[str] = None
    applies_to: Optional[AppliesTo] = None
    source: Source


class RelayBoxFile(BaseModel):
    description: str
    relays: list[Relay]


# --- Fluids ---

class Fluid(BaseModel):
    id: str
    system: str
    fluid_type: str
    mercedes_spec: Optional[str] = None
    recommended_products: Optional[list[str]] = None
    capacity_liters: Optional[float] = None
    capacity_notes: Optional[str] = None
    change_interval_km: Optional[int] = None
    change_interval_years: Optional[int] = None
    change_interval_notes: Optional[str] = None
    notes: Optional[str] = None
    applies_to: Optional[AppliesTo] = None
    source: Source


class FluidsFile(BaseModel):
    fluids: list[Fluid]


# --- Torques ---

class TorqueSpec(BaseModel):
    id: str
    system: str
    component: str
    torque_nm: float
    torque_note: Optional[str] = None
    thread_size: Optional[str] = None
    notes: Optional[str] = None
    applies_to: Optional[AppliesTo] = None
    source: Source


class TorquesFile(BaseModel):
    torques: list[TorqueSpec]


# --- Known issues ---

class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class KnownIssue(BaseModel):
    id: str
    title: str
    severity: Severity
    description: str
    affected_systems: list[str]
    affected_fuse: Optional[str] = None
    symptoms: Optional[list[str]] = None
    diagnostic_hint: Optional[str] = None
    part_numbers: Optional[list[str]] = None
    applies_to: Optional[AppliesTo] = None
    source: Source


class KnownIssuesFile(BaseModel):
    known_issues: list[KnownIssue]


# --- Service intervals ---

class ServiceItem(BaseModel):
    id: str
    system: str
    task: str
    interval_km: Optional[int] = None
    interval_years: Optional[int] = None
    interval_notes: Optional[str] = None
    notes: Optional[str] = None
    applies_to: Optional[AppliesTo] = None
    source: Source


class ServiceIntervalsFile(BaseModel):
    service_items: list[ServiceItem]


# --- Document index (per-PDF metadata) ---

class TocEntry(BaseModel):
    page: int
    heading: str


class DocumentMeta(BaseModel):
    doc_id: str
    title: str
    filename: str
    source_url: str
    pages: Optional[int] = None
    topics: list[str] = Field(default_factory=list)
    toc: list[TocEntry] = Field(default_factory=list)
    applies_to: Optional[AppliesTo] = None
    quality: Confidence = Confidence.MEDIUM


# --- Ingested chunk (JSONL records) ---

class ChunkImage(BaseModel):
    image_file: str
    transcription: str


class IngestedChunk(BaseModel):
    chunk_id: str
    doc_id: str
    doc_title: str
    page: int
    text: str
    images: list[ChunkImage] = Field(default_factory=list)
    source_url: str
    topics: list[str] = Field(default_factory=list)
    token_count: Optional[int] = None


# --- Components (Tier 2 placeholder) ---

class Component(BaseModel):
    id: str
    designation: str
    name: str
    system: str
    function: str
    location: Optional[str] = None
    connector_pins: Optional[int] = None
    notes: Optional[str] = None
    applies_to: Optional[AppliesTo] = None
    source: Source


class ComponentsFile(BaseModel):
    components: list[Component]


# --- Ground points (Tier 2 placeholder) ---

class GroundPoint(BaseModel):
    id: str
    location: str
    circuits: list[str] = Field(default_factory=list)
    notes: Optional[str] = None
    applies_to: Optional[AppliesTo] = None
    source: Source


class GroundPointsFile(BaseModel):
    ground_points: list[GroundPoint]
