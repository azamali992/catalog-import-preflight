# Quantity annotation protocol

Frozen 3 October 2026 (Asia/Karachi), before parser/application code. Fifty source rows selected with `random.Random(20261003).sample(range(300), 50)`, sorted by ordinal. Reviewer saw **only source row and raw quantity**, not publisher normalized quantity, quality tags, brands or model output. Labels were manually transcribed in `scripts/freeze_annotations.py`; that script merely recreates the label file.

Rubric: single positive decimal plus metric mass/volume is interpretable; kg → g and L/cl → mL. Decimal commas in a single number are decimal marks. A missing string is `missing`. Unitless counts, ounces, pieces/tablets, ranges, multipacks, extraneous text and estimated marking `e` are `unsupported` under this deliberately bounded importer. Unsupported does **not** mean the product fact is incorrect. Never infer density, missing units or product facts. Labels measure agreement with this import rubric, not correctness of original product packaging.

One author reviewed these 50 entries. This is not blinded two-reviewer ground truth; independent QA may identify annotation mistakes, which must be recorded before metric correction. All 50 were read before parser implementation; no label-driven tuning after final scoring. The 300-record prefix is biased by publisher order and is not representative of all products or buyer supplier files.
