# Catalog Import Preflight

**Keep the original. Review every change before importing.** A grocery catalog operator receives quantities like `78,9g`, `1 kg`, ranges and blank fields. Importing them unchanged can fail a destination schema; guessing missing units can corrupt the catalog. This bounded public-data workbench separates metric quantities it can normalize from records a person must check.

**Live demo:** publication pending; no public link is claimed yet. The local demo, tests and unattended capture work without login. This repository demonstrates a fixed public dataset; it is not a customer-facing upload service or live Shopify integration.

## What it does

Load 300 real Open Food Facts text/numeric product records, inspect each source → proposed quantity diff, filter the review queue, try a new quantity in the actual browser parser, then download ready rows and exceptions. Every output keeps the original source row/code/quantity. Nothing writes to a store. Missing product facts stay missing.

Single metric mass/volume only: g/gram/grams/gr/kg and mL/cl/L. Exact decimal conversion keeps mass separate from volume. Ranges, multipacks, ounces, counts and estimated markings such as `300 g e` need review; unsupported does not mean the original fact is wrong. Row 92 is a natural `1.2-2.1 kg` example, preserved without a guessed replacement.

## Run in 60 seconds

Python 3.12+, no runtime dependencies:

```sh
python scripts/serve.py --reset
```

Open `http://127.0.0.1:8013`. Each reload resets the stateless demo. The committed snapshot works offline after the page loads; no external CDN assets or runtime API requests are used. Default processing is deterministic; no cold model loading.

**No API key or environment variable is required for the default demo or public-data acquisition.** There is no paid API. The acquisition script uses the publisher's public export URL and an identifying User-Agent, without credentials. Never put future vendor keys in this browser bundle; a custom integration needs a separate authenticated server and secrets environment.

## Measured results

Run `python scripts/evaluate.py`. Exact source/annotations are committed; [results](data/results.json) and [annotation protocol](data/ANNOTATION.md) describe the denominator.

| Fixed 50-row quantity review | Unchanged canonical-only import baseline | Conservative normalizer |
|---|---:|---:|
| Quantities normalized and agreeing with manual rubric | 10 / 50 | 25 / 50 |
| Wrong normalized quantities | 0 | 0 |
| Unresolved quantities | 40 / 50 | 25 / 50 |
| Status + value agreement, including missing/unsupported | 35 / 50 | 50 / 50 |

The baseline accepts only unchanged canonical `number g` / `number mL` strings. It is a declared destination policy, not a measured merchant error rate. Labels were manually frozen before parser code; the reviewer saw raw quantity only, not publisher normalized fields or parser answers. **One author annotated 50 rows.** This measures agreement with the rubric, not verified product/packaging accuracy, generalization or calibrated confidence. No time/money savings are claimed.

On all **300** pinned records: **116** metric quantities normalize; **142** quantities are missing and **42** unsupported; **107** rows pass name/code/quantity schema, **193** need review, **81** quantity strings differ, and **300/300** originals are preserved. Diagnostic dimensions overlap; ready/review is a disjoint partition. Code policy is 8–14 digits, not a verified barcode checksum or guaranteed SKU identity. Processing milliseconds in the result file are the observed local Python run, not a browser speed guarantee.

## Honest limits

- Publisher-order prefix is biased, not a representative supplier feed. Products include non-grocery entries; no prevalence claim is made about real stores.
- No extraction from product images, price/stock guesses, taxonomy mapping, density conversion, nutritional advice, barcode authenticity check, vendor writes or business ROI evidence.
- Missing names/quantities cannot be repaired automatically. Review is a successful disposition, not “100% cleanup accuracy.”
- CSV values beginning with spreadsheet formula characters receive a protective apostrophe. Exact unmodified originals remain available in source JSON; do not treat Excel-reformatted codes as original strings.
- Checkbox acknowledgement enables a local download only. It is not backend authorization or an enforced ERP approval gate.

## Data, code and reproduction

Data is attributed to **Open Food Facts contributors**: database ODbL 1.0 / individual contents DbCL 1.0. Source and derived databases are freely downloadable from the UI under those terms; software is MIT. No photos/logos are acquired. See [DATA.md](DATA.md) and [data licence notice](DATA-LICENSE.md).

```sh
python scripts/acquire.py --limit 300
python scripts/freeze_annotations.py
python scripts/evaluate.py
python -m unittest discover -s tests -v
```

The acquisition command streams only a bounded prefix of the official gzip TSV export, then closes the response. The export changes over time; rerunning acquisition produces a new cohort, which must be separately annotated before reusing old benchmark claims. The frozen labels are intended for the committed hash, not arbitrary refreshed data. Full gzip checksum and source order stability are not claimed.

Browser verification/capture requires Node.js (parity test), Python Playwright 1.60.0 and its Chromium:

```sh
python -m pip install playwright==1.60.0
python -m playwright install chromium
python scripts/capture.py
# To check a published demo instead:
python scripts/capture.py --url https://your-verified-demo-url/
```

The headless script creates a clean 1920×1080 browser, pre-warms data, checks the 300-row batch, changes an input, inspects the natural range exception, verifies both CSV downloads and saves five actual UI frames in ignored `artifacts/`. CI runs tests/evaluation/capture. The Pages workflow stages runtime/sample/licence files only. Independent launch QA and cold public-link verification remain required.

## Purchase-sized scope

A first pilot can audit up to 100 supplied rows against one agreed schema and return a source-preserving exception file. Buyer data permission, expected units/fields and acceptance examples are required. A reusable importer or vendor write is a separately scoped engagement; runtime costs and authenticated integration depend on the buyer's systems. This public demo does not establish premium demand or imply completed buyer work.
