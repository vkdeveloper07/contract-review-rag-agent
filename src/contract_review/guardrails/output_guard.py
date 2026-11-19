from contract_review.guardrails.result import GuardrailResult


def check_output(answer: str, context: str) -> GuardrailResult:
    if not context.strip():
        return GuardrailResult("output", False, "no supporting contract passages were found")
    if "[" not in answer or "]" not in answer:
        return GuardrailResult("output", False, "answer is missing source citations")
    return GuardrailResult("output", True, "answer includes source citations")
