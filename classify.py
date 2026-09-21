#!/usr/bin/env python3
"""
Классификатор обращений.

Читает messages.txt (одно обращение на строку), для каждого определяет
категорию — "справка" / "жалоба" / "другое" — и печатает черновик ответа
на русском.

Категория определяется набором ключевых слов (простые правила).
Никаких внешних зависимостей и API-ключей не требуется — скрипт работает
из коробки. При желании классификацию по ключевым словам легко заменить
одним вызовом LLM (см. функцию classify_with_llm ниже — закомментирована,
показывает, как это могло бы выглядеть).
"""

import re
from pathlib import Path

MESSAGES_FILE = Path(__file__).parent / "messages.txt"

# --- Ключевые слова для правил -------------------------------------------

SPRAVKA_KEYWORDS = [
    "справк", "справку", "справка", "справки",
    "документ", "выписк", "подтвержден",
]

ZHALOBA_KEYWORDS = [
    "жалоб", "очеред", "холодн", "плох", "не работает",
    "пропал", "пропала", "пропало", "сломал", "проблема",
    "долго", "грязн", "испортил",
]

# --- Правила -> категория ---------------------------------------------


def classify(text: str) -> str:
    t = text.lower()

    if any(kw in t for kw in SPRAVKA_KEYWORDS):
        return "справка"

    if any(kw in t for kw in ZHALOBA_KEYWORDS):
        return "жалоба"

    return "другое"


# --- Черновики ответов ---------------------------------------------------

DRAFT_TEMPLATES = {
    "справка": (
        "Добрый день! Чтобы получить справку, обратитесь в деканат "
        "(лично или через личный кабинет) с заявлением — справка "
        "обычно готовится в течение 1–3 рабочих дней."
    ),
    "жалоба": (
        "Здравствуйте! Спасибо, что сообщили — приносим извинения за "
        "неудобства. Мы передали информацию ответственному отделу, "
        "проблему постараются решить в ближайшее время."
    ),
    "другое": (
        "Добрый день! Спасибо за обращение. Уточните, пожалуйста, "
        "детали (дату, время, место), и мы поможем с вашим вопросом."
    ),
}


def draft_reply(category: str) -> str:
    return DRAFT_TEMPLATES[category]


# --- (опционально) как выглядела бы классификация через LLM -------------
#
# def classify_with_llm(text: str) -> str:
#     import anthropic
#     client = anthropic.Anthropic()
#     resp = client.messages.create(
#         model="claude-sonnet-4-6",
#         max_tokens=10,
#         messages=[{
#             "role": "user",
#             "content": (
#                 "Определи категорию обращения одним словом: "
#                 "справка, жалоба или другое.\n\n"
#                 f"Обращение: {text}"
#             ),
#         }],
#     )
#     return resp.content[0].text.strip().lower()


def main() -> None:
    if not MESSAGES_FILE.exists():
        raise SystemExit(f"Не найден файл: {MESSAGES_FILE}")

    messages = [
        line.strip()
        for line in MESSAGES_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    for i, msg in enumerate(messages, start=1):
        category = classify(msg)
        reply = draft_reply(category)

        print(f"--- Обращение {i} ---")
        print(f"Текст:     {msg}")
        print(f"Категория: {category}")
        print(f"Ответ:     {reply}")
        print()


if __name__ == "__main__":
    main()
