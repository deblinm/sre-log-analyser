from typing import List
from fastapi import APIRouter,HTTPException
from app.core.models import LogEntry,LogEntryCreate
from app.db.database import DatabaseManager
from app.llm.analyser import LLMAnalyser


router = APIRouter()
db = DatabaseManager("logs.db")
analyser = LLMAnalyser()


@router.post("/logs",response_model=LogEntry)
def create_log (log: LogEntryCreate):
    return db.insert_log(LogEntry (level=log.level, service=log.service, message=log.message))

@router.post("/logs/{log_id}/analyse",response_model=LogEntry)
def loganalyzer (log_id: int):
    log = db.get_log_by_id(log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    log.analysis = analyser.analyse(log)
    db.update_analysis(log_id,log.analysis)
    return log

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
