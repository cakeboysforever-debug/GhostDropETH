"""Scrape community discussions for VPN-related leads.

This helper consolidates Reddit searches and forum RSS feeds that often surface
people asking about VPN recommendations, streaming issues, or privacy
concerns. The goal is to gather fresh conversation starters so the outreach
team can join the discussion with value-first advice that references the
GhostDropETH guide.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Iterable
from xml.etree import ElementTree

USER_AGENT = "GhostDropETHLeadScraper/1.0 (+https://ghostdrop.eth)"


@dataclass(slots=True)
class Lead:
    """Represents a single scraped discussion."""

    source: str
    title: str
    url: str
    created: datetime

    def to_dict(self) -> dict[str, str]:
        return {
            "source": self.source,
            "title": self.title,
            "url": self.url,
            "created": self.created.isoformat(),
        }


# Search configurations that target common "looking for a VPN" chatter.
REDDIT_SEARCHES: list[dict[str, object]] = [
    {
        "name": "r/VPN — Troubleshooting & help",
        "subreddit": "VPN",
        "query": "help OR recommendation",
    },
    {
        "name": "r/Privacy — VPN shopping threads",
        "subreddit": "privacy",
        "query": "vpn recommendation",
    },
    {
        "name": "r/cordcutters — Streaming blocks",
        "subreddit": "cordcutters",
        "query": "vpn netflix OR vpn hulu",
    },
]


# Forum RSS feeds that routinely surface VPN interest threads.
FORUM_FEEDS: list[dict[str, str]] = [
    {
        "name": "Wilders Security — Privacy & Anonymity",
        "feed": "https://www.wilderssecurity.com/forums/privacy-anonymity.44/index.rss",
    },
    {
        "name": "Linus Tech Tips — Networking",
        "feed": "https://linustechtips.com/rss/7-networking.xml",
    },
    {
        "name": "Tom's Hardware — Networking",
        "feed": "https://www.tomshardware.com/feeds/all",
    },
]


def fetch_url(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read()


def scrape_reddit(limit: int) -> Iterable[Lead]:
    for search in REDDIT_SEARCHES:
        params = {
            "q": search["query"],
            "restrict_sr": 1,
            "sort": "new",
            "limit": str(limit),
        }
        url = (
            f"https://www.reddit.com/r/{search['subreddit']}/search.json?"
            f"{urllib.parse.urlencode(params)}"
        )
        try:
            payload = fetch_url(url)
        except urllib.error.URLError as exc:
            print(
                f"[warning] Failed to query {search['name']} ({exc.reason if hasattr(exc, 'reason') else exc}).",
                file=sys.stderr,
            )
            continue

        try:
            data = json.loads(payload)
        except json.JSONDecodeError as exc:
            print(f"[warning] Could not decode JSON for {search['name']}: {exc}.", file=sys.stderr)
            continue

        posts = data.get("data", {}).get("children", [])
        for post in posts:
            node = post.get("data", {})
            title = node.get("title")
            permalink = node.get("permalink")
            created_utc = node.get("created_utc")
            if not title or not permalink or not created_utc:
                continue
            created = datetime.fromtimestamp(float(created_utc), tz=timezone.utc)
            yield Lead(
                source=search["name"],
                title=title.strip(),
                url=f"https://www.reddit.com{permalink}",
                created=created,
            )


def parse_rss_datetime(raw: str | None) -> datetime:
    if not raw:
        return datetime.now(tz=timezone.utc)
    try:
        parsed = parsedate_to_datetime(raw)
    except (TypeError, ValueError):
        return datetime.now(tz=timezone.utc)
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def scrape_forums(limit: int) -> Iterable[Lead]:
    for feed in FORUM_FEEDS:
        try:
            payload = fetch_url(feed["feed"])
        except urllib.error.URLError as exc:
            print(
                f"[warning] Failed to fetch feed {feed['name']} ({exc.reason if hasattr(exc, 'reason') else exc}).",
                file=sys.stderr,
            )
            continue

        try:
            root = ElementTree.fromstring(payload)
        except ElementTree.ParseError as exc:
            print(f"[warning] Invalid RSS for {feed['name']}: {exc}.", file=sys.stderr)
            continue

        channel = root.find("channel")
        items = [] if channel is None else channel.findall("item")
        for item in items[:limit]:
            title = item.findtext("title")
            link = item.findtext("link")
            published = parse_rss_datetime(item.findtext("pubDate"))
            if not title or not link:
                continue
            yield Lead(
                source=feed["name"],
                title=title.strip(),
                url=link.strip(),
                created=published,
            )


def format_leads(leads: list[Lead]) -> str:
    lines: list[str] = []
    for lead in leads:
        timestamp = lead.created.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        lines.append(f"[{timestamp}] {lead.source}\n  {lead.title}\n  {lead.url}")
    return "\n\n".join(lines)


def collect_leads(limit: int) -> list[Lead]:
    leads = list(scrape_reddit(limit)) + list(scrape_forums(limit))
    leads.sort(key=lambda entry: entry.created, reverse=True)
    return leads


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scrape subreddit searches and forum RSS feeds for VPN-focused discussions.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Maximum posts to fetch per source (default: 5).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON instead of plain text.",
    )
    args = parser.parse_args()

    try:
        leads = collect_leads(limit=max(1, args.limit))
    except Exception as exc:  # pragma: no cover - defensive catch for CLI usage
        print(f"[error] Unexpected failure: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps([lead.to_dict() for lead in leads], indent=2))
    else:
        if not leads:
            print("No leads found. Try increasing --limit or editing the source lists.")
        else:
            print(format_leads(leads))


if __name__ == "__main__":
    # Respectful pacing between requests when called repeatedly via cron or CI.
    time.sleep(0.5)
    main()
