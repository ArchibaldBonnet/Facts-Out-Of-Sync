# Facts Out of Sync: Tracking Knowledge Freshness Across Text, Tables, and Knowledge Graphs

This repository contains the source code, manually curated examples, and automated reproduction pipelines for the EURECOM semester project **"Facts out of Sync"** (supervised by Raphaël Troncy, Fanfu Wei, and Thibault Ehrhart).

The goal of this project is to measure, categorize, and analyze asynchronous factual updates across three knowledge modalities within the professional tennis ecosystem:
1. **Wikipedia Text** (unstructured prose in lead sections and tournament summaries)
2. **Wikipedia Tables** (semi-structured infoboxes, brackets, and performance timelines)
3. **Wikidata Knowledge Graph (KG)** (structured RDF claims, qualifiers, and truthy rank lifecycles)

---

## Repository Structure

```text
.
├── README.md
├── requirements.txt
├── data/
│   └── asynchronous_knowledge_examples.md   # Curated examples (Ex 0 to Ex 10) with verified diff URLs and timelines
└── src/
    └── reproduce_examples.py                # Automated MediaWiki API audit and update cycle calculation
```

---

## Current Progress (Snapshot at $t$)

### 1. Manual Collection (`data/asynchronous_knowledge_examples.md`)
We documented **11 asynchronous knowledge update examples** (1 baseline example + 10 diverse tennis ecosystem cases) spanning Grand Slam singles finals, tournament prize money, ATP/WTA world rankings, career title counts, player retirements, tournament venue relocations, Olympic gold medals, and sports awards:
* **Example 0:** Wimbledon 2026 Men's Singles Final (Jannik Sinner) — *Baseline*
* **Example 1:** Wimbledon 2024 Prize Money (£50 Million)
* **Example 2:** 2024 French Open Men's Singles Final (Carlos Alcaraz)
* **Example 3:** 2024 US Open Men's Singles Final (Jannik Sinner)
* **Example 4:** 2025 Australian Open Men's Singles Final (Jannik Sinner)
* **Example 5:** Carlos Alcaraz Career Titles Update at Indian Wells (*Schema gap on Wikidata*)
* **Example 6:** Roger Federer's Retirement Announcement
* **Example 7:** Aryna Sabalenka Reclaims WTA World No. 1
* **Example 8:** Paris Masters Relocation to La Défense Arena
* **Example 9:** Novak Djokovic Olympic Gold Medal (Paris 2024)
* **Example 10:** Laureus World Sports Award for Sportsman of the Year (Rafael Nadal, 2021)

### 2. Automatic Reproduction Pipeline (`src/reproduce_examples.py`)
Given revision diff URLs from Wikipedia and Wikidata, the script queries the live **MediaWiki Action API** (`prop=revisions`) to:
1. **Resolve Revision Identifiers:** Automatically normalizes heterogeneous diff URLs (`diff=prev`, `diff=next`, or explicit revision IDs) to identify the exact post-change revision $r_i$.
2. **Fetch Parent-Child Snapshots:** Retrieves the full content of both the target revision $r_i$ and its immediate predecessor $r_{i-1}$ via `parentid`.
3. **Extract Diff Evidence:** Uses `difflib.ndiff` on Wikitext to print newly added lines (`+ `) for Wikipedia Text/Tables, and parses Wikidata JSON `claims` dictionaries to identify modified property IDs (e.g., `P1346`, `P1352`, `P2121`, `P106`, `P115`, `P166`).
4. **Compute Synchronization Statistics:** Calculates exact timestamps and outputs Min, Max, Mean, and Median update cycles across all modalities.

> **Current Limitation:** The script currently extracts diff evidence (printing added lines and modified Wikidata claims in the terminal) and computes time delays from pre-identified revision URLs, but does not yet perform automated semantic verification to confirm whether the target fact is updated.

---

## Summary Statistics (Examples 1 to 10)

