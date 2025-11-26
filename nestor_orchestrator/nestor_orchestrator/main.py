from fastapi import FastAPI
import uvicorn


app = FastAPI(title="Nestor Orchestrator")


@app.get("/health")
async def health() -> dict[str, str]:
    """Health probe for orchestrator."""
    return {"status": "nestor_alive"}


def main() -> None:
    """Entry-point for local execution."""
    uvicorn.run("nestor_orchestrator.main:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    main()

