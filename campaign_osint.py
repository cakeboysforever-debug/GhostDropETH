"""Render OSINT-style username dossiers grouped by campaign niche."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from textwrap import indent

DATA_FILE = Path(__file__).with_name("campaign_profiles.json")


def load_campaigns() -> list[dict[str, object]]:
    if not DATA_FILE.exists():
        raise SystemExit(
            "Missing campaign_profiles.json. Copy the template or run the script with --template to generate one."
        )
    with DATA_FILE.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def render_username(entry: dict[str, object]) -> str:
    lines = [
        f"Handle: {entry.get('handle', 'Unknown')}",
        f"Platform: {entry.get('platform', 'Unknown')}",
        f"Profile URL: {entry.get('profile_url', 'N/A')}",
        f"Audience Summary: {entry.get('audience_summary', 'Not documented')}",
        f"Vetting Status: {entry.get('vetting_status', 'Unreviewed')}",
        f"Last Reviewed: {entry.get('last_reviewed', 'Unspecified')}",
        f"Risk Flags: {entry.get('risk_flags') or 'None noted'}",
        f"Notes: {entry.get('notes') or 'None'}",
    ]
    return "\n".join(lines)


def render_campaign(entry: dict[str, object]) -> str:
    usernames = entry.get("usernames", [])
    if not usernames:
        usernames_section = "  - No usernames documented yet"
    else:
        usernames_section = "\n\n".join(indent(render_username(item), "  ") for item in usernames)

    lines = [
        f"Campaign: {entry['campaign']}",
        f"Niche: {entry['niche']}",
        f"Objective: {entry['objective']}",
        f"Lead Channels: {', '.join(entry.get('lead_channels', [])) or 'N/A'}",
        f"Review Cadence: {entry.get('review_cadence', 'Unspecified')}",
        "Usernames:",
        usernames_section,
    ]
    return "\n".join(lines)


def template() -> str:
    skeleton = [
        {
            "campaign": "Campaign Name",
            "niche": "Target Niche or Vertical",
            "objective": "Goal for the outreach or activation.",
            "lead_channels": ["Primary discovery channels"],
            "review_cadence": "How often the OSINT review occurs (e.g., Weekly)",
            "usernames": [
                {
                    "handle": "@ExampleHandle",
                    "platform": "Platform name",
                    "profile_url": "https://platform.com/example",
                    "audience_summary": "Why this profile matters to the campaign.",
                    "vetting_status": "Approved/Research/Hold",
                    "last_reviewed": "YYYY-MM-DD",
                    "risk_flags": "Red flags or due diligence notes.",
                    "notes": "Next steps, intros, or context."
                }
            ]
        }
    ]
    return json.dumps(skeleton, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Display OSINT username dossiers grouped by campaign niche.",
    )
    parser.add_argument(
        "campaign",
        nargs="?",
        help="Optional campaign name. If omitted, prints every campaign.",
    )
    parser.add_argument(
        "--template",
        action="store_true",
        help="Print a JSON template you can copy to start a new campaign file.",
    )
    args = parser.parse_args()

    if args.template:
        print(template())
        return

    campaigns = load_campaigns()

    if args.campaign:
        match = next(
            (entry for entry in campaigns if entry["campaign"].lower() == args.campaign.lower()),
            None,
        )
        if not match:
            available = ", ".join(entry["campaign"] for entry in campaigns)
            raise SystemExit(f"Campaign '{args.campaign}' not found. Available: {available}")
        print(render_campaign(match))
    else:
        for index, entry in enumerate(campaigns, start=1):
            if index > 1:
                print("\n" + "=" * 60 + "\n")
            print(render_campaign(entry))


if __name__ == "__main__":
    main()
