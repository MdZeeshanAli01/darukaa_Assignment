from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class KnowledgeSource:
    title: str
    source_org: str
    url: str
    year: str | None = None
    domain: str = "general"
    doc_type: str = "pdf"


SOURCE_CATALOG: list[KnowledgeSource] = [
    KnowledgeSource(
        title="FAO Global Soil Organic Carbon Map (GSOCmap) Technical Report",
        source_org="FAO",
        url="https://www.fao.org/soils-portal/data-hub/soil-maps-and-databases/global-soil-organic-carbon-map-gsocmap/en/",
        year="2024",
        domain="soil",
        doc_type="web",
    ),
    KnowledgeSource(
        title="Soil Organic Carbon: The Hidden Potential",
        source_org="FAO",
        url="https://openknowledge.fao.org/server/api/core/bitstreams/b382a255-5bd5-4656-a8cd-e30fff1a8bfe/content",
        year="2017",
        domain="soil",
        doc_type="web",
    ),
    KnowledgeSource(
        title="IPCC AR6 Working Group II",
        source_org="IPCC",
        url="https://www.ipcc.ch/report/ar6/wg2/",
        year="2022",
        domain="climate",
        doc_type="web",
    ),
    KnowledgeSource(
        title="IPCC AR6 WGII Fact Sheet: Biodiversity",
        source_org="IPCC",
        url="https://www.ipcc.ch/report/ar6/wg2/downloads/outreach/IPCC_AR6_WGII_FactSheet_Biodiversity.pdf",
        year="2022",
        domain="biodiversity",
        doc_type="pdf",
    ),
    KnowledgeSource(
        title="Climate Change Knowledge Portal",
        source_org="World Bank",
        url="https://climateknowledgeportal.worldbank.org/",
        year="2024",
        domain="climate",
        doc_type="web",
    ),
    KnowledgeSource(
        title="GBIF Species and Occurrence API Technical Documentation",
        source_org="GBIF",
        url="https://techdocs.gbif.org/en/openapi/",
        year="2024",
        domain="biodiversity",
        doc_type="web",
    ),
    KnowledgeSource(
        title="Copernicus Global Land Cover",
        source_org="Copernicus",
        url="https://land.copernicus.eu/",
        year="2024",
        domain="land_use",
        doc_type="web",
    ),
    KnowledgeSource(
        title="Habitat Loss and Fragmentation",
        source_org="Fahrig",
        url="https://carleton.ca/glel/wp-content/uploads/Bird-Jackson-Fahrig_2013-Habitat-loss-and-fragmentation.pdf",
        year="2003",
        domain="fragmentation",
        doc_type="pdf",
    ),
    KnowledgeSource(
        title="Water Scarcity: Causes, Impacts, and Solutions",
        source_org="WWF",
        url="https://www.worldwildlife.org/our-work/freshwater/water-scarcity/",
        year="2024",
        domain="water",
        doc_type="web",
    ),
    KnowledgeSource(
        title="Agroforestry Systems meta-analysis",
        source_org="Springer",
        url="https://link.springer.com/article/10.1007/s10457-026-01507-6",
        year="2026",
        domain="intervention_agroforestry",
        doc_type="web",
    ),
    KnowledgeSource(
        title="Agroforestry and Biodiversity",
        source_org="MDPI",
        url="https://www.mdpi.com/2071-1050/11/10/2879",
        year="2019",
        domain="intervention_agroforestry",
        doc_type="web",
    ),
    KnowledgeSource(
        title="Cover crops improve soil microbial diversity",
        source_org="Springer",
        url="https://link.springer.com/article/10.1007/s13593-016-0385-7",
        year="2016",
        domain="intervention_cover_crop",
        doc_type="web",
    ),
    KnowledgeSource(
        title="Pollinator.org cover crop blog",
        source_org="Pollinator.org",
        url="https://www.pollinator.org/blog/cover-crops",
        year="2024",
        domain="intervention_cover_crop",
        doc_type="web",
    ),
]


def get_sources_for_domain(domain: str) -> list[KnowledgeSource]:
    return [source for source in SOURCE_CATALOG if source.domain == domain]
