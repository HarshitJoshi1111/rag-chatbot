"""Generation: build a grounded prompt from the retrieved chunks and ask the LLM."""
from openai import OpenAI

from app.config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL

_client = OpenAI(base_url=LLM_BASE_URL, api_key=LLM_API_KEY)

SYSTEM_PROMPT = """You answer questions using ONLY the numbered context passages provided.
Rules:
- Cite every claim with the passage number in square brackets, e.g. [1] or [2][3].
- If the context does not contain the answer, say so plainly. Never invent rules, numbers or dates.
- The passages may be in German. Answer in the language of the question.
- Be concise: a short direct answer first, then details if needed."""


def format_context(chunks: list[dict]) -> str:
    parts = []
    for i, c in enumerate(chunks, start=1):
        where = f"{c['doc_name']}, p. {c['page']}" if c["page"] else c["doc_name"]
        parts.append(f"[{i}] ({where})\n{c['content']}")
    return "\n\n".join(parts)


def generate_answer(question: str, chunks: list[dict]) -> str:
    if not chunks:
        return "I couldn't find anything relevant in the indexed documents."
    response = _client.chat.completions.create(
        model=LLM_MODEL,
        temperature=0.1,  # low temperature = fewer creative (made-up) answers
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{format_context(chunks)}\n\nQuestion: {question}"},
        ],
    )
    return response.choices[0].message.content
