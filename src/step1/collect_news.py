import json
import time
import urllib.parse
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from pathlib import Path

import requests

SOURCES = {
    "ATP": "atptour.com",
    "Australian Open": "ausopen.com",
    "Roland Garros": "rolandgarros.com",
    "US Open": "usopen.org",
    "Wimbledon": "wimbledon.com",
}

YEARS = range(2015, 2027)

KEYWORDS = [
    "champion OR title OR final",
    "prize money",
    "ranking OR \"No. 1\"",
    "retire OR retirement",
    "coach",
    "venue OR stadium OR surface",
    "award",
]

HEADERS = {"User-Agent": "Mozilla/5.0 (Facts-Out-Of-Sync EURECOM student project)"}

OUTPUT = Path(__file__).resolve().parents[2] / "data" / "step1" / "raw_news.json"


def build_url(domain, keyword, year):
    query = f"site:{domain} ({keyword}) after:{year}-01-01 before:{year + 1}-01-01"
    params = urllib.parse.urlencode({"q": query, "hl": "en-US", "gl": "US", "ceid": "US:en"})
    return f"https://news.google.com/rss/search?{params}"


def fetch(url):
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    return ET.fromstring(response.content).findall(".//item")


def parse_item(item, source_name, domain):
    source_tag = item.find("source")
    source_url = source_tag.get("url", "") if source_tag is not None else ""
    if domain not in source_url:
        return None
    raw_title = item.findtext("title") or ""
    publisher = source_tag.text or ""
    title = raw_title.removesuffix(f" - {publisher}").strip()
    published = parsedate_to_datetime(item.findtext("pubDate"))
    return {
        "source": source_name,
        "title": title,
        "published": published.date().isoformat(),
        "published_utc": published.isoformat(),
        "link": item.findtext("link"),
        "source_url": source_url,
    }


def collect():
    news = {}
    for source_name, domain in SOURCES.items():
        for year in YEARS:
            for keyword in KEYWORDS:
                url = build_url(domain, keyword, year)
                try:
                    items = fetch(url)
                except Exception as error:
                    print(f"FAILED {source_name} {year} {keyword}: {error}")
                    continue
                for item in items:
                    record = parse_item(item, source_name, domain)
                    if record is None:
                        continue
                    key = (record["source"], record["title"].lower())
                    news.setdefault(key, record)
                time.sleep(1)
            print(f"{source_name} {year}: {len(news)} unique news so far")
    return sorted(news.values(), key=lambda r: r["published"], reverse=True)


def main():
    news = collect()
    for index, record in enumerate(news, start=1):
        record["id"] = f"NEWS-{index:04d}"
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps(news, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved {len(news)} news to {OUTPUT}")


if __name__ == "__main__":
    main()
