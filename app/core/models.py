from datetime import datetime, timezone
from enum import StrEnum
from typing import Optional
from pydantic import BaseModel, Field


class LogLevel(StrEnum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"



class LogEntry(BaseModel):
    id: Optional[int] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    level: LogLevel
    service: str
    message: str
    analysis: Optional[str] = None


class LogEntryCreate(BaseModel):
    level: LogLevel
    service: str
    message: str