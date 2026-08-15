"""Pydantic models for AI Workbench API request and response payloads."""

from pydantic import BaseModel, Field


class TextRequest(BaseModel):
    """Input text to process with an AI task."""

    text: str = Field(..., min_length=1, max_length=10000, description="The text to process")


class LLMResponse(BaseModel):
    """Structured response from an LLM task."""

    content: str = Field(..., description="Generated content from the LLM")
    tokens: int = Field(..., ge=0, description="Total tokens consumed")
    model: str = Field(..., description="Model used for generation")
    task: str = Field(..., description="Name of the task that was executed")
