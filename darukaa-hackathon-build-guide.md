# Darukaa.Earth Hackathon — Build Guide
### AI Biodiversity Intelligence Chatbot Challenge

This guide breaks the challenge PDF into a buildable system, maps every requirement to the evaluation rubric, and points you to the **official documentation** for each piece so you build it by hand rather than by prompting an AI to generate the whole repo.

---

## 1. What the evaluators are actually scoring

| Criterion | Weight | What it really means |
|---|---|---|
| Depth of Reasoning | 30% | Recommendations must be non-obvious and combine ≥2 variables. Not "plant trees." |
| Scientific Grounding | 25% | Every claim traces to a real, citable source (FAO, IPCC, peer-reviewed study). |
| Knowledge System Design | 20% | A real retrieval pipeline (RAG/vector DB/structured data) — not the LLM's own memory. |
| Conversational Intelligence | 15% | Multi-turn memory, clarifying questions when data is missing. |
| Output Clarity | 10% | Structured: recommendation, impacted metrics, time horizon, confidence. |

The PDF explicitly says: **"No generic LLM-only solutions. No shallow or obvious recommendations."** This means the knowledge layer and the reasoning layer must visibly do work — if you can delete your vector DB and get the same answer, you'll lose most of the 20% + 25% + 30%.

---

