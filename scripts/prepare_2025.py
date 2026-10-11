"""Reproduce the enriched accepted extract from the bundled 2025 transaction snapshot.

No network, third-party Python packages, or other checkouts are used.
"""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/2025"
BASELINE = ROOT / "PTR_transactions_2025_ACCEPTED_STOCK_PURCHASES.csv"
EXTRA_FIELDS = ["source_year", "transaction_number_in_filing", "owner", "filing_status",
                "needs_review", "review_level", "review_reason", "notification_date"]

def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))

def write_csv(path, rows, fields):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fields, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def prepare():
    manifest = json.loads((DATA / "source-manifest.json").read_text(encoding="utf-8"))
    assert digest(DATA / "transactions.csv") == manifest["files"]["transactions.csv"]["sha256"], "Transaction snapshot changed"
    assert digest(BASELINE) == manifest["baseline_sha256"], "Original accepted extract changed"
    source = read_csv(DATA / "transactions.csv")
    baseline = read_csv(BASELINE)
    assert source and all(r["transaction_date"].startswith("2025-") for r in source), "Out-of-period transaction"
    accepted = [r for r in source if r["transaction_type"] == "P" and r["asset_type"] == "ST"
                and r["ticker_parse_status"] == "accepted" and r["ticker_v8_2_cleaned"].strip()]
    baseline_fields = list(baseline[0])
    # Exact sequence equality proves enrichment does not silently change the frozen analysis.
    assert [tuple(r[k] for k in baseline_fields) for r in accepted] == [tuple(r[k] for k in baseline_fields) for r in baseline], "Accepted extract no longer reconciles"
    for row in accepted:
        row["record_id"] = "/".join(row[k] for k in ["source_year", "filing_id", "transaction_number_in_filing"])
    assert len({r["record_id"] for r in accepted}) == len(accepted), "Parsed record identity is not unique"
    write_csv(DATA / "accepted-stock-purchases.csv", accepted, baseline_fields + EXTRA_FIELDS + ["record_id"])
    reduced = Counter(tuple(r[k] for k in baseline_fields) for r in accepted)
    audit = {
        "transaction_year": 2025, "upstream_commit": manifest["upstream_commit"],
        "all_parsed_2025_transactions": len(source), "accepted_stock_purchases": len(accepted),
        "accepted_members": len({r["politician"] for r in accepted}),
        "accepted_extract_sequence_matches_baseline": True,
        "unique_parsed_record_ids": len({r["record_id"] for r in accepted}),
        "excess_equal_baseline_signatures": len(accepted) - len(reduced),
        "rows_in_equal_baseline_signature_groups": sum(n for n in reduced.values() if n > 1),
        "missing_owner_codes": sum(not r["owner"].strip() for r in accepted),
        "owner_codes": dict(Counter(r["owner"] or "not parsed" for r in accepted)),
        "filing_status_values": dict(Counter(r["filing_status"] for r in accepted)),
        "parser_review_flagged_rows": sum(r["needs_review"].lower() == "true" for r in accepted),
        "transaction_rows_by_filing_year": dict(Counter(r["source_year"] for r in source)),
        "accepted_rows_by_filing_year": dict(Counter(r["source_year"] for r in accepted)),
        "scope": "Transaction dates in calendar 2025, including late reports filed in 2026. Parsed source rows are not a certified census of all purchases.",
        "identity_limit": "Record IDs are parser-assigned within a source filing, not official transaction identifiers or amendment-to-original links.",
        "repeat_limit": "Equal signatures in the former reduced extract are not proof of duplicate transactions. Distinct parsed row IDs do not certify extraction accuracy or remove amendment double counting."
    }
    (ROOT / "validation/input-audit.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(audit, indent=2))

if __name__ == "__main__":
    prepare()
