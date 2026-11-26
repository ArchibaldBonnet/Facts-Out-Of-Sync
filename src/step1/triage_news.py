import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

DATA = Path(__file__).resolve().parents[2] / "data" / "step1"
INPUT = DATA / "raw_news.json"
OUTPUT = DATA / "triaged_news.json"
CHECKPOINT = DATA / "triage_checkpoint.json"
BATCH_SIZE = 50

PREDICATES = {
    "winner",
    "prize money",
    "ranking",
    "retirement",
    "coach",
    "venue",
    "award",
    "career titles",
    "match result",
}

SYSTEM_PROMPT = """You screen tennis news headlines.
For each numbered headline, decide whether it states one concrete fact of these types:
- winner: a player or team won a whole tournament (including a final won) or an award edition
- prize money: the total prize money of a tournament edition
- ranking: a player reaches a ranking position (e.g. world No. 1, year-end No. 1)
- retirement: a player retires or announces a retirement date
- coach: a player or federation appoints or separates from a coach
- venue: a tournament moves, gets a new venue, stadium or surface
- award: a player receives an award
- career titles: a player reaches a number of career titles
- match result: a player defeats another player in a match that is not the final
Set keep to false for player profiles, ranking history pages, interviews, previews,
opinions, schedules, tickets, and any headline without a concrete fact.
Return only JSON: {"results": [{"id": 1, "keep": true, "predicate": "winner"}, ...]}
with exactly one entry per headline, using the same numbers. Use predicate null when keep is false."""

client = OpenAI(base_url=os.environ["EURECOM_LLM_URL"], api_key=os.environ["EURECOM_LLM_KEY"])
MODEL = os.environ["EURECOM_LLM_MODEL"]


def parse_json(content):
    start = content.find("{")
    end = content.rfind("}")
    return json.loads(content[start:end + 1])


def ask(batch):
    headlines = "\n".join(f"{i}. {record['title']}" for i, record in enumerate(batch, start=1))
    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": headlines},
        ],
    )
    results = parse_json(response.choices[0].message.content)["results"]
    decisions = {int(result["id"]): result for result in results}
    if set(decisions) != set(range(1, len(batch) + 1)):
        raise ValueError("ids do not match the batch")
    for result in decisions.values():
        if result.get("predicate"):
            result["predicate"] = result["predicate"].replace("_", " ").lower()
        if result["keep"] and result.get("predicate") not in PREDICATES:
            raise ValueError(f"unknown predicate {result.get('predicate')}")
    return decisions


def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    news = json.loads(INPUT.read_text(encoding="utf-8"))
    done = json.loads(CHECKPOINT.read_text(encoding="utf-8")) if CHECKPOINT.exists() else {}
    batches = [news[i:i + BATCH_SIZE] for i in range(0, len(news), BATCH_SIZE)][:limit]

    for index, batch in enumerate(batches):
        if str(index) in done:
            continue
        decisions = None
        for attempt in range(3):
            try:
                decisions = ask(batch)
                break
            except Exception as error:
                print(f"Batch {index + 1} attempt {attempt + 1} failed: {error}")
                time.sleep(2)
        if decisions is None:
            print(f"Batch {index + 1} skipped")
            continue
        done[str(index)] = [
            {
                "id": record["id"],
                "keep": bool(decisions[i]["keep"]),
                "predicate": decisions[i]["predicate"] if decisions[i]["keep"] else None,
            }
            for i, record in enumerate(batch, start=1)
        ]
        CHECKPOINT.write_text(json.dumps(done), encoding="utf-8")
        print(f"Batch {index + 1}/{len(batches)} done")

    by_id = {decision["id"]: decision for batch in done.values() for decision in batch}
    for record in news:
        decision = by_id.get(record["id"])
        record["triage_keep"] = decision["keep"] if decision else None
        record["triage_predicate"] = decision["predicate"] if decision else None
    OUTPUT.write_text(json.dumps(news, indent=2, ensure_ascii=False), encoding="utf-8")
    kept = sum(1 for record in news if record["triage_keep"])
    print(f"Kept {kept} news out of {len(by_id)} triaged ({len(news)} total)")


if __name__ == "__main__":
    main()
