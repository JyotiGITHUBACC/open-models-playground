# Getting Started

This guide walks through running your first benchmark from a clean machine.

## 1. Install Ollama

Download from [ollama.com/download](https://ollama.com/download) and install.
Verify it is running:

```bash
ollama --version
ollama serve        # starts the local server if it isn't already running
```

## 2. Pull a few open models

Smaller models download faster and run on modest hardware:

```bash
ollama pull llama3.2
ollama pull gemma2
ollama pull qwen2.5
```

List what you have:

```bash
ollama list
```

## 3. Set up the project

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 4. Run it

```bash
python -m open_models_bench --models llama3.2 gemma2 qwen2.5
```

Your results land in `results/results.json` and `results/results.md`.

## 5. Interpret the numbers

- **Latency (s):** lower is better — how long the full answer took.
- **Tokens/sec:** higher is better — raw generation throughput.
- **Output preview:** a quick sense of answer quality; open the JSON for full text.

A model that is slightly slower but noticeably more accurate may still be the
right product choice. Speed is one axis; quality and cost are the others.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| "Could not reach Ollama" | Run `ollama serve` in another terminal. |
| "No models found" | Pull one: `ollama pull llama3.2`. |
| A single model errors | The run continues; the error is recorded in the table. |
