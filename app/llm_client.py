"""OpenAI client wrapper for AI Workbench LLM calls."""

import os

from dotenv import load_dotenv
from openai import APIConnectionError, AuthenticationError, OpenAI, RateLimitError

load_dotenv()

MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

_client: OpenAI | None = None


def get_client() -> OpenAI:
    """Return a lazily initialized OpenAI client."""
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set. Copy .env.example to .env and add your key.")
        _client = OpenAI(api_key=api_key)
    return _client


def call_llm(system_prompt: str, user_text: str) -> dict[str, str | int]:
    """
    Call the LLM with a system prompt and user text.

    Returns dict with 'content', 'tokens', and 'model' keys.
    Handles errors gracefully with specific messages.
    """
    try:
        response = get_client().chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text},
            ],
            temperature=0.7,
            max_tokens=500,
        )
        return {
            "content": response.choices[0].message.content or "",
            "tokens": response.usage.total_tokens if response.usage else 0,
            "model": response.model,
        }
    except AuthenticationError:
        return {
            "content": "Error: Invalid API key. Check your .env file.",
            "tokens": 0,
            "model": "N/A",
        }
    except RateLimitError:
        return {
            "content": "Error: Rate limit hit. Wait a moment and try again.",
            "tokens": 0,
            "model": "N/A",
        }
    except APIConnectionError:
        return {
            "content": "Error: Cannot connect to OpenAI. Check your internet.",
            "tokens": 0,
            "model": "N/A",
        }
    except Exception as e:
        return {"content": f"Error: {e}", "tokens": 0, "model": "N/A"}
