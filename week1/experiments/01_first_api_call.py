import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("OPENAI_API_KEY not found in .env")

client = OpenAI(api_key=api_key)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a strict technical tutor."},
        {"role": "user", "content": "Explain what embeddings are in 4 bullet points."}
    ],
    temperature=0.2
)

print("\n--- MODEL RESPONSE ---\n")
print(response.choices[0].message.content)

print("\n--- TOKEN USAGE ---\n")
print(response.usage)