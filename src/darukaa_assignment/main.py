import os
from fastapi import FastAPI

from darukaa_assignment.api.routes import router as api_router
from darukaa_assignment.db.database import init_db

app = FastAPI(title="Darukaa Biodiversity Intelligence API")
app.include_router(api_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.on_event("startup")
def startup_event() -> None:
    init_db()


def main() -> None:
    import uvicorn

    # Read from environment variables, fallback to local defaults
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    uvicorn.run("darukaa_assignment.main:app", host=host, port=port, reload=True)

if __name__ == "__main__":
    main()