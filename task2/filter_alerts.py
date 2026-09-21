#!/usr/bin/env python3
"""
Фильтр алертов.

Читает events.json (список событий с уровнем info/warn/critical),
печатает только события с уровнем "critical" и итоговую фразу
"критичных N".

Обычный if/filter, без агентов и внешних инструментов.
"""

import json
from pathlib import Path

EVENTS_FILE = Path(__file__).parent / "events.json"


def main() -> None:
    if not EVENTS_FILE.exists():
        raise SystemExit(f"Не найден файл: {EVENTS_FILE}")

    events = json.loads(EVENTS_FILE.read_text(encoding="utf-8"))

    critical_events = [e for e in events if e.get("level") == "critical"]

    for e in critical_events:
        print(f"[CRITICAL] {e['event']}")

    print(f"критичных {len(critical_events)}")


if __name__ == "__main__":
    main()
