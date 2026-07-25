# Humanitarian Labour Market Analysis (HLMA)

## Project Overview

**HLMA** stands for **Humanitarian Labour Market Analysis**.

**Key Research Question:** What can humanitarian recruitment data tell us about the humanitarian labour market?

### Supporting Business Questions

**1. Workforce Demand**
- Which humanitarian organizations are hiring the most?
- Which countries or regions have the highest demand for humanitarian professionals?
- Which organizations recruit locally, regionally, or globally?

**2. Skills and Occupations**
- What job roles are most frequently advertised?
- Which professional fields/skills (e.g., Health, HR, Finance, Logistics, Monitoring & Evaluation) are in greatest demand?
- Are organizations hiring more technical, operational, or leadership roles?

**3. Recruitment Trends**
- How does hiring vary over time?
- Is remote work becoming more common?
- Which organizations appear to recruit continuously?

**4. Labour Market Intelligence**
- What labour market insights can be derived from humanitarian recruitment data?
- How can these insights support job seekers, humanitarian organizations, and researchers?

This project began as **"Humanitarian Labour Market Observatory (HLMO)"** and was deliberately reframed as **"Analysis (HLMA)"** — an honest scope for a first-time, pilot-stage project, with the "Observatory" vision (an ongoing, re-runnable system) noted as a natural future direction, not a current claim.

---

## 1. Data Source Discovery & Vetting

Before collecting any data, each candidate source was checked for:
- **robots.txt** — technical crawling permissions
- **Terms of Use** — legal permissions (watching for "resell," "compile," "derivative works," "scrape," "bot")
- **Official API availability** — always preferred over scraping when one exists

| Source | Outcome |
|---|---|
| ReliefWeb | API requires appname pre-approval (pending); direct scraping blocked by AWS WAF bot protection — paused |
| Impactpool | Terms explicitly forbid scraping — dropped |
| DevNetJobs | robots.txt allows crawling; Terms permit metadata (not full-text reproduction) — cleared |
| Amref, GiveDirectly, HRW, MSF USA, USA for UNHCR | Official ATS APIs (SmartRecruiters, Greenhouse) — cleared |

**Key distinction learned:** ATS (per-org hiring software) vs. job board (shared platform orgs post to directly) vs. job aggregator (auto-pulls listings from other platforms).

---

## 2. Data Collection

| Source | Method | Platform | Jobs Collected |
|---|---|---|---|
| Amref Health Africa | API | SmartRecruiters | 8 |
| GiveDirectly | API | Greenhouse | 21 |
| Human Rights Watch | API | Greenhouse | 10 |
| MSF USA | API | Greenhouse | 21 |
| DevNetJobs | Scraping (BeautifulSoup) | Standalone job board | ~628 |
| USA for UNHCR | API (inactive) | Greenhouse | 0 (toggled off — no current postings) |

**Total raw dataset:** 689 job postings.

---

## 3. Pipeline Architecture

- **`sources.csv`** — a source registry tracking each source's name, platform, identifier, active status, and collection method (`api` / `scrape`)
- **`pull_all_jobs.py`** — a unified script that reads the registry, routes each active source through the correct logic, and combines results into one dataset
- Designed for extensibility: new API sources need only a new registry row; new scraped sources need one new function

---

## 4. Data Cleaning

### Location Standardization
Raw `location` values (309 distinct formats across 5 sources) were parsed into two clean columns:
- **`country`** — 100 standardized country names, built via prefix-stripping, comma-splitting, city→country lookups, US state-code mapping, and country-alias resolution
- **`work_arrangement`** — Remote / Onsite / Regional-Global / Not specified

### Data Quality Sweep
Removed:
- 145 paywalled placeholder rows (`"(Value Members only)"` from DevNetJobs)
- 8 completely blank rows
- Exact duplicate rows (already captured within the above two removals)

Investigated 26 same-organization+title pairs — confirmed legitimate (same role posted for different locations), left untouched.

**Result: 536 clean rows.**

---

## 5. Data Standardization (Round 2)

- **Dates:** `date_posted` and `deadline` converted from raw text to proper `datetime` types (`pd.to_datetime()`), with the `"Apply by: "` prefix stripped from `deadline` first. Confirmed structural pattern: API sources populate `date_posted` only; DevNetJobs populates `deadline` only — not a data error, a source limitation.
- **Organization names:** Checked via **fuzzy string matching** (`difflib.SequenceMatcher`, threshold 0.85) to catch near-duplicate spellings missed by eye. Each flagged pair was individually researched (not auto-merged) before deciding:
  - **Merged** (confirmed same entity, formatting-only differences): CARE/Care, GOAL/Goal, SEARCA/Searca, Better Cotton Initiative, Asian Development Bank, United Nations University
  - **Kept distinct** (confirmed separate legal entities via research): MSF country sections (Belgium/CH/USA), Concern Worldwide (UK) vs. Concern Worldwide, Social Finance vs. Social Finance UK — each is part of a federated/affiliate network with its own legal registration, not a spelling variant

**Current dataset: `data/master_dataset_v3.csv`** — 536 rows, 8 columns (`organization`, `title`, `location`, `date_posted`, `deadline`, `source_url`, `country`, `work_arrangement`).

---

## 6. Key Concepts & Skills Practiced

- API vs. web scraping: when each applies, legal/technical tradeoffs
- ATS vs. job board vs. job aggregator (distinct architectures)
- Reading Terms of Use / robots.txt for automated-access signals
- Data wrangling stages: collection → integration → cleaning → standardization
- Fuzzy string matching for near-duplicate detection (vs. rule-based parsing for structural inconsistency)
- Scraping practice on a dedicated sandbox site (`books.toscrape.com`) and a permissive real API (RemoteOK) after correctly identifying that Indeed and LinkedIn are explicitly prohibited

---

## 7. Known Limitations

- `date_posted` / `deadline` are inherently source-dependent (structural, not a collection gap)
- Sample size (536 postings, 5 sources) represents a **pilot-stage dataset** — not a comprehensive picture of the humanitarian labour market
- "Not specified" values remain in both `country` (62 rows) and `work_arrangement` (40 rows) where source data was genuinely ambiguous

---

## 8. Next Steps

- Exploratory analysis: job title/skills text extraction, country distribution visualization, remote-work trend analysis
- Potential future expansion: additional NGO sources (API-first), evolution toward the "Observatory" vision (ongoing, re-runnable pipeline)