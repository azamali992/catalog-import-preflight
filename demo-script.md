# 75-second product walkthrough / optional voiceover

All actions can be captured unattended by `python scripts/capture.py`. Frames are actual 1920×1080 UI, not a mocked result. No seller face/voice is generated; seller may record this narration personally. Captions must carry the story when muted. Source-credit footer persists or is repeated on closing card.

| Time | Actual scene/action | Caption / optional narration |
|---|---|---|
| 0–9s | `01-before.png`, title emphasis | “Supplier quantities arrive in different formats. Keep the original before importing.” |
| 9–22s | Click Review batch; `02-normalized.png` | “300 public product records: 107 pass this schema, 193 need review.” |
| 22–35s | Zoom source/proposed `78,9g` → `78.9 g` | “Normalize supported metric quantities and keep a traceable diff.” |
| 35–48s | Select real row 92; `03-exception.png` | “A real range stays unresolved. No guessed replacement.” |
| 48–58s | Try input `750ml`, click Check; `04-live-input.png` | “The browser computes the new quantity: 750 mL. Mass and volume stay separate.” |
| 58–68s | Review acknowledgement, download both exports; `05-handoff.png` | “Export schema-ready rows and an exception file. Nothing writes to your store.” |
| 68–75s | Result/credit card | “Frozen 50-row author review: 10 → 25 normalized agreements; 25 unresolved, zero wrong accepted. Keep the original. Review every change.” |

Gig cut: 58 seconds by shortening setup/detail sections; use 10→25 only with “50-row author rubric; 25 unresolved” visible. Portfolio cut: 75 seconds, disclose source-preserving rules, single-author limitation and publisher-order sample. Dataset credit: Open Food Facts contributors; ODbL 1.0 / DbCL 1.0. Do not caption results as real-client ROI, AI accuracy, verified barcodes or live Shopify write.
