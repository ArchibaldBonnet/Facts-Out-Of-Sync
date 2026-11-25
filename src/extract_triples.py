import json
import os
import re
import sys
import time
from datetime import date
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

DATA = Path(__file__).resolve().parent.parent / "data"
INPUT = DATA / "selected_news.json"
OUTPUT = DATA / "extracted_news.json"
CHECKPOINT = DATA / "extraction_checkpoint.json"

PREDICATES = {
    "winner": "P1346",
    "ranking": "P1352",
    "retirement": "P2032",
    "prize money": "P2121",
    "coach": "P286",
    "award": "P166",
    "venue": "P115",
}

SYSTEM_PROMPT = """You extract facts from a tennis news headline as knowledge-graph triples.
Only extract facts of these predicates:
- winner: who won a whole tournament event or an award edition (object: the winner names)
- ranking: a ranking position reached by a player (object: the position, e.g. "1")
- retirement: a player retires or announces retirement (object: the retirement year if stated, else null)
- prize money: total prize money of a tournament edition (object: amount and currency, e.g. "53000000 USD")
- coach: a player starts or ends working with a coach (object: the coach name)
- award: a player receives an award (object: the award name)
- venue: a tournament gets a new venue, stadium, court or roof (object: the venue name)

SUBJECT RULES (the subject is the entity that carries the fact on Wikidata):
- winner: the tournament edition and event, written like its English Wikipedia title,
  e.g. "2024 Australian Open – Men's singles"
- prize money: the tournament edition, e.g. "2024 Australian Open"
- ranking, retirement, coach, award: the player full name
- venue: the tournament, e.g. "French Open"

OTHER RULES:
- Use only the headline. Never invent a value: if the value is not in the headline, set object to null.
- date: the day the fact happened or was announced, format YYYY-MM-DD. If the headline gives no date,
  use the publication date. Never later than the publication date.
- retrospective: true if the headline recalls a past event (anniversary, flashback, "on this day",
  history series) instead of reporting news. Then date is the year of the past event (YYYY) or null.
- ended: true if the fact is the end of a relation (e.g. a coach split), else false.
- wikipedia_search_query: a short query to find the English Wikipedia page of the subject.
- A headline can contain several facts: return all of them. Return an empty list if there is no fact.

Return only JSON:
{"facts": [{"subject": "...", "predicate": "...", "object": "...", "date": "...",
"retrospective": false, "ended": false, "wikipedia_search_query": "..."}]}"""

EXAMPLES = [
    (
        {"title": "Krawietz/Puetz Win Hamburg Title, Lammons/Withrow Claim Atlanta Crown", "source": "ATP", "published": "2023-07-30"},
        {"facts": [
            {"subject": "2023 Hamburg European Open – Men's doubles", "predicate": "winner", "object": "Kevin Krawietz and Tim Pütz", "date": "2023-07-30", "retrospective": False, "ended": False, "wikipedia_search_query": "2023 Hamburg European Open men's doubles"},
            {"subject": "2023 Atlanta Open – Doubles", "predicate": "winner", "object": "Nathaniel Lammons and Jackson Withrow", "date": "2023-07-30", "retrospective": False, "ended": False, "wikipedia_search_query": "2023 Atlanta Open doubles"},
        ]},
    ),
    (
        {"title": "AO Flashback: 'Change-agent' Agassi beats Sampras in blockbuster 1995 final", "source": "Australian Open", "published": "2024-09-30"},
        {"facts": [
            {"subject": "1995 Australian Open – Men's singles", "predicate": "winner", "object": "Andre Agassi", "date": "1995", "retrospective": True, "ended": False, "wikipedia_search_query": "1995 Australian Open men's singles"},
        ]},
    ),
    (
        {"title": "2025 Rome prize money", "source": "ATP", "published": "2025-05-02"},
        {"facts": [
            {"subject": "2025 Italian Open", "predicate": "prize money", "object": None, "date": "2025-05-02", "retrospective": False, "ended": False, "wikipedia_search_query": "2025 Italian Open tennis"},
        ]},
    ),
    (
        {"title": "Rune & Mouratoglou mutually split", "source": "ATP", "published": "2024-07-29"},
        {"facts": [
            {"subject": "Holger Rune", "predicate": "coach", "object": "Patrick Mouratoglou", "date": "2024-07-29", "retrospective": False, "ended": True, "wikipedia_search_query": "Holger Rune"},
        ]},
    ),
    (
        {"title": "Sinner rises to No. 1, Mover of Week", "source": "ATP", "published": "2024-06-10"},
        {"facts": [
            {"subject": "Jannik Sinner", "predicate": "ranking", "object": "1", "date": "2024-06-10", "retrospective": False, "ended": False, "wikipedia_search_query": "Jannik Sinner"},
        ]},
    ),
    (
        {"title": "Final Preview: Zverev vs. Alcaraz in Nitto ATP Finals championship blockbuster", "source": "ATP", "published": "2026-11-22"},
        {"facts": []},
    ),
]

