from datetime import datetime
import difflib
import json
import statistics
from urllib.parse import parse_qs, unquote, urlparse
import requests

HEADERS = {
    "User-Agent": (
        "AsyncKnowledgeReproduction/2.0 (archibald.bonnet@eurecom.fr)"
        " python-requests/2.32.3"
    )
}

EXAMPLES = [
    {
        "id": "Example 0",
        "name": "Wimbledon 2026 Men's Singles Final: Jannik Sinner",
        "urls": {
            "Table": "https://en.wikipedia.org/w/index.php?diff=1363830828&oldid=1363825275&title=2026_Wimbledon_Championships_%E2%80%93_Men%27s_singles",
            "Text": "https://en.wikipedia.org/w/index.php?diff=1363831183&oldid=1363830994&title=2026_Wimbledon_Championships_%E2%80%93_Men%27s_singles",
            "KG": "https://www.wikidata.org/w/index.php?diff=prev&oldid=2516735987&title=Q135443559",
        }
    },
    {
        "id": "Example 1",
        "name": "Wimbledon 2024 Prize Money (£50 Million)",
        "urls": {
            "Text": "https://en.wikipedia.org/w/index.php?diff=1228882896&oldid=1228592214&title=2024+Wimbledon+Championships",
            "KG": "https://www.wikidata.org/w/index.php?diff=prev&oldid=2191692104&title=Q121046430",
            "Table": "https://en.wikipedia.org/w/index.php?diff=1294327380&oldid=1292390294&title=Wimbledon+Championships",
        },
    },
    {
        "id": "Example 2",
        "name": "2024 French Open Men's Singles Final: Carlos Alcaraz",
        "urls": {
            "Table": "https://en.wikipedia.org/w/index.php?title=2024_French_Open_–_Men%27s_singles&diff=next&oldid=1228130514",
            "Text": "https://en.wikipedia.org/w/index.php?title=2024_French_Open_–_Men%27s_singles&diff=next&oldid=1228139843",
            "KG": "https://www.wikidata.org/w/index.php?title=Q119056221&diff=prev&oldid=2175226479",
        },
    },
    {
        "id": "Example 3",
        "name": "2024 US Open Men's Singles Final: Jannik Sinner",
        "urls": {
            "Text": "https://en.wikipedia.org/w/index.php?title=2024_US_Open_–_Men%27s_singles&diff=next&oldid=1244719958",
            "Table": "https://en.wikipedia.org/w/index.php?title=2024_US_Open_–_Men%27s_singles&diff=next&oldid=1244719958",
            "KG": "https://www.wikidata.org/w/index.php?title=Q121872692&diff=prev&oldid=2245951608",
        },
    },
    {
        "id": "Example 4",
        "name": "2025 Australian Open Men's Singles Final: Jannik Sinner",
        "urls": {
            "Table": "https://en.wikipedia.org/w/index.php?title=2025_Australian_Open_–_Men%27s_singles&diff=prev&oldid=1271935138",
            "Text": "https://en.wikipedia.org/w/index.php?title=2025_Australian_Open_–_Men%27s_singles&diff=prev&oldid=1271935138",
            "KG": "https://www.wikidata.org/w/index.php?title=Q124376625&diff=prev&oldid=2415551897",
        },
    },
    {
        "id": "Example 5",
        "name": "Carlos Alcaraz Career Titles Update at Indian Wells",
        "urls": {
            "Table": "https://en.wikipedia.org/w/index.php?title=Carlos_Alcaraz&diff=prev&oldid=1214269497",
            "Text": "https://en.wikipedia.org/w/index.php?title=Carlos_Alcaraz&diff=prev&oldid=1214271430",
            "KG": None,
        },
    },
    {
        "id": "Example 6",
        "name": "Roger Federer's Retirement Announcement",
        "urls": {
            "Table": "https://en.wikipedia.org/w/index.php?title=Roger_Federer&diff=prev&oldid=1110438943",
            "Text": "https://en.wikipedia.org/w/index.php?title=Roger_Federer&diff=prev&oldid=1110439588",
            "KG": "https://www.wikidata.org/w/index.php?title=Q1426&diff=prev&oldid=1730388694",
        },
    },
    {
        "id": "Example 7",
        "name": "Aryna Sabalenka Reclaims WTA World No. 1",
        "urls": {
            "Table": "https://en.wikipedia.org/w/index.php?title=Aryna_Sabalenka&diff=prev&oldid=1174790045",
            "Text": "https://en.wikipedia.org/w/index.php?title=Aryna_Sabalenka&diff=prev&oldid=1174790045",
            "KG": "https://www.wikidata.org/w/index.php?title=Q23448791&diff=prev&oldid=1972321300",
        },
    },
    {
        "id": "Example 8",
        "name": "Paris Masters Relocation to La Defense Arena",
        "urls": {
            "Table": "https://en.wikipedia.org/w/index.php?title=Paris_Masters&diff=next&oldid=1255493767",
            "Text": "https://en.wikipedia.org/w/index.php?title=Paris_Masters&diff=prev&oldid=1318423472",
            "KG": "https://www.wikidata.org/w/index.php?title=Q1230166&diff=prev&oldid=2269555477",
        },
    },
    {
        "id": "Example 9",
        "name": "Novak Djokovic Olympic Gold Medal",
        "urls": {
            "Table": "https://en.wikipedia.org/w/index.php?title=Novak_Djokovic&diff=next&oldid=1238561667",
            "Text": "https://en.wikipedia.org/w/index.php?title=Novak_Djokovic&diff=prev&oldid=1238561956",
            "KG": "https://www.wikidata.org/w/index.php?title=Q5812&diff=prev&oldid=2223966491",
        },
    },
    {
        "id": "Example 10",
        "name": "Laureus World Sports Award for Sportsman of the Year (2021)",
        "urls": {
            "Table": "https://en.wikipedia.org/w/index.php?title=Laureus_World_Sports_Award_for_Sportsman_of_the_Year&diff=next&oldid=1016630803",
            "KG": "https://www.wikidata.org/w/index.php?title=Q1808301&diff=prev&oldid=1416621887",
            "Text": "https://en.wikipedia.org/w/index.php?title=Laureus_World_Sports_Award_for_Sportsman_of_the_Year&diff=next&oldid=1021921127",
        },
    },
]


