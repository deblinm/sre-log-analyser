from fastapi import FastAPI, Response
from app.api.routes import router
from prometheus_client import generate_latest,CONTENT_TYPE_LATEST


app = FastAPI(title="SRE Log Analyser",version="1.0.0")

app.include_router(router)


@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/health")
def health():
    return{"status" : "ok" , "service" : "sre-log-analyser"}