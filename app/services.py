"""Task definitions and prompt templates for AI Workbench."""

from enum import Enum


class TaskType(str, Enum):
    """Supported AI workbench tasks."""

    SUMMARIZE = "summarize"
    REWRITE = "rewrite"
    KEY_POINTS = "key_points"
    EXPLAIN = "explain"


TASKS: dict[TaskType, dict[str, str]] = {
    TaskType.SUMMARIZE: {
        "name": "Summarize",
        "prompt": (
            "You are a concise summarizer. Summarize the user's text in 3-5 clear "
            "bullet points. Focus on the most important information."
        ),
    },
    TaskType.REWRITE: {
        "name": "Rewrite",
        "prompt": (
            "You are a professional editor. Rewrite the user's text in a clear, "
            "professional tone. Maintain the original meaning but improve clarity "
            "and readability."
        ),
    },
    TaskType.KEY_POINTS: {
        "name": "Key Points",
        "prompt": (
            "You are an analyst. Extract the key points from the user's text as a "
            "numbered list. Each point should be one clear sentence."
        ),
    },
    TaskType.EXPLAIN: {
        "name": "Explain",
        "prompt": (
            "You are a patient teacher. Explain the user's text in simple terms that "
            "a non-expert can understand. Use analogies where helpful."
        ),
    },
}


def get_task_prompt(task: TaskType) -> tuple[str, str]:
    """Return the display name and system prompt for a task."""
    task_config = TASKS[task]
    return task_config["name"], task_config["prompt"]
