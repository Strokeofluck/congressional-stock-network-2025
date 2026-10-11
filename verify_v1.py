"""Independent standard-library verification of the rendered R analysis."""
import csv
import json
import math
import re
import hashlib
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

rows = list(csv.DictReader(open('PTR_transactions_2025_ACCEPTED_STOCK_PURCHASES.csv')))
clean = lambda name: re.sub(r'^Honorable\s+', '', re.sub(r'^Hon\.\s*', '', name, flags=re.I), flags=re.I).strip()
# R strips honorifics; mapping to raw names is verified via the same stock sets.
members = list(csv.DictReader(open('validation/member-metrics.csv')))
edges = list(csv.DictReader(open('validation/member-overlap.csv')))
metrics = json.loads(Path('validation/metrics.json').read_text())
stocks = defaultdict(set)
for row in rows:
    symbol = row['ticker_v8_2_cleaned'].strip().upper()
    if symbol == 'SQ' and 'block' in row['asset_v8_2_cleaned'].lower():
        symbol = 'XYZ'
    stocks[symbol].add(clean(row['politician']))
shared = {ticker for ticker, buyers in stocks.items() if len(buyers) >= 2}
raw_sets = defaultdict(set)
for ticker, buyers in stocks.items():
    for buyer in buyers:
        raw_sets[buyer].add(ticker)
expected_weights = Counter()
for buyers in stocks.values():
    for pair in combinations(sorted(buyers), 2):
        expected_weights[pair] += 1
assert metrics['accepted_rows'] == len(rows) == 3179
assert metrics['accepted_members'] == len(raw_sets) == 55
assert metrics['accepted_tickers'] == len(stocks) == 854
assert metrics['source_ticker_strings'] == len({r['ticker_v8_2_cleaned'] for r in rows}) == 855
assert metrics['normalized_alias_rows'] == sum(r['ticker_v8_2_cleaned'] == 'SQ' and 'block' in r['asset_v8_2_cleaned'].lower() for r in rows) == 2
assert metrics['displayed_rows'] == sum((('XYZ' if r['ticker_v8_2_cleaned'] == 'SQ' and 'block' in r['asset_v8_2_cleaned'].lower() else r['ticker_v8_2_cleaned']) in shared) for r in rows) == 2404
assert metrics['hidden_tickers'] == len(stocks) - len(shared) == 499
assert hashlib.sha256(Path('PTR_transactions_2025_ACCEPTED_STOCK_PURCHASES.csv').read_bytes()).hexdigest() == '809bf153d2fe9ce842ae738d73008a53979446c697b2bc6c66f237b1baf89ad0'
assert metrics['identical_excess_rows'] == len(rows) - len({tuple(r.values()) for r in rows}) == 124
rich = list(csv.DictReader(open('data/2025/accepted-stock-purchases.csv',encoding='utf-8')))
assert metrics['unique_parsed_record_ids'] == len({r['record_id'] for r in rich}) == 3179
assert metrics['missing_owner_codes'] == sum(not r['owner'].strip() for r in rich) == 1951
assert metrics['parser_review_flagged_rows'] == sum(r['needs_review'].lower() == 'true' for r in rich) == 107
assert metrics['projected_edges'] == len(expected_weights) == len(edges)
assert {tuple(sorted((e['from'], e['to']))): int(e['shared_stocks']) for e in edges} == dict(expected_weights)
for e in edges:
    assert set(e['tickers'].split(', ')) == raw_sets[e['from']] & raw_sets[e['to']]
    a,b = raw_sets[e['from']], raw_sets[e['to']]
    assert int(e['from_degree']) == len(a) and int(e['to_degree']) == len(b)
    assert math.isclose(float(e['jaccard']),len(a & b)/len(a | b),abs_tol=1e-12)
for m in members:
    assert int(m['full_stock_degree']) == len(raw_sets[m['id']])
    assert int(m['shared_member_degree']) == sum(bool(raw_sets[m['id']] & ss) for n,ss in raw_sets.items() if n != m['id'])
assert metrics['isolates'] == sum(int(m['shared_member_degree']) == 0 for m in members) == 10
parties = {m['id']: m['party'] for m in members}
for weighted, key in [(False, 'assortativity'), (True, 'weighted_assortativity')]:
    endpoints = Counter(); total = 0; same = 0
    for edge in edges:
        a, b = parties[edge['from']], parties[edge['to']]
        if 'Unknown' in (a, b):
            continue
        w = int(edge['shared_stocks']) if weighted else 1
        endpoints[a] += w; endpoints[b] += w; total += w
        if a == b:
            same += w
    baseline = sum((v / (2 * total)) ** 2 for v in endpoints.values())
    result = (same / total - baseline) / (1 - baseline)
    assert math.isclose(result, metrics[key], abs_tol=1e-10), (key, result, metrics[key])
roster = list(csv.DictReader(open('house-roster-119th-congress-2025-v1.csv')))
assert metrics['roster_count'] == len(roster)
assert all(r['last_2025_term_date'] > '2025-01-03' for r in roster)
assert not any(r['full_name'] == 'Katie Porter' for r in roster)
# House subsetting must preserve every prior snapshot assignment (including HLIG).
reference_baseline = json.loads(Path('validation/reference-baseline.json').read_text())
for filename, expected in reference_baseline.items():
    if filename == 'provenance':
        continue
    with open(filename,encoding='utf-8-sig',newline='') as handle:
        reference_rows = list(csv.DictReader(handle))
    canonical = json.dumps(sorted(tuple(sorted(r.items())) for r in reference_rows),separators=(',',':'),ensure_ascii=True).encode()
    assert len(reference_rows) == expected['rows']
    assert hashlib.sha256(canonical).hexdigest() == expected['canonical_sha256'], filename
html = Path('index.html').read_text(encoding='utf-8')
for marker in ['v1Page', 'v1Threshold', 'v1StockSets', 'Compare members',
               'v1DirectoryFilter', 'Reading guide:', 'sna-deferred-widget', 'Jaccard',
               'two_mode.html#projecting-one-mode-networks',
               'assortitivity.html#estimating-assortativity']:
    assert marker in html, marker
print(json.dumps(metrics, indent=2))
print('PASS: independent counts, projection weights, both assortativity definitions, all reference-table values, roster boundary, and preview content.')
