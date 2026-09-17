# 30 Source Documents for the Knowledge Base

Real, citable documents/reports/papers across the five domains the challenge requires. Download the PDFs (or scrape the page text where no PDF exists), chunk them, embed with `sentence-transformers`, and store in your vector DB with `{title, source_org, url, year}` metadata on every chunk — that metadata is what lets your output formatter attach a real citation to every recommendation.

## A. Soil Health (7)
1. FAO — Global Soil Organic Carbon Map (GSOCmap) Technical Report — https://www.fao.org/soils-portal/data-hub/soil-maps-and-databases/global-soil-organic-carbon-map-gsocmap/en/
2. FAO — *Soil Organic Carbon: The Hidden Potential* (2017) — https://openknowledge.fao.org/server/api/core/bitstreams/b382a255-5bd5-4656-a8cd-e30fff1a8bfe/content
3. FAO Global Soil Partnership — Soil Organic Carbon Manual — https://www.fao.org/global-soil-partnership/areas-of-work/soil-organic-carbon-manual/en/
4. FAO Forestry Paper 168 — *Soil Carbon Monitoring Using Surveys and Modelling* — https://www.fao.org/4/i2793e/i2793e.pdf
5. FAO/Global Soil Partnership — *Unlocking the Potential of Soil Organic Carbon: A Feasible Way Forward* — https://www.fao.org/fileadmin/user_upload/GSP/docs/Unlocking_SOC.pdf
6. World Bank — *Soil Organic Carbon MRV Sourcebook for Agricultural Landscapes* — https://documents1.worldbank.org/curated/en/948041625049766862/pdf/Soil-Organic-Carbon-MRV-Sourcebook-for-Agricultural-Landscapes.pdf
7. ISRIC — SoilGrids technical documentation & FAQ (pH, SOC, texture methodology) — https://docs.isric.org/globaldata/soilgrids/SoilGrids_faqs.html

## B. Climate Factors (3)
8. IPCC AR6 Working Group II — full report landing page (Impacts, Adaptation & Vulnerability) — https://www.ipcc.ch/report/ar6/wg2/
9. IPCC AR6 WGII — Fact Sheet: Biodiversity — https://www.ipcc.ch/report/ar6/wg2/downloads/outreach/IPCC_AR6_WGII_FactSheet_Biodiversity.pdf
10. World Bank — Climate Change Knowledge Portal (country/region climate data) — https://climateknowledgeportal.worldbank.org/

## C. Biodiversity Indicators (2)
11. GBIF — Species & Occurrence API technical documentation (species richness data) — https://techdocs.gbif.org/en/openapi/
12. GBIF — data blog: working with the Species API — https://data-blog.gbif.org/post/gbif-species-api/

## D. Land Use / Land Cover / Fragmentation (5)
13. Copernicus Global Land Cover / Land Monitoring Service — https://land.copernicus.eu/
14. Fahrig, L. (2003), reproduced as *Habitat Loss and Fragmentation* chapter — https://carleton.ca/glel/wp-content/uploads/Bird-Jackson-Fahrig_2013-Habitat-loss-and-fragmentation.pdf
15. Wilson et al. — *Habitat Fragmentation and Biodiversity Conservation: Key Findings* (editorial synthesis) — https://russolab.unl.edu/PDF/Wilson%20et%20al%202016%20Habitat%20fragmentation%20biodiversity%20conservation.pdf
16. *Nature Sustainability* — Biodiversity impacts of recent land-use change driven by increases in agri-food imports — https://www.nature.com/articles/s41893-024-01433-4
17. *Impacts of Land-use Change on Biodiversity of Tropical Forests* (review) — https://www.researchgate.net/publication/387964972_Impacts_of_Land-use_Change_on_Biodiversity_of_Tropical_Forests

## E. Water / Freshwater Ecosystems (4)
18. WWF — Water Scarcity: Causes, Impacts, and Solutions (cites Living Planet Report 2024 freshwater-species decline figures) — https://www.worldwildlife.org/our-work/freshwater/water-scarcity/
19. NOAA-hosted — *Freshwater Biodiversity: Importance, Threats, Status and Conservation Challenges* — https://www.noaa.gov/sites/default/files/legacy/document/2020/Oct/07354626162.pdf
20. OECD — Biodiversity, Water and Ecosystems — https://www.oecd.org/en/topics/biodiversity-water-and-ecosystems.html
21. PMC review — *Water Scarcity in Agriculture: Causes, Impacts and Approaches for Reducing the Risks* — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10392093/

## F. Interventions — Agroforestry (evidence for recommendations) (5)
22. *Agroforestry Systems* (Springer) — meta-analysis: intercropping effects on soil nutrients & SOC (35 studies) — https://link.springer.com/article/10.1007/s10457-026-01507-6
23. *Climate Resilience and Sustainability* (Wiley) — systematic review: agroforestry for climate mitigation/adaptation, 109 studies — https://rmets.onlinelibrary.wiley.com/doi/10.1002/cli2.70018
24. *Sustainability* (MDPI) — Agroforestry and Biodiversity (review) — https://www.mdpi.com/2071-1050/11/10/2879
25. *GJESM* — The Role of Carbon Sequestration and Biodiversity in Agroforestry — https://www.gjesm.net/article_731134.html
26. PMC — Integrated agroforestry systems improve soil carbon storage & water productivity in semi-arid marginal land — https://pmc.ncbi.nlm.nih.gov/articles/PMC9460509/

## G. Interventions — Cover Crops & Pollinators (evidence for recommendations) (4)
27. *Agronomy for Sustainable Development* (Springer) — Cover crops to increase soil microbial diversity in perennial agriculture (review) — https://link.springer.com/article/10.1007/s13593-016-0385-7
28. ScienceDirect — Microbial communities mediate the effect of cover cropping on soil ecosystem functions under precipitation reduction — https://www.sciencedirect.com/science/article/abs/pii/S004896972404720X
29. PMC — Impact of Cover Crops on the Soil Microbiome of Tree Crops (nitrogen fixation mechanisms) — https://pmc.ncbi.nlm.nih.gov/articles/PMC7143828/
30. Pollinator.org — Connecting the Dots Between Cover Crops, Soil Health, and Pollinators — https://www.pollinator.org/blog/cover-crops

---

## How to use this list

- **Reports/manuals (A, B, part of D/E)** are your grounding for policy-level claims and general mechanisms — good for the "why it works" field.
- **Meta-analyses/systematic reviews (agroforestry, cover crops)** give you real percentage ranges (e.g. SOC +15–25% over 2–3 years, biodiversity +25–40%) — use these numbers directly in your `expected_change` field instead of inventing figures.
- **API docs (SoilGrids, GBIF, Copernicus)** aren't for the vector DB — wire them in as live data-fetch tools so a query with a real region/coordinates pulls real current metrics rather than relying only on retrieved text.
- Keep one `sources.bib`-style file (title, org, year, url) in your repo — your README should point to it, and it doubles as proof for evaluators that grounding is real, not fabricated.

If you need a different mix (more on pollution/deforestation specifically, or region-specific data for India, since the challenge's example region is semi-arid), let me know and I'll pull a targeted batch.
