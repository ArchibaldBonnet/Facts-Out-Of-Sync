import json
import random
from collections import Counter, defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
INPUT = DATA / "triaged_news.json"
OUTPUT = DATA / "selected_news.json"

YEARS = range(2018, 2027)
SEED = 42

QUOTAS = {
    "winner": 45,
    "ranking": 23,
    "retirement": 23,
    "prize money": 23,
    "coach": 15,
    "award": 15,
    "venue": 8,
}


def select(news, predicate, quota, rng):
    by_year = defaultdict(list)
    for record in news:
        if record["triage_keep"] and record["triage_predicate"] == predicate:
            if int(record["published"][:4]) in YEARS:
                by_year[record["published"][:4]].append(record)
    for items in by_year.values():
        rng.shuffle(items)
    selected = []
    while len(selected) < quota and any(by_year.values()):
        for year in sorted(by_year):
            if by_year[year] and len(selected) < quota:
                selected.append(by_year[year].pop())
    return selected


def main():
    rng = random.Random(SEED)
    news = json.loads(INPUT.read_text(encoding="utf-8"))
    selected = []
    for predicate, quota in QUOTAS.items():
        picked = select(news, predicate, quota, rng)
        print(f"{predicate}: {len(picked)} / {quota}")
        selected.extend(picked)
    selected.sort(key=lambda record: record["published"])
    OUTPUT.write_text(json.dumps(selected, indent=2, ensure_ascii=False), encoding="utf-8")
    by_year = Counter(record["published"][:4] for record in selected)
    print("By year:", dict(sorted(by_year.items())))
    print(f"Saved {len(selected)} news to {OUTPUT}")


if __name__ == "__main__":
    main()
