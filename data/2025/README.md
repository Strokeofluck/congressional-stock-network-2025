# Frozen inputs for the 2025 network

This directory makes the analysis rebuild independent of the portfolio, the House scraper checkout and the congress-legislators checkout. Install the documented R packages and Python 3, then run `Rscript render.R` from the repository root. The renderer verifies the bundled hashes before reading data. Original filing PDFs and educational readings remain external links; this is not an offline PDF archive or a replacement scraping service.

## Period and lineage

The period is **transaction dates in calendar 2025**, not filing year. `transactions.csv` contains 7,797 parsed rows, retaining all 61 source columns and transaction types. Of these, 634 were filed in 2026. The network's accepted stock-purchase subset contains 3,179 rows, including 212 reported in 2026 filings. Other transaction years are excluded.

The snapshot was imported on October 11, 2026 from [house-ptr-scraper at a064720](https://github.com/StrokeOfLuck/house-ptr-scraper/tree/a064720e90e715f516cd2a725ece0b6f7a73632b). `source-manifest.json` records the full upstream CSV hash, exact source URLs, transformations and hashes of the bundled files. The original accepted CSV at the repository root is preserved byte-for-byte for reconciliation.

## Files and reproduction

- `transactions.csv`: frozen 2025 parsed source rows. It is review evidence, not automatically included in the browser payload.
- `accepted-stock-purchases.csv`: original 14 fields plus filing year, parsed transaction number, owner code, filing status, review flags and notification date. Its sequence and all original fields exactly match the former accepted extract. Reproduce it with `python3 scripts/prepare_2025.py`.
- `filing-status.csv`: all 2025 parser checkpoints and the later filing checkpoints containing 2025 transactions. Checkpoints represent parser accounting, not proof of correct extraction.
- `2025FD.xml`: unchanged archived annual Clerk index. It does not independently certify completeness for late 2026 filings.
- `upstream-2025-archive-check.json`: upstream reports 515 expected/archived 2025 PTR PDFs, zero missing and 66 parser-flagged files. This is an archive-accounting claim. Do not equate “Complete” with complete or error-free transaction extraction.
- `reference/`: 32 YAML files derived from exact pinned congress-legislators commits. Committee files retain House committees/membership only. Legislator files retain only House people and terms overlapping January 3–December 31, 2025. The December 17, 2024 committee snapshot is required for January 1–2. The manifest records each original hash and subset rule. The upstream CC0 license is included.

`scripts/vendor_references.R` documents the deterministic House subset transformation. It is a maintenance helper for exact raw files under `source-cache/<commit>/<filename>`; it is not needed during a normal build. Missing bundled sources stop rendering instead of silently downloading replacements.

Run `python3 scripts/verify_2025_inputs.py` to check byte integrity, period, enrichment, filing-checkpoint joins and the reference inventory. After rendering, `python3 verify_v1.py` independently checks the network calculations and every field in the 26,015 committee membership records and 445 roster entries against the full-source baseline. This protects House Intelligence memberships, whose identifier uses HLIG instead of the usual HS prefix. `validation/input-audit.json` preserves the import reconciliation and field coverage.

## Interpretation limits

All accepted rows have distinct **parser-assigned** IDs of the form `filing-year/filing-id/transaction-number`. These are not official transaction IDs. The 124 additional equal signatures in the former reduced extract are distinct parsed records; equal reduced signatures alone do not prove duplication. Original filings are still needed to verify extraction and amendment-to-original relationships.

The legacy `identical_excess_rows` metric still counts equality across the original 14 baseline fields, not equality of the enriched records. Interpret it together with `unique_parsed_record_ids` and `validation/input-audit.json`.

Owner codes are retained as parsed: SP, JT and DC. A missing code is shown as “Not parsed,” never assumed to mean the member personally owned the asset. Codes are missing in 1,951 accepted rows. There are 107 parser-review-flagged accepted rows, three with filing status “Amended” and 28 with the suspicious parsed status “New $200?”; the original values are preserved for review. Successful reconciliation does not certify these fields or eliminate upstream parsing gaps.

The stock threshold remains two **distinct reporting members**. Imported metadata does not change the 55 accepted purchasers, 355 displayed stocks, 45 displayed members, 1,292 displayed affiliations or 494 projected member pairs.
