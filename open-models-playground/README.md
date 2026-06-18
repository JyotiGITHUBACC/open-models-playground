# Open Models Playground

A small, dependency-light Python toolkit for **benchmarking and comparing local open models** served by [Ollama](https://ollama.com). Give it a list of models and a suite of prompts; it measures latency and throughput, then writes a JSON file and a Markdown comparison table you can paste straight into a report.

Built to explore the practical trade-offs that matter when adopting open-weight models (Llama, Gemma, Qwen, and friends): **how fast, how cheap, and how good** for a given task.

> Why this exists: choosing an open model is a product decision, not just a technical one. This tool turns "which model should we use?" into a side-by-side table of evidence.

---

## Features

- Runs any number of models against a shared prompt suite
- Measures wall-clock latency, token counts, and tokens/sec
- Outputs both machine-readable JSON and a human-readable Markdown table
- Graceful error handling — a failing model is recorded, not fatal
- Zero heavy dependencies (only `requests`); unit-tested core
- Clean, documented, type-hinted Python you can read in one sitting

---

## Project structure

```
open-models-playground/
├── src/open_models_bench/
│   ├── __init__.py        # public API
│   ├── client.py          # thin Ollama HTTP client
│   ├── models.py          # PromptCase + BenchmarkResult dataclasses
│   ├── prompts.py         # the default prompt suite
│   ├── benchmark.py       # the run loop
│   ├── report.py          # JSON + Markdown rendering
│   └── cli.py             # command-line entry point
├── tests/                 # pytest unit tests (no Ollama required)
├── results/               # generated output lands here
├── docs/                  # extra notes and a getting-started guide
├── pyproject.toml         # packaging + tooling config
├── requirements.txt
└── README.md
```

---

## Prerequisites

1. **Python 3.10+**
2. **[Ollama](https://ollama.com/download)** installed and running locally
3. At least one model pulled, for example:

   ```bash
   ollama pull llama3.2
   ollama pull gemma2
   ollama pull qwen2.5
   ```

---

## Quick start

```bash
# 1. Clone your repo
git clone https://github.com/<your-username>/open-models-playground.git
cd open-models-playground

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the benchmark (compares three models)
python -m open_models_bench --models llama3.2 gemma2 qwen2.5
```

Omit `--models` to benchmark every model Ollama currently has installed.

---

## Example output

The tool prints a table like this and saves it to `results/results.md`:

| Model | Prompt | Category | Latency (s) | Tokens | Tokens/sec | Output preview |
| --- | --- | --- | ---: | ---: | ---: | --- |
| llama3.2 | summarize | summarization | 1.84 | 142 | 77.17 | Open-weight models let teams run AI locally for cost, privacy, and latency control… |
| gemma2 | summarize | summarization | 2.61 | 158 | 60.54 | Running open models locally gives teams control over cost and privacy, but… |
| qwen2.5 | summarize | summarization | 2.07 | 150 | 72.46 | Open models can be run on local hardware, which improves privacy and cost… |

> The numbers above are illustrative. Your results depend on your hardware, the models you pull, and the prompts you run.

See [`results/results.example.md`](results/results.example.md) for a full sample.

---

## How it works

1. `cli.py` parses your arguments and confirms Ollama is reachable.
2. `benchmark.py` loops over every (model, prompt) pair, calling `client.py`.
3. Each call to the Ollama `/api/generate` endpoint is timed; token counts come from the response.
4. `report.py` serialises everything to JSON and renders the Markdown table.

---

## Running the tests

The core logic is unit-tested and **does not require Ollama** to be installed:

```bash
pip install -r requirements-dev.txt
pytest
```

---

## Extending it

- **Add your own prompts:** edit `src/open_models_bench/prompts.py`.
- **Score quality, not just speed:** `BenchmarkResult.raw` holds the full response if you want to add a scoring step.
- **Try a different backend:** `client.py` is the only file that talks to Ollama — swap it to target another local server.

---

## Roadmap

- [ ] Optional quality scoring with a judge model
- [ ] CSV export
- [ ] Side-by-side diff view of two models' answers

---

## License

[MIT](LICENSE) © 2026 Jyoti Shukla
