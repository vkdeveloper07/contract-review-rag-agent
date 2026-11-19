from contract_review.llm import get_agent_model

REWRITE_PROMPT = """Rewrite this question as a short search query for a contract. Keep the legal/commercial terms and return only the query.

Question: {question}"""


def rewrite_query(question: str) -> str:
    model = get_agent_model()
    if model is None:
        return question
    return model.invoke(REWRITE_PROMPT.format(question=question)).text.strip().strip('"')
