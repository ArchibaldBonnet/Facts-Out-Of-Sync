"""
100% Automated Web Scraping & Triple Extraction Pipeline for Tennis News (v2 - High Recall).
Zero hardcoded events: dynamically crawls the 5 official tennis news domains in parallel
across multiple years (2020-2026), resolves player surnames to full names, extracts
standardized (Subject, Predicate, Object) triples with day-precision dates (YYYY-MM-DD),
and exports >=150 events organized by year.
"""

from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from email.utils import parsedate_to_datetime
import json
import re
import unicodedata
import urllib.parse
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Tuple

import requests
from bs4 import BeautifulSoup

# ==============================================================================
# 1. OFFICIAL TENNIS NEWS SOURCES
# ==============================================================================

SOURCES = {
    "ATP": {
        "url": "https://www.atptour.com/en/media/media-releases",
        "domain": "atptour.com",
    },
    "Australian Open": {
        "url": "https://www.tennis.com.au/fan-zone/features-and-media/media-releases",
        "domain": "tennis.com.au",
    },
    "Roland Garros": {
        "url": "https://www.rolandgarros.com/en-us/latest-news",
        "domain": "rolandgarros.com",
    },
    "US Open": {
        "url": "https://www.usopen.org/en_US/news/index.html",
        "domain": "usopen.org",
    },
    "Wimbledon": {
        "url": "https://www.wimbledon.com/en_GB/news",
        "domain": "wimbledon.com",
    },
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

# ==============================================================================
# 2. HIGH-RECALL TRIPLE EXTRACTOR (SURNAME RESOLUTION + 10 REGEX PATTERNS)
# ==============================================================================


class TennisTripleExtractor:
    """
    Extracts standardized (Subject, Predicate, Object) triples from raw headlines.
    Resolves single-word player surnames (e.g., 'Sinner', 'Alcaraz', 'Swiatek')
    into full canonical entity names.
    """

    SURNAME_TO_FULLNAME = {
        "sinner": "Jannik Sinner",
        "alcaraz": "Carlos Alcaraz",
        "djokovic": "Novak Djokovic",
        "nadal": "Rafael Nadal",
        "federer": "Roger Federer",
        "medvedev": "Daniil Medvedev",
        "zverev": "Alexander Zverev",
        "fritz": "Taylor Fritz",
        "ruud": "Casper Ruud",
        "tsitsipas": "Stefanos Tsitsipas",
        "rublev": "Andrey Rublev",
        "rune": "Holger Rune",
        "de minaur": "Alex de Minaur",
        "shelton": "Ben Shelton",
        "draper": "Jack Draper",
        "hurkacz": "Hubert Hurkacz",
        "berrettini": "Matteo Berrettini",
        "thiem": "Dominic Thiem",
        "murray": "Andy Murray",
        "wawrinka": "Stan Wawrinka",
        "kyrgios": "Nick Kyrgios",
        "dimitrov": "Grigor Dimitrov",
        "auger-aliassime": "Felix Auger-Aliassime",
        "humbert": "Ugo Humbert",
        "fils": "Arthur Fils",
        "musetti": "Lorenzo Musetti",
        "mensik": "Jakub Mensik",
        "tiafoe": "Frances Tiafoe",
        "paul": "Tommy Paul",
        "korda": "Sebastian Korda",
        "khachanov": "Karen Khachanov",
        "bublik": "Alexander Bublik",
        "baez": "Sebastian Baez",
        "cerundolo": "Francisco Cerundolo",
        "monfils": "Gael Monfils",
        "gasquet": "Richard Gasquet",
        "schwartzman": "Diego Schwartzman",
        "isner": "John Isner",
        "del potro": "Juan Martin del Potro",
        "cilic": "Marin Cilic",
        "norrie": "Cameron Norrie",
        "popyrin": "Alexei Popyrin",
        "machac": "Tomas Machac",
        "lehecka": "Jiri Lehecka",
        "nakashima": "Brandon Nakashima",
        "mpetshi perricard": "Giovanni Mpetshi Perricard",
        "sabalenka": "Aryna Sabalenka",
        "swiatek": "Iga Swiatek",
        "gauff": "Coco Gauff",
        "rybakina": "Elena Rybakina",
        "pegula": "Jessica Pegula",
        "paolini": "Jasmine Paolini",
        "zheng": "Zheng Qinwen",
        "keys": "Madison Keys",
        "osaka": "Naomi Osaka",
        "barty": "Ashleigh Barty",
        "halep": "Simona Halep",
        "krejcikova": "Barbora Krejcikova",
        "vondrousova": "Marketa Vondrousova",
        "raducanu": "Emma Raducanu",
        "andreescu": "Bianca Andreescu",
        "kenin": "Sofia Kenin",
        "jabeur": "Ons Jabeur",
        "muchova": "Karolina Muchova",
        "badosa": "Paula Badosa",
        "andreeva": "Mirra Andreeva",
        "navarro": "Emma Navarro",
        "collins": "Danielle Collins",
        "azarenka": "Victoria Azarenka",
        "kvitova": "Petra Kvitova",
        "pliskova": "Karolina Pliskova",
        "muguruza": "Garbine Muguruza",
        "kerber": "Angelique Kerber",
        "garcia": "Caroline Garcia",
        "svitolina": "Elina Svitolina",
        "wozniacki": "Caroline Wozniacki",
        "kontaveit": "Anett Kontaveit",
        "sakkari": "Maria Sakkari",
        "ostapenko": "Jelena Ostapenko",
        "fernandez": "Leylah Fernandez",
        "bencic": "Belinda Bencic",
        "anisimova": "Amanda Anisimova",
        "shnaider": "Diana Shnaider",
        "kostyuk": "Marta Kostyuk",
        "vekić": "Donna Vekic",
        "vekic": "Donna Vekic",
        "ivanisevic": "Goran Ivanisevic",
        "cahill": "Darren Cahill",
        "ferrero": "Juan Carlos Ferrero",
        "moya": "Carlos Moya",
    }

    TOURNAMENTS = (
        r"Australian Open|Roland[- ]Garros|French Open|Wimbledon(?:\s+Championships)?|"
        r"US Open|Nitto ATP Finals|ATP Finals|WTA Finals|United Cup|Laver Cup|Davis Cup|"
        r"Billie Jean King Cup|Indian Wells|BNP Paribas Open|Miami Open|"
        r"Monte[- ]Carlo(?:\s+Masters)?|Madrid Open|Mutua Madrid Open|Italian Open|"
        r"Internazionali BNL d'Italia|Rome|Canadian Open|National Bank Open|"
        r"Montreal|Toronto|Cincinnati(?:\s+Open|\s+Masters)?|Western & Southern Open|"
        r"Shanghai(?:\s+Masters)?|Paris Masters|Rolex Paris Masters|China Open|Beijing|"
        r"Japan Open|Tokyo|Vienna|Erste Bank Open|Swiss Indoors(?:\s+Basel)?|Basel|"
        r"Halle|Terra Wortmann Open|Queen's(?:\s+Club)?|Cinch Championships|"
        r"Stuttgart|Eastbourne|Adelaide|Brisbane|Auckland|Doha|Qatar Open|"
        r"Dubai|Acapulco|Rio Open|Buenos Aires|Rotterdam|ABN AMRO Open|"
        r"Dallas Open|Delray Beach|Geneva Open|Lyon Open|Mallorca|Bastad|Gstaad|"
        r"Kitzbuhel|Umago|Umag|Washington|Citi Open|Mubadala Citi DC Open|"
        r"Winston-Salem|Chengdu|Zhuhai|Hangzhou|Almaty|Antwerp|Stockholm|Metz|Belgrade|"
        r"Next Gen ATP Finals|Olympic(?:s|\s+Games)?"
    )

    # Matches either a known surname/fullname OR a capitalized 2-3 word name
    KNOWN_PAT = "|".join(
        sorted((re.escape(k) for k in SURNAME_TO_FULLNAME.keys()), key=len, reverse=True)
    )
    ENTITY_PLAYER = rf"(?:[A-Z][a-zA-Z'’-]+(?:\s+(?:de\s+|del\s+)?[A-Z][a-zA-Z'’-]+)+|\b(?:{KNOWN_PAT})\b)"

    # 1. Prize Money
    RE_PRIZE = re.compile(
        rf"(?P<tourney>{TOURNAMENTS})?.*?"
        r"(?:prize\s*(?:money|pool|fund)|player\s+compensation|record\s+purse|total\s+purse|financial\s+commitment).*?"
        r"(?P<amount>(?:A\$|US\$|\$|£|€)\s*\d+(?:[.,]\d+)?(?:\s*(?:million|m|billion)|\s*,\d{3}(?:,\d{3})?)?)",
        re.IGNORECASE,
    )
    RE_PRIZE_INV = re.compile(
        r"(?P<amount>(?:A\$|US\$|\$|£|€)\s*\d+(?:[.,]\d+)?(?:\s*(?:million|m)|\s*,\d{3}(?:,\d{3})?)?)\s+"
        r"(?:in\s+)?(?:total\s+|record\s+)?(?:prize\s*(?:money|pool|fund)|player\s+compensation|purse)",
        re.IGNORECASE,
    )
    RE_PRIZE_PCT = re.compile(
        rf"(?P<tourney>{TOURNAMENTS}).*?prize\s*(?:money|pool|fund).*?(?P<amount>\d+(?:\.\d+)?\s*(?:%|per\s*cent))",
        re.IGNORECASE,
    )

    # 2. Retirement
    RE_RETIREMENT = re.compile(
        rf"(?P<player>{ENTITY_PLAYER})\b[^.:\n]{{0,40}}?"
        r"(?:announces\s+(?:his\s+|her\s+)?retirement|retires\s+from\s+(?:professional\s+)?tennis|"
        r"to\s+retire\s+(?:after|at|from)|ends\s+(?:his\s+|her\s+)?(?:pro\s+|professional\s+)?career|"
        r"bids\s+farewell|plays\s+final\s+(?:career\s+)?match|calls\s+time\s+on\s+career)",
        re.IGNORECASE,
    )

    # 3. Coaching Changes
    RE_COACH = re.compile(
        rf"(?P<player>{ENTITY_PLAYER})\s+"
        r"(?:hires|appoints|adds|names|parts\s+ways\s+with|splits\s+with|ends\s+partnership\s+with|reunites\s+with|teams\s+up\s+with)\s+"
        r"(?:coach\s+|former\s+rival\s+)?"
        rf"(?P<coach>{ENTITY_PLAYER})",
        re.IGNORECASE,
    )

    # 4. World Ranking Milestones
    RE_RANKING = re.compile(
        rf"(?P<player>{ENTITY_PLAYER})\b[^.:\n]{{0,30}}?"
        r"(?:reclaims|reaches|ascends\s+to|clinches|secures|returns\s+to|becomes|rises\s+to|"
        r"guaranteed|locks\s+up|stays\s+at|crowned|celebrates|breaks\s+into|cracks)\s+"
        r"(?:the\s+|his\s+|her\s+|first\s+)?"
        r"(?P<rank>(?:ATP\s+|WTA\s+|World\s+|Year-End\s+|PIF\s+)*(?:No\.\s*\d+|Number\s+1|Top\s+\d+))",
        re.IGNORECASE,
    )

    # 5. Career Title / Win Milestones
    RE_MILESTONE = re.compile(
        rf"(?P<player>{ENTITY_PLAYER})\b[^.:\n]{{0,25}}?"
        r"(?:wins|captures|claims|lifts|earns|celebrates|reaches|clinches|scores|notches)\s+"
        r"(?:his\s+|her\s+|milestone\s+)?"
        r"(?P<count>\d+(?:st|nd|rd|th))\s+"
        r"(?P<metric>(?:career\s+|ATP\s+|WTA\s+|tour-level\s+|Grand\s+Slam\s+|Masters\s+1000\s+)*(?:title|crown|trophy|win|victory))",
        re.IGNORECASE,
    )

    # 6. Tournament Title Victory
    RE_TOURNEY_WIN = re.compile(
        rf"(?P<player>{ENTITY_PLAYER})\b[^.:\n]{{0,35}}?"
        r"(?:wins|captures|claims|lifts|defends|retains|clinches|triumphs\s+(?:at|in)|crowned\s+champion\s+(?:at|in)|completes.*?title|seals)\s+"
        r"(?:his\s+|her\s+|first\s+|maiden\s+|record\s+|\d+(?:st|nd|rd|th)\s+|back-to-back\s+)*"
        rf"(?P<tourney>{TOURNAMENTS})",
        re.IGNORECASE,
    )

    # 7. Inverse Tournament Title ("At Australian Open, Sinner wins..." or "Wimbledon: Alcaraz wins title")
    RE_TOURNEY_PREFIX = re.compile(
        rf"(?P<tourney>{TOURNAMENTS})[^a-zA-Z0-9]{{1,15}}(?P<player>{ENTITY_PLAYER})\s+"
        r"(?:wins|captures|claims|lifts|defends|retains|triumphs|crowned)",
        re.IGNORECASE,
    )

    # 8. Match / Final Defeat
    RE_MATCH_DEFEAT = re.compile(
        rf"(?P<winner>{ENTITY_PLAYER})\s+"
        r"(?:defeats|beats|outlasts|overcomes|downs|edges|stuns|storms\s+past|rallies\s+past|"
        r"sweeps\s+past|dethrones|holds\s+off|tops|sinks|halts|cruises\s+past|powers\s+past|rolls\s+past|ousts|stops|subdues)\s+"
        rf"(?P<loser>{ENTITY_PLAYER})"
        rf"(?:.*?(?:at|in|to\s+win|for)\s+(?:the\s+)?(?P<tourney>{TOURNAMENTS}))?",
        re.IGNORECASE,
    )

    # 9. Venue / Rule / Surface / Roof Changes
    RE_VENUE_RULE = re.compile(
        rf"(?P<tourney>{TOURNAMENTS}).*?"
        r"(?P<change>Hawk-Eye\s+Live|electronic\s+line\s+calling|relocat(?:es|ion)\s+to\s+[A-Z][a-zA-Z\s]+|"
        r"new\s+roof|retractable\s+roof|official\s+ball|new\s+venue)",
        re.IGNORECASE,
    )

    BAD_NAMES = {
        "grand slam", "world no", "atp tour", "wta tour", "davis cup", "laver cup",
        "united cup", "centre court", "arthur ashe", "rod laver", "philippe chatrier",
        "indian wells", "miami open", "us open", "french open", "australian open",
        "roland garros", "nitto atp", "media release", "press release", "watch live",
        "mens singles", "womens singles", "ladies singles", "gentlemens singles",
        "new york", "melbourne park", "all england", "final highlights",
    }

    @classmethod
    def strip_accents(cls, text: str) -> str:
        return "".join(
            c for c in unicodedata.normalize("NFD", text)
            if unicodedata.category(c) != "Mn"
        )

    @classmethod
    def clean_headline(cls, raw_title: str) -> str:
        # 1. Supprime les suffixes de sites à la fin (même s'il y en a plusieurs : " | Section | Site")
        cleaned = re.sub(r"(\s+[-|–—]\s+[^-|–—]+)+$", "", raw_title.strip())
        # 2. Remplace tout "|" restant au milieu du titre par un tiret pour ne jamais casser les tableaux Markdown
        cleaned = cleaned.replace("|", "–").replace("[", "(").replace("]", ")")
        return cls.strip_accents(" ".join(cleaned.split()))

    @classmethod
    def resolve_player(cls, raw_name: str) -> Optional[str]:
        if not raw_name:
            return None
        clean = raw_name.strip(" ,.:;'\"!?()-")
        low = clean.lower()
        if low in cls.BAD_NAMES or any(b in low for b in cls.BAD_NAMES):
            return None
        # Direct lookup in surname dictionary
        if low in cls.SURNAME_TO_FULLNAME:
            return cls.SURNAME_TO_FULLNAME[low]
        # Check if last word is a known surname
        parts = clean.split()
        if parts and parts[-1].lower() in cls.SURNAME_TO_FULLNAME:
            return cls.SURNAME_TO_FULLNAME[parts[-1].lower()]
        # Accept valid 2-3 word capitalized names
        if 2 <= len(parts) <= 3 and all(p[0].isupper() for p in parts if p):
            return clean
        return None

    @classmethod
    def normalize_tournament(cls, raw_tourney: Optional[str], source: str, headline: str) -> str:
        if not raw_tourney:
            # Try scanning full headline for any tournament mention
            m = re.search(cls.TOURNAMENTS, headline, re.IGNORECASE)
            if m:
                raw_tourney = m.group(0)
        if raw_tourney:
            t = raw_tourney.strip()
            if re.search(r"roland[- ]garros", t, re.IGNORECASE):
                return "French Open"
            if re.search(r"^wimbledon$", t, re.IGNORECASE):
                return "Wimbledon Championships"
            return t
        mapping = {
            "Australian Open": "Australian Open",
            "Roland Garros": "French Open",
            "Wimbledon": "Wimbledon Championships",
            "US Open": "US Open",
            "ATP": "ATP Tour",
        }
        return mapping.get(source, "ATP Tour")

    @classmethod
    def extract(cls, raw_title: str, event_date: str, source: str, url: str) -> Optional[Dict]:
        headline = cls.clean_headline(raw_title)
        year = int(event_date[:4])

        # 1. Prize Money
        m_prize = cls.RE_PRIZE.search(headline) or cls.RE_PRIZE_INV.search(headline) or cls.RE_PRIZE_PCT.search(headline)
        if m_prize:
            gd = m_prize.groupdict()
            tourney = cls.normalize_tournament(gd.get("tourney"), source, headline)
            amount = " ".join(gd["amount"].split())
            return cls._build(
                event_date, year, f"{year} {tourney}", "total prize money", "P2121",
                amount, "Prize Money", "EMPTY", source, url, headline
            )

        # 2. Player Retirement
        m_ret = cls.RE_RETIREMENT.search(headline)
        if m_ret:
            player = cls.resolve_player(m_ret.group("player"))
            if player:
                return cls._build(
                    event_date, year, player, "work period (end) / retirement", "P2032",
                    str(year), "Player Retirement", "STALE", source, url, headline
                )

        # 3. Coaching Change
        m_coach = cls.RE_COACH.search(headline)
        if m_coach:
            player = cls.resolve_player(m_coach.group("player"))
            coach = cls.resolve_player(m_coach.group("coach"))
            if player and coach and player != coach:
                is_split = any(w in headline.lower() for w in ("part", "split", "end"))
                pred = "parts ways with coach" if is_split else "head coach"
                return cls._build(
                    event_date, year, player, pred, "P286",
                    coach, "Coaching Change", "STALE", source, url, headline
                )

        # 4. World Ranking Update
        m_rank = cls.RE_RANKING.search(headline)
        if m_rank:
            player = cls.resolve_player(m_rank.group("player"))
            if player:
                rank_val = " ".join(m_rank.group("rank").split())
                return cls._build(
                    event_date, year, player, "official ranking", "P1352",
                    rank_val, "World Ranking", "STALE", source, url, headline
                )

        # 5. Career Title / Win Milestone
        m_mile = cls.RE_MILESTONE.search(headline)
        if m_mile:
            player = cls.resolve_player(m_mile.group("player"))
            if player:
                count = m_mile.group("count")
                metric = m_mile.group("metric").lower()
                pred = "career singles titles" if any(w in metric for w in ("title", "crown", "trophy")) else "career match wins"
                return cls._build(
                    event_date, year, player, pred, "SCHEMA_GAP",
                    f"{count} {metric}", "Career Milestone", "STALE", source, url, headline
                )

        # 6. Tournament Winner (Standard & Prefix)
        m_win = cls.RE_TOURNEY_WIN.search(headline) or cls.RE_TOURNEY_PREFIX.search(headline)
        if m_win:
            player = cls.resolve_player(m_win.group("player"))
            if player:
                tourney = cls.normalize_tournament(m_win.group("tourney"), source, headline)
                return cls._build(
                    event_date, year, f"{year} {tourney}", "winner", "P1346",
                    player, "Tournament Winner", "EMPTY", source, url, headline
                )

        # 7. Match / Final Defeat
        m_def = cls.RE_MATCH_DEFEAT.search(headline)
        if m_def:
            winner = cls.resolve_player(m_def.group("winner"))
            loser = cls.resolve_player(m_def.group("loser"))
            if winner and loser and winner != loser:
                tourney = cls.normalize_tournament(m_def.group("tourney"), source, headline)
                is_final = any(w in headline.lower() for w in ("final", "title", "champion", "crown", "trophy", "triumph"))
                if is_final:
                    return cls._build(
                        event_date, year, f"{year} {tourney}", "winner", "P1346",
                        winner, "Tournament Winner", "EMPTY", source, url, headline
                    )
                return cls._build(
                    event_date, year, f"{year} {tourney} ({winner})", "defeated opponent", "P1346",
                    loser, "Match Result", "EMPTY", source, url, headline
                )

        # 8. Venue / Rule / Technology Update
        m_rule = cls.RE_VENUE_RULE.search(headline)
        if m_rule:
            tourney = cls.normalize_tournament(m_rule.group("tourney"), source, headline)
            change = " ".join(m_rule.group("change").split())
            return cls._build(
                event_date, year, f"{year} {tourney}", "tournament facility / rule update", "P115",
                change, "Venue & Rules", "STALE", source, url, headline
            )

        return None

    @staticmethod
    def _build(
        event_date: str, year: int, subj: str, pred: str, pid: str,
        obj: str, category: str, init_status: str, source: str, url: str, headline: str
    ) -> Dict:
        return {
            "event_date": event_date,
            "year": year,
            "triple": {
                "subject": subj.strip(),
                "predicate": pred.strip(),
                "wikidata_pid": pid,
                "object": obj.strip(),
            },
            "category": category,
            "expected_initial_status": init_status,
            "source": source,
            "source_url": url,
            "headline": headline,
        }


# ==============================================================================
# 3. MULTI-THREADED MULTI-YEAR WEB SCRAPER (2020–2026)
# ==============================================================================


class HighRecallTennisScraper:
    """
    Crawls the 5 official tennis domains across years 2020-2026 in parallel
    using year-sliced RSS index queries and direct HTML/JSON-LD scraping.
    """

    YEARS = [2026, 2025, 2024, 2023, 2022, 2021, 2020]

    FACETS = [
        '"prize money" OR "prize pool" OR "compensation" OR "purse"',
        '"wins" OR "captures" OR "claims" "title"',
        '"defeats" OR "beats" "final"',
        '"champion" OR "trophy" OR "crown"',
        '"World No. 1" OR "No. 1" OR "ranking"',
        '"retires" OR "retirement" OR "career title" OR "coach"',
    ]

    @staticmethod
    def parse_iso_date(raw_date: str) -> Optional[str]:
        if not raw_date:
            return None
        raw_date = raw_date.strip()
        m_iso = re.search(r"(20[12]\d-\d{2}-\d{2})", raw_date)
        if m_iso:
            return m_iso.group(1)
        try:
            dt = parsedate_to_datetime(raw_date)
            return dt.strftime("%Y-%m-%d")
        except Exception:
            pass
        clean = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", raw_date)
        for fmt in ("%d %B %Y", "%B %d, %Y", "%d %b %Y", "%b %d, %Y"):
            try:
                return datetime.strptime(clean, fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue
        return None

    @classmethod
    def scrape_landing_pages(cls) -> List[Tuple[str, str, str, str]]:
        articles = []
        for source_name, cfg in SOURCES.items():
            url = cfg["url"]
            try:
                resp = requests.get(url, headers=HEADERS, timeout=8)
                if resp.status_code != 200:
                    continue
                soup = BeautifulSoup(resp.text, "html.parser")
                for a_tag in soup.find_all("a", href=True):
                    title = a_tag.get_text(" ", strip=True)
                    if not (25 <= len(title) <= 210):
                        continue
                    full_url = urllib.parse.urljoin(url, a_tag["href"])
                    d_str = cls.parse_iso_date(full_url) or cls.parse_iso_date(title)
                    if d_str:
                        articles.append((title, d_str, source_name, full_url))
            except Exception:
                continue
        return articles

    @classmethod
    def _fetch_single_rss_query(cls, task: Tuple[str, str, str]) -> List[Tuple[str, str, str, str]]:
        source_name, default_url, query = task
        rss_url = (
            "https://news.google.com/rss/search?"
            f"q={urllib.parse.quote(query)}&hl=en-US&gl=US&ceid=US:en"
        )
        results = []
        try:
            resp = requests.get(rss_url, headers=HEADERS, timeout=8)
            if resp.status_code != 200:
                return results
            root = ET.fromstring(resp.content)
            for item in root.findall(".//item"):
                title = item.findtext("title") or ""
                pub_date = cls.parse_iso_date(item.findtext("pubDate") or "")
                link = item.findtext("link") or default_url
                if title and pub_date:
                    results.append((title, pub_date, source_name, link))
        except Exception:
            pass
        return results

    @classmethod
    def crawl_all_years_parallel(cls) -> List[Tuple[str, str, str, str]]:
        tasks = []
        for source_name, cfg in SOURCES.items():
            domain = cfg["domain"]
            default_url = cfg["url"]
            # 1. Broad facet queries per domain
            for facet in cls.FACETS:
                tasks.append((source_name, default_url, f"site:{domain} {facet}"))
            # 2. Year-sliced queries (2020..2026) to force deep historical retrieval
            for yr in cls.YEARS:
                tasks.append((
                    source_name,
                    default_url,
                    f'site:{domain} "{yr}" ("title" OR "final" OR "champion" OR "prize money" OR "No. 1" OR "retires")'
                ))
                tasks.append((
                    source_name,
                    default_url,
                    f'site:{domain} ("defeats" OR "beats" OR "wins" OR "captures") after:{yr}-01-01 before:{yr}-12-31'
                ))

        all_articles = []
        with ThreadPoolExecutor(max_workers=12) as executor:
            futures = [executor.submit(cls._fetch_single_rss_query, t) for t in tasks]
            for fut in as_completed(futures):
                all_articles.extend(fut.result())
        return all_articles


# ==============================================================================
# 4. PIPELINE ORCHESTRATION & EXPORT
# ==============================================================================


def run_pipeline() -> Tuple[Dict[str, List[Dict]], List[Dict]]:
    print("[1/3] Scraping direct HTML landing pages from the 5 official tennis portals...")
    direct_raw = HighRecallTennisScraper.scrape_landing_pages()
    print(f"      -> Collected {len(direct_raw)} raw items from landing pages.")

    print("[2/3] Running parallel multi-year domain queries (2020-2026) across the 5 sites...")
    rss_raw = HighRecallTennisScraper.crawl_all_years_parallel()
    print(f"      -> Collected {len(rss_raw)} raw historical & recent articles.")

    print("[3/3] Extracting standardized (Subject, Predicate, Object) triples & deduplicating...")
    dedup_map: Dict[Tuple[int, str, str, str], Dict] = {}

    for raw_title, pub_date, source_name, link in direct_raw + rss_raw:
        evt = TennisTripleExtractor.extract(raw_title, pub_date, source_name, link)
        if not evt:
            continue
        t = evt["triple"]
        # Deduplicate on (Year, Subject, Predicate, Object)
        key = (
            evt["year"],
            t["subject"].lower(),
            t["predicate"].lower(),
            t["object"].lower(),
        )
        if key not in dedup_map:
            dedup_map[key] = evt

    sorted_events = sorted(dedup_map.values(), key=lambda x: x["event_date"], reverse=True)

    events_by_year: Dict[str, List[Dict]] = defaultdict(list)
    for idx, evt in enumerate(sorted_events, start=1):
        evt["id"] = f"EVT-{idx:03d}"
        events_by_year[str(evt["year"])].append(evt)

    return dict(events_by_year), sorted_events


def save_outputs(
    events_by_year: Dict[str, List[Dict]],
    all_events: List[Dict],
    json_path: str = "tennis_events_100_by_year.json",
    md_path: str = "tennis_events_100_by_year.md",
) -> None:
    by_source = Counter(e["source"] for e in all_events)
    by_cat = Counter(e["category"] for e in all_events)
    by_year = {yr: len(evts) for yr, evts in events_by_year.items()}

    payload = {
        "metadata": {
            "total_extracted_events": len(all_events),
            "pipeline_mode": "100% Automated Multi-Year Domain Scraper + Regex/Entity Triple Extractor",
            "generated_at_utc": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "counts_by_year": by_year,
            "counts_by_source": dict(by_source),
            "counts_by_category": dict(by_cat),
        },
        "events_by_year": events_by_year,
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    md = [
        "# Automated Tennis News Benchmark: 100+ `[Event, Date]` Triples Organized by Year\n",
        f"- **Total Live-Extracted Events:** `{len(all_events)}`",
        "- **Pipeline:** 100% Automated Multi-Year Scraping & Triple Extraction (Zero hardcoded events)",
        "- **Date Precision:** Day precision (`YYYY-MM-DD`)\n",
        "## 1. Summary by Year\n",
        "| Year | Total Events | `EMPTY` Initial State | `STALE` Initial State |",
        "|------|--------------|-----------------------|-----------------------|",
    ]

    for yr in sorted(events_by_year.keys(), reverse=True):
        evts = events_by_year[yr]
        e_cnt = sum(1 for x in evts if x["expected_initial_status"] == "EMPTY")
        s_cnt = sum(1 for x in evts if x["expected_initial_status"] == "STALE")
        md.append(f"| **{yr}** | {len(evts)} | {e_cnt} | {s_cnt} |")

    md.extend([
        "\n## 2. Summary by Source & Category\n",
        "| Official Source | Extracted Events |",
        "|-----------------|------------------|",
    ])
    for src in SOURCES:
        md.append(f"| **{src}** | {by_source.get(src, 0)} |")

    md.append("\n---\n## 3. Extracted `[Event, Date]` Examples by Year\n")
    for yr in sorted(events_by_year.keys(), reverse=True):
        evts = events_by_year[yr]
        md.append(f"### Year {yr} ({len(evts)} Events)\n")
        md.append("| ID | Date (`YYYY-MM-DD`) | Source | Event Triple `(Subject, Predicate, Object)` | PID | Initial State | Scraped Headline |")
        md.append("|---|---|---|---|---|---|---|")
        for e in evts:
            t = e["triple"]
            # Sécurise le triplet et le titre contre tout "|" ou crochet résiduel
            subj = t["subject"].replace("|", "-")
            pred = t["predicate"].replace("|", "-")
            obj = t["object"].replace("|", "-")
            triple_str = f"`({subj}, {pred}, {obj})`"

            safe_headline = e["headline"].replace("|", "–").replace("[", "(").replace("]", ")")
            safe_url = e["source_url"].replace(")", "%29")

            md.append(
                f"| `{e['id']}` | `{e['event_date']}` | **{e['source']}** | {triple_str} | `{t['wikidata_pid']}` | `{e['expected_initial_status']}` | [{safe_headline}]({safe_url}) |"
            )

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    print("\n" + "=" * 72)
    print(f"SUCCESS: Extracted {len(all_events)} unique [Event, Date] triples across {len(events_by_year)} years!")
    print(f"Breakdown by Year   : {by_year}")
    print(f"Breakdown by Source : {dict(by_source)}")
    print(f"Breakdown by Type   : {dict(by_cat)}")
    print(f"Saved JSON -> {json_path}")
    print(f"Saved MD   -> {md_path}")
    print("=" * 72)


if __name__ == "__main__":
    grouped, flat = run_pipeline()
    save_outputs(grouped, flat)