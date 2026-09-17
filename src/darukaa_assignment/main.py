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

    uvicorn.run("darukaa_assignment.main:app", host="127.0.0.1", port=8000, reload=True)
