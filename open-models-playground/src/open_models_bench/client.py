"""A thin client for the local Ollama HTTP API.

Ollama (https://ollama.com) runs open models locally and exposes a simple HTTP
endpoint on http://localhost:11434. We only need the /api/generate route, so
this wrapper stays deliberately small and dependency-light (just `requests`).
"""

from __future__ import annotations

import time

import requests


class OllamaClient:
    """Minimal wrapper around the Ollama generate endpoint.

    Args:
        host: Base URL of the running Ollama server.
        timeout: Per-request timeout in seconds.
    """

    def __init__(self, host: str = "http://localhost:11434", timeout: int = 120) -> None:
        self.host = host.rstrip("/")
        self.timeout = timeout

    def is_available(self) -> bool:
        """Return True if an Ollama server responds on the configured host."""
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def list_models(self) -> list[str]:
        """Return the names of models currently pulled into Ollama."""
        response = requests.get(f"{self.host}/api/tags", timeout=self.timeout)
        response.raise_for_status()
        payload = response.json()
        return [entry["name"] for entry in payload.get("models", [])]

    def generate(self, model: str, prompt: str) -> dict:
        """Send a single prompt to a model and return the parsed response.

        Returns a dict with at least:
            response       -- the generated text
            latency        -- wall-clock seconds we measured
            total_tokens   -- prompt + completion tokens (best effort)
        """
        body = {"model": model, "prompt": prompt, "stream": False}

        start = time.perf_counter()
        response = requests.post(
            f"{self.host}/api/generate", json=body, timeout=self.timeout
        )
        latency = time.perf_counter() - start
        response.raise_for_status()

        payload = response.json()
        prompt_tokens = payload.get("prompt_eval_count", 0)
        completion_tokens = payload.get("eval_count", 0)

        return {
            "response": payload.get("response", ""),
            "latency": latency,
            "total_tokens": prompt_tokens + completion_tokens,
            "raw": payload,
        }
