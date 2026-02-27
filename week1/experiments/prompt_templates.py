JSON_SCHEMA_EMBEDDINGS = """
Return ONLY valid JSON.

Schema:
{
  "topic": "string",
  "bullets": ["string", "string", "string", "string"],
  "example": "string"
}
"""

def make_embeddings_prompt() -> str:
    return JSON_SCHEMA_EMBEDDINGS + "\nTopic: embeddings\n"