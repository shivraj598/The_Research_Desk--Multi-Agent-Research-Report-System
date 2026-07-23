import asyncio
import uuid
from concurrent.futures import ThreadPoolExecutor

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
executor = ThreadPoolExecutor(max_workers=1)


class ResearchRequest(BaseModel):
    topic: str
    mode: str = "quick"


class ResearchResponse(BaseModel):
    report: str = ""
    subtasks: list[str] = []
    fact_checks: list[dict] = []
    error: str | None = None
    run_id: str = ""
    status: str = "pending"


def execute_graph(topic: str, run_id: str, mode: str = "quick"):
    try:
        state = initial_state(topic, mode=mode)
        config = {"configurable": {"thread_id": run_id}}
        result = graph.invoke(state, config)
        if jobs.get(run_id, {}).get("status") == "cancelled":
            return
        jobs[run_id] = {
            "status": "done",
            "report": result.get("final_report", "") or result.get("draft_report", ""),
            "subtasks": result.get("subtasks", []),
            "fact_checks": result.get("fact_check_results", []),
            "error": result.get("error"),
        }
    except Exception as e:
        if jobs.get(run_id, {}).get("status") != "cancelled":
            jobs[run_id] = {"status": "error", "error": f"Research failed: {e}"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/research")
async def start_research(req: ResearchRequest):
    if not req.topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty")

    run_id = str(uuid.uuid4())
    jobs[run_id] = {"status": "running"}
    asyncio.get_event_loop().run_in_executor(
        executor, execute_graph, req.topic.strip(), run_id, req.mode
    )
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


@app.post("/research/{run_id}/stop")
async def stop_research(run_id: str):
    if run_id not in jobs:
        raise HTTPException(status_code=404, detail="Research run not found")
    jobs[run_id] = {"status": "cancelled", "report": "", "error": "Cancelled by user"}
    return {"status": "cancelled"}
