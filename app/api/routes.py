from typing import List
from fastapi import APIRouter,HTTPException
from app.core.models import LogEntry,LogEntryCreate
from app.db.database import DatabaseManager


router = APIRouter()
db = DatabaseManager("logs.db")


@router.post("/logs",response_model=LogEntry)
def create_log (log: LogEntryCreate):
    return db.insert_log(LogEntry (level=log.level, service=log.service, message=log.message))


@router.get("/logs",response_model=List[LogEntry])
def get_logs():
    return db.get_all_logs()


@router.get("/logs/{log_id}",response_model=LogEntry)
def get_log (log_id: int):
    res = db.get_log_by_id(log_id)
    if res :
        return res
    else:
        raise HTTPException(
            status_code=404,
            detail="Log not found"
        )
