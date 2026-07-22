import os
import uuid

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.graph import compile_graph
from app.state import AppState

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

    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    initial_state = AppState(topic=req.topic.strip())

    try:
        result = graph.invoke(initial_state, config)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Research pipeline failed: {e}")

    return ResearchResponse(
        report=result.final_report or result.draft_report,
        subtasks=result.subtasks,
        fact_checks=result.fact_check_results,
        error=result.error,
        run_id=config["configurable"]["thread_id"],
    )


@app.post("/research/approve")
async def approve_report(thread_id: str):
    try:
        state = graph.get_state({"configurable": {"thread_id": thread_id}})
        if not state:
            raise HTTPException(status_code=404, detail="Research run not found")
        state.values["approval_status"] = "approved"
        result = graph.invoke(None, {"configurable": {"thread_id": thread_id}})
        return {"status": "approved", "report": result.final_report or result.draft_report}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Approval failed: {e}")


@app.post("/research/revise")
async def request_revision(thread_id: str, notes: str):
    try:
        state = graph.get_state({"configurable": {"thread_id": thread_id}})
        if not state:
            raise HTTPException(status_code=404, detail="Research run not found")
        state.values["approval_status"] = "revision_requested"
        state.values["revision_notes"] = notes
        result = graph.invoke(None, {"configurable": {"thread_id": thread_id}})
        return {"status": "revised", "report": result.final_report or result.draft_report}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Revision failed: {e}")
