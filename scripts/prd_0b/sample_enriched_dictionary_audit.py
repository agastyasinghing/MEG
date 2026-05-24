from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

AUDIT_MODE = "sample_enriched_dictionary_local_audit_only"


def run_sample_enriched_dictionary_audit(
    archive_root: Path,
    row_limit: int = 1000,
    family_allowlist: list[str] | None = None,
) -> dict[str, object]:
    if archive_root is None:
        raise ValueError("archive_root is required")

    from scripts.prd_0b.data_dictionary_sample_enrichment import (
        enrich_data_dictionary_with_samples,
        get_sample_enrichment_mode,
        validate_sample_enrichment_summary,
    )

    summary = enrich_data_dictionary_with_samples(
        archive_root=archive_root,
        row_limit=row_limit,
        family_allowlist=family_allowlist,
    )
    contract_errors = validate_sample_enrichment_summary(summary)

    sample_results = summary.get("sample_enrichment_results")
    timing_rows = [r for r in sample_results if isinstance(r, dict)] if isinstance(sample_results, list) else []
    elapsed_pairs: list[tuple[str, float]] = []
    for row in timing_rows:
        elapsed = row.get("sample_elapsed_ms")
        family = str(row.get("family", ""))
        if isinstance(elapsed, (int, float)):
            elapsed_pairs.append((family, float(elapsed)))

    timing_missing = len(timing_rows) == 0 or len(elapsed_pairs) != len(timing_rows)
    sample_total_elapsed_ms = round(sum(ms for _, ms in elapsed_pairs), 3) if elapsed_pairs else None
    sample_max_elapsed_ms = round(max((ms for _, ms in elapsed_pairs), default=0.0), 3) if elapsed_pairs else None
    sample_avg_elapsed_ms = round(sample_total_elapsed_ms / len(elapsed_pairs), 3) if elapsed_pairs else None
    slowest_sample_family = max(elapsed_pairs, key=lambda p: p[1])[0] if elapsed_pairs else None

    wrote_outputs = bool(summary.get("wrote_outputs", False))
    created_duckdb_file = bool(summary.get("created_duckdb_file", False))
    generated_artifacts = summary.get("generated_artifacts") if isinstance(summary.get("generated_artifacts"), list) else []
    committed_fixtures = bool(summary.get("committed_fixtures", False))

    production_readiness_claim = False
    production_latency_slo_claim = False
    final_trading_readiness_claim = False

    enrichment_ok = summary.get("ok") is True
    contract_ok = len(contract_errors) == 0
    outputs_ok = (not wrote_outputs) and (not created_duckdb_file) and (generated_artifacts == []) and (not committed_fixtures)
    claims_ok = not any(
        [
            production_readiness_claim,
            production_latency_slo_claim,
            final_trading_readiness_claim,
        ]
    )

    status = "ok"
    if not enrichment_ok:
        status = "enrichment_not_ok"
    elif not contract_ok:
        status = "contract_validation_failed"
    elif timing_missing:
        status = "sample_timing_missing"

    ok = status == "ok" and outputs_ok and claims_ok

    readiness_flags = {
        "local_sample_enrichment_contract_ready": bool(ok and contract_ok),
        "local_sample_enrichment_latency_observed": bool(ok and not timing_missing),
        "production_readiness_approved": False,
        "production_latency_slo_approved": False,
        "final_trading_readiness_approved": False,
    }

    return {
        "ok": ok,
        "status": status,
        "audit_mode": AUDIT_MODE,
        "archive_root_status": summary.get("archive_root_status"),
        "enrichment_status": summary.get("status"),
        "contract_validation_status": "pass" if contract_ok else "fail",
        "enrichment_mode": get_sample_enrichment_mode(),
        "family_count": int(summary.get("family_count", 0)),
        "enriched_family_count": len(summary.get("enriched_families", [])) if isinstance(summary.get("enriched_families"), list) else 0,
        "missing_family_count": len(summary.get("missing_families", [])) if isinstance(summary.get("missing_families"), list) else 0,
        "skipped_family_count": len(summary.get("skipped_families", [])) if isinstance(summary.get("skipped_families"), list) else 0,
        "row_limit": row_limit,
        "sample_result_count": len(timing_rows),
        "sample_total_elapsed_ms": sample_total_elapsed_ms,
        "sample_max_elapsed_ms": sample_max_elapsed_ms,
        "sample_avg_elapsed_ms": sample_avg_elapsed_ms,
        "slowest_sample_family": slowest_sample_family,
        "contract_errors": contract_errors,
        "readiness_flags": readiness_flags,
        "warnings": summary.get("warnings", []),
        "wrote_outputs": wrote_outputs,
        "created_duckdb_file": created_duckdb_file,
        "generated_artifacts": generated_artifacts,
        "committed_fixtures": committed_fixtures,
        "production_readiness_claim": production_readiness_claim,
        "production_latency_slo_claim": production_latency_slo_claim,
        "final_trading_readiness_claim": final_trading_readiness_claim,
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Sample-enriched dictionary local audit harness")
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run", help="Run local audit")
    run.add_argument("--archive-root", required=True)
    run.add_argument("--row-limit", type=int, default=1000)
    run.add_argument("--family", action="append", default=None)
    run.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    result = run_sample_enriched_dictionary_audit(
        archive_root=Path(args.archive_root),
        row_limit=args.row_limit,
        family_allowlist=args.family,
    )

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(
            "\\n".join(
                [
                    f"audit_mode: {result['audit_mode']}",
                    f"status: {result['status']}",
                    f"ok: {result['ok']}",
                    f"enrichment_status: {result['enrichment_status']}",
                    f"contract_validation_status: {result['contract_validation_status']}",
                    f"sample_result_count: {result['sample_result_count']}",
                    f"sample_total_elapsed_ms: {result['sample_total_elapsed_ms']}",
                    f"slowest_sample_family: {result['slowest_sample_family']}",
                ]
            )
        )
    return 0 if result.get("ok") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
