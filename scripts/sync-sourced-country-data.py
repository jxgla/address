#!/usr/bin/env python3
"""
Sync selected country datasets from public Wikidata sources.

This script keeps the existing JSON file shape used by the frontend, but
replaces hand-curated city lists with source-backed region and city data from
Wikidata Query Service. Region names stay aligned with the current UI labels.
"""

from __future__ import annotations

import argparse
import json
import re
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from requests import HTTPError

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"
DOCS_DIR = REPO_ROOT / "docs"

WDQS_ENDPOINT = "https://query.wikidata.org/sparql"
WDQS_DOCS_URL = "https://www.mediawiki.org/wiki/Wikidata_Query_Service/User_Manual/en"
WDQS_HOME_URL = "https://query.wikidata.org/"
USER_AGENT = "AddressDataSync/1.0 (https://github.com/jxgla/address-system)"
ASCII_REPLACEMENTS = str.maketrans(
    {
        "ß": "ss",
        "Æ": "AE",
        "æ": "ae",
        "Ø": "O",
        "ø": "o",
        "Å": "A",
        "å": "a",
        "Œ": "OE",
        "œ": "oe",
    }
)

# Override any mojibake introduced by legacy file encodings.
ASCII_REPLACEMENTS = str.maketrans(
    {
        "\u00df": "ss",
        "\u00c6": "AE",
        "\u00e6": "ae",
        "\u00d8": "O",
        "\u00f8": "o",
        "\u00c5": "A",
        "\u00e5": "a",
        "\u0152": "OE",
        "\u0153": "oe",
    }
)

STRICT_PLACE_TYPES = (
    "city",
    "town",
    "municipality",
    "commune",
    "borough",
    "village",
    "capital",
    "census town",
)
RELAXED_PLACE_TYPES = STRICT_PLACE_TYPES + ("human settlement",)
BLOCKED_PLACE_TYPES = (
    "administrative territorial entity",
    "province",
    "county",
    "region",
    "state",
    "district",
    "city district",
    "diocese",
    "metropolitan area",
    "archipelago",
    "country",
    "sovereign state",
    "department",
    "community of belgium",
    "option municipality",
    "municipality seat",
    "special municipality association",
    "former municipality",
    "chef-lieu",
    "ortsteil",
    "quarter",
    "urban quarter",
    "neighborhood",
    "suburb",
    "local government",
    "administrative division",
    "metropolitan city",
)
COUNTRY_ROOT_BLOCKED_TYPE_TERMS = (
    "district",
    "borough",
    "quarter",
    "neighborhood",
    "suburb",
    "municipal district",
    "administrative district",
    "arrondissement",
    "bezirk",
)
COUNTRY_ROOT_ALLOWED_TYPE_TERMS = (
    "city",
    "town",
    "capital",
    "metropolis",
    "municipality",
    "major regional center",
    "urban municipality",
    "commune",
)
ADMIN_REGION_NAME_TOKENS = (
    "region",
    "province",
    "county",
    "state",
    "district",
    "department",
    "community",
    "capital region",
)
BLOCKED_PLACE_LABEL_PREFIXES = (
    "district ",
    "metropolitan city of ",
    "municipality ",
    "municipio ",
    "consorzio ",
)
CANONICAL_PLACE_LABEL_PREFIXES = (
    "city of ",
)
CANONICAL_PLACE_LABEL_SUFFIXES = (
    " city",
    " municipality",
)
REGION_CITY_PREFIXES = (
    "province of ",
    "county of ",
    "canton of ",
    "community of ",
)
REGION_CITY_SUFFIXES = (
    " district",
    " county",
    " province",
    " canton",
    " capital region",
)

