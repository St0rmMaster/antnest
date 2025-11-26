from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from nestor_orchestrator.graph import graph


app = FastAPI(title="Nestor Orchestrator")


class TaskRequest(BaseModel):
    """Запрос на обработку задачи."""
    task_spec: str


@app.get("/health")
async def health() -> dict[str, str]:
    """Health probe for orchestrator."""
    return {"status": "nestor_alive"}


@app.post("/tasks/debug")
async def debug_task(request: TaskRequest) -> dict:
    """Отладочный endpoint для выполнения графа."""
    initial_state = {
        "task_spec": request.task_spec,
        "plan": None,
        "status": "new"
    }
    result = graph.invoke(initial_state)
    return result


def main() -> None:
    """Entry-point for local execution."""
    uvicorn.run("nestor_orchestrator.main:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    main()

