from fastapi import FastAPI

app = FastAPI(title="Darukaa Biodiversity Intelligence API")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


def main() -> None:
    import uvicorn

    uvicorn.run("darukaa_assignment.main:app", host="127.0.0.1", port=8000, reload=True)
