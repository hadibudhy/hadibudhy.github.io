from dataclasses import asdict
import os

from fastapi import FastAPI
from pydantic import BaseModel, Field

from .schemas import Complaint
from .service import default_service

app = FastAPI(title="ComplaintFlow", version="0.1.0")
service = default_service(os.getenv("COMPLAINTFLOW_DB_PATH", "complaintflow.db"))


class TriageRequest(BaseModel):
    complaint_id: str = Field(min_length=1, max_length=100)
    text: str = Field(default="", max_length=10000)
    product: str | None = None
    issue: str | None = None


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "complaintflow"}


@app.post("/triage")
def triage(request: TriageRequest) -> dict:
    result = service.triage(Complaint(request.complaint_id, request.text, request.product, request.issue))
    return asdict(result)
