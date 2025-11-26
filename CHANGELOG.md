# Changelog

Все значимые изменения в проекте документируются в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.0.0/),
и проект придерживается [Semantic Versioning](https://semver.org/lang/ru/).

## [Unreleased]

### Added
- Создан сервис `nestor_orchestrator` - центральный оркестратор ИИ-агентов
- Добавлен базовый FastAPI-сервер с эндпоинтом `GET /health`
- Реализован граф LangGraph с узлами `intake` и `clarify`
- Добавлена интеграция с OpenAI LLM для генерации планов выполнения задач
- Добавлена генерация уточняющих вопросов через LLM
- Добавлен эндпоинт `POST /tasks/debug` для отладки выполнения графа
- Добавлен эндпоинт `POST /tasks/clarify` для получения уточняющих вопросов
- Добавлена поддержка переменных окружения через `python-dotenv`
- Создана документация для всех модулей проекта

### Changed
- Обновлён README.md сервиса nestor_orchestrator с актуальной информацией

### Technical
- Настроен `pyproject.toml` с зависимостями: fastapi, uvicorn, langgraph, pydantic, langchain-openai, python-dotenv
- Добавлена обработка ошибок LLM с дефолтными значениями
- Реализован парсинг ответов LLM для планов и вопросов

