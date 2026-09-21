# Фильтр алертов

Маленький скрипт, который отфильтровывает шум: из 8 событий оставляет
только критичные (`level: critical`) и печатает итоговую сводку.

## Как запустить

```bash
python3 filter_alerts.py
```

Требования: Python 3.8+, никаких сторонних библиотек не нужно.

Скрипт читает `events.json` (список из 8 событий, у каждого есть
`event` и `level`: info / warn / critical) из той же папки, печатает
каждое критичное событие и одну итоговую фразу — «критичных N».

## Что получилось

Обычная фильтрация списком (`level == "critical"`), без агентов и
внешних инструментов — так, как и просили в задании.

Вход (`events.json`, 8 событий):

| Событие | Уровень |
|---|---|
| disk 90% | critical |
| user login | info |
| cpu 40% | info |
| payment failed | critical |
| heartbeat | info |
| db timeout | critical |
| cache miss | warn |
| deploy ok | info |

Вывод скрипта:

```
[CRITICAL] disk 90%
[CRITICAL] payment failed
[CRITICAL] db timeout
критичных 3
```
