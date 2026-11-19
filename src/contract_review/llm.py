import os
from functools import lru_cache

from contract_review.config import settings


def build_chat_model(openai_model: str, ollama_model: str):
    if settings.llm_provider == "ollama":
        from langchain_ollama import ChatOllama

        return ChatOllama(model=ollama_model, temperature=0)
    if settings.llm_provider == "openai":
        if not os.getenv("OPENAI_API_KEY", "").strip():
            return None
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(model=openai_model, temperature=0)
    if settings.llm_provider == "none":
        return None
    raise ValueError("LLM_PROVIDER must be openai, ollama, or none")


@lru_cache
def get_agent_model():
    return build_chat_model(settings.openai_agent_model, settings.ollama_agent_model)


@lru_cache
def get_guardrail_model():
    return build_chat_model(settings.openai_guardrail_model, settings.ollama_guardrail_model)
