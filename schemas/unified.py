#schemas/unified.py

from pydantic import BaseModel
from datetime import datetime

class UnifiedSchema(BaseModel):
    name: str
    value: float
    source: str
    ingested_at: datetime | None = None
