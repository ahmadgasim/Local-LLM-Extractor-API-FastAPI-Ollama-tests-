import json
import re
from typing import Any, Dict

def extract_first_json(text: str) -> Dict[str, Any]:
    """
    Extract and parse the first JSON object found in a model response.
    Raises ValueError with a clear message if parsing fails.
    """
    if not text or not text.strip():
        raise ValueError("Empty response; no JSON to parse.")

    # 1) Remove markdown fences (```json ... ```)
    cleaned = re.sub(r"```(?:json)?\s*", "", text, flags=re.IGNORECASE).replace("```", "").strip()

    # 2) Heuristic: take substring from first '{' to last '}'
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("No JSON object braces found in response.")

    candidate = cleaned[start : end + 1].strip()

    # 3) Try normal parse
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        # 4) Common fix: remove trailing commas before } or ]
        candidate2 = re.sub(r",\s*([}\]])", r"\1", candidate)
        try:
            return json.loads(candidate2)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON. Candidate starts with: {candidate[:80]!r}") from e