"""
AI Workbench API — FastAPI application.

Architecture:
  HTTP request → Task endpoint → Prompt template → LLM API → JSON response
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.llm_client import call_llm, get_client
from app.models import LLMResponse, TextRequest
from app.services import TaskType, get_task_prompt


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Validate configuration before serving requests."""
    get_client()
    yield


app = FastAPI(
    title="AI Workbench API",
    description="REST API for Summarize, Rewrite, Key Points, and Explain tasks.",
    version="1.0.0",
    lifespan=lifespan,
)


def _run_task(task: TaskType, request: TextRequest) -> LLMResponse:
    """Execute a task by mapping it to its prompt template and calling the LLM."""
    task_name, system_prompt = get_task_prompt(task)
    result = call_llm(system_prompt, request.text)
    return LLMResponse(
        content=result["content"],
        tokens=result["tokens"],
        model=result["model"],
        task=task_name,
    )


@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/summarize", response_model=LLMResponse)
def summarize(request: TextRequest) -> LLMResponse:
    """Summarize input text in 3-5 bullet points."""
    return _run_task(TaskType.SUMMARIZE, request)


@app.post("/rewrite", response_model=LLMResponse)
def rewrite(request: TextRequest) -> LLMResponse:
    """Rewrite input text in a clear, professional tone."""
    return _run_task(TaskType.REWRITE, request)


@app.post("/key-points", response_model=LLMResponse)
def key_points(request: TextRequest) -> LLMResponse:
    """Extract key points from input text as a numbered list."""
    return _run_task(TaskType.KEY_POINTS, request)


@app.post("/explain", response_model=LLMResponse)
def explain(request: TextRequest) -> LLMResponse:
    """Explain input text in simple terms for a non-expert audience."""
    return _run_task(TaskType.EXPLAIN, request)
