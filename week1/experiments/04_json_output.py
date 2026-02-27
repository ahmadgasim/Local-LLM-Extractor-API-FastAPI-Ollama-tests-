from llm_client import OllamaLLM
from json_utils import extract_first_json

llm = OllamaLLM(model="llama3.1:8b")

prompt = """
Return ONLY valid JSON (no markdown, no extra text).

Schema:
{
  "topic": "string",
  "bullets": ["string", "string", "string", "string"],
  "example": "string"
}

Topic: embeddings
"""

raw = llm.generate(prompt, temperature=0.2)
data = extract_first_json(raw)

print("Parsed OK ✅")
print(data)