# Nestor Orchestrator

Минимальный сервис-орchestrator ИИ-агентов. Сейчас содержит только FastAPI-проброс проверки здоровья, но далее станет центральным узлом на базе LangGraph для координации множества специализированных агентов.

## Быстрый старт

```bash
cd nestor_orchestrator
python -m venv .venv && source .venv/bin/activate
pip install .
python -m nestor_orchestrator.main
```

Эндпоинт `GET /health` вернёт `{"status": "nestor_alive"}`.

