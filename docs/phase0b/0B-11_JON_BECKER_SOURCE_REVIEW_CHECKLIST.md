# Phase 0B-11 — Jon-Becker / Local Archive Source Review Checklist

## 1) Purpose

This checklist is a **review-before-import control** for candidate historical sources in Phase 0B.

It exists to ensure:

- source, license, and provenance clarity is documented before any loader/import ticket,
- inspection is read-only and documentation-first,
- no source bytes are loaded into MEG research tables yet,
- and there is no live-trading/runtime impact.

This ticket is documentation-only and does not change execution behavior, Redis/Postgres contracts, or Telegram approval flow.

## 2) Review targets

Review one or more of the following sources before any import implementation:

1. `Jon-Becker/prediction-market-analysis` repository snapshot.
2. Local ~36 GiB Polymarket/Kalshi historical archive (if present in local environment).
3. Any proposed tiny fixture derivation candidates from the above sources.

## 3) Questions to answer before import

Record explicit answers (with evidence paths/commands) for each source:

1. What files exist?
2. What formats are present?
3. What time range is covered?
4. What fields/columns exist?
5. Are `condition_id`, `token_id`, and `outcome` available?
6. Are legacy market identifier fields present?
7. Are wallet/fill/trade rows present?
8. Are price snapshots present?
9. Are resolution/outcome labels present?
10. What is the license/terms status?
11. Is local-only inspection allowed?
12. Can tiny fixtures be derived safely?

## 4) Repository/source inspection commands to record (read-only)

Use read-only inspection commands and save command output excerpts in the review notes.

### 4.1 Git provenance snapshot (repository sources)

```bash
git remote -v
git rev-parse HEAD
```

### 4.2 File inventory and format discovery

```bash
find . -maxdepth 3 -type f | sort | head -200
find . -type f \( -name "*.parquet" -o -name "*.csv" -o -name "*.json" -o -name "*.jsonl" \)
```

### 4.3 Size check

```bash
du -sh .
```

### 4.4 Optional Python snippets (inspection-only examples)

Use only for local counting/summarization during review (no mutation/no import side effects):

```bash
python - <<'PY'
from pathlib import Path
from collections import Counter

root = Path(".")
ext_counts = Counter(p.suffix.lower() for p in root.rglob("*") if p.is_file())
for ext, count in sorted(ext_counts.items()):
    if ext in {".parquet", ".csv", ".json", ".jsonl"}:
        print(ext, count)
PY
```

```bash
python - <<'PY'
import csv
from pathlib import Path

sample = Path("TODO_SAMPLE_FILE.csv")
with sample.open(newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader, [])
print("columns", header)
PY
```

## 5) Review output table template

Use a per-source table with at least the following columns:

| item | finding | evidence/path | risk | decision | follow-up ticket |
|---|---|---|---|---|---|
| license/terms | pending_review / approved / restricted / rejected | command output + file path | high/medium/low | hold/proceed-local/proceed-import-plan | Phase 0B-12 / other |
| provenance completeness | source ID + acquisition + snapshot coverage documented or missing | manifest draft path | high/medium/low | hold/proceed | ticket id |
| canonical identifier coverage | condition/token/outcome present/partial/missing | schema sample path | high/medium/low | hold/proceed | ticket id |
| fixture viability | tiny deterministic subset feasible or blocked | local notes path | high/medium/low | hold/proceed | ticket id |

## 6) License/provenance gate (hard stop rules)

Before any import/loader ticket:

1. `pending_review` means **no import**.
2. Unknown license/terms means **local inspection only**.
3. No external repo vendoring without explicit review.
4. No large data commits.
5. No generated `.duckdb` commits.

## 7) Tiny fixture derivation gate

A tiny fixture may be proposed only if all conditions are met:

1. Source has reviewed `allowed_use` compatible with fixture derivation.
2. Fixture has checksum recorded.
3. Fixture has deterministic regeneration instructions.
4. Fixture remains tiny and repository-safe.
5. Fixture references manifest `source_id`.

## 8) Recommended next ticket

Choose exactly one follow-up based on review outcome:

1. **Phase 0B-12: Fill out `source_manifest.example.yaml` for Jon-Becker/local archive with reviewed placeholders**, or
2. **Phase 0B-12: Tiny source-derived fixture plan**, only if review and terms/provenance gates pass.

## 9) Non-goals

This checklist does not:

- authorize importing real data,
- authorize vendoring external repositories,
- authorize loader implementation,
- alter runtime/shared-rail behavior,
- or grant autonomous execution authority.
