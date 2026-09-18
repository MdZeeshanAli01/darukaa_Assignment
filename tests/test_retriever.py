from darukaa_assignment.schemas.recommendation import Recommendation, SourceInfo

def test_recommendation_schema_validation():
    primary_source = SourceInfo(
        title="Soil Organic Carbon: The Hidden Potential",
        source_org="FAO",
        url="https://openknowledge.fao.org",
        year="2017",
        domain="soil"
    )
    
    supporting_source = SourceInfo(
        title="Habitat Loss and Fragmentation",
        source_org="Fahrig",
        url="https://carleton.ca",
        year="2013",
        domain="fragmentation"
    )

    rec = Recommendation(
        recommendation="Implement agroforestry buffers and organic mulch.",
        mechanism="Enhances carbon sequestration while increasing soil moisture.",
        impacted_metrics=["soc", "moisture", "species_richness"],
        expected_change="Increase in SOC by 0.3-0.5% over 3 years",
        time_horizon="medium-term (1-3 years)",
        confidence="evidence-supported",
        source=primary_source,
        supporting_sources=[supporting_source]
    )

    assert rec.source.source_org == "FAO"
    assert len(rec.supporting_sources) == 1
    assert rec.supporting_sources[0].domain == "fragmentation"
    assert "soc" in rec.impacted_metrics