## 2. System architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                        │
│         (text chat + JSON input + optional geo-coords)       │
└───────────────────────────┬────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                  CONVERSATION MANAGER                        │
│  - session memory (buffer per user/session)                  │
│  - slot-filling: checks which of {soil, land use, biodiv,    │
│    climate, human impact} are missing → asks clarifying Q    │
└───────────────────────────┬────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│               STRUCTURED METRICS STORE (SQL)                 │
│  land_id | soc% | ph | rainfall | land_use | species_rich…   │
└───────────────────────────┬────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                  RETRIEVAL LAYER (RAG)                       │
│  Vector DB of chunked FAO/IPCC/journal PDFs + embeddings     │
│  Query = current metrics + user question → top-k passages    │
└───────────────────────────┬────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│              MULTI-METRIC REASONING ENGINE                   │
│  Rule graph (soil↔biodiversity, water↔species,               │
│  land-use↔fragmentation) + retrieved evidence → LLM synthesis│
└───────────────────────────┬────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                 STRUCTURED OUTPUT FORMATTER                  │
│  recommendation | mechanism | metric impacted | % change |   │
│  time horizon | confidence | source citation                 │
└─────────────────────────────────────────────────────────────┘
```

Build it as **separate, inspectable modules** (not one giant prompt). Evaluators will look at your repo structure, not just chat output.

---

## 3. Tech stack (manual setup, official docs only)

| Layer | Tool | Why | Official docs |
|---|---|---|---|
| Backend API | FastAPI | Simple, async, auto OpenAPI docs (helps your README) | https://fastapi.tiangolo.com/ |
| Structured DB | SQLite → Postgres | Holds land/session metric records | https://www.sqlite.org/docs.html / https://www.postgresql.org/docs/ |
| Embeddings | `sentence-transformers` (e.g. `all-MiniLM-L6-v2`) — free, local, no API cost | https://www.sbert.net/ |
| Vector DB | ChromaDB (simplest to self-host and explain in a README) | https://docs.trychroma.com/ |
| RAG orchestration | LangChain **or** hand-rolled retrieval (write it yourself — scores higher on "depth of thinking" than a black-box chain) | https://python.langchain.com/docs/ |
| LLM | Anthropic API (Claude) for the synthesis step only, never for grounding | https://docs.claude.com/ |
| Conversation memory | LangChain `ConversationBufferMemory` or your own session dict keyed by session_id | https://python.langchain.com/docs/how_to/chatbots_memory/ |
| Frontend | Minimal Streamlit app (judge said "not UI-heavy" — so keep this thin) | https://docs.streamlit.io/ |
| Deployment (live demo) | Render / Railway / HuggingFace Spaces (all have free tiers) | https://render.com/docs |
| CI/CD | GitHub Actions (basic lint + test workflow) | https://docs.github.com/en/actions |

**Why manual matters here:** the rubric rewards you being able to explain *why* a retrieved passage led to a recommendation. If you generate the whole pipeline via AI without understanding it, you won't be able to defend the reasoning chain if asked — and "depth of thinking" is 30% of the score.

---

## 4. Knowledge base — real, citable sources to ingest

Don't invent numbers. Pull real datasets/reports and chunk them into your vector DB with proper citation metadata attached to every chunk.

| Domain | Source | Access |
|---|---|---|
| Soil health (pH, organic carbon, texture) | **ISRIC SoilGrids** — global soil property maps at 250m resolution, 6 depth intervals, free REST API <cite index="6-1">accessible with fair-use of 5 calls/minute and full OpenAPI docs</cite> | https://rest.isric.org/soilgrids/v2.0/docs |
| Biodiversity indicators (species richness) | **GBIF** — <cite index="16-1">free and open access to biodiversity data</cite>, with a documented Species and Occurrence API and a Python client (`pygbif`) | https://techdocs.gbif.org/en/openapi/ |
| Climate factors (temperature, rainfall) | **IPCC Data Distribution Centre** / **World Bank Climate Change Knowledge Portal** | https://climateknowledgeportal.worldbank.org/ |
| Land use / land cover | **Copernicus Global Land Cover** or **ESA WorldCover** | https://land.copernicus.eu/ |
| Soil–biodiversity–carbon scientific grounding | FAO reports on soil organic carbon and cover cropping, IPCC AR6 WG2 chapters on ecosystems | https://www.fao.org/soils-portal/ |

**Ingestion workflow (do this by hand, following each tool's own docs):**
1. Download 5–10 real PDFs/reports (FAO soil carbon reports, IPCC chapter excerpts, a couple of peer-reviewed papers on agroforestry/cover-cropping).
2. Chunk them (500–800 tokens, with overlap) — LangChain's `RecursiveCharacterTextSplitter` docs show the exact pattern: https://python.langchain.com/docs/how_to/recursive_text_splitter/
3. Embed each chunk with `sentence-transformers`, store in Chroma with metadata: `{source, title, year, url, page}`.
4. At query time, retrieve top-k chunks, and **require your output formatter to only cite from retrieved metadata** — never let the LLM freehand a citation.
5. For the numeric datasets (SoilGrids, GBIF, climate portal), pull real values for a handful of demo regions and store them in your structured DB — this lets your "Example Use Case" walkthrough use real numbers instead of the PDF's example (0.3% SOC, semi-arid, monoculture wheat).

---

## 5. Conversational intelligence

- Maintain a `session_state` per conversation with slots: `soc`, `ph`, `moisture`, `land_use`, `rainfall`, `temperature`, `species_richness`, `pollution`, `deforestation_rate`, `region`, `geo_coords`.
- Before generating a recommendation, check which required slots are empty. If any of soil / land-use / rainfall is missing, ask exactly one clarifying question (mirrors the PDF's own example).
- Store the last N turns so follow-ups ("what about pollinators specifically?") resolve using stored context, not just the last message.
- A simple, defensible implementation: a Python dict/session store + explicit slot-filling logic — this is easy to explain live to evaluators, which matters more than a fancy memory framework.

---

## 6. Evidence-backed recommendation format

Every recommendation object your system returns should be structured, e.g.:

```json
{
  "recommendation": "Introduce legume-based cover crops between wheat rows",
  "mechanism": "Legume root nodules fix atmospheric nitrogen and add biomass, raising soil organic carbon and feeding soil microbial communities",
  "impacted_metrics": ["soil_organic_carbon", "microbial_diversity", "pollinator_visitation"],
  "expected_change": "+15% to +25% SOC over 2–3 years",
  "time_horizon": "medium_term",
  "confidence": "high",
  "source": {"title": "FAO Soil Organic Carbon report", "url": "https://www.fao.org/soils-portal/"}
}
```

Build a **rule table** connecting metric ranges → interventions → mechanisms → sources (a CSV or SQL table you curate manually from the papers you ingested). The RAG layer retrieves the supporting evidence; the rule table ensures the recommendation is never "shallow" or generic.

---

## 7. Multi-metric reasoning — make the connections explicit

Hard-code (then let the LLM narrate) at least these three coupling rules, since the PDF calls this out as "the core differentiator":

- **Soil ↔ biodiversity**: low SOC → reduced microbial/soil fauna diversity → weaker nutrient cycling → lower plant diversity.
- **Water ↔ species survival**: low rainfall + monoculture → reduced habitat moisture refugia → species range contraction.
- **Land use ↔ fragmentation**: monoculture cropping → reduced habitat connectivity → isolated species populations → lower genetic diversity.

Encode these as a small graph/rule engine (a Python dict of `{condition: linked_effects}` is enough) that the LLM must consult before answering — this is what makes your reasoning "non-obvious" rather than a single-variable answer.

---

## 8. Input handling

- **Text**: free-form chat.
- **Structured (JSON)**: accept a payload matching your metric schema directly (skip slot-filling if provided).
- **Bonus — geo-coordinates**: if lat/lon given, auto-pull SoilGrids point data and nearest climate-portal averages via their REST APIs, so the system can answer with real regional data instead of asking the user for numbers they may not have.

---

## 9. Suggested build timeline

| Phase | Days | Deliverable |
|---|---|---|
| 1 | 1–2 | Repo scaffold, FastAPI skeleton, SQLite schema, GitHub Actions lint/test |
| 2 | 3–5 | Ingest real datasets (FAO/IPCC PDFs, SoilGrids/GBIF pulls), build Chroma index |
| 3 | 6–8 | Conversation manager + slot-filling + memory |
| 4 | 9–11 | Multi-metric rule graph + recommendation rule table |
| 5 | 12–13 | Output formatter, structured JSON schema, Streamlit thin UI |
| 6 | 14 | Deploy live demo, write README (architecture, schema, setup, CI/CD), record a short walkthrough |

---

## 10. README.md — required sections

Per the submission guidelines, your README must cover:
1. **Architecture** — reuse the diagram in Section 2, briefly explained.
2. **Database/schema** — your SQL tables + vector DB collection schema.
3. **Local setup** — exact `pip install`, `.env` variables, `uvicorn` run command.
4. **CI/CD** — what your GitHub Actions workflow does (lint, test, maybe auto-deploy).

## 11. Submission checklist

- [ ] One Word (.docx) document submitted via the applied-job page
- [ ] GitHub repo link (public → link only; private → grant access to `ankita.dasgupta@darukaa.com`, `harsh.kumar@darukaa.com`, `utkarsh.gauniyal@darukaa.com`, `guneet.mutreja@darukaa.com`)
- [ ] Live demo URL
- [ ] README overview embedded/linked in the .docx (architecture, schema, setup, CI/CD)
- [ ] Any credentials/notes needed to run the project

---

## 12. What separates a winning submission from an average one

- **Show your retrieval, don't just claim it** — log which chunks were retrieved for a given query in your demo, so it's visibly not "LLM-only."
- **Use real numbers from real datasets** for at least one worked example (pull an actual region's SoilGrids values rather than reusing the PDF's sample numbers verbatim).
- **Never output a recommendation without a source** — enforce this at the code level (reject/flag any LLM output missing a citation field).
- **Keep the UI minimal** — the brief explicitly de-prioritizes UI polish; spend that time on the reasoning graph and knowledge grounding instead.
