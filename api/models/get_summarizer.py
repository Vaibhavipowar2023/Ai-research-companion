# get_summarizer.py
from openai import OpenAI
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

def try_llm_completion(prompt: str, expect_json: bool = False, max_tokens: int = 500):
    if not client:
        return {"error": "Missing OPENAI_API_KEY"}

    messages = [
        {"role": "system", "content": "You are a helpful, concise research assistant."},
        {"role": "user", "content": prompt},
    ]

    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.3,
            response_format={"type": "json_object"} if expect_json else None,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return {"error": str(e)}

def generate_abstractive(prompt: str, max_tokens: int = 300) -> str:
    resp = try_llm_completion(prompt, expect_json=False, max_tokens=max_tokens)
    if isinstance(resp, dict) and "error" in resp:
        raise RuntimeError(resp["error"])
    return resp
