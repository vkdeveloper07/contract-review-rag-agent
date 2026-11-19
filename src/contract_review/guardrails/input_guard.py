import re

from contract_review.guardrails.result import GuardrailResult

INJECTION = re.compile(r"ignore (all |any )?(previous|prior|above) instructions|reveal .*system prompt|you are now|jailbreak", re.I)


def check_input(question: str) -> GuardrailResult:
    if len(question) > 1000:
        return GuardrailResult("input", False, "question is longer than 1,000 characters")
    if INJECTION.search(question):
        return GuardrailResult("input", False, "prompt injection phrase detected")
    return GuardrailResult("input", True, "question accepted")
