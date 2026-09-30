import time
from fastapi import FastAPI, Response, Request
from prometheus_client import (
    CONTENT_TYPE_LATEST, 
    Counter ,  
    generate_latest ,
    Histogram , 
)
from pydantic import BaseModel

app = FastAPI(title="ai-platform")

REQUEST = Counter(
    "http_requests_total", "Total HTTP Requests", ["method", "path", "status"]
)
LATENCY = Histogram(
    "http_request_duration_seconds", "Request latency in seconds", ["method", "path"]
)

@app.middleware("http")
async def count_requests(request: Request, call_next):
    start_time = time.perf_counter()
    status = 500
    try:
        response = await call_next(request)
        status = response.status_code
        return response
    finally:
        route = request.scope.get("route")
        path = route.path if route else "unmatched"
        REQUEST.labels(request.method, path, str(status)).inc()
        LATENCY.labels(request.method, path).observe(time.perf_counter() - start_time)

POSITIVE = {"good", "great", "excellent", "love", "happy", "works"}
NEGATIVE = {"bad", "terrible", "awful", "hate", "broken" , "fails"}

def predict_sentiment(text: str) -> tuple[str, float]:
    """Stand-in model. Replace this function with a real model later."""
    words = text.lower().split()
    score = sum(w in POSITIVE for w in words) - sum(w in NEGATIVE for w in words)
    label = "positive" if score > 0 else "negative" if score < 0 else "neutral"
    confidence = min(1.0, 0.5 + 0.25 * abs(score))
    return label, confidence

class PredictRequest(BaseModel):
    text: str

@app.post("/predict")
async def predict(req: PredictRequest):
    label, confidence = predict_sentiment(req.text)
    return {"label": label, "confidence": confidence}

@app.get("/healthz")
async def health():
    return {"status": "ok"}

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)