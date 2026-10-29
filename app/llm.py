"""Generation: build a grounded prompt from the retrieved chunks and ask the LLM."""
import re

from openai import OpenAI

from app.config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL, PROMPT_VERSION

_client = OpenAI(base_url=LLM_BASE_URL, api_key=LLM_API_KEY)

NOT_FOUND = {
    "en": "The documents do not contain this information.",
    "de": "Die Dokumente enthalten dazu keine Angabe.",
}
LANGUAGE_NAME = {"en": "English", "de": "German"}

PROMPTS = {
    # v1: the first version, kept so that earlier results can be reproduced
    "v1": """You answer questions using ONLY the numbered context passages provided.
Rules:
- Cite every claim with the passage number in square brackets, e.g. [1] or [2][3].
- If the context does not contain the answer, say so plainly. Never invent rules, numbers or dates.
- The passages may be in German. Answer in the language of the question.
- Be concise: a short direct answer first, then details if needed.""",
    # v2: fixes the failure types found in the evaluation (citation-only answers, wrong language,
    # misread tables, guessing instead of declining)
    "v2": """You answer questions about German university regulations using ONLY the numbered passages.
Rules:
1. Start with one complete sentence that directly answers the question and states the exact number, duration or name from the passages.
2. Put the passage number in square brackets after the claim, e.g. "... 18 weeks [2]." Never reply with citations only.
3. If the passages do not contain the answer, reply exactly: "{not_found}" Do not guess and do not use outside knowledge.
4. The passages are in German; translate their content if the question is in English.
5. Tables are flattened into text. In a module row, the first number after the module name is its credits, the next its weekly hours (SWS).
6. Write the whole answer in {language}. Keep it to 1-3 sentences.""",
}

_GERMAN_HINTS = set(
    "der die das und ist wie was wann welche welcher welches wer wo warum darf muss kann man nicht ein eine im "
    "für mit von zu sind wird werden gibt viele lange braucht".split()
)


def question_language(question: str) -> str:
    """Rough language detection: umlauts/ß or at least two common German words -> German."""
    text = question.lower()
    words = re.findall(r"[a-zäöüß]+", text)
    if any(ch in text for ch in "äöüß") or sum(w in _GERMAN_HINTS for w in words) >= 2:
        return "de"
    return "en"


def format_context(chunks: list[dict]) -> str:
    parts = []
    for i, c in enumerate(chunks, start=1):
        where = f"{c['doc_name']}, p. {c['page']}" if c["page"] else c["doc_name"]
        parts.append(f"[{i}] ({where})\n{c['content']}")
    return "\n\n".join(parts)


def generate_answer(question: str, chunks: list[dict], model: str | None = None, prompt: str | None = None) -> str:
    lang = question_language(question)
    if not chunks:
        return NOT_FOUND[lang]
    system = PROMPTS[prompt or PROMPT_VERSION].format(not_found=NOT_FOUND[lang], language=LANGUAGE_NAME[lang])
    response = _client.chat.completions.create(
        model=model or LLM_MODEL,
        temperature=0.1,  # low temperature = fewer creative (made-up) answers
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": f"Context:\n{format_context(chunks)}\n\nQuestion: {question}"},
        ],
    )
    return response.choices[0].message.content
