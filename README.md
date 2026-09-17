# Darukaa.Earth Hackathon — Biodiversity Intelligence Assistant

## 1. Architecture

This project is a biodiversity intelligence assistant built around a simple but explainable architecture:

- User input enters via a lightweight API or Streamlit interface.
- The application checks missing land and biodiversity metrics and asks clarifying questions when needed.
- The system stores structured land metrics in SQLite.
- The knowledge layer retrieves evidence across multiple source documents using a vector database and embeddings.
- A reasoning layer connects soil, water, land-use, and biodiversity signals into a structured recommendation.
- The final answer includes recommendation, mechanism, impacted metrics, expected change, time horizon, confidence, and source metadata.

## 2. Database schema

### land_metrics

| Column | Type | Description |
| --- | --- | --- |
| id | INTEGER | primary key |
| region | TEXT | region name |
| soc | REAL | soil organic carbon |
| ph | REAL | soil pH |
| rainfall | REAL | annual rainfall |
| temperature | REAL | average temperature |
| land_use | TEXT | land use category |
| species_richness | REAL | biodiversity indicator |
| moisture | REAL | soil moisture proxy |
| pollution | REAL | pollution index |
| deforestation_rate | REAL | deforestation measure |
| created_at | TEXT | record timestamp |

### sessions

Stores conversation/session state for slot-filling and follow-up memory.

### recommendations

Stores recommendation outputs and their source title / URL.

## 3. Local setup

1. Create a virtual environment:
   ```bash
   uv venv
   .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Build or refresh the local knowledge index from the downloaded files:
   ```bash
   uv run python -c "from darukaa_assignment.knowledge.documents import ingest_all_documents; print(len(ingest_all_documents()))"
   ```

4. Start the API:
   ```bash
   uv run python -m darukaa_assignment.main
   ```

5. Or run the UI:
   ```bash
   uv run streamlit run src/darukaa_assignment/ui/streamlit_app.py
   ```

5. Environment variables:
   ```env
   ANTHROPIC_API_KEY=
   DATABASE_PATH=data/darukaa.db
   VECTOR_DB_PATH=data/vector_store
   EMBEDDING_MODEL=all-MiniLM-L6-v2
   ```

## 4. CI/CD

This project is structured for a GitHub Actions workflow that can:

- install dependencies,
- run pytest,
- run ruff lint checks,
- validate the API entry points,
- prepare for deployment to a hosted platform later.

## 5. Knowledge base

The project uses a document-driven knowledge base composed of real biodiversity, soil, climate, and land-use sources. These source references are tracked in the repository metadata and should be used as evidence for recommendations.

The ingestion command is idempotent: it reads local files under `data/knowledge_base/`, chunks them, embeds them locally, and upserts metadata-rich records into `data/vector_store/`. The `/chat` endpoint retrieves those records and returns both a structured recommendation and the supporting evidence excerpts.

## 6. Notes

- The structured database is intentionally simple and inspectable.
- The reasoning layer is rule-based and easy to explain.
- The vector/RAG layer is designed to retrieve evidence across multiple documents rather than a single text blob.
