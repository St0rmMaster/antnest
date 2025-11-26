# main.py

## Описание

Основной модуль FastAPI-приложения Nestor Orchestrator. Предоставляет HTTP API для работы с графом обработки задач.

## Changelog

### 2024-12-XX
- Создан базовый FastAPI-сервер с эндпоинтом `/health`
- Добавлен эндпоинт `POST /tasks/debug` для отладки выполнения графа
- Добавлен эндпоинт `POST /tasks/clarify` для получения уточняющих вопросов
- Реализована функция `main()` для локального запуска сервера

## Структура

### Классы

#### `TaskRequest`
Pydantic-модель для запросов на обработку задачи.

**Поля:**
- `task_spec: str` - спецификация задачи

### Функции

#### `health() -> dict[str, str]`
Эндпоинт проверки здоровья сервиса.

**Метод:** `GET /health`

**Возвращает:**
- `{"status": "nestor_alive"}`

#### `debug_task(request: TaskRequest) -> dict`
Отладочный эндпоинт для выполнения полного графа обработки задачи.

**Метод:** `POST /tasks/debug`

**Параметры:**
- `request: TaskRequest` - запрос с `task_spec`

**Возвращает:**
- Полное состояние задачи после выполнения графа (включает `task_spec`, `plan`, `clarifying_questions`, `status`)

**Логика:**
- Создаёт начальное состояние с `status="new"`
- Выполняет граф через `graph.invoke()`
- Возвращает результат

#### `clarify(request: TaskRequest) -> dict[str, list[str]]`
Эндпоинт для получения только уточняющих вопросов по задаче.

**Метод:** `POST /tasks/clarify`

**Параметры:**
- `request: TaskRequest` - запрос с `task_spec`

**Возвращает:**
- `{"clarifying_questions": list[str]}` - список уточняющих вопросов

**Логика:**
- Выполняет граф для генерации вопросов
- Извлекает только поле `clarifying_questions`
- Возвращает пустой список, если вопросы не сгенерированы

#### `main() -> None`
Точка входа для локального запуска сервера.

**Логика:**
- Запускает uvicorn на `0.0.0.0:8000`
- Использует приложение `nestor_orchestrator.main:app`

### Переменные

#### `app: FastAPI`
Экземпляр FastAPI-приложения с названием "Nestor Orchestrator".

## Зависимости

- `fastapi` - веб-фреймворк
- `uvicorn` - ASGI-сервер
- `pydantic` - валидация данных

## Использование

Запуск сервера:
```bash
python -m nestor_orchestrator.main
```

Или через uvicorn напрямую:
```bash
uvicorn nestor_orchestrator.main:app --host 0.0.0.0 --port 8000
```

