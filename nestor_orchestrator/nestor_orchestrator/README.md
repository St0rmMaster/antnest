# Nestor Orchestrator

Центральный сервис-оркестратор ИИ-агентов на базе LangGraph. Обрабатывает задачи, генерирует планы выполнения и уточняющие вопросы через LLM.

## Возможности

- FastAPI API для работы с задачами
- Граф LangGraph с узлами обработки (`intake`, `clarify`)
- Интеграция с OpenAI LLM для генерации планов и вопросов
- Обработка ошибок с дефолтными значениями

## Быстрый старт

### Установка

```bash
cd nestor_orchestrator
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install .
```

### Настройка окружения

Создайте файл `.env` в папке `nestor_orchestrator/`:

```
OPENAI_API_KEY=your_openai_api_key_here
```

### Запуск

```bash
python -m nestor_orchestrator.main
```

Сервис будет доступен на `http://localhost:8000`

## API Endpoints

### `GET /health`
Проверка здоровья сервиса.

**Ответ:**
```json
{"status": "nestor_alive"}
```

### `POST /tasks/debug`
Выполнение полного графа обработки задачи.

**Запрос:**
```json
{
  "task_spec": "Описание задачи"
}
```

**Ответ:**
```json
{
  "task_spec": "Описание задачи",
  "plan": ["Шаг 1: ...", "Шаг 2: ..."],
  "clarifying_questions": ["Вопрос 1?", "Вопрос 2?"],
  "status": "planned"
}
```

### `POST /tasks/clarify`
Получение только уточняющих вопросов по задаче.

**Запрос:**
```json
{
  "task_spec": "Описание задачи"
}
```

**Ответ:**
```json
{
  "clarifying_questions": ["Вопрос 1?", "Вопрос 2?"]
}
```

## Структура модулей

- `main.py` - FastAPI приложение и эндпоинты
- `graph.py` - определение графа LangGraph и узлов обработки

Подробная документация по каждому модулю доступна в соответствующих `.md` файлах.

