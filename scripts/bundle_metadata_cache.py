#!/usr/bin/env python3
"""Pack or restore the committed scholarly-metadata cache.

The API pipeline writes one immutable JSON envelope per request. Committing those
files individually makes the research record hard to review, so this utility
stores each provider's envelopes in one deterministic JSONL bundle. ``unpack``
restores the original request cache for offline rebuilding.
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_ROOT = ROOT / "data" / "raw" / "scholarly_metadata"
BUNDLE_ROOT = RAW_ROOT / "bundles"


def provider_dirs() -> list[Path]:
    return sorted(
        path
        for path in RAW_ROOT.iterdir()
        if path.is_dir() and path.name != "bundles"
    )


def pack(remove_files: bool = False) -> tuple[int, int]:
    BUNDLE_ROOT.mkdir(parents=True, exist_ok=True)
    provider_count = 0
    record_count = 0
    for provider_dir in provider_dirs():
        records = []
        for path in sorted(provider_dir.glob("*.json")):
            records.append(
                {
                    "cache_file": path.name,
                    "envelope": json.loads(path.read_text(encoding="utf-8")),
                }
            )
        if not records:
            continue
        output = BUNDLE_ROOT / f"{provider_dir.name}.jsonl"
        output.write_text(
            "".join(
                json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n"
                for record in records
            ),
            encoding="utf-8",
        )
        provider_count += 1
        record_count += len(records)
        if remove_files:
            shutil.rmtree(provider_dir)
    manifest = {
        "format": "scholarly-metadata-cache-jsonl-v1",
        "providers": provider_count,
        "records": record_count,
    }
    (BUNDLE_ROOT / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return provider_count, record_count


def unpack() -> tuple[int, int]:
    provider_count = 0
    record_count = 0
    for bundle in sorted(BUNDLE_ROOT.glob("*.jsonl")):
        provider_dir = RAW_ROOT / bundle.stem
        provider_dir.mkdir(parents=True, exist_ok=True)
        for line in bundle.read_text(encoding="utf-8").splitlines():
            if not line:
                continue
            record = json.loads(line)
            destination = provider_dir / record["cache_file"]
            destination.write_text(
                json.dumps(record["envelope"], indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            record_count += 1
        provider_count += 1
    return provider_count, record_count


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    pack_parser = subparsers.add_parser("pack")
    pack_parser.add_argument("--remove-files", action="store_true")
    subparsers.add_parser("unpack")
    args = parser.parse_args()
    if args.command == "pack":
        providers, records = pack(args.remove_files)
    else:
        providers, records = unpack()
    print(f"{args.command}: {providers} providers, {records} records")


if __name__ == "__main__":
    main()
