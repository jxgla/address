# Country Sources

This file records the source pipeline for the newly added country datasets.

- Primary source: [Wikidata Query Service](https://query.wikidata.org/)
- Source docs: [Wikidata Query Service User Manual](https://www.mediawiki.org/wiki/Wikidata_Query_Service/User_Manual/en)
- Sync script: `scripts/sync-sourced-country-data.py`
- Output manifest: `data/countrySources.json`

Notes:
- Region labels stay aligned with the current frontend UI.
- City labels are ASCII-normalized for consistency with the existing project data files.
- If a region cannot be resolved cleanly, the script keeps the previous seed list and marks that region as a fallback in the manifest.
- City-state regions can be reduced to their exact region label when Wikidata cleanly resolves the region but not a separate city list; these cases are marked as `sourced_wikidata_region_label` in the manifest.
- A small number of municipality-heavy regions or country roots can use curated place-label overrides while still keeping the Wikidata-backed region source; these cases are marked as `sourced_wikidata_curated_labels` in the manifest or country notes.

## AT Austria

- Output: `data/atData.json`
- Country item: [Q40](https://www.wikidata.org/wiki/Q40)
- Source: [Wikidata Query Service](https://query.wikidata.org/)
- Regions sourced: 9/9
- Country root cities: population-ranked countrywide places from Wikidata
- Generated: `2026-03-28T11:08:24.059440+00:00`
- Notes: Region labels stay aligned with the existing UI. Cities are population-ranked place entities sourced from Wikidata and ASCII-normalized for frontend consistency. Coverage: 8 region(s) sourced directly from Wikidata; 1 city-state region(s) reduced to the exact Wikidata region label.

## BE Belgium

- Output: `data/beData.json`
- Country item: [Q31](https://www.wikidata.org/wiki/Q31)
- Source: [Wikidata Query Service](https://query.wikidata.org/)
- Regions sourced: 10/10
- Country root cities: population-ranked countrywide places from Wikidata
- Generated: `2026-03-28T12:14:54.950782+00:00`
- Notes: Region labels stay aligned with the existing UI. Cities are population-ranked place entities sourced from Wikidata and ASCII-normalized for frontend consistency. Coverage: 10 region(s) sourced directly from Wikidata.

## CA Canada

- Output: `data/caData.json`
- Country item: [Q16](https://www.wikidata.org/wiki/Q16)
- Source: [Wikidata Query Service](https://query.wikidata.org/)
- Regions sourced: 13/13
- Country root cities: curated countrywide labels anchored to the sourced region dataset
- Generated: `2026-03-28T15:19:30.759464+00:00`
- Notes: Region labels stay aligned with the existing UI. Cities are population-ranked place entities sourced from Wikidata and ASCII-normalized for frontend consistency. Coverage: 0 region(s) sourced directly from Wikidata; 13 region(s) use curated city labels to avoid municipality-heavy Wikidata outputs; the country root list uses curated labels for stable nationwide coverage.

## CH Switzerland

- Output: `data/chData.json`
- Country item: [Q39](https://www.wikidata.org/wiki/Q39)
- Source: [Wikidata Query Service](https://query.wikidata.org/)
- Regions sourced: 9/9
- Country root cities: population-ranked countrywide places from Wikidata
- Generated: `2026-03-28T14:28:00.2458482+00:00`
- Notes: Region labels stay aligned with the existing UI. Cities are population-ranked place entities sourced from Wikidata and ASCII-normalized for frontend consistency. Coverage: 8 region(s) sourced directly from Wikidata; 1 region(s) use curated city labels to avoid municipality-heavy Wikidata outputs.

## DE Germany

- Output: `data/deData.json`
- Country item: [Q183](https://www.wikidata.org/wiki/Q183)
- Source: [Wikidata Query Service](https://query.wikidata.org/)
- Regions sourced: 16/16
- Country root cities: population-ranked countrywide places from Wikidata
- Generated: `2026-03-28T09:39:33.006293+00:00`
- Notes: Region labels stay aligned with the existing UI. Cities are population-ranked place entities sourced from Wikidata and ASCII-normalized for frontend consistency. Coverage: 16 region(s) sourced directly from Wikidata.

## ES Spain

- Output: `data/esData.json`
- Country item: [Q29](https://www.wikidata.org/wiki/Q29)
- Source: [Wikidata Query Service](https://query.wikidata.org/)
- Regions sourced: 10/10
- Country root cities: population-ranked countrywide places from Wikidata
- Generated: `2026-03-28T10:51:23.220442+00:00`
- Notes: Region labels stay aligned with the existing UI. Cities are population-ranked place entities sourced from Wikidata and ASCII-normalized for frontend consistency. Coverage: 10 region(s) sourced directly from Wikidata.

## FR France

- Output: `data/frData.json`
- Country item: [Q142](https://www.wikidata.org/wiki/Q142)
- Source: [Wikidata Query Service](https://query.wikidata.org/)
- Regions sourced: 10/10
- Country root cities: population-ranked countrywide places from Wikidata
- Generated: `2026-03-28T10:20:15.183034+00:00`
- Notes: Region labels stay aligned with the existing UI. Cities are population-ranked place entities sourced from Wikidata and ASCII-normalized for frontend consistency. Coverage: 10 region(s) sourced directly from Wikidata.

## GB United Kingdom

- Output: `data/gbData.json`
- Country item: [Q145](https://www.wikidata.org/wiki/Q145)
- Source: [Wikidata Query Service](https://query.wikidata.org/)
- Regions sourced: 4/4
- Country root cities: curated countrywide labels anchored to the sourced region dataset
- Generated: `2026-03-28T17:48:10.294202+00:00`
- Notes: Region labels stay aligned with the existing UI. Cities are population-ranked place entities sourced from Wikidata and ASCII-normalized for frontend consistency. Coverage: 0 region(s) sourced directly from Wikidata; 4 region(s) use curated city labels to avoid municipality-heavy Wikidata outputs; the country root list uses curated labels for stable nationwide coverage.

## HK Hong Kong

- Output: `data/hkData.json`
- Country item: [Q8646](https://www.wikidata.org/wiki/Q8646)
- Source: [Wikidata Query Service](https://query.wikidata.org/)
- Regions sourced: 14/14
- Country root cities: curated countrywide labels anchored to the sourced region dataset
- Generated: `2026-03-28T17:42:46.397557+00:00`
- Notes: Region labels stay aligned with the existing UI. Cities are population-ranked place entities sourced from Wikidata and ASCII-normalized for frontend consistency. Coverage: 0 region(s) sourced directly from Wikidata; 14 region(s) use curated city labels to avoid municipality-heavy Wikidata outputs; the country root list uses curated labels for stable nationwide coverage.

## IE Ireland

- Output: `data/ieData.json`
- Country item: [Q27](https://www.wikidata.org/wiki/Q27)
- Source: [Wikidata Query Service](https://query.wikidata.org/)
- Regions sourced: 9/9
- Country root cities: curated countrywide labels anchored to the sourced region dataset
- Generated: `2026-03-28T15:47:09.671760+00:00`
- Notes: Region labels stay aligned with the existing UI. Cities are population-ranked place entities sourced from Wikidata and ASCII-normalized for frontend consistency. Coverage: 8 region(s) sourced directly from Wikidata; 1 region(s) use curated city labels to avoid municipality-heavy Wikidata outputs; the country root list uses curated labels for stable nationwide coverage.

## IT Italy

- Output: `data/itData.json`
- Country item: [Q38](https://www.wikidata.org/wiki/Q38)
- Source: [Wikidata Query Service](https://query.wikidata.org/)
- Regions sourced: 10/10
- Country root cities: population-ranked countrywide places from Wikidata
- Generated: `2026-03-28T10:56:30.462763+00:00`
- Notes: Region labels stay aligned with the existing UI. Cities are population-ranked place entities sourced from Wikidata and ASCII-normalized for frontend consistency. Coverage: 10 region(s) sourced directly from Wikidata.

## JP Japan

- Output: `data/jpData.json`
- Country item: [Q17](https://www.wikidata.org/wiki/Q17)
- Source: [Wikidata Query Service](https://query.wikidata.org/)
- Regions sourced: 10/10
- Country root cities: curated countrywide labels anchored to the sourced region dataset
- Generated: `2026-03-28T17:42:45.493346+00:00`
- Notes: Region labels stay aligned with the existing UI. Cities are population-ranked place entities sourced from Wikidata and ASCII-normalized for frontend consistency. Coverage: 0 region(s) sourced directly from Wikidata; 10 region(s) use curated city labels to avoid municipality-heavy Wikidata outputs; the country root list uses curated labels for stable nationwide coverage.

## KR South Korea

- Output: `data/krData.json`
- Country item: [Q884](https://www.wikidata.org/wiki/Q884)
- Source: [Wikidata Query Service](https://query.wikidata.org/)
- Regions sourced: 14/14
- Country root cities: curated countrywide labels anchored to the sourced region dataset
- Generated: `2026-03-28T17:42:47.383816+00:00`
- Notes: Region labels stay aligned with the existing UI. Cities are population-ranked place entities sourced from Wikidata and ASCII-normalized for frontend consistency. Coverage: 0 region(s) sourced directly from Wikidata; 14 region(s) use curated city labels to avoid municipality-heavy Wikidata outputs; the country root list uses curated labels for stable nationwide coverage.

## NL Netherlands

- Output: `data/nlData.json`
- Country item: [Q55](https://www.wikidata.org/wiki/Q55)
- Source: [Wikidata Query Service](https://query.wikidata.org/)
- Regions sourced: 12/12
- Country root cities: population-ranked countrywide places from Wikidata
- Generated: `2026-03-27T15:22:08.760440+00:00`
- Notes: Region labels stay aligned with the existing UI. Cities are population-ranked place entities sourced from Wikidata and ASCII-normalized for frontend consistency. Coverage: 12 region(s) sourced directly from Wikidata.

## NO Norway

- Output: `data/noData.json`
- Country item: [Q20](https://www.wikidata.org/wiki/Q20)
- Source: [Wikidata Query Service](https://query.wikidata.org/)
- Regions sourced: 9/9
- Country root cities: population-ranked countrywide places from Wikidata
- Generated: `2026-03-28T14:28:00.2458482+00:00`
- Notes: Region labels stay aligned with the existing UI. Cities are population-ranked place entities sourced from Wikidata and ASCII-normalized for frontend consistency. Coverage: 1 region(s) sourced directly from Wikidata; 8 region(s) use curated city labels to avoid municipality-heavy Wikidata outputs.

## PT Portugal

- Output: `data/ptData.json`
- Country item: [Q45](https://www.wikidata.org/wiki/Q45)
- Source: [Wikidata Query Service](https://query.wikidata.org/)
- Regions sourced: 9/9
- Country root cities: population-ranked countrywide places from Wikidata
- Generated: `2026-03-28T12:47:35.538573+00:00`
- Notes: Region labels stay aligned with the existing UI. Cities are population-ranked place entities sourced from Wikidata and ASCII-normalized for frontend consistency. Coverage: 9 region(s) sourced directly from Wikidata.

## SE Sweden

- Output: `data/seData.json`
- Country item: [Q34](https://www.wikidata.org/wiki/Q34)
- Source: [Wikidata Query Service](https://query.wikidata.org/)
- Regions sourced: 8/8
- Country root cities: population-ranked countrywide places from Wikidata
- Generated: `2026-03-28T14:28:00.2458482+00:00`
- Notes: Region labels stay aligned with the existing UI. Cities are population-ranked place entities sourced from Wikidata and ASCII-normalized for frontend consistency. Coverage: 4 region(s) sourced directly from Wikidata; 4 region(s) use curated city labels to avoid municipality-heavy Wikidata outputs.

## SG Singapore

- Output: `data/sgData.json`
- Country item: [Q334](https://www.wikidata.org/wiki/Q334)
- Source: [Wikidata Query Service](https://query.wikidata.org/)
- Regions sourced: 5/5
- Country root cities: curated countrywide labels anchored to the sourced region dataset
- Generated: `2026-03-28T15:20:10.902538+00:00`
- Notes: Region labels stay aligned with the existing UI. Cities are population-ranked place entities sourced from Wikidata and ASCII-normalized for frontend consistency. Coverage: 0 region(s) sourced directly from Wikidata; 5 region(s) use curated city labels to avoid municipality-heavy Wikidata outputs; the country root list uses curated labels for stable nationwide coverage.

## US United States

- Output: `data/usData.json`
- Country item: [Q30](https://www.wikidata.org/wiki/Q30)
- Source: [Wikidata Query Service](https://query.wikidata.org/)
- Regions sourced: 50/50
- Country root cities: curated countrywide labels anchored to the sourced region dataset
- Generated: `2026-03-28T17:42:45.699488+00:00`
- Notes: Region labels stay aligned with the existing UI. Cities are population-ranked place entities sourced from Wikidata and ASCII-normalized for frontend consistency. Coverage: 0 region(s) sourced directly from Wikidata; 50 region(s) use curated city labels to avoid municipality-heavy Wikidata outputs; the country root list uses curated labels for stable nationwide coverage.