COUNTRY_CONFIG: dict[str, dict[str, Any]] = {
    "US": {
        "label": "United States",
        "qid": "Q30",
        "file": "usData.json",
        "existing_region_field": "state",
        "existing_seed_limit": 5,
        "seed_cities_as_manual_overrides": True,
        "skip_region_place_queries": True,
        "skip_country_place_queries": True,
        "manual_country_root_labels": [
            "New York City",
            "Los Angeles",
            "Chicago",
            "Houston",
            "Phoenix",
            "Philadelphia",
            "San Antonio",
            "San Diego",
        ],
    },
    "GB": {
        "label": "United Kingdom",
        "qid": "Q145",
        "file": "gbData.json",
        "ignore_existing_file": True,
        "balance_country_root_by_region": True,
        "skip_region_place_queries": True,
        "skip_country_place_queries": True,
        "region_qids": {
            "England": "Q21",
            "Scotland": "Q22",
            "Wales": "Q25",
            "Northern Ireland": "Q26",
        },
        "seed_root_cities": [
            "London",
            "Manchester",
            "Birmingham",
            "Leeds",
            "Glasgow",
            "Edinburgh",
            "Cardiff",
            "Belfast",
        ],
        "manual_country_root_labels": [
            "London",
            "Manchester",
            "Birmingham",
            "Leeds",
            "Glasgow",
            "Edinburgh",
            "Cardiff",
            "Belfast",
        ],
        "seed_data": {
            "England": ["London", "Birmingham", "Manchester", "Leeds", "Liverpool"],
            "Scotland": ["Glasgow", "Edinburgh", "Aberdeen", "Dundee", "Inverness"],
            "Wales": ["Cardiff", "Swansea", "Newport", "Wrexham", "Bangor"],
            "Northern Ireland": ["Belfast", "Derry", "Lisburn", "Newtownabbey", "Bangor"],
        },
        "manual_city_overrides": {
            "England": ["London", "Birmingham", "Manchester", "Leeds", "Liverpool"],
            "Scotland": ["Glasgow", "Edinburgh", "Aberdeen", "Dundee", "Inverness"],
            "Wales": ["Cardiff", "Swansea", "Newport", "Wrexham", "Bangor"],
            "Northern Ireland": ["Belfast", "Derry", "Lisburn", "Newtownabbey", "Bangor"],
        },
    },
    "JP": {
        "label": "Japan",
        "qid": "Q17",
        "file": "jpData.json",
        "ignore_existing_file": True,
        "balance_country_root_by_region": True,
        "skip_region_place_queries": True,
        "skip_country_place_queries": True,
        "region_qids": {
            "Tokyo": "Q1490",
            "Osaka Prefecture": "Q122723",
            "Kanagawa Prefecture": "Q127513",
            "Aichi Prefecture": "Q80434",
            "Saitama Prefecture": "Q128186",
            "Chiba Prefecture": "Q80011",
            "Hokkaido": "Q1037393",
            "Fukuoka Prefecture": "Q123258",
            "Kyoto Prefecture": "Q120730",
            "Hyogo Prefecture": "Q130290",
        },
        "seed_root_cities": [
            "Tokyo",
            "Yokohama",
            "Osaka",
            "Nagoya",
            "Sapporo",
            "Fukuoka",
            "Kyoto",
            "Kobe",
        ],
        "manual_country_root_labels": [
            "Tokyo",
            "Yokohama",
            "Osaka",
            "Nagoya",
            "Sapporo",
            "Fukuoka",
            "Kyoto",
            "Kobe",
        ],
        "seed_data": {
            "Tokyo": ["Tokyo", "Hachioji", "Machida", "Fuchu", "Chofu"],
            "Osaka Prefecture": ["Osaka", "Sakai", "Higashiosaka", "Toyonaka", "Takatsuki"],
            "Kanagawa Prefecture": ["Yokohama", "Kawasaki", "Sagamihara", "Fujisawa", "Yokosuka"],
            "Aichi Prefecture": ["Nagoya", "Toyota", "Okazaki", "Ichinomiya", "Toyohashi"],
            "Saitama Prefecture": ["Saitama", "Kawaguchi", "Kawagoe", "Tokorozawa", "Koshigaya"],
            "Chiba Prefecture": ["Chiba", "Funabashi", "Matsudo", "Kashiwa", "Ichikawa"],
            "Hokkaido": ["Sapporo", "Asahikawa", "Hakodate", "Kushiro", "Otaru"],
            "Fukuoka Prefecture": ["Fukuoka", "Kitakyushu", "Kurume", "Omuta", "Iizuka"],
            "Kyoto Prefecture": ["Kyoto", "Uji", "Kameoka", "Maizuru", "Fukuchiyama"],
            "Hyogo Prefecture": ["Kobe", "Himeji", "Nishinomiya", "Amagasaki", "Akashi"],
        },
        "manual_city_overrides": {
            "Tokyo": ["Tokyo", "Hachioji", "Machida", "Fuchu", "Chofu"],
            "Osaka Prefecture": ["Osaka", "Sakai", "Higashiosaka", "Toyonaka", "Takatsuki"],
            "Kanagawa Prefecture": ["Yokohama", "Kawasaki", "Sagamihara", "Fujisawa", "Yokosuka"],
            "Aichi Prefecture": ["Nagoya", "Toyota", "Okazaki", "Ichinomiya", "Toyohashi"],
            "Saitama Prefecture": ["Saitama", "Kawaguchi", "Kawagoe", "Tokorozawa", "Koshigaya"],
            "Chiba Prefecture": ["Chiba", "Funabashi", "Matsudo", "Kashiwa", "Ichikawa"],
            "Hokkaido": ["Sapporo", "Asahikawa", "Hakodate", "Kushiro", "Otaru"],
            "Fukuoka Prefecture": ["Fukuoka", "Kitakyushu", "Kurume", "Omuta", "Iizuka"],
            "Kyoto Prefecture": ["Kyoto", "Uji", "Kameoka", "Maizuru", "Fukuchiyama"],
            "Hyogo Prefecture": ["Kobe", "Himeji", "Nishinomiya", "Amagasaki", "Akashi"],
        },
    },
    "HK": {
        "label": "Hong Kong",
        "qid": "Q8646",
        "file": "hkData.json",
        "ignore_existing_file": True,
        "balance_country_root_by_region": True,
        "skip_region_place_queries": True,
        "skip_country_place_queries": True,
        "region_qids": {
            "Central and Western District": "Q312485",
            "Wan Chai District": "Q986434",
            "Eastern District": "Q727054",
            "Southern District": "Q986431",
            "Yau Tsim Mong District": "Q157669",
            "Sham Shui Po District": "Q655626",
            "Kowloon City District": "Q986415",
            "Wong Tai Sin District": "Q878503",
            "Kwun Tong District": "Q875773",
            "Kwai Tsing District": "Q877132",
            "Sha Tin District": "Q15019",
            "Sai Kung District": "Q155697",
            "Tuen Mun District": "Q986383",
            "Yuen Long District": "Q871442",
        },
        "seed_root_cities": [
            "Central",
            "Wan Chai",
            "Quarry Bay",
            "Aberdeen",
            "Mong Kok",
            "Sha Tin",
            "Kwai Chung",
            "Tseung Kwan O",
        ],
        "manual_country_root_labels": [
            "Central",
            "Wan Chai",
            "Quarry Bay",
            "Aberdeen",
            "Mong Kok",
            "Sha Tin",
            "Kwai Chung",
            "Tseung Kwan O",
        ],
        "seed_data": {
            "Central and Western District": ["Central", "Admiralty", "Sheung Wan", "Sai Ying Pun", "Kennedy Town"],
            "Wan Chai District": ["Wan Chai", "Causeway Bay", "Happy Valley", "Tin Hau", "Tai Hang"],
            "Eastern District": ["Quarry Bay", "Tai Koo", "North Point", "Shau Kei Wan", "Chai Wan"],
            "Southern District": ["Aberdeen", "Ap Lei Chau", "Stanley", "Repulse Bay", "Wong Chuk Hang"],
            "Yau Tsim Mong District": ["Mong Kok", "Tsim Sha Tsui", "Yau Ma Tei", "Jordan", "West Kowloon"],
            "Sham Shui Po District": ["Sham Shui Po", "Cheung Sha Wan", "Lai Chi Kok", "Mei Foo", "Nam Cheong"],
            "Kowloon City District": ["Hung Hom", "To Kwa Wan", "Ho Man Tin", "Kowloon City", "Kai Tak"],
            "Wong Tai Sin District": ["Wong Tai Sin", "Diamond Hill", "San Po Kong", "Chuk Yuen", "Lok Fu"],
            "Kwun Tong District": ["Kwun Tong", "Lam Tin", "Yau Tong", "Ngau Tau Kok", "Sau Mau Ping"],
            "Kwai Tsing District": ["Kwai Chung", "Tsing Yi", "Lai King", "Kwai Fong", "Kwai Hing"],
            "Sha Tin District": ["Sha Tin", "Tai Wai", "Fo Tan", "Ma On Shan", "Wu Kai Sha"],
            "Sai Kung District": ["Sai Kung", "Tseung Kwan O", "Hang Hau", "Po Lam", "Clear Water Bay"],
            "Tuen Mun District": ["Tuen Mun", "Siu Hong", "Sam Shing", "Butterfly Beach", "Gold Coast"],
            "Yuen Long District": ["Yuen Long", "Tin Shui Wai", "Kam Tin", "Hung Shui Kiu", "Lau Fau Shan"],
        },
        "manual_city_overrides": {
            "Central and Western District": ["Central", "Admiralty", "Sheung Wan", "Sai Ying Pun", "Kennedy Town"],
            "Wan Chai District": ["Wan Chai", "Causeway Bay", "Happy Valley", "Tin Hau", "Tai Hang"],
            "Eastern District": ["Quarry Bay", "Tai Koo", "North Point", "Shau Kei Wan", "Chai Wan"],
            "Southern District": ["Aberdeen", "Ap Lei Chau", "Stanley", "Repulse Bay", "Wong Chuk Hang"],
            "Yau Tsim Mong District": ["Mong Kok", "Tsim Sha Tsui", "Yau Ma Tei", "Jordan", "West Kowloon"],
            "Sham Shui Po District": ["Sham Shui Po", "Cheung Sha Wan", "Lai Chi Kok", "Mei Foo", "Nam Cheong"],
            "Kowloon City District": ["Hung Hom", "To Kwa Wan", "Ho Man Tin", "Kowloon City", "Kai Tak"],
            "Wong Tai Sin District": ["Wong Tai Sin", "Diamond Hill", "San Po Kong", "Chuk Yuen", "Lok Fu"],
            "Kwun Tong District": ["Kwun Tong", "Lam Tin", "Yau Tong", "Ngau Tau Kok", "Sau Mau Ping"],
            "Kwai Tsing District": ["Kwai Chung", "Tsing Yi", "Lai King", "Kwai Fong", "Kwai Hing"],
            "Sha Tin District": ["Sha Tin", "Tai Wai", "Fo Tan", "Ma On Shan", "Wu Kai Sha"],
            "Sai Kung District": ["Sai Kung", "Tseung Kwan O", "Hang Hau", "Po Lam", "Clear Water Bay"],
            "Tuen Mun District": ["Tuen Mun", "Siu Hong", "Sam Shing", "Butterfly Beach", "Gold Coast"],
            "Yuen Long District": ["Yuen Long", "Tin Shui Wai", "Kam Tin", "Hung Shui Kiu", "Lau Fau Shan"],
        },
    },
    "KR": {
        "label": "South Korea",
        "qid": "Q884",
        "file": "krData.json",
        "ignore_existing_file": True,
        "balance_country_root_by_region": True,
        "skip_region_place_queries": True,
        "skip_country_place_queries": True,
        "region_qids": {
            "Seoul": "Q8684",
            "Busan": "Q16520",
            "Incheon": "Q20934",
            "Daegu": "Q20927",
            "Daejeon": "Q20921",
            "Gwangju": "Q41283",
            "Ulsan": "Q41278",
            "Gyeonggi Province": "Q20937",
            "Gangwon Province": "Q41071",
            "North Chungcheong Province": "Q41066",
            "South Chungcheong Province": "Q41070",
            "North Gyeongsang Province": "Q41154",
            "South Gyeongsang Province": "Q41151",
            "Jeju Province": "Q41164",
        },
        "seed_root_cities": [
            "Seoul",
            "Busan",
            "Incheon",
            "Daegu",
            "Daejeon",
            "Gwangju",
            "Ulsan",
            "Suwon",
        ],
        "manual_country_root_labels": [
            "Seoul",
            "Busan",
            "Incheon",
            "Daegu",
            "Daejeon",
            "Gwangju",
            "Ulsan",
            "Suwon",
        ],
        "aliases": {
            "Gyeonggi Province": ["Gyeonggi Province", "Gyeonggi-do"],
            "Gangwon Province": ["Gangwon Province", "Gangwon State", "Gangwon-do"],
            "North Chungcheong Province": ["North Chungcheong Province", "Chungcheongbuk-do"],
            "South Chungcheong Province": ["South Chungcheong Province", "Chungcheongnam-do"],
            "North Gyeongsang Province": ["North Gyeongsang Province", "Gyeongsangbuk-do"],
            "South Gyeongsang Province": ["South Gyeongsang Province", "Gyeongsangnam-do"],
            "Jeju Province": ["Jeju Province", "Jeju Special Self-Governing Province", "Jeju-do"],
        },
        "seed_data": {
            "Seoul": ["Seoul"],
            "Busan": ["Busan"],
            "Incheon": ["Incheon"],
            "Daegu": ["Daegu"],
            "Daejeon": ["Daejeon"],
            "Gwangju": ["Gwangju"],
            "Ulsan": ["Ulsan"],
            "Gyeonggi Province": ["Suwon", "Seongnam", "Goyang", "Yongin", "Bucheon"],
            "Gangwon Province": ["Chuncheon", "Wonju", "Gangneung", "Sokcho", "Donghae"],
            "North Chungcheong Province": ["Cheongju", "Chungju", "Jecheon", "Eumseong", "Jincheon"],
            "South Chungcheong Province": ["Cheonan", "Asan", "Seosan", "Dangjin", "Boryeong"],
            "North Gyeongsang Province": ["Pohang", "Gumi", "Gyeongju", "Andong", "Gimcheon"],
            "South Gyeongsang Province": ["Changwon", "Jinju", "Gimhae", "Yangsan", "Geoje"],
            "Jeju Province": ["Jeju City", "Seogwipo"],
        },
        "manual_city_overrides": {
            "Seoul": ["Seoul"],
            "Busan": ["Busan"],
            "Incheon": ["Incheon"],
            "Daegu": ["Daegu"],
            "Daejeon": ["Daejeon"],
            "Gwangju": ["Gwangju"],
            "Ulsan": ["Ulsan"],
            "Gyeonggi Province": ["Suwon", "Seongnam", "Goyang", "Yongin", "Bucheon"],
            "Gangwon Province": ["Chuncheon", "Wonju", "Gangneung", "Sokcho", "Donghae"],
            "North Chungcheong Province": ["Cheongju", "Chungju", "Jecheon", "Eumseong", "Jincheon"],
            "South Chungcheong Province": ["Cheonan", "Asan", "Seosan", "Dangjin", "Boryeong"],
            "North Gyeongsang Province": ["Pohang", "Gumi", "Gyeongju", "Andong", "Gimcheon"],
            "South Gyeongsang Province": ["Changwon", "Jinju", "Gimhae", "Yangsan", "Geoje"],
            "Jeju Province": ["Jeju City", "Seogwipo"],
        },
        "exact_only_regions": {"Seoul", "Busan", "Incheon", "Daegu", "Daejeon", "Gwangju", "Ulsan"},
    },
    "DE": {
        "label": "Germany",
        "qid": "Q183",
        "file": "deData.json",
        "aliases": {},
        "exact_only_regions": {"Berlin", "Hamburg"},
    },
    "NL": {
        "label": "Netherlands",
        "qid": "Q55",
        "file": "nlData.json",
        "aliases": {},
        "exclude_regions": {"Bonaire", "Saba", "Sint Eustatius"},
    },
    "FR": {
        "label": "France",
        "qid": "Q142",
        "file": "frData.json",
        "aliases": {
            "Occitanie": ["Occitania"],
        },
    },
    "ES": {
        "label": "Spain",
        "qid": "Q29",
        "file": "esData.json",
        "aliases": {
            "Castile and Leon": ["Castile and Leon", "Castile and Leon"],
        },
    },
    "IT": {
        "label": "Italy",
        "qid": "Q38",
        "file": "itData.json",
        "aliases": {},
    },
    "BE": {
        "label": "Belgium",
        "qid": "Q31",
        "file": "beData.json",
        "balance_country_root_by_region": True,
        "region_qids": {
            "Brussels-Capital Region": "Q240",
            "Antwerp Province": "Q1116",
            "East Flanders": "Q1114",
            "West Flanders": "Q1113",
            "Flemish Brabant": "Q1118",
            "Limburg": "Q1095",
            "Hainaut": "Q1129",
            "Liege": "Q1127",
            "Namur": "Q1125",
            "Luxembourg": "Q1126",
        },
        "aliases": {
            "Brussels-Capital Region": ["Brussels"],
            "Antwerp Province": ["Province of Antwerp", "Antwerp"],
            "East Flanders": ["East Flanders"],
            "West Flanders": ["West Flanders"],
            "Flemish Brabant": ["Flemish Brabant"],
            "Limburg": ["Province of Limburg", "Limburg"],
            "Hainaut": ["Hainaut"],
            "Liege": ["Liege", "Li\u00e8ge"],
            "Namur": ["Namur"],
            "Luxembourg": ["Luxembourg Province", "Luxembourg"],
        },
    },
    "PT": {
        "label": "Portugal",
        "qid": "Q45",
        "file": "ptData.json",
        "balance_country_root_by_region": True,
        "aliases": {
            "Lisbon District": ["Lisbon"],
            "Porto District": ["Porto"],
            "Braga District": ["Braga"],
            "Setubal District": ["Setubal", "Set\u00fabal"],
            "Aveiro District": ["Aveiro"],
            "Coimbra District": ["Coimbra"],
            "Faro District": ["Faro"],
        },
    },
    "AT": {
        "label": "Austria",
        "qid": "Q40",
        "file": "atData.json",
        "aliases": {},
        "exact_only_regions": {"Vienna"},
    },
    "CH": {
        "label": "Switzerland",
        "qid": "Q39",
        "file": "chData.json",
        "region_qids": {
            "Zurich": "Q11943",
            "Geneva": "Q11917",
            "Bern": "Q11911",
            "Basel-Stadt": "Q12172",
            "Vaud": "Q12771",
            "Lucerne": "Q12121",
            "Aargau": "Q11972",
            "Ticino": "Q12724",
            "St. Gallen": "Q12746",
        },
        "aliases": {
            "St. Gallen": ["St. Gallen", "Canton of St. Gallen"],
        },
        "preferred_city_labels": {
            "St. Gallen": ["St. Gallen", "Rapperswil-Jona", "Wil", "Gossau"],
        },
        "manual_city_overrides": {
            "St. Gallen": ["St. Gallen", "Rapperswil-Jona", "Wil", "Gossau", "Uzwil"],
        },
    },
    "IE": {
        "label": "Ireland",
        "qid": "Q27",
        "file": "ieData.json",
        "manual_country_root_labels": [
            "Dublin",
            "Cork",
            "Galway",
            "Limerick",
            "Waterford",
            "Kilkenny",
            "Letterkenny",
            "Ballina",
        ],
        "aliases": {
            "Dublin": ["County Dublin"],
            "Cork": ["County Cork"],
            "Galway": ["County Galway"],
            "Limerick": ["County Limerick"],
            "Waterford": ["County Waterford"],
            "Kildare": ["County Kildare"],
            "Mayo": ["County Mayo"],
            "Donegal": ["County Donegal"],
            "Kilkenny": ["County Kilkenny"],
        },
        "manual_city_overrides": {
            "Galway": ["Oranmore", "Athenry", "Ballinasloe", "Loughrea", "Claregalway"],
        },
    },
    "SE": {
        "label": "Sweden",
        "qid": "Q34",
        "file": "seData.json",
        "balance_country_root_by_region": True,
        "aliases": {
            "Vastra Gotaland": ["Vastra Gotaland County"],
            "Skane": ["Skane County"],
            "Ostergotland": ["Ostergotland County"],
            "Vasterbotten": ["Vasterbotten County"],
            "Orebro County": ["Orebro County"],
            "Jonkoping County": ["Jonkoping County"],
        },
        "preferred_city_labels": {
            "Uppsala County": ["Uppsala", "Enkoping", "Balsta", "Knivsta", "Osthammar"],
            "Jonkoping County": ["Jonkoping", "Huskvarna", "Varnamo", "Nassjo", "Vetlanda"],
        },
        "manual_city_overrides": {
            "Stockholm County": ["Stockholm", "Solna", "Sodertalje", "Nacka", "Huddinge"],
            "Vastra Gotaland": ["Gothenburg", "Boras", "Trollhattan", "Skovde", "Uddevalla"],
            "Uppsala County": ["Uppsala", "Enkoping", "Balsta", "Tierp", "Osthammar"],
            "Jonkoping County": ["Jonkoping", "Huskvarna", "Nassjo", "Varnamo", "Vetlanda"],
        },
    },
    "NO": {
        "label": "Norway",
        "qid": "Q20",
        "file": "noData.json",
        "balance_country_root_by_region": True,
        "region_qids": {
            "Oslo": "Q585",
            "Vestland": "Q56407177",
            "Trondelag": "Q127676",
            "Rogaland": "Q50624",
            "Troms": "Q50631",
            "Agder": "Q2729021",
            "Akershus": "Q50615",
            "More og Romsdal": "Q50627",
            "Nordland": "Q50630",
        },
        "aliases": {
            "Trondelag": ["Trondelag"],
            "More og Romsdal": ["More og Romsdal"],
        },
        "preferred_city_labels": {
            "Vestland": ["Bergen", "Floro", "Voss", "Forde", "Odda"],
            "Rogaland": ["Stavanger", "Sandnes", "Haugesund", "Bryne", "Egersund"],
            "Troms": ["Tromso", "Harstad", "Finnsnes", "Bardufoss"],
            "Agder": ["Kristiansand", "Arendal", "Grimstad", "Mandal"],
            "Akershus": ["Lillestrom", "Sandvika", "Asker"],
            "Nordland": ["Bodo", "Mo i Rana", "Narvik"],
        },
        "manual_city_overrides": {
            "Vestland": ["Bergen", "Floro", "Voss", "Forde", "Odda"],
            "Trondelag": ["Trondheim", "Steinkjer", "Levanger", "Namsos", "Stjordal"],
            "Rogaland": ["Stavanger", "Sandnes", "Haugesund", "Bryne", "Egersund"],
            "Troms": ["Tromso", "Harstad", "Finnsnes", "Bardufoss"],
            "Agder": ["Kristiansand", "Arendal", "Grimstad", "Mandal", "Farsund"],
            "Akershus": ["Lillestrom", "Asker", "Ski", "Jessheim", "Drobak"],
            "More og Romsdal": ["Alesund", "Molde", "Kristiansund", "Ulsteinvik", "Volda"],
            "Nordland": ["Bodo", "Narvik", "Mo i Rana", "Svolvaer", "Sortland"],
        },
        "exact_only_regions": {"Oslo"},
    },
    "CA": {
        "label": "Canada",
        "qid": "Q16",
        "file": "caData.json",
        "ignore_existing_file": True,
        "balance_country_root_by_region": True,
        "seed_root_cities": [
            "Toronto",
            "Montreal",
            "Vancouver",
            "Calgary",
            "Edmonton",
            "Ottawa",
            "Winnipeg",
            "Quebec City",
        ],
        "manual_country_root_labels": [
            "Toronto",
            "Montreal",
            "Vancouver",
            "Calgary",
            "Edmonton",
            "Ottawa",
            "Winnipeg",
            "Quebec City",
        ],
        "manual_city_overrides": {
            "Ontario": ["Toronto", "Ottawa", "Hamilton", "London", "Kitchener"],
            "Quebec": ["Montreal", "Quebec City", "Laval", "Gatineau", "Longueuil"],
            "British Columbia": ["Vancouver", "Surrey", "Burnaby", "Richmond", "Kelowna"],
            "Alberta": ["Calgary", "Edmonton", "Red Deer", "Lethbridge", "Medicine Hat"],
            "Manitoba": ["Winnipeg", "Brandon", "Steinbach", "Thompson", "Portage la Prairie"],
            "Saskatchewan": ["Saskatoon", "Regina", "Prince Albert", "Moose Jaw", "Swift Current"],
            "Nova Scotia": ["Halifax", "Sydney", "Truro", "New Glasgow", "Kentville"],
            "New Brunswick": ["Moncton", "Saint John", "Fredericton", "Dieppe", "Miramichi"],
            "Newfoundland and Labrador": [
                "St. John's",
                "Mount Pearl",
                "Corner Brook",
                "Conception Bay South",
                "Gander",
            ],
            "Prince Edward Island": ["Charlottetown", "Summerside", "Stratford", "Cornwall", "Montague"],
            "Northwest Territories": ["Yellowknife", "Hay River", "Inuvik", "Fort Smith", "Behchoko"],
            "Nunavut": ["Iqaluit", "Rankin Inlet", "Arviat", "Cambridge Bay", "Baker Lake"],
            "Yukon": ["Whitehorse", "Dawson City", "Watson Lake", "Haines Junction", "Carmacks"],
        },
        "seed_data": {
            "Ontario": ["Toronto", "Ottawa", "Hamilton", "London", "Kitchener"],
            "Quebec": ["Montreal", "Quebec City", "Laval", "Gatineau", "Longueuil"],
            "British Columbia": ["Vancouver", "Surrey", "Burnaby", "Richmond", "Kelowna"],
            "Alberta": ["Calgary", "Edmonton", "Red Deer", "Lethbridge", "Medicine Hat"],
            "Manitoba": ["Winnipeg", "Brandon", "Steinbach", "Thompson", "Portage la Prairie"],
            "Saskatchewan": ["Saskatoon", "Regina", "Prince Albert", "Moose Jaw", "Swift Current"],
            "Nova Scotia": ["Halifax", "Sydney", "Truro", "New Glasgow", "Kentville"],
            "New Brunswick": ["Moncton", "Saint John", "Fredericton", "Dieppe", "Miramichi"],
            "Newfoundland and Labrador": [
                "St. John's",
                "Mount Pearl",
                "Corner Brook",
                "Conception Bay South",
                "Gander",
            ],
            "Prince Edward Island": ["Charlottetown", "Summerside", "Stratford", "Cornwall", "Montague"],
            "Northwest Territories": ["Yellowknife", "Hay River", "Inuvik", "Fort Smith", "Behchoko"],
            "Nunavut": ["Iqaluit", "Rankin Inlet", "Arviat", "Cambridge Bay", "Baker Lake"],
            "Yukon": ["Whitehorse", "Dawson City", "Watson Lake", "Haines Junction", "Carmacks"],
        },
    },
    "SG": {
        "label": "Singapore",
        "qid": "Q334",
        "file": "sgData.json",
        "ignore_existing_file": True,
        "balance_country_root_by_region": True,
        "region_qids": {
            "Central Singapore Community Development Council": "Q2544592",
            "North East Community Development Council": "Q3710534",
            "North West Community Development Council": "Q5784118",
            "South East Community Development Council": "Q1687545",
            "South West Community Development Council": "Q5784126",
        },
        "seed_root_cities": [
            "Singapore",
            "Bedok",
            "Jurong East",
            "Tampines",
            "Toa Payoh",
            "Woodlands",
            "Hougang",
            "Bukit Merah",
        ],
        "manual_country_root_labels": [
            "Singapore",
            "Bedok",
            "Jurong East",
            "Tampines",
            "Toa Payoh",
            "Woodlands",
            "Hougang",
            "Bukit Merah",
        ],
        "seed_data": {
            "Central Singapore Community Development Council": [
                "Bishan",
                "Bukit Merah",
                "Kallang",
                "Queenstown",
                "Toa Payoh",
            ],
            "North East Community Development Council": [
                "Hougang",
                "Punggol",
                "Sengkang",
                "Serangoon",
                "Ang Mo Kio",
            ],
            "North West Community Development Council": [
                "Woodlands",
                "Yishun",
                "Sembawang",
                "Bukit Panjang",
                "Choa Chu Kang",
            ],
            "South East Community Development Council": [
                "Bedok",
                "Tampines",
                "Pasir Ris",
                "Marine Parade",
                "Geylang",
            ],
            "South West Community Development Council": [
                "Jurong East",
                "Jurong West",
                "Bukit Batok",
                "Clementi",
                "Pioneer",
            ],
        },
        "manual_city_overrides": {
            "Central Singapore Community Development Council": [
                "Bishan",
                "Bukit Merah",
                "Kallang",
                "Queenstown",
                "Toa Payoh",
            ],
            "North East Community Development Council": [
                "Hougang",
                "Punggol",
                "Sengkang",
                "Serangoon",
                "Ang Mo Kio",
            ],
            "North West Community Development Council": [
                "Woodlands",
                "Yishun",
                "Sembawang",
                "Bukit Panjang",
                "Choa Chu Kang",
            ],
            "South East Community Development Council": [
                "Bedok",
                "Tampines",
                "Pasir Ris",
                "Marine Parade",
                "Geylang",
            ],
            "South West Community Development Council": [
                "Jurong East",
                "Jurong West",
                "Bukit Batok",
                "Clementi",
                "Pioneer",
            ],
        },
    },
}