| Synchronization Metric | Min | Max | Median | Mean (Average) |
| :--- | :---: | :---: | :---: | :---: |
| **Total Update Cycle** ($n=10$, First $\rightarrow$ Last) | 16 min (Ex 5) | 358d 07h 11m (Ex 1) | 3d 12h 16m | 85d 17h 28m |
| **Total 3-Modality Cycle** ($n=9$, w/ KG) | 1h 51m (Ex 2) | 358d 07h 11m (Ex 1) | 5d 04h 04m | 95d 06h 02m |
| **Wikipedia Internal Gap** ($\|t_{\text{Table}} - t_{\text{Text}}\|$, $n=10$) | 0 min (Ex 2, 4, 7) | 358d 07h 11m (Ex 1) | **2 min** | 53d 16h 09m |
| **Table $\leftrightarrow$ KG Delay** ($\|t_{\text{KG}} - t_{\text{Table}}\|$, $n=9$) | 1h 51m (Ex 2) | 342d 01h 59m (Ex 1) | 5d 04h 04m | 93d 01h 21m |
| **Text $\leftrightarrow$ KG Delay** ($\|t_{\text{KG}} - t_{\text{Text}}\|$, $n=9$) | 1h 32m (Ex 10) | 259d 05h 25m (Ex 4) | 5d 04h 03m | 37d 10h 05m |

---

## Event Status Taxonomy

To track factual evolution across the **four modal update stages** (Stage 0: Before first update $\rightarrow$ Stage 3: Third modal update), each modality is assigned one of five exact status labels:

* **`UP_TO_DATE`**: Contains the correct fact for the requested time.
* **`STALE`**: Presents a previously valid fact as if it were still current.
* **`EMPTY`**: Does not contain the relevant fact.
* **`INCORRECT`**: Contains a value that is invalid for any time (e.g., premature edits or vandalism reverted shortly after).
* **`UNCERTAIN`**: Available evidence cannot justify a reliable diagnosis.

### Example — 4-Stage Modal Evolution (Wimbledon 2026 Men's Singles: Jannik Sinner)

| Stage | Timestamp (UTC) | Text | Table | KG |
| :--- | :---: | :---: | :---: | :---: |
| **0 — Before first update** | Before 18:56 | `EMPTY` | `EMPTY` | `EMPTY` |
| **1 — First modal update** | 18:57 | `EMPTY` | `UP_TO_DATE` | `EMPTY` |
| **2 — Second modal update** | 19:01 | `UP_TO_DATE` | `UP_TO_DATE` | `EMPTY` |
| **3 — Third modal update** | 19:13 | `UP_TO_DATE` | `UP_TO_DATE` | `UP_TO_DATE` |

---

## Installation & Usage

### Prerequisites
* Python 3.8+
* `requests`

### Setup
```bash
git clone https://github.com/ArchibaldBonnet/Facts-Out-Of-Sync
cd Facts-Out-Of-Sync
pip install -r requirements.txt
```

### Run the Audit & Statistics Script
```bash
python src/Automatic.py
```

---

## Next Steps (Roadmap)

- [ ] **Event Status Labeling & 4-Stage Reproduction:** Assign `UP_TO_DATE`, `STALE`, `EMPTY`, `INCORRECT`, and `UNCERTAIN` across all annotated examples (with $\ge 3$ examples per status label) and categorize events by year.
- [ ] **Event Triples & Information Placement Patterns:** Formalize triple templates (e.g., `(player_name, win, tournament_name)`) and structural placement patterns across tennis competitions (ATP, Australian Open, Roland Garros, Wimbledon, US Open).
- [ ] **100 Tennis News Dataset:** Build a benchmark of 100 official tennis news releases mapping `news_title` $\rightarrow$ `(triples, timestamp)`.
- [ ] **Automated Target Fact Verification:** Upgrade the reproduction pipeline (leveraging `wd-provenance` and pattern matching/LLM filtering) to automatically verify target values and classify the 4-stage event statuses.