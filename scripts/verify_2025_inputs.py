"""Fail closed on missing, altered, or out-of-period bundled analysis inputs."""
import csv
import hashlib
import json
from pathlib import Path
from prepare_2025 import EXTRA_FIELDS, read_csv

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/2025'
manifest = json.loads((DATA/'source-manifest.json').read_text(encoding='utf-8'))
entries = [{'path':path, **meta} for path,meta in manifest['files'].items()] + manifest['reference_files']
for entry in entries:
    path = (DATA/entry['path']).resolve()
    assert path.is_relative_to(DATA.resolve()), 'Source path leaves data directory'
    assert path.is_file(), f'Missing bundled source: {entry["path"]}'
    assert hashlib.sha256(path.read_bytes()).hexdigest() == entry['sha256'], f'Changed bundled source: {entry["path"]}'
baseline_path = ROOT/'PTR_transactions_2025_ACCEPTED_STOCK_PURCHASES.csv'
assert hashlib.sha256(baseline_path.read_bytes()).hexdigest() == manifest['baseline_sha256'] == '967a49115179d5458ff339c89e561cbe49913956172cfd2313183d997cfdabeb'
source, accepted, baseline = [read_csv(p) for p in [DATA/'transactions.csv',DATA/'accepted-stock-purchases.csv',baseline_path]]
assert len(source) == 7797 and all(r['transaction_date'].startswith('2025-') for r in source)
candidate = [r for r in source if r['transaction_type']=='P' and r['asset_type']=='ST' and r['ticker_parse_status']=='accepted' and r['ticker_v8_2_cleaned'].strip()]
fields = list(baseline[0])
assert len(candidate) == len(accepted) == len(baseline) == 3179
assert [tuple(r[k] for k in fields) for r in candidate] == [tuple(r[k] for k in fields) for r in baseline]
for full, enriched in zip(candidate,accepted):
    assert all(full[k] == enriched[k] for k in fields + EXTRA_FIELDS), 'Enrichment changed a source value'
    assert enriched['record_id'] == '/'.join(full[k] for k in ['source_year','filing_id','transaction_number_in_filing'])
assert len({r['record_id'] for r in accepted}) == 3179
checkpoints = {(r['source_year'],r['filing_id']) for r in read_csv(DATA/'filing-status.csv')}
assert all((r['source_year'],r['filing_id']) in checkpoints for r in accepted), 'Accepted filing lacks parser checkpoint'
with (ROOT/'committee-snapshot-index-2025.csv').open(encoding='utf-8-sig',newline='') as handle:
    snapshot_commits = {r['source_commit'] for r in csv.DictReader(handle)}
expected_refs = {f'reference/{commit}/{name}' for commit in snapshot_commits
                 for name in ['committee-membership-current.yaml','committees-current.yaml']}
expected_refs.update(f'reference/82b1eaccd2cad9e4172059507f5129fc513962af/{name}' for name in ['legislators-current.yaml','legislators-historical.yaml'])
assert {r['path'] for r in manifest['reference_files']} == expected_refs, 'Pinned reference inventory mismatch'
print(f'PASS: {len(entries)} bundled file hashes, 2025 scope, 3,179 enriched records, frozen baseline and pinned reference inventory.')
