import uuid

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.graph import compile_graph
from app.state import initial_state

load_dotenv()

app = FastAPI(
    title="Multi-Agent Research & Report System",
    description="Autonomous research pipeline with 4 specialized AI agents",
    version="1.0.0",
)

graph = compile_graph()


class ResearchRequest(BaseModel):
    topic: str


class ResearchResponse(BaseModel):
    report: str
    subtasks: list[str] = []
    fact_checks: list[dict] = []
    error: str | None = None
    run_id: str = ""


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/research", response_model=ResearchResponse)
async def run_research(req: ResearchRequest):
    if not req.topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty")

    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    try:
        result = graph.invoke(initial_state(req.topic.strip()), config)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Research pipeline failed: {e}")

    return ResearchResponse(
        report=result.get("final_report", "") or result.get("draft_report", ""),
        subtasks=result.get("subtasks", []),
        fact_checks=result.get("fact_check_results", []),
        error=result.get("error"),
        run_id=thread_id,
    )
