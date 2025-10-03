"""Generate OSINT-style provider summaries for the GhostDropETH VPN guide."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from textwrap import indent

DATA_FILE = Path(__file__).with_name("data_providers.json")


def load_providers() -> list[dict[str, object]]:
    if not DATA_FILE.exists():
        raise SystemExit(
            f"Missing data file: {DATA_FILE}. Ensure the repository was cloned with data_providers.json present."
        )
    with DATA_FILE.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def find_provider(name: str, providers: list[dict[str, object]]) -> dict[str, object]:
    name_lower = name.lower()
    for entry in providers:
        if entry["name"].lower() == name_lower:
            return entry
    raise SystemExit(f"Provider '{name}' not found. Available: {', '.join(p['name'] for p in providers)}")


def render_provider(entry: dict[str, object]) -> str:
    audits = "\n".join(f"- {audit}" for audit in entry.get("independent_audits", [])) or "- No audits listed"

    lines = [
        f"Provider: {entry['name']}",
        f"Headquarters: {entry['hq']}",
        f"Ownership: {entry['ownership']}",
        "Independent Audits:",
        indent(audits, "  "),
        f"Breach History: {entry['breach_history']}",
        f"Warrant Canary: {entry['warrant_canary']}",
        f"Logging Policy: {entry['logging_policy']}",
        f"Transparency Reports: {entry['transparency_reports']}",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run an OSINT-style profiling report for the supported VPN providers.",
    )
    parser.add_argument(
        "provider",
        nargs="?",
        help="Optional provider name. If omitted, prints all providers.",
    )
    args = parser.parse_args()

    providers = load_providers()
    if args.provider:
        entry = find_provider(args.provider, providers)
        print(render_provider(entry))
    else:
        for index, entry in enumerate(providers, start=1):
            if index > 1:
                print("\n" + "-" * 40 + "\n")
            print(render_provider(entry))


if __name__ == "__main__":
    main()
