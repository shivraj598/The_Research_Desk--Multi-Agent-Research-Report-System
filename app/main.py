import uuid
import threading

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.graph import compile_graph
from app.state import initial_state

load_dotenv()

app = FastAPI(
    title="Multi-Agent Research & Report System",
    description="Autonomous research pipeline with 4 specialized AI agents",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graph = compile_graph()

jobs: dict[str, dict] = {}


class ResearchRequest(BaseModel):
    topic: str


class ResearchResponse(BaseModel):
    report: str = ""
    subtasks: list[str] = []
    fact_checks: list[dict] = []
    error: str | None = None
    run_id: str = ""
    status: str = "pending"


def _run_research(topic: str, run_id: str):
    try:
        config = {"configurable": {"thread_id": run_id}}
        result = graph.invoke(initial_state(topic), config)
        jobs[run_id] = {
            "status": "done",
            "report": result.get("final_report", "") or result.get("draft_report", ""),
            "subtasks": result.get("subtasks", []),
            "fact_checks": result.get("fact_check_results", []),
            "error": result.get("error"),
        }
    except Exception as e:
        jobs[run_id] = {"status": "error", "error": str(e)}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/research")
async def start_research(req: ResearchRequest):
    if not req.topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty")

    run_id = str(uuid.uuid4())
    jobs[run_id] = {"status": "running"}
    thread = threading.Thread(target=_run_research, args=(req.topic.strip(), run_id), daemon=True)
    thread.start()

    return {"run_id": run_id, "status": "running"}


@app.get("/research/{run_id}")
async def get_research(run_id: str):
    job = jobs.get(run_id)
    if not job:
        raise HTTPException(status_code=404, detail="Research run not found")

    return ResearchResponse(
        status=job.get("status", "unknown"),
        report=job.get("report", ""),
        subtasks=job.get("subtasks", []),
        fact_checks=job.get("fact_checks", []),
        error=job.get("error"),
        run_id=run_id,
    )
