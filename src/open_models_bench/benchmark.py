"""Run a suite of prompts across several models and collect the results."""

from __future__ import annotations

from .client import OllamaClient
from .models import BenchmarkResult, PromptCase

# How many characters of the model output to keep for the at-a-glance table.
PREVIEW_CHARS = 160


def _preview(text: str, limit: int = PREVIEW_CHARS) -> str:
    """Collapse whitespace and trim text to a short single-line preview."""
    collapsed = " ".join(text.split())
    if len(collapsed) <= limit:
        return collapsed
    return collapsed[: limit - 1].rstrip() + "\u2026"


def run_single(
    client: OllamaClient, model: str, case: PromptCase
) -> BenchmarkResult:
    """Run one prompt against one model, capturing timing or any error."""
    try:
        result = client.generate(model=model, prompt=case.prompt)
        return BenchmarkResult(
            model=model,
            prompt_name=case.name,
            category=case.category,
            latency_seconds=round(result["latency"], 2),
            total_tokens=result["total_tokens"],
            response_preview=_preview(result["response"]),
            raw=result["raw"],
        )
    except Exception as exc:  # noqa: BLE001 - we want to record any failure
        return BenchmarkResult(
            model=model,
            prompt_name=case.name,
            category=case.category,
            latency_seconds=0.0,
            total_tokens=0,
            response_preview="",
            error=str(exc),
        )


def run_benchmark(
    models: list[str],
    cases: list[PromptCase],
    client: OllamaClient | None = None,
    verbose: bool = True,
) -> list[BenchmarkResult]:
    """Run every prompt against every model.

    Args:
        models: Ollama model names, e.g. ["llama3.2", "gemma2", "qwen2.5"].
        cases: The prompts to evaluate.
        client: An OllamaClient; one is created with defaults if omitted.
        verbose: Print progress as the benchmark runs.

    Returns:
        A flat list of BenchmarkResult, one per (model, prompt) pair.
    """
    client = client or OllamaClient()
    results: list[BenchmarkResult] = []

    for model in models:
        for case in cases:
            if verbose:
                print(f"  Running [{model}] on '{case.name}' ...", flush=True)
            result = run_single(client, model, case)
            if verbose and result.error:
                print(f"    ! error: {result.error}", flush=True)
            results.append(result)

    return results
