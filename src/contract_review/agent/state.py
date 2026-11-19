from typing import TypedDict

from contract_review.guardrails.result import GuardrailResult
from contract_review.rag.models import RetrievedChunk


class AgentState(TypedDict, total=False):
    question: str
    search_query: str
    chunks: list[RetrievedChunk]
    context: str
    answer: str
    demo_mode: bool
    guardrail: GuardrailResult
