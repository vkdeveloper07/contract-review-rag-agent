from contract_review.agent.state import AgentState
from contract_review.config import settings
from contract_review.guardrails.input_guard import check_input
from contract_review.guardrails.output_guard import check_output
from contract_review.rag.context_builder import build_context
from contract_review.rag.generator import generate_answer
from contract_review.rag.query_rewriter import rewrite_query
from contract_review.rag.retriever import retrieve


def input_guard_node(state: AgentState) -> dict:
    return {"guardrail": check_input(state["question"])}


def rewrite_query_node(state: AgentState) -> dict:
    return {"search_query": rewrite_query(state["question"])}


def retrieve_node(state: AgentState, collection) -> dict:
    return {"chunks": retrieve(state["search_query"], settings.top_k, collection)}


def build_context_node(state: AgentState) -> dict:
    return {"context": build_context(state.get("chunks", []))}


def generate_node(state: AgentState) -> dict:
    answer, demo_mode = generate_answer(state["question"], state.get("context", ""))
    return {"answer": answer, "demo_mode": demo_mode}


def output_guard_node(state: AgentState) -> dict:
    result = check_output(state.get("answer", ""), state.get("context", ""))
    if not result.allowed:
        return {"answer": "I couldn't produce a sufficiently supported answer. Review the retrieved passages below or try a more specific question.", "guardrail": result}
    return {"guardrail": result}


def refuse_node(state: AgentState) -> dict:
    reason = state.get("guardrail")
    if reason and reason.guard == "input":
        answer = "I can't process that question. Please ask a direct question about a clause in the uploaded contract."
    else:
        answer = "I couldn't find a relevant passage in the uploaded contracts. Try different wording or check the document text."
    return {"answer": answer, "chunks": []}


def route_after_input(state: AgentState) -> str:
    return "continue" if state["guardrail"].allowed else "refuse"


def route_after_output(state: AgentState) -> str:
    return "end" if state["guardrail"].allowed else "refuse"
