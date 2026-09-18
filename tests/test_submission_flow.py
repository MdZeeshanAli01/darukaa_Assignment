from __future__ import annotations

from fastapi.testclient import TestClient

from darukaa_assignment.api import routes
from darukaa_assignment.knowledge.retriever import MultiDocumentRetriever
from darukaa_assignment.main import app
from darukaa_assignment.reasoning.slot_filler import ask_clarifying_question
from darukaa_assignment.schemas.recommendation import Recommendation


class FakeCollection:
    def query(self, query_texts: list[str], n_results: int) -> dict[str, list[list[object]]]:
        return {
            "documents": [["soil evidence", "habitat evidence", "climate evidence"]],
            "metadatas": [[
                {"title": "FAO Soil Report", "source_org": "FAO", "url": "https://fao.org/soil", "year": "2017", "domain": "soil"},
                {"title": "Habitat Study", "source_org": "Fahrig", "url": "https://example.org/habitat", "year": "2003", "domain": "fragmentation"},
                {"title": "IPCC Biodiversity", "source_org": "IPCC", "url": "https://ipcc.ch/biodiversity", "year": "2022", "domain": "biodiversity"},
            ]],
        }


def test_missing_metrics_return_one_clarifying_question() -> None:
    question = ask_clarifying_question({"soc": 0.8})

    assert question is not None
    assert "soil organic carbon" in question
    assert "annual rainfall" in question


def test_recommendation_schema_validates_source_metadata() -> None:
    recommendation = Recommendation(
        recommendation="Use cover crops.",
        mechanism="Cover crops add organic matter.",
        impacted_metrics=["soc", "species_richness"],
        expected_change="Improved soil condition.",
        time_horizon="medium-term",
        confidence="moderate",
        source={
            "title": "FAO Soil Report",
            "source_org": "FAO",
            "url": "https://fao.org/soil",
            "year": "2017",
            "domain": "soil",
        },
    )

    assert recommendation.source.domain == "soil"
    assert recommendation.supporting_sources == []


def test_retriever_groups_chunks_by_source() -> None:
    retriever = MultiDocumentRetriever(vector_store=FakeCollection())

    chunks = retriever.retrieve("soil and habitat", top_k=3)
    grouped = retriever.aggregate_sources(chunks)

    assert len(chunks) == 3
    assert [source["title"] for source in grouped] == [
        "FAO Soil Report",
        "Habitat Study",
        "IPCC Biodiversity",
    ]
    assert [source["domain"] for source in grouped] == ["soil", "fragmentation", "biodiversity"]


def test_chat_returns_clarification_for_incomplete_metrics() -> None:
    client = TestClient(app)

    response = client.post(
        "/chat",
        json={"message": "Help this land", "metrics": {"soc": 0.8}},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "needs_more_context"
    assert response.json()["clarifying_question"]


def test_chat_returns_structured_recommendation(monkeypatch) -> None:
    recommendation = Recommendation(
        recommendation="Use locally appropriate cover crops.",
        mechanism="They increase organic matter and habitat complexity.",
        impacted_metrics=["soc", "species_richness"],
        expected_change="Improved soil and habitat conditions.",
        time_horizon="medium-term",
        confidence="moderate",
        source={
            "title": "FAO Soil Report",
            "source_org": "FAO",
            "url": "https://fao.org/soil",
            "year": "2017",
            "domain": "soil",
        },
    )
    grouped_sources = [{
        "title": "FAO Soil Report",
        "source_org": "FAO",
        "url": "https://fao.org/soil",
        "year": "2017",
        "domain": "soil",
        "matches": ["soil evidence"],
    }]
    monkeypatch.setattr(routes, "build_recommendation", lambda message, metrics: (recommendation, grouped_sources))

    response = TestClient(app).post(
        "/chat",
        json={
            "message": "Improve biodiversity",
            "metrics": {
                "soc": 0.8,
                "ph": 6.3,
                "rainfall": 480,
                "land_use": "monoculture wheat",
                "region": "Local site",
            },
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["recommendation"]["source"]["source_org"] == "FAO"
    assert body["evidence"][0]["match_count"] == 1


def test_sqlite_persistence_on_chat_endpoint(monkeypatch) -> None:
    from darukaa_assignment.db.database import get_connection

    recommendation = Recommendation(
        recommendation="Implement agroforestry buffers.",
        mechanism="Tree roots retain soil structure.",
        impacted_metrics=["soc", "land_use"],
        expected_change="Increased carbon.",
        time_horizon="long-term",
        confidence="high",
        source={
            "title": "FAO Soil Report",
            "source_org": "FAO",
            "url": "https://fao.org/soil",
            "year": "2017",
            "domain": "soil",
        },
    )
    grouped_sources = [{
        "title": "FAO Soil Report",
        "source_org": "FAO",
        "url": "https://fao.org/soil",
        "year": "2017",
        "domain": "soil",
        "matches": ["soil evidence"],
    }]
    monkeypatch.setattr(routes, "build_recommendation", lambda message, metrics: (recommendation, grouped_sources))

    session_id = "test-sqlite-session"
    client = TestClient(app)
    response = client.post(
        "/chat",
        json={
            "session_id": session_id,
            "message": "Persist test",
            "metrics": {
                "soc": 1.2,
                "ph": 6.8,
                "rainfall": 750,
                "land_use": "pasture",
                "region": "Midwest",
            },
        },
    )
    assert response.status_code == 200

    with get_connection() as conn:
        metrics_row = conn.execute("SELECT * FROM land_metrics WHERE region = 'Midwest'").fetchone()
        assert metrics_row is not None
        assert metrics_row["soc"] == 1.2

        rec_row = conn.execute("SELECT * FROM recommendations WHERE session_id = ?", (session_id,)).fetchone()
        assert rec_row is not None
        assert "agroforestry buffers" in rec_row["recommendation"]
