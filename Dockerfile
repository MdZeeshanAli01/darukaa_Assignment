FROM python:3.11-slim

WORKDIR /app

RUN pip install uv

COPY . .

RUN uv sync

# Ingest documents, start the API internally, and start Streamlit on Railway's dynamic PORT
CMD bash -c "uv run python -c 'from darukaa_assignment.knowledge.documents import ingest_all_documents; ingest_all_documents()' && \
    uv run uvicorn darukaa_assignment.main:app --host 127.0.0.1 --port 8000 & \
    API_URL=http://127.0.0.1:8000 uv run streamlit run src/darukaa_assignment/ui/streamlit_app.py --server.port ${PORT:-8501} --server.address 0.0.0.0"