client = OpenAI(base_url=os.environ["EURECOM_LLM_URL"], api_key=os.environ["EURECOM_LLM_KEY"])
MODEL = os.environ["EURECOM_LLM_MODEL"]


def user_message(record):
    return f"Headline: {record['title']}\nSource: {record['source']}\nPublished: {record['published']}"


def build_messages(record):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for example, answer in EXAMPLES:
        messages.append({"role": "user", "content": user_message(example)})
        messages.append({"role": "assistant", "content": json.dumps(answer, ensure_ascii=False)})
    messages.append({"role": "user", "content": user_message(record)})
    return messages


def parse_json(content):
    start = content.find("{")
    end = content.rfind("}")
    return json.loads(content[start:end + 1])


def check_date(fact, published):
    value = fact["date"]
    if fact["retrospective"]:
        if value is not None and not re.fullmatch(r"\d{4}(-\d{2}(-\d{2})?)?", str(value)):
            raise ValueError(f"bad retrospective date {value}")
        return
    if date.fromisoformat(value) > date.fromisoformat(published):
        raise ValueError(f"date {value} after publication {published}")


def validate(answer, record):
    facts = answer["facts"]
    if not isinstance(facts, list):
        raise ValueError("facts is not a list")
    for fact in facts:
        fact["predicate"] = str(fact["predicate"]).replace("_", " ").lower()
        if fact["predicate"] not in PREDICATES:
            raise ValueError(f"unknown predicate {fact['predicate']}")
        if not isinstance(fact["subject"], str) or not fact["subject"].strip():
            raise ValueError("empty subject")
        if fact["object"] is not None and not str(fact["object"]).strip():
            raise ValueError("empty object")
        if not isinstance(fact["retrospective"], bool) or not isinstance(fact["ended"], bool):
            raise ValueError("retrospective and ended must be booleans")
        check_date(fact, record["published"])
        fact["wikidata_pid"] = PREDICATES[fact["predicate"]]
    return facts


def extract(record):
    response = client.chat.completions.create(model=MODEL, temperature=0, messages=build_messages(record))
    return validate(parse_json(response.choices[0].message.content), record)


def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    news = json.loads(INPUT.read_text(encoding="utf-8"))
    done = json.loads(CHECKPOINT.read_text(encoding="utf-8")) if CHECKPOINT.exists() else {}

    for record in news[:limit]:
        if record["id"] in done:
            continue
        facts = None
        for attempt in range(3):
            try:
                facts = extract(record)
                break
            except Exception as error:
                print(f"{record['id']} attempt {attempt + 1} failed: {error}")
                time.sleep(2)
        if facts is None:
            print(f"{record['id']} skipped")
            continue
        done[record["id"]] = facts
        CHECKPOINT.write_text(json.dumps(done, ensure_ascii=False), encoding="utf-8")
        print(f"{record['id']}: {len(facts)} fact(s) | {record['title'][:70]}")

    for record in news:
        if record["id"] in done:
            record["facts"] = done[record["id"]]
            record["extraction_status"] = "facts" if done[record["id"]] else "none"
        else:
            record["facts"] = []
            record["extraction_status"] = "failed"
    OUTPUT.write_text(json.dumps(news, indent=2, ensure_ascii=False), encoding="utf-8")

    facts = [fact for record in news for fact in record["facts"]]
    print(f"News with facts: {sum(r['extraction_status'] == 'facts' for r in news)}")
    print(f"News without fact: {sum(r['extraction_status'] == 'none' for r in news)}")
    print(f"News failed: {sum(r['extraction_status'] == 'failed' for r in news)}")
    print(f"Facts: {len(facts)} | retrospective: {sum(f['retrospective'] for f in facts)} | object null: {sum(f['object'] is None for f in facts)}")


if __name__ == "__main__":
    main()
