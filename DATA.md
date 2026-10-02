# Data provenance

**Dataset:** Open Food Facts public product database; contributors retain individual-content attribution. Official export: <https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv.gz>. Publisher documentation: <https://world.openfoodfacts.org/data>. Primary licensing declaration: <https://github.com/openfoodfacts/openfoodfacts-server/blob/main/docs/api/tutorials/license-be-on-the-legal-side.md>.

**Retrieved:** 3 October 2026, Asia/Karachi (2026-10-02T20:32:03.306273+00:00). Actual HTTP 200. Last-Modified `Fri, 02 Oct 2026 12:29:34 GMT`. `data/provenance.json` records source response metadata and the exact saved sample hash.

**Selection:** first 300 data rows in publisher TSV order, no filtering or reshuffling. `source_row` is the 1-based data ordinal of this downloaded export prefix, not a permanent publisher ID; `code` is retained exactly. This biased prefix contains products beyond groceries. No image, personal account data, nutritional field, publisher normalized quantity or quality-tag field is fetched into the sample.

**Preprocessing:** stream gzip + TSV decode as UTF-8; retain only `code`, `product_name`, `brands`, `quantity`; attach source ordinal; write JSON without changing field strings. Original values remain in every derived record. Canonical quantity and review diagnostics are added by `core.py` / browser `parser.js`. The sample and derived databases remain under ODbL/DbCL. No arbitrary unknown value is filled.

**Exact committed source SHA-256:** `520931fd9a12f568b9b5992496c7ab68a017606e6877cb15dc100c9a435fe1ed`. The full compressed dump was intentionally not downloaded or checksum verified; connection closes after the bounded decoded prefix. Hash pins exact saved records only. The live export is mutable, so refreshed cohorts need new annotation and measurement.

**Evaluation truth:** 50 fixed random source rows, seed `20261003`, sorted, manually raw-quantity-only annotated before parser implementation. `data/ANNOTATION.md` records rubric and one-author limitation; `data/annotations.json` is scoring input only. Browser inference reads source JSON and parser rules; annotation/results/derived files never feed its parser. Published derivative/results downloads are inspectable evidence, not model inputs.

**Licence:** database [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/); individual contents [DbCL 1.0](https://opendatacommons.org/licenses/dbcl/1-0/). Attribution: “Contains information from Open Food Facts, made available under the Open Database License (ODbL).” Distributed sample/annotations/derivative databases carry these terms and are offered machine-readable without charge. Code is MIT. No endorsement is implied. No product-image/logo rights are assumed.

Run `python scripts/acquire.py --limit 300` to acquire a new bounded snapshot from the primary source with an identifying User-Agent. This is a single public export request, not API search hammering or restricted-site scraping. Requests use no authentication/API key. No synthetic record appears in the primary sample; separate unit-test strings are expressly test fixtures and never counted in real-data metrics.
