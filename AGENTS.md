# MEG Agent Rules

- Treat `MEG_MASTER_PRD_v4.1_patched.md` as the frozen source of truth; do not edit it unless explicitly asked.
- Keep Phase 0A work limited to shared rail infrastructure: identifiers, event contracts, Redis channels, market/user streams, Telegram approval queue, Postgres journaling, paper execution, heartbeat, and risk gates.
- Do not add weather strategy, whale strategy, or live-trading strategy implementation while working on Phase 0A documentation.
- Prefer small tickets with explicit acceptance criteria and tests before broad refactors.
- Preserve the canonical identifier contract everywhere: `condition_id`, `token_id`, and `outcome`; never route on `market_id`.
- All execution paths must remain operator-approved through Telegram; no autonomous execution authority.
- Postgres is for operational journaling; DuckDB/Parquet is for historical research data.
