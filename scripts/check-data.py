#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"
MANIFEST_PATH = DATA_DIR / "countrySources.json"
SUSPICIOUS_CITY_TOKENS = (
    "municipality",
    "district",
    "borough",
    "county",
    "province",
    "region",
)


def normalize_label(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_only = normalized.encode("ascii", "ignore").decode("ascii")
    return " ".join(ascii_only.replace("&", "and").replace("-", " ").split()).strip().lower()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def find_duplicates(values: list[str]) -> list[str]:
    counts = Counter(normalize_label(value) for value in values if value)
    return sorted(label for label, count in counts.items() if count > 1)


def find_suspicious_labels(values: list[str]) -> list[str]:
    suspicious: list[str] = []
    for value in values:
        normalized = normalize_label(value)
        if any(token in normalized for token in SUSPICIOUS_CITY_TOKENS):
            suspicious.append(value)
    return suspicious


def validate_country(country_code: str, manifest_entry: dict[str, Any]) -> tuple[list[str], list[str], str]:
    errors: list[str] = []
    warnings: list[str] = []

    output_file = manifest_entry.get("output_file")
    if not isinstance(output_file, str) or not output_file.startswith("data/"):
        return [f"{country_code}: invalid output_file {output_file!r}"], warnings, country_code

    json_path = REPO_ROOT / output_file
    if not json_path.exists():
        return [f"{country_code}: missing output file {json_path}"], warnings, country_code

    try:
        data = load_json(json_path)
    except Exception as error:
        return [f"{country_code}: failed to parse {json_path.name}: {error}"], warnings, country_code

    if not isinstance(data, dict):
        return [f"{country_code}: {json_path.name} does not contain a JSON object"], warnings, country_code

    country_name = manifest_entry.get("country", country_code)
    root_entry = data.get(country_code)
    if not isinstance(root_entry, dict):
        errors.append(f"{country_code}: missing root entry {country_code} in {json_path.name}")
        root_cities: list[str] = []
    else:
        root_region = root_entry.get("region")
        if root_region != country_name:
            errors.append(
                f"{country_code}: root region mismatch in {json_path.name} (expected {country_name!r}, got {root_region!r})"
            )
        root_cities = root_entry.get("cities", [])
        if not isinstance(root_cities, list) or not root_cities:
            errors.append(f"{country_code}: root city list is empty or invalid in {json_path.name}")
            root_cities = []
        duplicate_root_cities = find_duplicates(root_cities)
        if duplicate_root_cities:
            errors.append(f"{country_code}: duplicate root cities {duplicate_root_cities}")
        suspicious_root_cities = find_suspicious_labels(root_cities)
        if suspicious_root_cities:
            warnings.append(f"{country_code}: suspicious root city labels {suspicious_root_cities}")

    expected_root_count = manifest_entry.get("country_root_city_count")
    if isinstance(expected_root_count, int) and expected_root_count != len(root_cities):
        errors.append(
            f"{country_code}: country_root_city_count mismatch (manifest {expected_root_count}, actual {len(root_cities)})"
        )

    manifest_regions = manifest_entry.get("regions")
    if not isinstance(manifest_regions, list) or not manifest_regions:
        errors.append(f"{country_code}: manifest entry has no regions")
        manifest_regions = []

    manifest_labels: list[str] = []
    for region in manifest_regions:
        if not isinstance(region, dict):
            errors.append(f"{country_code}: invalid region metadata entry {region!r}")
            continue
        label = region.get("label")
        if not isinstance(label, str) or not label:
            errors.append(f"{country_code}: invalid region label in manifest entry {region!r}")
            continue
        manifest_labels.append(label)

    data_labels = [label for label in data.keys() if label != country_code]
    missing_regions = sorted(label for label in manifest_labels if label not in data)
    extra_regions = sorted(label for label in data_labels if label not in set(manifest_labels))
    if missing_regions:
        errors.append(f"{country_code}: manifest regions missing from data file: {missing_regions}")
    if extra_regions:
        errors.append(f"{country_code}: data file has regions absent from manifest: {extra_regions}")

    for region in manifest_regions:
        if not isinstance(region, dict):
            continue
        label = region.get("label")
        if not isinstance(label, str) or label not in data:
            continue

        region_entry = data.get(label)
        if not isinstance(region_entry, dict):
            errors.append(f"{country_code}: region {label!r} is not an object in {json_path.name}")
            continue

        region_name = region_entry.get("region")
        if region_name != label:
            errors.append(
                f"{country_code}: region name mismatch for {label!r} (expected {label!r}, got {region_name!r})"
            )

        cities = region_entry.get("cities")
        if not isinstance(cities, list) or not cities:
            errors.append(f"{country_code}: region {label!r} has an empty or invalid city list")
            continue

        city_count = region.get("city_count")
        if not isinstance(city_count, int):
            errors.append(f"{country_code}: region {label!r} has invalid city_count metadata {city_count!r}")
        elif city_count != len(cities):
            errors.append(
                f"{country_code}: region {label!r} city_count mismatch (manifest {city_count}, actual {len(cities)})"
            )

        duplicate_cities = find_duplicates(cities)
        if duplicate_cities:
            errors.append(f"{country_code}: region {label!r} has duplicate cities {duplicate_cities}")

        suspicious_cities = find_suspicious_labels(cities)
        if suspicious_cities:
            warnings.append(f"{country_code}: region {label!r} has suspicious city labels {suspicious_cities}")

        if region.get("status") == "fallback_existing_seed":
            warnings.append(f"{country_code}: region {label!r} is still using fallback_existing_seed")

    summary = (
        f"{country_code}: {len(manifest_labels)} region(s), "
        f"{sum(len(data.get(label, {}).get('cities', [])) for label in manifest_labels if label in data)} region city entries, "
        f"{len(root_cities)} root city entries"
    )
    return errors, warnings, summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate source-backed country data files and manifest consistency.")
    parser.add_argument("countries", nargs="*", help="Optional country codes to validate. Defaults to all manifest entries.")
    return parser.parse_args()


def main() -> None:
    if not MANIFEST_PATH.exists():
        raise SystemExit(f"Missing manifest: {MANIFEST_PATH}")

    try:
        manifest = load_json(MANIFEST_PATH)
    except Exception as error:
        raise SystemExit(f"Failed to parse manifest {MANIFEST_PATH}: {error}") from error

    countries = manifest.get("countries")
    if not isinstance(countries, dict) or not countries:
        raise SystemExit(f"Manifest has no countries: {MANIFEST_PATH}")

    args = parse_args()
    requested = [country.upper() for country in args.countries] if args.countries else sorted(countries)
    unknown = [country for country in requested if country not in countries]
    if unknown:
        raise SystemExit(f"Unknown manifest countries: {', '.join(unknown)}")

    all_errors: list[str] = []
    all_warnings: list[str] = []

    for country_code in requested:
        entry = countries[country_code]
        if not isinstance(entry, dict):
            all_errors.append(f"{country_code}: manifest entry is not an object")
            continue

        errors, warnings, summary = validate_country(country_code, entry)
        if errors:
            print(f"[error] {summary}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"[ok] {summary}")

        for warning in warnings:
            print(f"[warn] {warning}")

        all_errors.extend(errors)
        all_warnings.extend(warnings)

    print(
        f"[summary] validated {len(requested)} country file(s), "
        f"{len(all_warnings)} warning(s), {len(all_errors)} error(s)"
    )

    if all_errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
