from prometheus_client import Counter, Histogram,generate_latest

LOGS_TOTAL = Counter(name="sre_logs_total" , documentation="Total number of log entries received")
LOGS_BY_LEVEL = Counter(name="sre_logs_by_level",documentation="Log entries by level",labelnames=["level"])
LLM_RESPONSE_TIME = Histogram(name="sre_llm_response_seconds",documentation="Time taken for LLM to analyse a log entry")
