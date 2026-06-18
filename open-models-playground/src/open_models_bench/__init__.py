"""open_models_bench: a small toolkit for benchmarking local open models via Ollama.

Public API:
    OllamaClient       -- thin wrapper around the local Ollama HTTP API
    PromptCase         -- a single evaluation prompt
    BenchmarkResult    -- the measured result for one (model, prompt) pair
    run_benchmark      -- run a suite of prompts across a list of models
"""

from .client import OllamaClient
from .models import PromptCase, BenchmarkResult
from .benchmark import run_benchmark

__all__ = [
    "OllamaClient",
    "PromptCase",
    "BenchmarkResult",
    "run_benchmark",
]

__version__ = "0.1.0"
