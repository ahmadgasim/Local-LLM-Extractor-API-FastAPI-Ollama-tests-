from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

import json
from datetime import datetime

from week1.experiments.llm_client import OllamaLLM
from week1.experiments.json_utils import extract_first_json

app = FastAPI()
llm = OllamaLLM(model="llama3.1:8b")

def log_api_run(endpoint: str, model: str, temperature: float, input_text: str, prompt: str, raw: str):
    record = {
        "ts": datetime.utcnow().isoformat() + "Z",
        "endpoint": endpoint,
        "model": model,
        "temperature": temperature,
        "input_text": input_text,
        "prompt": prompt,
        "raw": raw,
    }
    with open(r"week1/experiments/api_runs.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

class ExtractRequest(BaseModel):
    text: str


class ExtractorRequest(BaseModel):
    text: str
    mode: str  # "summary" or "action_items"


class ExtractResponse(BaseModel):
    summary: str
    key_points: list[str]


class ActionItem(BaseModel):
    owner: str
    task: str
    due_date: Optional[str] = None   # e.g., "Monday"
    priority: Optional[str] = None   # "high" | "medium" | "low"

class ActionItemsResponse(BaseModel):
    action_items: list[ActionItem]

@app.get("/health")
def health():
    return {"ok": True, "model": llm.model}


@app.post("/extract")
def extract(req: ExtractRequest):
    prompt = f"""
Return ONLY valid JSON (no markdown, no extra text).

Schema: 
{{
  "summary": "string",
  "key_points": ["string", "string", "string"]
}}

Text:
{req.text}
""".strip()

    try:
        raw = llm.generate(prompt, temperature=0.2)
        log_api_run("/extract", llm.model, 0.2, req.text, prompt, raw)
        data = extract_first_json(raw)

        # Validate schema strictly
        validated = ExtractResponse(**data)

        return {"ok": True, "data": validated.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/action-items")
def action_items(req: ExtractRequest):
    prompt = f"""
Return ONLY valid JSON (no markdown, no extra text).

Schema:
{{
  "action_items": [
    {{
      "owner": "string",
      "task": "string",
      "due_date": "string|null",
      "priority": "high|medium|low|null"
    }}
  ]
}}

Rules:
- Extract ALL action items mentioned in the text. Do not omit any.
- If owner is not explicit, use "Unknown".
- If due date is not explicit, use null.
- Keep tasks short (3–10 words) and actionable (verb first).
- Priority: "high" if deadline soon/explicit, else "medium" if important, else "low".
- If you are unsure, still include the item with best guess and nulls.


Text:
{req.text}
""".strip()

    try:
        raw = llm.generate(prompt, temperature=0.2)
        log_api_run("/action-items", llm.model, 0.2, req.text, prompt, raw)
        data = extract_first_json(raw)

        validated = ActionItemsResponse(**data)
        if not validated.action_items:
            raise ValueError("No action items extracted.")

        return {"ok": True, "data": validated.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# @app.post("/extractor")
# def extractor(req: ExtractorRequest):
#     mode = req.mode.strip().lower()

#     try:
#         if mode == "summary":
#             prompt = f"""
# Return ONLY valid JSON (no markdown, no extra text).

# Schema:
# {{
#   "summary": "string",
#   "key_points": ["string", "string", "string"]
# }}

# Text:
# {req.text}
# """.strip()

#             raw = llm.generate(prompt, temperature=0.2)
#             log_api_run("/extractor:summary", llm.model, 0.2, req.text, prompt, raw)
#             data = extract_first_json(raw)
#             validated = ExtractResponse(**data)
#             return {"ok": True, "data": validated.model_dump()}

#         elif mode == "action_items":
#             prompt = f"""
# Return ONLY valid JSON (no markdown, no extra text).

# Schema:
# {{
#   "action_items": [
#     {{
#       "owner": "string",
#       "task": "string",
#       "due_date": "string|null",
#       "priority": "high|medium|low|null"
#     }}
#   ]
# }}

# Rules:
# - Extract ALL action items mentioned in the text. Do not omit any.
# - If owner is not explicit, use "Unknown".
# - If due date is not explicit, use null.
# - Keep tasks short (3–10 words) and actionable (verb first).
# - Priority: "high" if deadline soon/explicit, else "medium" if important, else "low".

# Text:
# {req.text}
# """.strip()

#             raw = llm.generate(prompt, temperature=0.2)
#             log_api_run("/extractor:action_items", llm.model, 0.2, req.text, prompt, raw)
#             data = extract_first_json(raw)
#             validated = ActionItemsResponse(**data)
#             if not validated.action_items:
#                 raise ValueError("No action items extracted.")
#             return {"ok": True, "data": validated.model_dump()}

#         else:
#             raise HTTPException(status_code=400, detail="mode must be 'summary' or 'action_items'")

#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@app.post("/extractor")
def extractor(req: ExtractorRequest):
    mode = req.mode.strip().lower()

    if mode not in {"summary", "action_items"}:
        raise HTTPException(status_code=400, detail="mode must be 'summary' or 'action_items'")

    try:
        if mode == "summary":
            prompt = f"""
Return ONLY valid JSON (no markdown, no extra text).

Schema:
{{
  "summary": "string",
  "key_points": ["string", "string", "string"]
}}

Text:
{req.text}
""".strip()

        else:  # action_items
            prompt = f"""
Return ONLY valid JSON (no markdown, no extra text).

Schema:
{{
  "action_items": [
    {{
      "owner": "string",
      "task": "string",
      "due_date": "string|null",
      "priority": "high|medium|low|null"
    }}
  ]
}}

Rules:
- Extract ALL action items mentioned in the text.
- If owner is not explicit, use "Unknown".
- If due date is not explicit, use null.
- Keep tasks short and actionable.
- Priority: "high" if deadline soon/explicit, else "medium" if important, else "low".

Text:
{req.text}
""".strip()

        raw = llm.generate(prompt, temperature=0.2)
        log_api_run(f"/extractor:{mode}", llm.model, 0.2, req.text, prompt, raw)

        # Step 1: JSON extraction
        try:
            data = extract_first_json(raw)
        except Exception:
            raise HTTPException(status_code=422, detail="Model returned invalid JSON")

        # Step 2: Schema validation
        try:
            if mode == "summary":
                validated = ExtractResponse(**data)
            else:
                validated = ActionItemsResponse(**data)
        except Exception:
            raise HTTPException(status_code=422, detail="JSON schema validation failed")

        return {"ok": True, "data": validated.model_dump()}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")