"""Command-line entry point.

Usage:
    python -m open_models_bench --models llama3.2 gemma2 qwen2.5

If --models is omitted, every model currently available in Ollama is used.
"""

from __future__ import annotations

import argparse
import sys

from .benchmark import run_benchmark
from .client import OllamaClient
from .prompts import DEFAULT_PROMPTS
from .report import save_json, save_markdown, to_markdown_table


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="open_models_bench",
        description="Benchmark local open models served by Ollama.",
    )
    parser.add_argument(
        "--models",
        nargs="*",
        default=None,
        help="Model names to test (default: all models available in Ollama).",
    )
    parser.add_argument(
        "--host",
        default="http://localhost:11434",
        help="Ollama server URL (default: http://localhost:11434).",
    )
    parser.add_argument(
        "--json-out",
        default="results/results.json",
        help="Where to write the JSON results.",
    )
    parser.add_argument(
        "--md-out",
        default="results/results.md",
        help="Where to write the Markdown results table.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    client = OllamaClient(host=args.host)

    if not client.is_available():
        print(
            "Could not reach Ollama at "
            f"{args.host}. Is it running? Try `ollama serve`.",
            file=sys.stderr,
        )
        return 1

    models = args.models or client.list_models()
    if not models:
        print(
            "No models found. Pull one first, e.g. `ollama pull llama3.2`.",
            file=sys.stderr,
        )
        return 1

    print(f"Benchmarking {len(models)} model(s) on {len(DEFAULT_PROMPTS)} prompt(s):")
    results = run_benchmark(models=models, cases=DEFAULT_PROMPTS, client=client)

    json_path = save_json(results, args.json_out)
    md_path = save_markdown(results, args.md_out)

    print("\nResults\n")
    print(to_markdown_table(results))
    print(f"\nSaved JSON  -> {json_path}")
    print(f"Saved table -> {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
