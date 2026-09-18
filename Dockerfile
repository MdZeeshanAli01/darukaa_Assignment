FROM python:3.11-slim

WORKDIR /app

RUN pip install uv

COPY . .

RUN uv sync

EXPOSE 7860

CMD bash -c "uv run python -c 'from darukaa_assignment.knowledge.documents import ingest_all_documents; ingest_all_documents()' && \
    uv run uvicorn darukaa_assignment.main:app --host 0.0.0.0 --port 8000 & \
    API_URL=http://localhost:8000 uv run streamlit run src/darukaa_assignment/ui/streamlit_app.py --server.port 7860 --server.address 0.0.0.0"
