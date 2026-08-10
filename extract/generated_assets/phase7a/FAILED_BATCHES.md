# FAILED BATCHES LOG (Phase 7A)

Policy: any batch that fails to write/validate twice during authoring is logged here
and skipped (no blocking retries). Failed batches are backfilled in a single sweep
AFTER all books are attempted.

| Batch | Book | #Fails | First Failure | Last Attempt | Error / Notes |
|-------|------|--------|---------------|--------------|----------------|
| spec_lucifer_effect_b15 | lucifer_effect | 3 | 2026-08-10 | 2026-08-10, wave b15+waves | Agent session returned empty result; no file written (3 consecutive attempts). Chapter ch21 (CHAPTER FIFTEEN). Backfill needed. |
| spec_emotional_intelligence_b06 | emotional_intelligence | 2 | 2026-08-10 | 2026-08-10, retry | Agent session returned empty result; no file written (2 attempts: initial + retry). Chapter ch12. Backfill needed. |
| spec_drive_b01 | drive | 2 | 2026-08-10 | 2026-08-10, retry | Agent session returned empty result; no file written (2 attempts: initial + retry). Chapters ch04+ch05. Backfill needed. |
| spec_drive_b06 | drive | 2 | 2026-08-10 | 2026-08-10, retry | Agent session returned empty result; no file written (2 attempts: initial + retry). Chapters ch11-ch14. Backfill needed. |
| spec_drive_b07 | drive | 2 | 2026-08-10 | 2026-08-10, retry | Agent session returned empty result; no file written (2 attempts: initial + retry). Chapters ch15-ch18. Backfill needed. |
| spec_gift_of_fear_b03 | gift_of_fear | 2 | 2026-08-10 | 2026-08-10, retry | Agent session returned empty result; no file written (2 attempts: initial + retry). Chapter ch03. Backfill needed. |
| spec_gift_of_fear_b17 | gift_of_fear | 2 | 2026-08-10 | 2026-08-10, retry | Agent session returned empty result; no file written (2 attempts: initial + retry). Chapters ch21-ch24. Backfill needed. |