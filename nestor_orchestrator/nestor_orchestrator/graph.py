from typing import Literal, TypedDict
from langgraph.graph import StateGraph, START, END


class TaskState(TypedDict):
    """Состояние задачи в графе."""
    task_spec: str
    plan: list[str] | None
    status: Literal["new", "planned", "done"]


def intake_node(state: TaskState) -> TaskState:
    """Узел приёма задачи: создаёт план, если его нет."""
    if state.get("plan") is None:
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


workflow = StateGraph(TaskState)
workflow.add_node("intake", intake_node)
workflow.add_edge(START, "intake")
workflow.add_edge("intake", END)

graph = workflow.compile()

