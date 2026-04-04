from typing import Any

from pydantic import BaseModel, Field


# ─── KPIs ─────────────────────────────────────────────────────────────────────

class AnalyticsKPIResponse(BaseModel):
    """Aggregate KPIs for the authenticated user over a given date range."""

    total_documents: int
    success_count: int
    failure_count: int
    success_rate: float


# ─── Time series ──────────────────────────────────────────────────────────────

class AnalyticsTimeSeriesPoint(BaseModel):
    """Single day in the time-series aggregation."""

    date: str  # YYYY-MM-DD
    total: int
    success: int
    failure: int


class AnalyticsTimeSeriesResponse(BaseModel):
    """Daily-aggregated time-series data with metadata."""

    points: list[AnalyticsTimeSeriesPoint]
    date_range: str  # human-readable, e.g. "Últimos 7 dias"
    presets: dict[str, str]  # {"7d": "7 dias", "30d": "30 dias", ...}


# ─── Document breakdown ───────────────────────────────────────────────────────

class AnalyticsDocumentBreakdown(BaseModel):
    """Per-document detail row for the analytics breakdown table."""

    document_id: str    # UUID
    batch_id: str       # UUID
    type: str           # doc_type: xml, pdf, img
    status: str         # document status
    processing_time_ms: int = Field(default=0)  # ms between upload_confirmed and completed
    extraction_result: str = Field(default="")   # success, failed, partial, skipped
    created_at: str     # ISO 8601


class AnalyticsDocumentBreakdownList(BaseModel):
    """Paginated list of document breakdown entries."""

    items: list[AnalyticsDocumentBreakdown]
    total: int
    page: int
    page_size: int
