"""Unit tests for the data models. These run without Ollama installed."""

from open_models_bench.models import BenchmarkResult, PromptCase


def test_prompt_case_defaults():
    case = PromptCase(name="t", prompt="hello")
    assert case.category == "general"


def test_tokens_per_second_normal():
    result = BenchmarkResult(
        model="m",
        prompt_name="p",
        category="general",
        latency_seconds=2.0,
        total_tokens=100,
        response_preview="ok",
    )
    assert result.tokens_per_second == 50.0


def test_tokens_per_second_handles_error():
    result = BenchmarkResult(
        model="m",
        prompt_name="p",
        category="general",
        latency_seconds=0.0,
        total_tokens=0,
        response_preview="",
        error="boom",
    )
    assert result.tokens_per_second == 0.0


def test_to_dict_excludes_raw_and_adds_throughput():
    result = BenchmarkResult(
        model="m",
        prompt_name="p",
        category="general",
        latency_seconds=1.0,
        total_tokens=10,
        response_preview="hi",
        raw={"big": "payload"},
    )
    data = result.to_dict()
    assert "raw" not in data
    assert data["tokens_per_second"] == 10.0
