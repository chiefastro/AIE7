"""Safety guard configuration and helpers for use in LangGraph agents.

This module wraps Guardrails validators into a compact, reusable interface
with no side effects at import time. It exposes a `SafetyGuards` class with
`run_input` and `run_output` helpers as well as a `build_default_guards`
factory for common production defaults.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional


try:  # Optional dependency: guardrails-ai
    from guardrails.hub import (
        RestrictToTopic,
        DetectJailbreak,
        LlmRagEvaluator,
        HallucinationPrompt,
        ProfanityFree,
        GuardrailsPII,
    )
    from guardrails import Guard

    _GUARDRAILS_AVAILABLE = True
except Exception:  # pragma: no cover - we gracefully degrade if missing
    RestrictToTopic = DetectJailbreak = LlmRagEvaluator = HallucinationPrompt = None  # type: ignore
    ProfanityFree = GuardrailsPII = Guard = None  # type: ignore
    _GUARDRAILS_AVAILABLE = False


@dataclass
class GuardCheckOutcome:
    """Outcome of a single guard check."""

    name: str
    passed: bool
    message: str = ""
    validated_text: Optional[str] = None


@dataclass
class GuardRunResult:
    """Aggregated result from running a set of guards."""

    passed: bool
    validated_text: str
    checks: List[GuardCheckOutcome]


class SafetyGuards:
    """Wrapper around Guardrails validators for input and output checks.

    Instances are lightweight and safe to construct at runtime.
    When Guardrails is not installed, all checks pass-through by default.
    """

    def __init__(
        self,
        *,
        topic_guard: Optional[Any] = None,
        jailbreak_guard: Optional[Any] = None,
        pii_guard: Optional[Any] = None,
        profanity_guard: Optional[Any] = None,
        factuality_guard: Optional[Any] = None,
    ) -> None:
        self.topic_guard = topic_guard
        self.jailbreak_guard = jailbreak_guard
        self.pii_guard = pii_guard
        self.profanity_guard = profanity_guard
        self.factuality_guard = factuality_guard

    def run_input(self, text: str) -> GuardRunResult:
        """Validate and possibly transform user input.

        Order: topic -> jailbreak -> PII
        """
        checks: List[GuardCheckOutcome] = []
        current_text = text

        if not _GUARDRAILS_AVAILABLE:
            return GuardRunResult(True, current_text, checks)

        # Topic restriction
        if self.topic_guard is not None:
            try:
                self.topic_guard.validate(current_text)
                checks.append(GuardCheckOutcome("topic", True))
            except Exception as exc:  # configured as on_fail="exception"
                checks.append(GuardCheckOutcome("topic", False, str(exc)))

        # Jailbreak detection
        if self.jailbreak_guard is not None:
            try:
                result = self.jailbreak_guard.validate(current_text)
                passed = getattr(result, "validation_passed", True)
                checks.append(GuardCheckOutcome("jailbreak", bool(passed)))
            except Exception as exc:
                checks.append(GuardCheckOutcome("jailbreak", False, str(exc)))

        # PII redaction (on_fail="fix")
        if self.pii_guard is not None:
            try:
                result = self.pii_guard.validate(current_text)
                redacted = getattr(result, "validated_output", current_text)
                if isinstance(redacted, str) and redacted:
                    current_text = redacted
                checks.append(GuardCheckOutcome("pii", True, validated_text=current_text))
            except Exception as exc:
                checks.append(GuardCheckOutcome("pii", False, str(exc)))

        overall_passed = all(c.passed for c in checks) if checks else True
        return GuardRunResult(overall_passed, current_text, checks)

    def run_output(self, text: str) -> GuardRunResult:
        """Validate and possibly transform model output.

        Order: profanity -> factuality
        """
        checks: List[GuardCheckOutcome] = []
        current_text = text

        if not _GUARDRAILS_AVAILABLE:
            return GuardRunResult(True, current_text, checks)

        # Content moderation
        if self.profanity_guard is not None:
            try:
                self.profanity_guard.validate(current_text)
                checks.append(GuardCheckOutcome("profanity", True))
            except Exception as exc:  # configured as on_fail="exception"
                checks.append(GuardCheckOutcome("profanity", False, str(exc)))

        # Factuality (LLM-based evaluator)
        if self.factuality_guard is not None:
            try:
                result = self.factuality_guard.validate(current_text)
                passed = getattr(result, "validation_passed", True)
                checks.append(GuardCheckOutcome("factuality", bool(passed)))
            except Exception as exc:
                checks.append(GuardCheckOutcome("factuality", False, str(exc)))

        overall_passed = all(c.passed for c in checks) if checks else True
        return GuardRunResult(overall_passed, current_text, checks)


def build_default_guards(
    *,
    valid_topics: Optional[List[str]] = None,
    invalid_topics: Optional[List[str]] = None,
    llm_callable: str = "gpt-4.1-mini",
    enable_topic: bool = True,
    enable_jailbreak: bool = True,
    enable_pii: bool = True,
    enable_profanity: bool = True,
    enable_factuality: bool = True,
) -> SafetyGuards:
    """Factory for a production default set of safety guards.

    Returns a `SafetyGuards` instance. If Guardrails is not installed,
    returns a pass-through set that always approves.
    """

    if not _GUARDRAILS_AVAILABLE:
        return SafetyGuards()

    # Defaults tailored to student-loan assistant
    valid_topics = valid_topics or [
        "student loans",
        "financial aid",
        "education financing",
        "loan repayment",
    ]
    invalid_topics = invalid_topics or [
        "investment advice",
        "crypto",
        "gambling",
        "politics",
    ]

    topic_guard = (
        Guard().use(
            RestrictToTopic(
                valid_topics=valid_topics,
                invalid_topics=invalid_topics,
                disable_classifier=True,
                disable_llm=False,
                on_fail="exception",
            )
        )
        if enable_topic
        else None
    )

    jailbreak_guard = Guard().use(DetectJailbreak()) if enable_jailbreak else None

    pii_guard = (
        Guard().use(
            GuardrailsPII(
                entities=["CREDIT_CARD", "SSN", "PHONE_NUMBER", "EMAIL_ADDRESS"],
                on_fail="fix",
            )
        )
        if enable_pii
        else None
    )

    profanity_guard = (
        Guard().use(ProfanityFree(threshold=0.8, validation_method="sentence", on_fail="exception"))
        if enable_profanity
        else None
    )

    factuality_guard = (
        Guard().use(
            LlmRagEvaluator(
                eval_llm_prompt_generator=HallucinationPrompt(prompt_name="hallucination_judge_llm"),
                llm_evaluator_fail_response="hallucinated",
                llm_evaluator_pass_response="factual",
                llm_callable=llm_callable,
                on_fail="exception",
                on="prompt",
            )
        )
        if enable_factuality
        else None
    )

    return SafetyGuards(
        topic_guard=topic_guard,
        jailbreak_guard=jailbreak_guard,
        pii_guard=pii_guard,
        profanity_guard=profanity_guard,
        factuality_guard=factuality_guard,
    )


__all__ = [
    "SafetyGuards",
    "GuardRunResult",
    "GuardCheckOutcome",
    "build_default_guards",
]


