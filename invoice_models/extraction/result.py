from pydantic import BaseModel

from .common import RoutingOverride
from .image import ImageExtractionResult
from .pdf import PdfExtractionResult
from .xml import NfeXmlResult


class ProcessorResult(BaseModel):
    result: NfeXmlResult | PdfExtractionResult | ImageExtractionResult | None
    is_terminal_failure: bool = False
    terminal_reason: str | None = None
    routing_override: RoutingOverride | None = None
