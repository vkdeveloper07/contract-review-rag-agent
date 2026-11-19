import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


@dataclass(frozen=True)
class Settings:
    llm_provider: str = os.getenv("LLM_PROVIDER", "openai").lower()
    openai_agent_model: str = os.getenv("OPENAI_AGENT_MODEL", "gpt-4o-mini")
    openai_guardrail_model: str = os.getenv("OPENAI_GUARDRAIL_MODEL", "gpt-4o-mini")
    ollama_agent_model: str = os.getenv("OLLAMA_AGENT_MODEL", "llama3.1:8b")
    ollama_guardrail_model: str = os.getenv("OLLAMA_GUARDRAIL_MODEL", "llama3.1:8b")
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "200"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "40"))
    top_k: int = int(os.getenv("TOP_K", "4"))


settings = Settings()
