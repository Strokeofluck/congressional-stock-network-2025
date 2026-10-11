"""Verify the recorded original-filing audit; optionally recheck source PDFs.

Default verification uses standard-library Python and performs no downloads.
--check-pdfs requires PyMuPDF and verifies the 118 recorded zero-row sources.
This checks extraction coverage, not transaction recovery or source correctness.
"""
from pathlib import Path
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request, urlopen
import argparse, csv, hashlib, json

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-pdfs', action='store_true')
    parser.add_argument('--cache', type=Path, default=ROOT / 'build/filing-audit-pdfs')
    args = parser.parse_args()
    csv_path = ROOT / 'validation/filing-coverage.csv'
    summary = json.loads((ROOT / 'validation/filing-coverage.json').read_text(encoding='utf-8'))
    assert hashlib.sha256(csv_path.read_bytes()).hexdigest() == summary['audit_inventory_sha256'], 'Audit inventory hash changed'
    with csv_path.open(encoding='utf-8', newline='') as f:
        rows = list(csv.DictReader(f))
    keys = [(r['filing_year'], r['filing_id']) for r in rows]
    assert len(keys) == len(set(keys)), 'Duplicate filing key'
    zero_rows = []
    for year in summary['years']:
        records = [r for r in rows if int(r['filing_year']) == year['filing_year']]
        assert len(records) == year['official_ptr_filings'], 'Index count mismatch'
        assert all(r['parser_status'] != 'missing_checkpoint' for r in records), 'Missing processing checkpoint'
        zero = [r for r in records if r['parsed_transaction_rows'] == '0']
        assert len(zero) == year['zero_row_filings'], 'Zero-row count mismatch'
        assert all(r['parser_status'] == 'needs_fallback' for r in zero), 'Unexpected zero-row status'
        assert all(r['pdf_text_characters'] == '0' and len(r['pdf_sha256']) == 64 for r in zero), 'PDF text/hash evidence missing'
        assert sum(int(r['pdf_pages']) for r in zero) == year['zero_row_pdf_pages'], 'Page count mismatch'
        assert len({r['reporter'] for r in zero}) == year['reporters_with_zero_row_filings'], 'Reporter count mismatch'
        zero_rows.extend(zero)
        print(f"{year['filing_year']}: {len(records)} indexed filings; {len(zero)} image-only zero-row filings; {year['zero_row_pdf_pages']} pages.")
    assert summary['transaction_completeness_verified'] is False, 'Audit must not certify completeness'
    case = summary['confirmed_missing_filing']
    record = next(r for r in rows if r['filing_year'] == str(case['filing_year']) and r['filing_id'] == case['filing_id'])
    assert record['parsed_transaction_rows'] == '0'
    if args.check_pdfs:
        import pymupdf
        def check(r):
            path = args.cache / r['filing_year'] / (r['filing_id'] + '.pdf')
            if path.exists():
                data = path.read_bytes()
            else:
                data = urlopen(Request(r['official_pdf_url'], headers={'User-Agent':'House-PTR-coverage-audit'}), timeout=60).read()
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
            assert hashlib.sha256(data).hexdigest() == r['pdf_sha256'], f"Source bytes changed: {r['filing_year']}/{r['filing_id']}"
            with pymupdf.open(stream=data, filetype='pdf') as doc:
                assert len(doc) == int(r['pdf_pages']), 'PDF page count changed'
                assert sum(len(p.get_text().strip()) for p in doc) == int(r['pdf_text_characters']), 'PDF text-layer result changed'
            return r['filing_id']
        with ThreadPoolExecutor(max_workers=6) as pool:
            checked = list(pool.map(check, zero_rows))
        print(f'PASS: original bytes, pages and text layers for {len(checked)} zero-row PDFs.')
    print('PASS: recorded coverage evidence. The source extraction is known to be incomplete; missing purchases have not been recovered.')

if __name__ == '__main__':
    main()
