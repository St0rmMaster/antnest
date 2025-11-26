# Antnest

Репозиторий проекта Antnest.

## Структура проекта

### nestor_orchestrator

Центральный сервис-оркестратор для координации ИИ-агентов на базе LangGraph.

**Описание:** Минимальный сервис с FastAPI API и графом обработки задач. Использует LLM для генерации планов выполнения и уточняющих вопросов.

**Документация:** См. [nestor_orchestrator/nestor_orchestrator/README.md](nestor_orchestrator/nestor_orchestrator/README.md)

## Быстрый старт

### Nestor Orchestrator

```bash
cd nestor_orchestrator
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install .
python -m nestor_orchestrator.main
```

Сервис будет доступен на `http://localhost:8000`

## Документация

- [CHANGELOG.md](CHANGELOG.md) - история изменений проекта
- [PLAN.md](PLAN.md) - планы и цели проекта

