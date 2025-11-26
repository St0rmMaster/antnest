import os
from typing import Literal, TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()


class TaskState(TypedDict):
    """Состояние задачи в графе."""
    task_spec: str
    plan: list[str] | None
    clarifying_questions: list[str] | None
    status: Literal["new", "planned", "done"]


_llm_client: ChatOpenAI | None = None


def _get_llm_client() -> ChatOpenAI | None:
    """Создаёт и возвращает LLM-клиент, если доступен API ключ."""
    global _llm_client
    if _llm_client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            _llm_client = ChatOpenAI(model="gpt-5.1", temperature=0.3)
    return _llm_client


def _parse_plan_from_llm_response(response_text: str) -> list[str]:
    """Парсит ответ LLM в список шагов плана."""
    lines = response_text.strip().split("\n")
    plan = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Убираем маркеры списка (1., -, *, • и т.д.)
        for marker in ["- ", "* ", "• ", "1. ", "2. ", "3. ", "4. ", "5. "]:
            if line.startswith(marker):
                line = line[len(marker):].strip()
                break
        # Убираем нумерацию вида "Шаг 1:", "1)", и т.д.
        if line.startswith("Шаг "):
            colon_pos = line.find(":")
            if colon_pos > 0:
                line = line[colon_pos + 1:].strip()
        if line:
            plan.append(line)
    return plan if plan else ["Шаг 1: разобрать задачу", "Шаг 2: подготовить уточняющие вопросы"]


def _parse_questions_from_llm_response(response_text: str) -> list[str]:
    """Парсит ответ LLM в список вопросов."""
    lines = response_text.strip().split("\n")
    questions = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Убираем маркеры списка (1., -, *, • и т.д.)
        for marker in ["- ", "* ", "• ", "1. ", "2. ", "3. ", "4. ", "5. ", "6. ", "7. "]:
            if line.startswith(marker):
                line = line[len(marker):].strip()
                break
        # Убираем нумерацию вида "Вопрос 1:", "1)", и т.д.
        if line.startswith("Вопрос "):
            colon_pos = line.find(":")
            if colon_pos > 0:
                line = line[colon_pos + 1:].strip()
        if line:
            questions.append(line)
    return questions if questions else ["Какая целевая аудитория сервиса?", "Какие основные сценарии использования?"]


def intake_node(state: TaskState) -> TaskState:
    """Узел приёма задачи: создаёт план через LLM, если его нет."""
    if state.get("plan") is None or not state.get("plan"):
        plan: list[str]
        try:
            llm = _get_llm_client()
            if llm:
                prompt = f"""Составь краткий план выполнения задачи. Ответь списком коротких шагов на русском языке, каждый шаг с новой строки.

Задача: {state["task_spec"]}

План:"""
                response = llm.invoke(prompt)
                response_text = response.content if hasattr(response, "content") else str(response)
                plan = _parse_plan_from_llm_response(response_text)
            else:
                raise ValueError("LLM client not available")
        except Exception:
            # Дефолтный план при ошибке LLM
            plan = [
                "Шаг 1: разобрать задачу",
                "Шаг 2: подготовить уточняющие вопросы"
            ]
    else:
        plan = state["plan"]
    
    return {
        **state,
        "plan": plan,
        "status": "planned"
    }


def clarify_node(state: TaskState) -> TaskState:
    """Узел уточнения: генерирует уточняющие вопросы через LLM."""
    if state.get("clarifying_questions") is None or not state.get("clarifying_questions"):
        questions: list[str]
        try:
            llm = _get_llm_client()
            if llm:
                plan_text = ""
                if state.get("plan"):
                    plan_text = f"\nПлан выполнения:\n" + "\n".join(f"- {step}" for step in state["plan"])
                
                prompt = f"""Составь 3-7 уточняющих вопросов по задаче. Ответь списком вопросов на русском языке, каждый вопрос с новой строки.

Задача: {state["task_spec"]}{plan_text}

Уточняющие вопросы:"""
                response = llm.invoke(prompt)
                response_text = response.content if hasattr(response, "content") else str(response)
                questions = _parse_questions_from_llm_response(response_text)
                # Добавляем знак вопроса к каждому вопросу, если его нет
                questions = [q.rstrip(".") if q.endswith(".") else q for q in questions]
                questions = [q if q.endswith("?") else f"{q}?" for q in questions]
            else:
                raise ValueError("LLM client not available")
        except Exception:
            # Дефолтные вопросы при ошибке LLM
            questions = [
                "Какая целевая аудитория сервиса?",
                "Какие основные сценарии использования?"
            ]
    else:
        questions = state["clarifying_questions"]
    
    return {
        **state,
        "clarifying_questions": questions
    }


workflow = StateGraph(TaskState)
workflow.add_node("intake", intake_node)
workflow.add_node("clarify", clarify_node)
workflow.add_edge(START, "intake")
workflow.add_edge("intake", "clarify")
workflow.add_edge("clarify", END)

graph = workflow.compile()

