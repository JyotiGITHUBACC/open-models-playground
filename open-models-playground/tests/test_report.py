"""Unit tests for the Markdown report rendering."""

from open_models_bench.models import BenchmarkResult
from open_models_bench.report import to_markdown_table


def _sample_result(**overrides):
    base = dict(
        model="llama3.2",
        prompt_name="summarize",
        category="summarization",
        latency_seconds=1.5,
        total_tokens=60,
        response_preview="A short summary.",
    )
    base.update(overrides)
    return BenchmarkResult(**base)


def test_table_has_header_and_row():
    table = to_markdown_table([_sample_result()])
    assert "| Model |" in table
    assert "llama3.2" in table
    assert "summarize" in table


def test_table_escapes_pipes_in_preview():
    table = to_markdown_table([_sample_result(response_preview="a | b")])
    assert "a \\| b" in table


def test_table_shows_error():
    table = to_markdown_table([_sample_result(error="timeout")])
    assert "ERROR: timeout" in table
