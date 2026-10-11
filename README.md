# Version 1.1 — 2025 House purchase network

**[Open the interactive network](https://strokeofluck.github.io/congressional-stock-network-2025/)**

**[Compare reporting members](https://strokeofluck.github.io/congressional-stock-network-2025/?analysis=1)**

Version 1.1 adds member overlap, all accepted member–stock ties, party assortativity, a corrected roster boundary, textbook/class references and a self-contained 2025 source snapshot. The main Pages deployment renders the R source and independently verifies the result before publishing. The portfolio embeds this standalone network.

**[Open the textbook and class methodology guide](https://strokeofluck.github.io/congressional-stock-network-2025/?methods=1)**

The guide links actual project methods to the SNA book and relevant [DSA 495 class modules](https://courseweb.site/dsa495-2026/materials.html#12), with scheduled dates and a presentation review path. It distinguishes adapted course principles from implemented methods and labels future sessions as of the October 11, 2026 review.

Read [Version 1.1 scope and limitations](VERSION_1_NOTES.md), [the executable new analysis](v1-analysis.R), and [the independent checks](verify_v1.py). Generated counts and analytical exports are in [validation](validation/).

---

# Congressional Stock Trading Network 2025

Interactive network analysis of reported 2025 U.S. House public-stock purchases.

This repository is intentionally separate from `sean-data-portfolio`. The portfolio repository contains only a lightweight project page and links here. Keeping the analysis, data extract, methodology, responsive interface code, and deployment history in their own Git repository reduces coupling and keeps changes to this project from creating technical debt in the website repo.

## Interactive project

The rendered page contains four internal sections:

- **Explore** — lower-left buttons identify **Member–stock · Two-mode (bipartite)**, **Member–member · One-mode projection**, and mixed networks with three or four node types. The active button and legend identify the current network.
- **About** — source definitions, provenance, and caveats
- **Methodology** — design and analytical choices
- **Comparison details** — projected member overlap, all accepted affiliations, and descriptive party mixing

The member projection opens with **Democrats left · Republicans right** and retains all 55 reporters and their shared-stock lines. Members are alphabetical within each party; the positions are assigned, not detected communities or numerical similarities. The **Member layout** control switches to the original stabilized **Network structure (force-directed)** layout. Main-view and comparison-page controls stay synchronized; shared links preserve `layout=party` or `layout=network`. Layout changes do not alter the accepted data, edge weights, threshold, or analytical statistics.

The interface also includes graph search, reset/recenter controls, institution drawers, original PTR links, shareable selections, CSV export, House coverage diagnostics, and a compact mobile view/legend control.

Member overlap uses the same comparison widget on the main canvas and the detailed comparison page. Its separate minimum-shared-stocks control filters member-pair lines; it does not change the opening stock rule, remove members or recalculate analytical statistics. The main search, zoom and reset controls apply to the selected graph. On phones, select Member–member · one-mode projection and use Options for its threshold and legend. A member–stock–member path becomes a direct member–member edge; committee views add node types and are mixed networks.

## Confirmed extraction gap

The [October 11 coverage audit](FILING_COVERAGE_AUDIT.md) established a **partial extraction**: 66 of 515 indexed 2025 PTRs are scanned filings with no extracted rows (451 pages, 14 reporters). Another 52 scanned 2026 filings have zero rows (401 pages); their transaction years still require review. A reviewed Khanna filing contains marked 2025 common-stock purchases absent from the extract. The 55 reporters are the accepted-extract population, not all House purchasers. Archive completeness is not transaction completeness.

Recover and verify the scanned filings, resolve symbols and amendments, then rebuild before making full-year coverage claims. The current graph uses the frozen accepted records. See the [executed notebook](validation/filing-coverage-audit.ipynb), [filing inventory](validation/filing-coverage.csv) and [audit results](validation/filing-coverage.json).

## Analysis input

The repository includes the parsed **2025 transaction-year snapshot** and bounded House reference snapshots under [data/2025](data/2025/README.md). Rebuilding does not read another checkout or download source data. The bundled transaction snapshot has 7,797 rows, including late 2026 filings with 2025 transactions; other transaction years are excluded.

The renderer uses `data/2025/accepted-stock-purchases.csv`: **3,179 accepted public-stock purchase records** with parsed owner codes, row IDs, filing status and review flags. All original 14 fields and their sequence exactly match the former extract. `PTR_transactions_2025_ACCEPTED_STOCK_PURCHASES.csv` is retained byte-for-byte as that baseline.

There are still 55 accepted purchasers. Importing the richer source does not add accepted purchases or members. Owner codes are missing in 1,951 records; 107 carry parser review flags. The 124 additional equal reduced signatures are not proof of duplicates: all accepted records have distinct parser-assigned IDs. Amendment linkage and source extraction accuracy remain unverified.

This split is deliberate:

- `house-ptr-scraper` remains the upstream extraction, parsing, cleaning and ticker-resolution source.
- `congressional-stock-network-2025` owns its frozen 2025 inputs, provenance, reproducible preparation, analysis and visualization.
- `sean-data-portfolio` owns only the portfolio presentation and links.

## Main graph rule

A ticker enters the opening network only when at least two different politicians have accepted 2025 purchases for it.

That is a display rule. Purchases are not removed because a politician lacks a committee match or because their stock is not shared with another politician.

## Committee matching

Committee membership is transaction-date-aware and Congress-aware:

- Jan. 1–2, 2025 → Dec. 17, 2024 snapshot (118th Congress)
- Jan. 3–20, 2025 → Jan. 21, 2025, the first usable 119th-Congress House snapshot
- Jan. 21 onward → latest available snapshot on or before the transaction date

Exact source commits are listed in `committee-snapshot-index-2025.csv`.

Original source:

https://github.com/unitedstates/congress-legislators

Development fork used during source work:

https://github.com/StrokeOfLuck/congress-legislators

## Run locally

Run:

```bash
Rscript render.R
```

`render.R` is the canonical renderer. It renders `2025_Congressional_Stock_Network.Rmd` and includes `mobile-network-controls.html`, so local and GitHub Pages builds use the same responsive interface source. The generated `index.html` is not patched after rendering.

Install Python 3, R and Pandoc, then `Rscript INSTALL_PACKAGES.R`. Source data are bundled; rebuilding needs no scraper or legislator repository. Downloading/installing software dependencies and opening original PDF/readings links still require their usual access. On systems with multiple Python installations, set `CONGRESS_PYTHON` to the desired Python 3 executable.

Optional input reproduction and verification:

```bash
python3 scripts/prepare_2025.py
python3 scripts/verify_2025_inputs.py
Rscript render.R
python3 verify_v1.py
```

Rendering verifies the manifest first and reuses compiled reference caches only while their source, code and table hashes match. Fresh checkouts reconstruct both reference tables from the bundled YAML subsets. See [input provenance and limits](data/2025/README.md) and [the import audit](validation/input-audit.json).

Required packages are listed in `INSTALL_PACKAGES.R`.

## GitHub Pages

`.github/workflows/pages.yml` runs the same `render.R` entry point and deploys the resulting `index.html` to GitHub Pages whenever `main` is updated.
