import sqlite3
from datetime import datetime
from app.core.models import  LogLevel,LogEntry



class DatabaseManager():
    def __init__(self,db_path):
        self.db_path = db_path
        self._init_db()

    def _init_db(self) :
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS logs
            (
                id  INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                level TEXT, 
                service TEXT, 
                message TEXT, 
                analysis TEXT
            )
            '''
        )

        conn.commit()
        conn.close()

    def insert_log (self,log:LogEntry) :
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            log_entry = (str(log.timestamp), log.level.value, log.service, log.message, log.analysis)
            cursor.execute("INSERT into logs (timestamp, level, service, message, analysis) VALUES (?, ?, ?, ?, ?)",log_entry)
            conn.commit()
            log.id = cursor.lastrowid
        return  log




    def get_all_logs(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM logs ORDER BY id DESC")
        rows = cursor.fetchall()
        logs = [LogEntry(id=row["id"], timestamp=row["timestamp"], level=LogLevel(row["level"]), service=row["service"],
                         message=row["message"], analysis=row["analysis"]) for row in rows]
        conn.close()
        return logs


    def get_log_by_id(self,log_id):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM logs WHERE id = ?",(log_id,))
        row = cursor.fetchone()
        if row:
            conn.close()
            return LogEntry(
                id=row["id"],
                timestamp=row["timestamp"],
                level=LogLevel(row["level"]),
                service=row["service"],
                message=row["message"],
                analysis=row["analysis"]
            )
        conn.close()
        return None