def parse_wiki_url(url):
  parsed = urlparse(url)
  api_url = f"{parsed.scheme}://{parsed.netloc}/w/api.php"
  qs = parse_qs(parsed.query)
  title = unquote(qs.get("title", [""])[0].replace("+", " "))
  diff_param = qs.get("diff", ["prev"])[0]
  oldid_param = qs.get("oldid", [None])[0]
  return api_url, title, diff_param, oldid_param


def resolve_and_fetch_revision_pair(url):
  api_url, title, diff_param, oldid_param = parse_wiki_url(url)

  if diff_param.isdigit():
    target_revid = int(diff_param)
  elif diff_param == "prev":
    target_revid = int(oldid_param)
  elif diff_param == "next":
    params_next = {
        "action": "query",
        "prop": "revisions",
        "titles": title,
        "redirects": 1,
        "rvstartid": int(oldid_param),
        "rvdir": "newer",
        "rvlimit": 2,
        "rvprop": "ids",
        "format": "json",
    }
    resp = requests.get(api_url, params=params_next, headers=HEADERS).json()
    pages = resp.get("query", {}).get("pages", {})
    revs = list(pages.values())[0].get("revisions", [])
    target_revid = revs[1]["revid"] if len(revs) > 1 else int(oldid_param)
  else:
    target_revid = int(oldid_param)

  params_target = {
      "action": "query",
      "revids": target_revid,
      "prop": "revisions",
      "rvprop": "ids|timestamp|user|comment|content",
      "rvslots": "main",
      "format": "json",
  }
  resp_target = requests.get(
      api_url, params=params_target, headers=HEADERS
  ).json()
  pages = resp_target.get("query", {}).get("pages", {})
  if not pages or "-1" in pages:
    return None, None

  revs = list(pages.values())[0].get("revisions", [])
  if not revs:
    return None, None
  curr_rev = revs[0]
  parent_id = curr_rev.get("parentid", 0)

  prev_rev = None
  if parent_id:
    params_prev = {
        "action": "query",
        "revids": parent_id,
        "prop": "revisions",
        "rvprop": "ids|timestamp|content",
        "rvslots": "main",
        "format": "json",
    }
    resp_prev = requests.get(
        api_url, params=params_prev, headers=HEADERS
    ).json()
    p_pages = resp_prev.get("query", {}).get("pages", {})
    if p_pages and "-1" not in p_pages:
      p_revs = list(p_pages.values())[0].get("revisions", [])
      if p_revs:
        prev_rev = p_revs[0]

  return prev_rev, curr_rev


def get_slot_content(rev):
  if not rev:
    return ""
  return rev.get("slots", {}).get("main", {}).get("*", "")


def verify_wikipedia_diff(prev_rev, curr_rev):
  prev_text = get_slot_content(prev_rev).splitlines()
  curr_text = get_slot_content(curr_rev).splitlines()
  added_lines = [
      line[2:].strip()
      for line in difflib.ndiff(prev_text, curr_text)
      if line.startswith("+ ") and line[2:].strip()
  ]
  return added_lines[:2]


def verify_wikidata_diff(prev_rev, curr_rev):
  prev_raw = get_slot_content(prev_rev)
  curr_raw = get_slot_content(curr_rev)
  if not curr_raw:
    return []

  prev_claims = json.loads(prev_raw).get("claims", {}) if prev_raw else {}
  curr_claims = json.loads(curr_raw).get("claims", {})

  modified_props = []
  for prop, statements in curr_claims.items():
    if prop not in prev_claims or prev_claims[prop] != statements:
      modified_props.append(prop)
  return modified_props