class WikidataSync:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/sparql-results+json",
                "User-Agent": USER_AGENT,
            }
        )
        self.search_cache: dict[tuple[str, str], list[dict[str, str]]] = {}

    @staticmethod
    def normalize_label(value: str) -> str:
        normalized = unicodedata.normalize("NFKD", value.translate(ASCII_REPLACEMENTS))
        ascii_only = normalized.encode("ascii", "ignore").decode("ascii")
        return " ".join(ascii_only.replace("&", "and").replace("-", " ").split()).strip().lower()

    @staticmethod
    def ascii_label(value: str) -> str:
        normalized = unicodedata.normalize("NFKD", value.translate(ASCII_REPLACEMENTS))
        return " ".join(normalized.encode("ascii", "ignore").decode("ascii").split()).strip()

    def canonicalize_place_label(self, value: str) -> str:
        label = self.ascii_label(value)
        lowered = label.lower()

        for prefix in CANONICAL_PLACE_LABEL_PREFIXES:
            if lowered.startswith(prefix):
                label = label[len(prefix) :]
                lowered = label.lower()

        for suffix in CANONICAL_PLACE_LABEL_SUFFIXES:
            if lowered.endswith(suffix):
                label = label[: -len(suffix)]
                lowered = label.lower()

        return " ".join(label.split()).strip()

    def derive_region_city_aliases(self, region_name: str) -> list[str]:
        label = self.ascii_label(region_name)
        lowered = label.lower()
        candidates: list[str] = []

        for prefix in REGION_CITY_PREFIXES:
            if lowered.startswith(prefix):
                candidates.append(label[len(prefix) :].strip(" -"))

        for suffix in REGION_CITY_SUFFIXES:
            if lowered.endswith(suffix):
                candidates.append(label[: -len(suffix)].strip(" -"))

        if lowered.endswith("-capital region"):
            candidates.append(label[: -len("-capital region")].strip(" -"))

        seen: set[str] = set()
        normalized_region = self.normalize_label(label)
        deduped: list[str] = []
        for candidate in candidates:
            normalized_candidate = self.normalize_label(candidate)
            if not candidate or normalized_candidate == normalized_region or normalized_candidate in seen:
                continue
            seen.add(normalized_candidate)
            deduped.append(candidate)

        return deduped

    def merge_preferred_places(
        self,
        preferred_places: list[dict[str, Any]],
        sourced_places: list[dict[str, Any]],
        max_cities: int = 5,
    ) -> list[dict[str, Any]]:
        merged: list[dict[str, Any]] = []
        seen_labels: set[str] = set()

        for place in [*preferred_places, *sourced_places]:
            normalized_label = self.normalize_label(place["label"])
            if normalized_label in seen_labels:
                continue
            seen_labels.add(normalized_label)
            merged.append(place)
            if len(merged) >= max_cities:
                break

        return merged

    def build_curated_places(
        self,
        curated_labels: list[str],
        sourced_places: list[dict[str, Any]],
        default_type: str = "city",
    ) -> list[dict[str, Any]]:
        source_places_by_label = {
            self.normalize_label(place["label"]): place for place in sourced_places
        }
        default_population = max(
            (int(place.get("population", 0)) for place in sourced_places),
            default=len(curated_labels),
        )

        curated_places: list[dict[str, Any]] = []
        seen_labels: set[str] = set()
        for index, label in enumerate(curated_labels):
            ascii_label = self.ascii_label(label)
            normalized_label = self.normalize_label(ascii_label)
            if not ascii_label or normalized_label in seen_labels:
                continue

            source_place = source_places_by_label.get(normalized_label, {})
            raw_types = source_place.get("types", [default_type])
            if isinstance(raw_types, set):
                types = sorted(self.ascii_label(item) for item in raw_types)
            else:
                types = [self.ascii_label(item) for item in raw_types]

            curated_places.append(
                {
                    "label": ascii_label,
                    "population": int(source_place.get("population", default_population - index)),
                    "types": types or [default_type],
                }
            )
            seen_labels.add(normalized_label)

        return curated_places

    def query(self, sparql: str, retries: int = 4) -> list[dict[str, Any]]:
        last_error: Exception | None = None
        for attempt in range(retries):
            try:
                response = self.session.get(
                    WDQS_ENDPOINT,
                    params={"query": sparql, "format": "json"},
                    timeout=60,
                )
                response.raise_for_status()
                data = response.json()
                time.sleep(0.5)
                return data["results"]["bindings"]
            except HTTPError as error:  # pragma: no cover - network retries
                last_error = error
                status_code = error.response.status_code if error.response is not None else 0
                if status_code == 429:
                    time.sleep(6 * (attempt + 1))
                    continue
                time.sleep(2 * (attempt + 1))
            except Exception as error:  # pragma: no cover - network retries
                last_error = error
                time.sleep(2 * (attempt + 1))
        raise RuntimeError(f"Wikidata query failed after {retries} attempts: {last_error}") from last_error

    def build_seed_dataset(self, country_code: str) -> tuple[dict[str, Any], list[str]]:
        config = COUNTRY_CONFIG[country_code]
        seed_data = config.get("seed_data")
        if not seed_data:
            raise FileNotFoundError(f"No seed data configured for {country_code}")

        root_cities = [self.ascii_label(city) for city in config.get("seed_root_cities", []) if self.ascii_label(city)]
        if not root_cities:
            root_cities = [
                self.ascii_label(cities[0])
                for cities in seed_data.values()
                if cities
            ][:8]

        ordered_data: dict[str, Any] = {
            country_code: {
                "region": config["label"],
                "cities": root_cities,
            }
        }
        desired_regions: list[str] = []

        for raw_region_name, raw_cities in seed_data.items():
            region_name = self.ascii_label(raw_region_name)
            desired_regions.append(region_name)
            ordered_data[region_name] = {
                "region": region_name,
                "cities": [self.ascii_label(city) for city in raw_cities if self.ascii_label(city)],
            }

        return ordered_data, desired_regions

    def remap_existing_dataset(self, country_code: str, data: dict[str, Any]) -> dict[str, Any]:
        config = COUNTRY_CONFIG[country_code]
        region_field = config.get("existing_region_field")
        if not region_field:
            return data

        remapped: dict[str, Any] = {}
        existing_seed_limit = config.get("existing_seed_limit")

        for key, value in data.items():
            if key.upper() == country_code:
                if isinstance(value, dict):
                    remapped[country_code] = value
                continue

            if not isinstance(value, dict):
                continue

            region_name = self.ascii_label(str(value.get(region_field) or key))
            if not region_name:
                continue

            raw_cities = value.get("cities", [])
            if not isinstance(raw_cities, list):
                raw_cities = []

            cities = [self.ascii_label(city) for city in raw_cities if self.ascii_label(city)]
            if isinstance(existing_seed_limit, int) and existing_seed_limit > 0:
                cities = cities[:existing_seed_limit]

            remapped[region_name] = {
                "region": region_name,
                "cities": cities,
            }

        return remapped

    def load_existing_file(self, country_code: str) -> tuple[dict[str, Any], list[str]]:
        config = COUNTRY_CONFIG[country_code]
        path = DATA_DIR / config["file"]

        if config.get("ignore_existing_file") or not path.exists():
            return self.build_seed_dataset(country_code)

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return self.build_seed_dataset(country_code)

        if isinstance(data, dict):
            data = self.remap_existing_dataset(country_code, data)

        regions = [key for key in data.keys() if key.upper() != country_code]
        if not regions and config.get("seed_data"):
            return self.build_seed_dataset(country_code)
        return data, regions

    def load_existing_manifest(self) -> dict[str, Any]:
        manifest_path = DATA_DIR / "countrySources.json"
        if not manifest_path.exists():
            return {}

        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}

        countries = manifest.get("countries")
        return countries if isinstance(countries, dict) else {}

    def fetch_country_regions(self, country_qid: str, excluded: set[str]) -> list[dict[str, str]]:
        query = f"""
        SELECT DISTINCT ?region ?regionLabel WHERE {{
          wd:{country_qid} wdt:P150 ?region.
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        ORDER BY ?regionLabel
        """
        rows = self.query(query)
        regions: list[dict[str, str]] = []
        for row in rows:
            label = row["regionLabel"]["value"]
            if label in excluded:
                continue
            regions.append(
                {
                    "qid": row["region"]["value"].rsplit("/", 1)[-1],
                    "label": label,
                    "normalized": self.normalize_label(label),
                }
            )
        return regions

    def search_region_by_alias(self, country_qid: str, alias: str) -> list[dict[str, str]]:
        cache_key = (country_qid, alias)
        if cache_key in self.search_cache:
            return self.search_cache[cache_key]

        alias_literal = json.dumps(alias.lower())
        query = f"""
        SELECT DISTINCT ?region ?regionLabel ?typeLabel WHERE {{
          VALUES ?country {{ wd:{country_qid} }}
          ?region rdfs:label ?label.
          FILTER(LANG(?label) = "en")
          FILTER(LCASE(STR(?label)) = {alias_literal})
          OPTIONAL {{ ?region wdt:P31 ?type. }}
          FILTER EXISTS {{
            {{ ?region wdt:P131* ?country. }} UNION {{ ?region wdt:P17 ?country. }}
          }}
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        LIMIT 20
        """
        rows = self.query(query)
        result = [
            {
                "qid": row["region"]["value"].rsplit("/", 1)[-1],
                "label": row["regionLabel"]["value"],
                "type": row.get("typeLabel", {}).get("value", ""),
                "normalized": self.normalize_label(row["regionLabel"]["value"]),
            }
            for row in rows
        ]
        self.search_cache[cache_key] = result
        return result

    def choose_region_candidate(
        self,
        desired_region: str,
        aliases: list[str],
        primary_regions: list[dict[str, str]],
        country_qid: str,
    ) -> dict[str, str] | None:
        desired_aliases = [desired_region, *aliases]
        desired_norms = {self.normalize_label(item) for item in desired_aliases}

        for region in primary_regions:
            if region["normalized"] in desired_norms:
                return region

        for alias in desired_aliases:
            try:
                candidates = self.search_region_by_alias(country_qid, alias)
            except RuntimeError:
                continue
            if not candidates:
                continue

            scored = sorted(candidates, key=self.region_candidate_score, reverse=True)
            return scored[0]

        return None

    def region_candidate_score(self, candidate: dict[str, str]) -> int:
        type_label = self.normalize_label(candidate.get("type", ""))
        score = 0
        if any(token in type_label for token in ("province", "county", "district", "region", "state", "canton", "community")):
            score += 10
        if "municipality" not in type_label:
            score += 2
        return score

    def fetch_region_places(self, region_qid: str, max_cities: int = 5) -> list[dict[str, Any]]:
        thresholds = (100000, 50000, 20000, 10000)
        places_by_id: dict[str, dict[str, Any]] = {}
        best_filtered: list[dict[str, Any]] = []

        for threshold in thresholds:
            query = f"""
            SELECT ?place ?placeLabel ?population ?typeLabel WHERE {{
              VALUES ?region {{ wd:{region_qid} }}
              ?place wdt:P131* ?region;
                     wdt:P1082 ?population;
                     wdt:P31 ?type.
              FILTER(?population >= {threshold})
              SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
            }}
            ORDER BY DESC(?population)
            LIMIT 100
            """
            try:
                rows = self.query(query)
            except RuntimeError:
                continue

            for row in rows:
                place_id = row["place"]["value"].rsplit("/", 1)[-1]
                place = places_by_id.setdefault(
                    place_id,
                    {
                        "label": row["placeLabel"]["value"],
                        "population": int(float(row["population"]["value"])),
                        "types": set(),
                    },
                )
                place["types"].add(row.get("typeLabel", {}).get("value", ""))

            filtered = self.filter_places(places_by_id, STRICT_PLACE_TYPES, max_cities)
            if filtered:
                best_filtered = filtered
            if len(filtered) >= max_cities:
                return filtered[:max_cities]

            filtered = self.filter_places(places_by_id, RELAXED_PLACE_TYPES, max_cities)
            if filtered:
                best_filtered = filtered
            if len(filtered) >= max(3, min(max_cities, 3)):
                return filtered[:max_cities]

        if best_filtered:
            return best_filtered[:max_cities]
        return self.filter_places(places_by_id, RELAXED_PLACE_TYPES, max_cities)[:max_cities]

    def fetch_country_places(self, country_qid: str, max_cities: int = 8) -> list[dict[str, Any]]:
        thresholds = (200000, 100000, 50000, 20000)
        places_by_id: dict[str, dict[str, Any]] = {}
        best_filtered: list[dict[str, Any]] = []

        for threshold in thresholds:
            query = f"""
            SELECT ?place ?placeLabel ?population ?typeLabel WHERE {{
              VALUES ?country {{ wd:{country_qid} }}
              ?place wdt:P17 ?country;
                     wdt:P1082 ?population;
                     wdt:P31 ?type.
              FILTER(?population >= {threshold})
              SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
            }}
            ORDER BY DESC(?population)
            LIMIT 120
            """
            try:
                rows = self.query(query)
            except RuntimeError:
                continue

            for row in rows:
                place_id = row["place"]["value"].rsplit("/", 1)[-1]
                place = places_by_id.setdefault(
                    place_id,
                    {
                        "label": row["placeLabel"]["value"],
                        "population": int(float(row["population"]["value"])),
                        "types": set(),
                    },
                )
                place["types"].add(row.get("typeLabel", {}).get("value", ""))

            filtered = self.filter_places(places_by_id, STRICT_PLACE_TYPES, max_cities)
            if filtered:
                best_filtered = filtered
            if len(filtered) >= max_cities:
                return filtered[:max_cities]

            filtered = self.filter_places(places_by_id, RELAXED_PLACE_TYPES, max_cities)
            if filtered:
                best_filtered = filtered
            if len(filtered) >= max(4, min(max_cities, 4)):
                return filtered[:max_cities]

        if best_filtered:
            return best_filtered[:max_cities]
        return self.filter_places(places_by_id, RELAXED_PLACE_TYPES, max_cities)[:max_cities]

    def fetch_exact_named_place(
        self,
        label: str,
        country_qid: str,
        region_qid: str | None = None,
    ) -> dict[str, Any] | None:
        label_literal = json.dumps(label.lower())
        location_filter = f"{{ ?place wdt:P131* wd:{region_qid}. }}" if region_qid else f"{{ ?place wdt:P17 wd:{country_qid}. }}"
        query = f"""
        SELECT DISTINCT ?place ?placeLabel ?population ?typeLabel WHERE {{
          ?place rdfs:label ?rawLabel;
                 wdt:P31 ?type.
          FILTER(LANG(?rawLabel) = "en")
          FILTER(LCASE(STR(?rawLabel)) = {label_literal})
          OPTIONAL {{ ?place wdt:P1082 ?population. }}
          FILTER EXISTS {{
            {location_filter} UNION {{ ?place wdt:P17 wd:{country_qid}. }}
          }}
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        ORDER BY DESC(?population)
        LIMIT 20
        """
        rows = self.query(query)
        places_by_id: dict[str, dict[str, Any]] = {}

        for row in rows:
            place_id = row["place"]["value"].rsplit("/", 1)[-1]
            place = places_by_id.setdefault(
                place_id,
                {
                    "label": row["placeLabel"]["value"],
                    "population": int(float(row.get("population", {}).get("value", 0) or 0)),
                    "types": set(),
                },
            )
            place["types"].add(row.get("typeLabel", {}).get("value", ""))

        exact_matches = self.filter_places(places_by_id, RELAXED_PLACE_TYPES, 1)
        return exact_matches[0] if exact_matches else None

    def place_type_score(self, types: set[str]) -> int:
        normalized_types = [self.ascii_label(item).lower() for item in types]
        if any(any(term in type_label for term in ("city", "town", "capital", "metropolis", "commune")) for type_label in normalized_types):
            return 3
        if any(any(term in type_label for term in ("municipality", "borough")) for type_label in normalized_types):
            return 2
        if any("village" in type_label for type_label in normalized_types):
            return 1
        if any("human settlement" in type_label for type_label in normalized_types):
            return 0
        return -1

    def has_allowed_place_type(self, types: set[str], allowed_type_terms: tuple[str, ...]) -> bool:
        normalized_types = [self.ascii_label(item).lower() for item in types]
        return any(
            any(term in type_label for term in allowed_type_terms)
            and not any(blocked in type_label for blocked in BLOCKED_PLACE_TYPES)
            for type_label in normalized_types
        )

    def has_allowed_country_root_type(self, types: set[str]) -> bool:
        normalized_types = [self.ascii_label(item).lower() for item in types]
        return any(
            any(term in type_label for term in COUNTRY_ROOT_ALLOWED_TYPE_TERMS)
            and not any(blocked in type_label for blocked in BLOCKED_PLACE_TYPES + COUNTRY_ROOT_BLOCKED_TYPE_TERMS)
            for type_label in normalized_types
        )

    def has_admin_like_label(self, label: str) -> bool:
        normalized_label = self.normalize_label(label)
        return any(token in normalized_label for token in ADMIN_REGION_NAME_TOKENS)

    def is_blocked_place_label(self, label: str) -> bool:
        normalized_label = self.normalize_label(label)
        return any(normalized_label.startswith(prefix) for prefix in BLOCKED_PLACE_LABEL_PREFIXES)

    @staticmethod
    def summarize_country_notes(metadata: dict[str, Any]) -> str:
        regions = metadata.get("regions", [])
        direct_count = sum(1 for region in regions if region["status"] == "sourced_wikidata")
        exact_label_count = sum(
            1 for region in regions if region["status"] == "sourced_wikidata_region_label"
        )
        curated_count = sum(
            1 for region in regions if region["status"] == "sourced_wikidata_curated_labels"
        )
        fallback_count = sum(1 for region in regions if region["status"] == "fallback_existing_seed")

        summary_parts = [f"{direct_count} region(s) sourced directly from Wikidata"]
        if exact_label_count:
            summary_parts.append(
                f"{exact_label_count} city-state region(s) reduced to the exact Wikidata region label"
            )
        if curated_count:
            summary_parts.append(
                f"{curated_count} region(s) use curated city labels to avoid municipality-heavy Wikidata outputs"
            )
        if fallback_count:
            summary_parts.append(f"{fallback_count} region(s) still use the previous seed fallback")
        if metadata.get("country_root_status") == "sourced_wikidata_curated_labels":
            summary_parts.append("the country root list uses curated labels for stable nationwide coverage")
        if metadata.get("country_root_status") == "fallback_existing_seed":
            summary_parts.append("the country root list still uses the previous seed fallback")

        return (
            "Region labels stay aligned with the existing UI. "
            "Cities are population-ranked place entities sourced from Wikidata and ASCII-normalized "
            "for frontend consistency. Coverage: "
            + "; ".join(summary_parts)
            + "."
        )

    def filter_country_root_places(self, places: list[dict[str, Any]], max_cities: int) -> list[dict[str, Any]]:
        return self.rank_country_root_places(places)[:max_cities]

    def rank_country_root_places(self, places: list[dict[str, Any]]) -> list[dict[str, Any]]:
        filtered: list[dict[str, Any]] = []
        seen_labels: set[str] = set()

        ranked_places = sorted(
            places,
            key=lambda item: (self.place_type_score(set(item["types"])), item["population"]),
            reverse=True,
        )

        for place in ranked_places:
            label = self.canonicalize_place_label(place["label"])
            normalized_label = self.normalize_label(label)
            if not label or normalized_label in seen_labels:
                continue
            if self.is_blocked_place_label(place["label"]):
                continue
            if self.has_admin_like_label(label):
                continue
            if not self.has_allowed_country_root_type(set(place["types"])):
                continue

            seen_labels.add(normalized_label)
            filtered.append(
                {
                    "label": label,
                    "population": place["population"],
                    "types": sorted(self.ascii_label(item) for item in place["types"]),
                }
            )

        return filtered

    def select_diverse_country_root_places(
        self,
        ranked_places: list[dict[str, Any]],
        max_cities: int,
        city_regions: dict[str, set[str]],
    ) -> list[dict[str, Any]]:
        if not city_regions:
            return ranked_places[:max_cities]

        selected: list[dict[str, Any]] = []
        selected_labels: set[str] = set()
        region_counts: dict[str, int] = {}

        for region_limit in range(1, max_cities + 1):
            added_in_pass = False
            for place in ranked_places:
                normalized_label = self.normalize_label(place["label"])
                if normalized_label in selected_labels:
                    continue

                regions = sorted(city_regions.get(normalized_label, set()))
                if regions and min(region_counts.get(region, 0) for region in regions) >= region_limit:
                    continue

                selected.append(place)
                selected_labels.add(normalized_label)
                if regions:
                    primary_region = min(regions, key=lambda region: (region_counts.get(region, 0), region))
                    region_counts[primary_region] = region_counts.get(primary_region, 0) + 1
                added_in_pass = True

                if len(selected) >= max_cities:
                    return selected

            if not added_in_pass:
                break

        for place in ranked_places:
            normalized_label = self.normalize_label(place["label"])
            if normalized_label in selected_labels:
                continue
            selected.append(place)
            if len(selected) >= max_cities:
                break

        return selected[:max_cities]

    def filter_places(
        self,
        places_by_id: dict[str, dict[str, Any]],
        allowed_type_terms: tuple[str, ...],
        max_cities: int,
    ) -> list[dict[str, Any]]:
        filtered: list[dict[str, Any]] = []
        seen_labels: set[str] = set()

        ranked_places = sorted(
            places_by_id.values(),
            key=lambda item: (self.place_type_score(item["types"]), item["population"]),
            reverse=True,
        )

        for place in ranked_places:
            label = self.canonicalize_place_label(place["label"])
            normalized_label = self.normalize_label(label)
            if not label or normalized_label in seen_labels:
                continue
            if re.fullmatch(r"Q\d+", label):
                continue
            if self.is_blocked_place_label(place["label"]):
                continue

            if not self.has_allowed_place_type(place["types"], allowed_type_terms):
                continue

            seen_labels.add(normalized_label)
            filtered.append(
                {
                    "label": label,
                    "population": place["population"],
                    "types": sorted(self.ascii_label(item) for item in place["types"]),
                }
            )
            if len(filtered) >= max_cities:
                break

        return filtered

    def build_country_dataset(self, country_code: str) -> tuple[dict[str, Any], dict[str, Any]]:
        config = COUNTRY_CONFIG[country_code]
        existing_data, desired_regions = self.load_existing_file(country_code)
        primary_regions = self.fetch_country_regions(
            config["qid"],
            set(config.get("exclude_regions", set())),
        )

        output: dict[str, Any] = {}
        region_metadata: list[dict[str, Any]] = []
        country_place_candidate_tiers: list[list[dict[str, Any]]] = []
        country_city_regions: dict[str, set[str]] = {}
        exact_only_regions = set(config.get("exact_only_regions", set()))
        for region_name in desired_regions:
            print(f"  [region] {country_code} {region_name}")
            aliases = config.get("aliases", {}).get(region_name, [])
            manual_override_labels = config.get("manual_city_overrides", {}).get(region_name, [])
            if not manual_override_labels and config.get("seed_cities_as_manual_overrides"):
                manual_override_labels = existing_data.get(region_name, {}).get("cities", [])
            skip_region_place_queries = config.get("skip_region_place_queries") and bool(manual_override_labels)
            configured_region_qid = config.get("region_qids", {}).get(region_name)
            region_candidate = (
                {
                    "qid": configured_region_qid,
                    "label": region_name,
                    "normalized": self.normalize_label(region_name),
                }
                if configured_region_qid
                else self.choose_region_candidate(region_name, aliases, primary_regions, config["qid"])
            )

            if not region_candidate:
                print(f"    [fallback] unresolved region label")
                fallback_cities = existing_data[region_name]["cities"]
                output[region_name] = {"region": region_name, "cities": fallback_cities}
                region_metadata.append(
                    {
                        "label": region_name,
                        "status": "fallback_existing_seed",
                        "wikidata_qid": None,
                        "wikidata_url": None,
                        "city_count": len(fallback_cities),
                    }
                )
                continue

            if skip_region_place_queries:
                sourced_places = []
            else:
                try:
                    sourced_places = self.fetch_region_places(region_candidate["qid"])
                except RuntimeError:
                    sourced_places = []

            normalized_region_name = self.normalize_label(region_name)
            existing_region_cities = existing_data.get(region_name, {}).get("cities", [])
            seed_has_matching_city = any(
                self.normalize_label(city) == normalized_region_name
                for city in existing_region_cities
            ) and not any(token in normalized_region_name for token in ADMIN_REGION_NAME_TOKENS)
            needs_exact_name_lookup = (
                seed_has_matching_city or region_name in exact_only_regions
            ) and not skip_region_place_queries and (
                not sourced_places
                or all(
                    self.normalize_label(place["label"]) != normalized_region_name
                    for place in sourced_places
                )
            )
            exact_named_place = None
            used_region_label_for_exact_only = False
            if needs_exact_name_lookup:
                try:
                    exact_named_place = self.fetch_exact_named_place(
                        region_name,
                        config["qid"],
                        region_candidate["qid"],
                    )
                except RuntimeError:
                    exact_named_place = None

            derived_city_alias = None
            derived_city_place = None
            if not skip_region_place_queries:
                for derived_city_alias in self.derive_region_city_aliases(region_name):
                    derived_city_place = next(
                        (
                            place
                            for place in sourced_places
                            if self.normalize_label(place["label"]) == self.normalize_label(derived_city_alias)
                        ),
                        None,
                    )
                    if derived_city_place:
                        break
                    try:
                        derived_city_place = self.fetch_exact_named_place(
                            derived_city_alias,
                            config["qid"],
                            region_candidate["qid"],
                        )
                    except RuntimeError:
                        derived_city_place = None
                    if derived_city_place:
                        break

            preferred_city_places: list[dict[str, Any]] = []
            if not skip_region_place_queries and len(sourced_places) < 5:
                seen_preferred_labels = {
                    self.normalize_label(place["label"]) for place in sourced_places
                }
                for preferred_city_label in config.get("preferred_city_labels", {}).get(region_name, []):
                    normalized_preferred_label = self.normalize_label(preferred_city_label)
                    if normalized_preferred_label in seen_preferred_labels:
                        continue
                    if len(sourced_places) + len(preferred_city_places) >= 5:
                        break
                    try:
                        preferred_city_place = self.fetch_exact_named_place(
                            preferred_city_label,
                            config["qid"],
                            region_candidate["qid"],
                        )
                    except RuntimeError:
                        preferred_city_place = None
                    if preferred_city_place:
                        preferred_city_places.append(preferred_city_place)
                        seen_preferred_labels.add(normalized_preferred_label)

            if exact_named_place:
                exact_label = exact_named_place["label"]
                if all(self.normalize_label(place["label"]) != self.normalize_label(exact_label) for place in sourced_places):
                    sourced_places = [exact_named_place, *sourced_places]
                    sourced_places = sourced_places[:5]

            if derived_city_place:
                derived_label = derived_city_place["label"]
                matching_place = next(
                    (
                        place
                        for place in sourced_places
                        if self.normalize_label(place["label"]) == self.normalize_label(derived_label)
                    ),
                    None,
                )
                remaining_places = [
                    place
                    for place in sourced_places
                    if self.normalize_label(place["label"]) != self.normalize_label(derived_label)
                ]
                sourced_places = [(matching_place or derived_city_place), *remaining_places]
                sourced_places = sourced_places[:5]

            if preferred_city_places:
                sourced_places = self.merge_preferred_places(preferred_city_places, sourced_places)

            used_manual_city_overrides = False
            if manual_override_labels:
                sourced_places = self.build_curated_places(manual_override_labels, sourced_places)
                used_manual_city_overrides = True

            if not seed_has_matching_city:
                sourced_places = [
                    place
                    for place in sourced_places
                    if self.normalize_label(place["label"]) != normalized_region_name
                ]

            if region_name in exact_only_regions:
                exact_from_region_list = next(
                    (
                        place
                        for place in sourced_places
                        if self.normalize_label(place["label"]) == normalized_region_name
                    ),
                    None,
                )
                if exact_from_region_list:
                    sourced_places = [exact_from_region_list]
                elif exact_named_place:
                    sourced_places = [exact_named_place]
                else:
                    sourced_places = [
                        {
                            "label": self.ascii_label(region_name),
                            "population": 0,
                            "types": [],
                        }
                    ]
                    used_region_label_for_exact_only = True

            if not sourced_places:
                print(f"    [fallback] no sourced cities")
                fallback_cities = existing_data[region_name]["cities"]
                output[region_name] = {"region": region_name, "cities": fallback_cities}
                region_metadata.append(
                    {
                        "label": region_name,
                        "status": "fallback_existing_seed",
                        "wikidata_qid": region_candidate["qid"],
                        "wikidata_url": f"https://www.wikidata.org/wiki/{region_candidate['qid']}",
                        "city_count": len(fallback_cities),
                    }
                )
                continue

            cities = [place["label"] for place in sourced_places]
            print(f"    [ok] {len(cities)} cities from {region_candidate['qid']}")
            output[region_name] = {"region": region_name, "cities": cities}
            for tier_index, place in enumerate(sourced_places):
                while len(country_place_candidate_tiers) <= tier_index:
                    country_place_candidate_tiers.append([])
                country_place_candidate_tiers[tier_index].append(place)
                country_city_regions.setdefault(self.normalize_label(place["label"]), set()).add(region_name)
            region_metadata.append(
                {
                    "label": region_name,
                    "status": (
                        "sourced_wikidata_curated_labels"
                        if used_manual_city_overrides
                        else
                        "sourced_wikidata_region_label"
                        if used_region_label_for_exact_only
                        else "sourced_wikidata"
                    ),
                    "wikidata_qid": region_candidate["qid"],
                    "wikidata_url": f"https://www.wikidata.org/wiki/{region_candidate['qid']}",
                    "city_count": len(cities),
                }
            )

        country_root_status = "sourced_wikidata"
        used_manual_country_root_labels = False

        skip_country_place_queries = config.get("skip_country_place_queries") and config.get(
            "manual_country_root_labels"
        )
        if skip_country_place_queries:
            country_places = []
        elif config.get("balance_country_root_by_region"):
            primary_country_pool = list(country_place_candidate_tiers[0]) if country_place_candidate_tiers else []
            ranked_country_places = self.rank_country_root_places(primary_country_pool)
            country_places = self.select_diverse_country_root_places(ranked_country_places, 8, country_city_regions)
            if len(country_places) < 8:
                supplemental_country_pool = self.fetch_country_places(config["qid"], max_cities=20)
                for tier in country_place_candidate_tiers[1:]:
                    supplemental_country_pool.extend(tier)
                ranked_country_places = self.rank_country_root_places(
                    [*country_places, *supplemental_country_pool]
                )
                country_places = self.select_diverse_country_root_places(
                    ranked_country_places,
                    8,
                    country_city_regions,
                )
        else:
            country_place_pool = self.fetch_country_places(config["qid"], max_cities=20)
            for tier in country_place_candidate_tiers:
                country_place_pool.extend(tier)
            ranked_country_places = self.rank_country_root_places(country_place_pool)
            country_places = ranked_country_places[:8]

        manual_country_root_labels = config.get("manual_country_root_labels", [])
        if manual_country_root_labels:
            country_root_source_pool = [place for tier in country_place_candidate_tiers for place in tier]
            country_root_source_pool.extend(country_places)
            country_places = self.build_curated_places(manual_country_root_labels, country_root_source_pool)
            used_manual_country_root_labels = True

        if not country_places:
            fallback_country_cities = existing_data.get(country_code, {}).get("cities", [])
            country_places = self.build_curated_places(fallback_country_cities, [])
            country_root_status = "fallback_existing_seed"
        elif used_manual_country_root_labels:
            country_root_status = "sourced_wikidata_curated_labels"

        print(f"  [country] {country_code} {len(country_places)} top cities")
        output[country_code] = {
            "region": config["label"],
            "cities": [place["label"] for place in country_places],
        }

        ordered_output = {country_code: output[country_code]}
        for region_name in desired_regions:
            ordered_output[region_name] = output[region_name]

        metadata = {
            "country_code": country_code,
            "country": config["label"],
            "output_file": f"data/{config['file']}",
            "country_qid": config["qid"],
            "country_url": f"https://www.wikidata.org/wiki/{config['qid']}",
            "source_name": "Wikidata Query Service",
            "source_url": WDQS_HOME_URL,
            "source_docs_url": WDQS_DOCS_URL,
            "script": "scripts/sync-sourced-country-data.py",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "regions": region_metadata,
            "country_root_status": country_root_status,
            "country_root_city_count": len(output[country_code]["cities"]),
        }
        metadata["notes"] = self.summarize_country_notes(metadata)
        return ordered_output, metadata

    def write_country_file(self, country_code: str, data: dict[str, Any]) -> None:
        config = COUNTRY_CONFIG[country_code]
        path = DATA_DIR / config["file"]
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def write_source_manifest(self, metadata_by_country: dict[str, Any]) -> dict[str, Any]:
        manifest_path = DATA_DIR / "countrySources.json"
        combined_metadata = self.load_existing_manifest()
        combined_metadata.update(metadata_by_country)
        for country_code, item in combined_metadata.items():
            item["country_code"] = country_code
            item["notes"] = self.summarize_country_notes(item)
        manifest = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "pipeline": {
                "script": "scripts/sync-sourced-country-data.py",
                "primary_source": {
                    "name": "Wikidata Query Service",
                    "url": WDQS_HOME_URL,
                    "docs_url": WDQS_DOCS_URL,
                },
                "notes": "Newly added country files are rebuilt from public structured data. Region labels are kept stable for the frontend, while city entries are refreshed from Wikidata.",
            },
            "countries": combined_metadata,
        }
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return combined_metadata

    def write_source_docs(self, metadata_by_country: dict[str, Any]) -> None:
        root_status_labels = {
            "sourced_wikidata": "population-ranked countrywide places from Wikidata",
            "sourced_wikidata_curated_labels": "curated countrywide labels anchored to the sourced region dataset",
            "fallback_existing_seed": "previous seed fallback",
        }
        lines = [
            "# Country Sources",
            "",
            "This file records the source pipeline for the newly added country datasets.",
            "",
            "- Primary source: [Wikidata Query Service](https://query.wikidata.org/)",
            f"- Source docs: [Wikidata Query Service User Manual]({WDQS_DOCS_URL})",
            "- Sync script: `scripts/sync-sourced-country-data.py`",
            "- Output manifest: `data/countrySources.json`",
            "",
            "Notes:",
            "- Region labels stay aligned with the current frontend UI.",
            "- City labels are ASCII-normalized for consistency with the existing project data files.",
            "- If a region cannot be resolved cleanly, the script keeps the previous seed list and marks that region as a fallback in the manifest.",
            "- City-state regions can be reduced to their exact region label when Wikidata cleanly resolves the region but not a separate city list; these cases are marked as `sourced_wikidata_region_label` in the manifest.",
            "- A small number of municipality-heavy regions or country roots can use curated place-label overrides while still keeping the Wikidata-backed region source; these cases are marked as `sourced_wikidata_curated_labels` in the manifest or country notes.",
            "",
        ]

        for country_code in sorted(metadata_by_country):
            item = metadata_by_country[country_code]
            sourced_count = sum(
                1 for region in item["regions"] if region["status"].startswith("sourced_wikidata")
            )
            total_count = len(item["regions"])
            lines.extend(
                [
                    f"## {country_code} {item['country']}",
                    "",
                    f"- Output: `{item['output_file']}`",
                    f"- Country item: [{item['country_qid']}]({item['country_url']})",
                    f"- Source: [{item['source_name']}]({item['source_url']})",
                    f"- Regions sourced: {sourced_count}/{total_count}",
                    f"- Country root cities: {root_status_labels.get(item.get('country_root_status', 'sourced_wikidata'), root_status_labels['sourced_wikidata'])}",
                    f"- Generated: `{item['generated_at']}`",
                    f"- Notes: {item['notes']}",
                    "",
                ]
            )

        docs_path = DOCS_DIR / "COUNTRY_SOURCES.md"
        docs_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def persist_source_outputs(self, metadata_by_country: dict[str, Any]) -> dict[str, Any]:
        combined_metadata = self.write_source_manifest(metadata_by_country)
        self.write_source_docs(combined_metadata)
        return combined_metadata


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync selected country files from Wikidata.")
    parser.add_argument(
        "countries",
        nargs="*",
        help="Country codes to sync. Defaults to all source-backed countries.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    requested = [country.upper() for country in args.countries] if args.countries else list(COUNTRY_CONFIG)
    invalid = [country for country in requested if country not in COUNTRY_CONFIG]
    if invalid:
        raise SystemExit(f"Unsupported country codes: {', '.join(invalid)}")

    sync = WikidataSync()
    metadata_by_country: dict[str, Any] = {}

    for country_code in requested:
        print(f"[sync] {country_code} {COUNTRY_CONFIG[country_code]['label']}")
        try:
            data, metadata = sync.build_country_dataset(country_code)
            sync.write_country_file(country_code, data)
            metadata_by_country[country_code] = metadata
            sync.persist_source_outputs(metadata_by_country)
        except Exception as error:
            print(f"[warn] {country_code} sync failed: {error}")

    print(f"[done] synced {len(metadata_by_country)} country files")


if __name__ == "__main__":
    main()
