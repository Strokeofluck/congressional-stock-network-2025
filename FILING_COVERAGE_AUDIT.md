# Original-filing coverage audit — October 11, 2026

**The 2025 network is known to be a partial extraction.** Its calculations reproduce the accepted input, but missing scanned filings mean that the 55 reporters and their shared-stock relationships do not describe the entire House purchaser population.

## Checks and findings

The live Clerk 2025 and 2026 XML indexes were downloaded from the [official disclosure service](https://disclosures-clerk.house.gov/FinancialDisclosure) and compared with index IDs and checkpoints at scraper commit `a064720e90e715f516cd2a725ece0b6f7a73632b`. No PTR IDs had been added or removed relative to those snapshots. All 118 zero-row filings were downloaded from their official PDF URLs; byte hashes, page counts and text-layer checks are recorded in [filing-coverage.csv](validation/filing-coverage.csv). Other PDFs' text layers were not checked.

| Filing year | Indexed PTRs | Checkpoints present | Zero-row, image-only filings | Pages in those filings |
|---|---:|---:|---:|---:|
| 2025 | 515 | 515 | 66 (12.8%) | 451 |
| 2026 | 418 | 418 | 52 (12.4%) | 401 |

All 118 zero-row checkpoints say `needs_fallback`; none of those PDFs has a usable text layer. The 2025 files belong to 14 distinct indexed reporter names. This counts affected filings and reporters, not missing stock purchasers.

## Confirmed omitted purchases

[Khanna filing 8220750](https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2025/8220750.pdf) identifies Rohit Khanna on page 1. It yielded zero rows; the frozen full public CSV has no Khanna transactions dated 2025. Visually inspected examples:

| PDF page | Asset exactly as shown | Marked action | Transaction date | Owner |
|---|---|---|---|---|
| 3 | GENERAL MILLS INC CMN | Purchase | Jan. 17, 2025 | DC |
| 3 | GENERAL MILLS INC CMN | Purchase | Jan. 21, 2025 | DC |
| 10 | DOW INC CMN | Purchase | Jan. 22, 2025 | DC |
| 20 | A.O. SMITH CORP (DEL) CMN | Purchase | Jan. 17, 2025 | SP |

Review covered rendered pages 1, 2, 3, 10, 20 and 34, not every row in the 34-page filing. These examples prove missing reported common-stock purchases. They have not been inserted into the accepted data or assigned tickers by an unreviewed automated resolver. DC and SP denote dependent-child and spouse assets; these are member-reported transactions, not claims about personal trading decisions.

## Consequence and limits

**High severity:** Missing purchases can add members and shared tickers, increase pair weights and alter descriptive party mixing. The current graph and statistics describe the frozen accepted extract. Disconnected nodes mean no observed shared ticker in that partial extract.

The exact missing purchase and additional-member counts remain unknown. The 52 scanned 2026 filings have not all been classified by transaction date; do not count all of them as missing 2025 purchases. This audit does not certify the nonzero parsed filings, resolve amendments or prove no future late filing will contain 2025 transactions. Archive completeness is not extraction completeness.

## Remediation and reproduction

Recover scanned filings with OCR and checkbox-aware table extraction. Verify action marks, assets, dates, owners and amounts against source images; retain filing/page provenance. Resolve symbols and amendments before adding records. Filter on 2025 transaction dates, then rebuild all network calculations. Separately check successfully parsed filings for partial-page or row omissions.

The [executed notebook](validation/filing-coverage-audit.ipynb) recomputes counts and shows source examples. [filing-coverage.json](validation/filing-coverage.json) records source URLs/hashes, observation time and limits. `python scripts/audit_filing_coverage.py` verifies the saved evidence; `--check-pdfs` redownloads zero-row PDFs and checks hashes/text layers (requires PyMuPDF).
