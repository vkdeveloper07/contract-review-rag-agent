from contract_review.llm import get_agent_model

ANSWER_PROMPT = """You are a careful contract review assistant. Answer using only the contract context. Never invent terms or fill gaps with assumptions. Cite each finding with the provided source number, such as [1]. State clearly when the evidence is incomplete or silent. Summarize relevant obligations, deadlines, exceptions, and risks in plain English. This is not legal advice; recommend qualified counsel for consequential decisions.

Context:
{context}

Question: {question}"""


def generate_answer(question: str, context: str) -> tuple[str, bool]:
    model = get_agent_model()
    if model is None:
        if not context:
            return "I couldn't find a relevant passage in the uploaded contracts. Try different wording or verify that the files contain selectable text.", True
        return "I found these relevant contract excerpts. Configure an LLM in .env to get a plain-English synthesis:\n\n" + context, True
    response = model.invoke(ANSWER_PROMPT.format(context=context, question=question))
    return response.text.strip(), False
