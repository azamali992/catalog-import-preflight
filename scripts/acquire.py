"""Acquire only a bounded prefix of the official gzip TSV export. No API key."""
import argparse, csv, gzip, hashlib, io, json, pathlib, urllib.request
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]
URL = 'https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv.gz'
FIELDS = ('code', 'product_name', 'brands', 'quantity')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, default=300)
    args = parser.parse_args()
    if not 100 <= args.limit <= 1000:
        parser.error('bounded limit must be 100..1000')
    req = urllib.request.Request(URL, headers={'User-Agent': 'CatalogImportPreflight/1.0 (public portfolio; github.com/azamali992)', 'Accept-Encoding': 'identity'})
    csv.field_size_limit(10_000_000)
    records = []
    with urllib.request.urlopen(req, timeout=90) as response:
        status = response.status
        headers = {k: response.headers.get(k) for k in ('Last-Modified', 'ETag', 'Content-Length')}
        with gzip.GzipFile(fileobj=response) as zipped:
            with io.TextIOWrapper(zipped, encoding='utf-8') as text:
                reader = csv.DictReader(text, delimiter='\t')
                if not set(FIELDS).issubset(reader.fieldnames or []):
                    raise RuntimeError('publisher schema missing required fields')
                for ordinal, row in enumerate(reader, 1):
                    records.append({'source_row': ordinal, **{k: row.get(k, '') for k in FIELDS}})
                    if len(records) == args.limit:
                        break
    data_dir = ROOT / 'data'; data_dir.mkdir(exist_ok=True)
    content = (json.dumps(records, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    (data_dir / 'source.json').write_bytes(content)
    ledger = {'source_url': URL, 'http_status': status, 'retrieved_utc': datetime.now(timezone.utc).isoformat(), 'headers': headers,
              'selection': f'first {args.limit} rows in publisher TSV order; no filtering', 'fields': list(FIELDS),
              'count': len(records), 'sha256_source_json': hashlib.sha256(content).hexdigest(),
              'licence_database': 'ODbL-1.0', 'licence_contents': 'DbCL-1.0',
              'note': 'Response closed after bounded decoded prefix. Full gzip not downloaded or hash-verified. Sample hash pins local exact records, not whole source.'}
    (data_dir / 'provenance.json').write_text(json.dumps(ledger, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(ledger, indent=2))

if __name__ == '__main__': main()
