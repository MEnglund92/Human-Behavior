# FAILED BATCHES LOG (Phase 7A)

Policy: any batch that fails to write/validate twice during authoring is logged here
and skipped (no blocking retries). Failed batches are backfilled in a single sweep
AFTER all books are attempted.

| Batch | Book | #Fails | First Failure | Last Attempt | Error / Notes |
|-------|------|--------|---------------|--------------|----------------|
| spec_lucifer_effect_b15 | lucifer_effect | 3 | 2026-08-10 | 2026-08-10, wave b15+waves | Agent session returned empty result; no file written (3 consecutive attempts). Chapter ch21 (CHAPTER FIFTEEN). Backfill needed. |