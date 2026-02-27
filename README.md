# Local LLM Extractor API (FastAPI + Ollama)

A production-style GenAI microservice that converts unstructured text into structured JSON using a local LLM (Ollama).

This project demonstrates:
- Structured LLM prompting
- Defensive JSON parsing
- Schema validation with Pydantic
- Retry logic for transient failures
- Observability logging
- Automated tests with pytest

---

## Features

- `POST /extractor`
  - `mode=summary`
  - `mode=action_items`
- Strict JSON-only prompting
- Defensive JSON extraction (handles markdown fences, trailing commas)
- Response schema validation
- Retry mechanism for LLM calls
- Observability logging to `api_runs.jsonl`
- Unit tests for parsing and health endpoint

---

## Architecture

Client → FastAPI → Prompt Template → Local LLM (Ollama) → JSON Extraction → Pydantic Validation → Response

The system is backend-agnostic and can later be connected to OpenAI or Azure OpenAI.

---

## Requirements

- Python 3.11
- Ollama installed
- Model pulled (example: `llama3.1:8b`)

---

## Setup

```bash
python -m venv genai311
# activate environment
pip install -r requirements.txt