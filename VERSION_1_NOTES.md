# Version 1.1 review branch

This version is an exploratory analysis of a frozen extract, not a certification of complete House trading coverage.

## Defensible claims

- The accepted extract contains 3,179 reported purchase records, 55 members, and 854 normalized stock symbols (855 retained source ticker strings).
- A two-mode affiliation represents at least one accepted member-reported stock purchase in calendar 2025.
- The original shared-stock display retains 355 tickers, 45 members, and 1,292 distinct affiliations. It hides 775 records and 499 one-member tickers without deleting them.
- The member projection uses distinct affiliations. Each pair's weight is its number of distinct shared tickers. All 55 purchasers are retained, including 10 isolates.
- Party assortativity is descriptive. The primary statistic weights each connected member pair equally. A separately labeled sensitivity statistic weights pairs by shared tickers. Neither statistic is recomputed when the display threshold changes.
- Committee links are context; they are not included in purchasing-similarity statistics.

## Corrections and limits

- Terms ending January 3, 2025 are excluded from the 119th-Congress roster. A new cache filename prevents stale roster reuse.
- The roster source is pinned December 5, 2025 and is not claimed as independently verified year-end completeness.
- The former accepted input remains byte-for-byte unchanged as a baseline. The richer accepted source preserves its exact original-field sequence and adds owner codes, parser-assigned row IDs, filing status and review flags. Its 124 additional equal reduced signatures have distinct parsed row IDs; equal signatures alone do not prove duplicate extraction.
- Owner codes are missing in 1,951 accepted records; 107 records carry parser review flags. Parsed row IDs are not official transaction IDs, and filing status does not establish amendment-to-original linkage. Personal-decision attribution and definitive source reconciliation remain unsupported.
- January 3–20 purchases use the later January 21 committee snapshot. This is an approximation, not contemporaneous membership proof.
- Binary ties and shared-ticker weights are unaffected by exact repeated rows. Frequency edges and summed amount bounds can be affected.
- Sales, other asset types, rejected tickers, missing filings, and upstream parsing losses are outside the accepted extract's scope.
- Popular stocks and broad purchasing patterns can create many projected ties. Overlap is not evidence of coordinated trades, influence, insider information, current holdings, or profit.

## Reproduce

Run `Rscript render.R`, then `python3 verify_v1.py`. The latter independently checks counts, projected weight distribution, party mixing, and the corrected roster boundary. Rendering exports inspectable CSVs and JSON under `validation/`.

The branch-only workflow renders `preview/index.html` without deploying GitHub Pages. It does not modify the portfolio or the production network deployment. The preview link uses a third-party HTML preview host and may cache updates briefly.

## Accuracy and performance review — October 11, 2026

- Combines Block Class A SQ/XYZ under XYZ in the derived analysis, with original symbols preserved. Two additional rows and one affiliation enter the shared-stock display; pair count stays 494.
- Uses equal-width binary Explore edges. Stock inspectors label summed record bounds, equal reduced signatures and snapshot age; the later source import adds parsed owner codes, record IDs, filing status and review flags.
- Adds pair list sizes and Jaccard overlap without treating it as significance or unusual coordination.
- Adds a searchable directory of all 55 reporting members, including the ten outside Explore.
- Adds a specific method-to-chapter reading guide, distinguishing applied methods from contextual/future readings.
- Adds DSA 495 Modules 1, 5, 7, 8 and 12 beside their project connections, with direct material links, scheduled dates and a presentation review path. Future sessions are labeled as of October 11, 2026. Text-analysis course principles are distinguished from the implemented SNA methods; this is not a claim of implementing the course’s Python text-analysis project.
- Initializes hidden graphs when opened and caps Explore layout at 200 iterations and Compare at 150. Edges stay visible during dragging and zooming. No transaction rows are removed for performance.
- Complete binary calculations are independently verified. Completeness of upstream transactions, all ticker histories, unparsed ownership and amendment/source reconciliation remain outside this extract.

## Self-contained 2025 snapshot — October 11, 2026

- Imports 7,797 parsed records with transaction dates in 2025 from pinned House scraper commit `a064720e90e715f516cd2a725ece0b6f7a73632b`, plus relevant parser checkpoints and the archived 2025 annual index. It does not import other transaction years or require the scraper checkout to build.
- Enriched accepted preparation exactly reproduces the former 3,179-row sequence, original values and 55 reporting members. Of the accepted records, 212 were filed in 2026; calendar transaction year defines scope.
- Bundles 32 House reference YAML subsets: 15 committee/member snapshot pairs and two bounded legislator sources. Original source hashes, exact commits, subset transformations, bundled hashes and the CC0 license are preserved.
- Adds deterministic preparation, input integrity checks and a source-field audit. Missing or modified inputs stop rendering; other repositories are not downloaded as a fallback. Derived cache reuse requires source, code and cache hashes to match.
- The CI verification build and Pages workflow check source inputs and rendered calculations. Original PDFs remain linked external evidence, not a complete offline archive.

## Textbook

McDonald, Steve, Tom R. Leppard, Andrew P. Davis, and Aditi Mallavarapu. 2026. *Introduction to Social Network Analysis*. https://stevemcd1.github.io/introSNA/

Sections are linked beside the relevant explanations in the interface: 2.0.1 and 2.1.2 (edge lists and valued ties), 13.1–13.4 (two-mode affiliation and degree), 13.6 (projection), 8.1 (assortativity), 4.1 (layout), and B.3 (visNetwork). Chapter 15 is conceptual context for time-aware institutional matching; this version does not claim a longitudinal network analysis. Communities and roles remain possible extensions, not implemented findings.
