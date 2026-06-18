"""A small, fixed suite of evaluation prompts.

Keeping the suite in code (rather than a config file) makes the project easy to
read and run for a newcomer. Swap these out for prompts that matter to your own
use case.
"""

from __future__ import annotations

from .models import PromptCase

DEFAULT_PROMPTS: list[PromptCase] = [
    PromptCase(
        name="summarize",
        category="summarization",
        prompt=(
            "Summarize the following in two sentences: Open-weight language "
            "models let teams run AI locally, controlling cost, privacy, and "
            "latency, but they require careful evaluation of quality and "
            "hardware fit before adoption."
        ),
    ),
    PromptCase(
        name="reasoning",
        category="reasoning",
        prompt=(
            "A team can deploy a model that is 90% as accurate but 5x cheaper "
            "to run. List three questions a product manager should ask before "
            "choosing it."
        ),
    ),
    PromptCase(
        name="code-explain",
        category="coding",
        prompt=(
            "Explain in plain English what this Python line does: "
            "result = sorted(items, key=lambda x: x.score, reverse=True)"
        ),
    ),
]