def parse_iso(ts):
  return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")


def format_duration(minutes):
  total_seconds = int(round(minutes * 60))
  days, rem = divmod(total_seconds, 86400)
  hours, rem = divmod(rem, 3600)
  mins, _ = divmod(rem, 60)
  parts = []
  if days > 0:
    parts.append(f"{days}d")
  if hours > 0 or days > 0:
    parts.append(f"{hours}h")
  parts.append(f"{mins}m")
  return " ".join(parts)


if __name__ == "__main__":
  wiki_internal_gaps = []
  table_to_kg_gaps = []
  text_to_kg_gaps = []
  total_cycle_gaps = []

  for ex in EXAMPLES:
    print("=" * 75)
    print(f"{ex['id']}: {ex['name']}")
    print("=" * 75)

    timestamps = {}

    for modality in ["Table", "Text", "KG"]:
      url = ex["urls"].get(modality)
      if not url:
        print(f"  [{modality:5s}] None (Property absent on Wikidata)")
        continue

      prev_rev, curr_rev = resolve_and_fetch_revision_pair(url)

      if curr_rev:
        ts = curr_rev["timestamp"]
        revid = curr_rev["revid"]
        timestamps[modality] = parse_iso(ts)

        if modality == "KG":
          changed_props = verify_wikidata_diff(prev_rev, curr_rev)
          verification = f"Modified claims: {changed_props}"
        else:
          added_sample = verify_wikipedia_diff(prev_rev, curr_rev)
          verification = (
              f"Added lines sample: {added_sample[0][:60]}..."
              if added_sample
              else "Verified"
          )

        print(f"  [{modality:5s}] revid={revid} | timestamp={ts}")
        print(f"          -> {verification}")

    if "Table" in timestamps and "Text" in timestamps:
      gap_wiki = (
          abs((timestamps["Text"] - timestamps["Table"]).total_seconds()) / 60.0
      )
      wiki_internal_gaps.append(gap_wiki)
      print(
          f"\n  * Wikipedia Sync Gap (|Table - Text|) : {gap_wiki:.2f} min"
          f" ({format_duration(gap_wiki)})"
      )

    if "Table" in timestamps and "KG" in timestamps:
      gap_t_kg = (
          abs((timestamps["KG"] - timestamps["Table"]).total_seconds()) / 60.0
      )
      table_to_kg_gaps.append(gap_t_kg)
      print(
          f"  * Table <-> KG Delay                  : {gap_t_kg:.2f} min"
          f" ({format_duration(gap_t_kg)})"
      )

    if "Text" in timestamps and "KG" in timestamps:
      gap_tx_kg = (
          abs((timestamps["KG"] - timestamps["Text"]).total_seconds()) / 60.0
      )
      text_to_kg_gaps.append(gap_tx_kg)
      print(
          f"  * Text <-> KG Delay                   : {gap_tx_kg:.2f} min"
          f" ({format_duration(gap_tx_kg)})"
      )

    if len(timestamps) >= 2:
      all_ts = list(timestamps.values())
      full_cycle = (max(all_ts) - min(all_ts)).total_seconds() / 60.0
      if ex["id"] != "Example 0":
        total_cycle_gaps.append((ex["id"], full_cycle))
      print(
          f"  * Total Update Cycle (First -> Last)  : {full_cycle:.2f} min"
          f" ({format_duration(full_cycle)})"
      )
    print()

  print("=" * 75)
  print("SUMMARY STATISTICS ACROSS COLLECTED EXAMPLES (EXAMPLES 1 TO 10)")
  print("=" * 75)

  def print_stats(label, values):
    min_v = min(values)
    max_v = max(values)
    avg_v = statistics.mean(values)
    med_v = statistics.median(values)
    print(f"\n--- {label} (n={len(values)}) ---")
    print(f"  Min    : {min_v:10.2f} min  ({format_duration(min_v)})")
    print(f"  Max    : {max_v:10.2f} min  ({format_duration(max_v)})")
    print(f"  Avg    : {avg_v:10.2f} min  ({format_duration(avg_v)})")
    print(f"  Median : {med_v:10.2f} min  ({format_duration(med_v)})")

  cycle_vals_10 = [v for _, v in total_cycle_gaps]
  print_stats(
      "Total Update Cycle (10 Curated Examples: Ex 1 to Ex 10)", cycle_vals_10
  )
  print_stats("Table <-> KG Delay (Examples 1 to 10 with KG)", table_to_kg_gaps[1:])
  print_stats("Text <-> KG Delay (Examples 1 to 10 with KG)", text_to_kg_gaps[1:])
  print_stats(
      "Wikipedia Internal Delay |Table - Text| (Ex 1 to Ex 10)",
      wiki_internal_gaps[1:],
  )