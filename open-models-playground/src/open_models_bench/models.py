"""Data models used across the benchmark.

These are plain dataclasses so the project stays dependency-light and easy to
read. Each class documents exactly what it carries and why.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass(frozen=True)
class PromptCase:
    """A single evaluation prompt.

    Attributes:
        name: A short, human-readable label (used in the results table).
        prompt: The actual text sent to the model.
        category: A loose grouping such as "reasoning" or "summarization",
            useful when you want to compare models per task type.
    """

    name: str
    prompt: str
    category: str = "general"


@dataclass
class BenchmarkResult:
    """The measured outcome for one (model, prompt) pair.

    Latency and token counts let you reason about cost/performance trade-offs,
    which is the whole point of comparing open models.
    """

    model: str
    prompt_name: str
    category: str
    latency_seconds: float
    total_tokens: int
    response_preview: str
    error: str | None = None
    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @property
    def tokens_per_second(self) -> float:
        """Throughput in tokens/sec. Returns 0.0 when it cannot be computed."""
        if self.error or self.latency_seconds <= 0:
            return 0.0
        return round(self.total_tokens / self.latency_seconds, 2)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable dict (excludes the bulky raw payload)."""
        data = asdict(self)
        data.pop("raw", None)
        data["tokens_per_second"] = self.tokens_per_second
        return data
