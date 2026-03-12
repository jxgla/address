#!/usr/bin/env python3
"""
自动化获取全球地址数据脚本
从 GeoNames 和其他公开源获取城市、邮编、名字等数据
生成 MockAddress 项目所需的 JSON 文件
"""

import os
import json
import requests
from pathlib import Path
import time
from urllib.parse import urlencode

# 配置
OUTPUT_DIR = Path(__file__).parent.absolute()
GEONAMES_USERNAME = "demo"  # 免费账户，建议自己注册：https://www.geonames.org/login
COUNTRIES = {
    "US": "United States",
    "CN": "China",
    "HK": "Hong Kong",
    "TW": "Taiwan",
    "JP": "Japan",
    "GB": "United Kingdom",
    "CA": "Canada",
    "AU": "Australia",
    "DE": "Germany",
    "IN": "India",
    "SG": "Singapore",
}

def ensure_dir():
    """确保输出目录存在"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✓ 输出目录: {OUTPUT_DIR}")

def fetch_cities_by_country(country_code):
    """从 GeoNames 获取指定国家的城市数据"""
    print(f"  获取 {COUNTRIES.get(country_code, country_code)} 的城市数据...")
    
    url = "http://api.geonames.org/searchJSON"
    params = {
        "country": country_code,
        "featureClass": "P",  # P = City/Town/Village
        "maxRows": 1000,
        "username": GEONAMES_USERNAME,
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "geonames" in data:
            cities = [
                {
                    "name": item["name"],
                    "admin1Code": item.get("adminCode1", ""),
                    "latitude": item.get("lat"),
                    "longitude": item.get("lng"),
                    "population": item.get("population", 0),
                }
                for item in data["geonames"]
            ]
            print(f"    ✓ 获得 {len(cities)} 个城市")
            return cities
        else:
            print(f"    ✗ 未获得数据")
            return []
    except Exception as e:
        print(f"    ✗ 错误: {e}")
        return []

def generate_us_data():
    """美国数据 - 所有州和主要城市"""
    print("[ 美国数据 ]")
    cities = fetch_cities_by_country("US")
    
    if not cities:
        print("  ⚠ 未能获取美国数据，使用预设数据")
        cities = _get_us_fallback()
    
    # 按州分组
    by_state = {}
    for city in cities:
        state = city.get("admin1Code", "")
        if state:
            if state not in by_state:
                by_state[state] = {"state": state, "cities": []}
            by_state[state]["cities"].append(city["name"])
    
    return by_state

def generate_cn_data():
    """中国数据 - 主要城市"""
    print("[ 中国数据 ]")
    cities = fetch_cities_by_country("CN")
    
    if not cities:
        print("  ⚠ 未能获取中国数据，使用预设数据")
        cities = _get_cn_fallback()
    
    # 按省份分组
    by_province = {}
    for city in cities:
        province = city.get("admin1Code", "未知")
        if province:
            if province not in by_province:
                by_province[province] = {
                    "province": province,
                    "cities": []
                }
            by_province[province]["cities"].append(city["name"])
    
    return by_province

def generate_hk_data():
    """香港数据"""
    print("[ 香港数据 ]")
    cities = fetch_cities_by_country("HK")
    
    if not cities:
        cities = _get_hk_fallback()
    
    return {"HK": {"cities": [c["name"] for c in cities]}}

def generate_tw_data():
    """台湾数据"""
    print("[ 台湾数据 ]")
    cities = fetch_cities_by_country("TW")
    
    if not cities:
        cities = _get_tw_fallback()
    
    return {"TW": {"cities": [c["name"] for c in cities]}}

def generate_jp_data():
    """日本数据"""
    print("[ 日本数据 ]")
    cities = fetch_cities_by_country("JP")
    
    if not cities:
        cities = _get_jp_fallback()
    
    # 按都道府县分组
    by_prefecture = {}
    for city in cities:
        prefecture = city.get("admin1Code", "未知")
        if prefecture:
            if prefecture not in by_prefecture:
                by_prefecture[prefecture] = {"prefecture": prefecture, "cities": []}
            by_prefecture[prefecture]["cities"].append(city["name"])
    
    return by_prefecture

def generate_uk_data():
    """英国数据"""
    print("[ 英国数据 ]")
    cities = fetch_cities_by_country("GB")
    
    if not cities:
        cities = _get_uk_fallback()
    
    return {"GB": {"cities": [c["name"] for c in cities]}}

def generate_ca_data():
    """加拿大数据"""
    print("[ 加拿大数据 ]")
    cities = fetch_cities_by_country("CA")
    
    if not cities:
        cities = _get_ca_fallback()
    
    return {"CA": {"cities": [c["name"] for c in cities]}}

def generate_in_data():
    """印度数据"""
    print("[ 印度数据 ]")
    cities = fetch_cities_by_country("IN")
    
    if not cities:
        cities = _get_in_fallback()
    
    return {"IN": {"cities": [c["name"] for c in cities]}}

def generate_sg_data():
    """新加坡数据"""
    print("[ 新加坡数据 ]")
    return {"SG": {"cities": ["Singapore", "Bukit Merah", "Toa Payoh", "Bedok", "Geylang"]}}

def generate_de_data():
    """德国数据"""
    print("[ 德国数据 ]")
    cities = fetch_cities_by_country("DE")
    
    if not cities:
        cities = _get_de_fallback()
    
    return {"DE": {"cities": [c["name"] for c in cities]}}

def generate_names_data():
    """常见名字数据"""
    print("[ 名字数据 ]")
    
    names_data = {
        "firstName_male": [
            "James", "John", "Robert", "Michael", "David", "Richard", "Joseph", "Thomas",
            "Charles", "Christopher", "Daniel", "Matthew", "José", "Mark", "Donald",
            "李", "王", "张", "刘", "陈", "杨", "黄", "赵", "吴", "周",
            "田中", "鈴木", "高橋", "渡辺", "伊藤", "中村", "小林", "加藤",
        ],
        "firstName_female": [
            "Mary", "Patricia", "Jennifer", "Linda", "Barbara", "Elizabeth", "Susan", "Jessica",
            "Sarah", "Karen", "Nancy", "Lisa", "Betty", "Margaret", "Sandra",
            "娜", "芳", "英", "玉", "秀英", "惠子", "由美", "智子",
            "田中", "鈴木", "高橋", "渡辺", "伊藤"
        ],
        "lastName": [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
            "Rodriguez", "Martinez", "Wilson", "Anderson", "Taylor", "Thomas", "Moore",
            "李", "王", "张", "刘", "陈", "杨", "黄", "赵", "吴", "周",
            "田中", "鈴木", "高橋", "渡辺", "伊藤", "中村", "小林", "加藤",
        ]
    }
    
    return names_data

def generate_mac_oui_data():
    """MAC 地址厂商代码数据"""
    print("[ MAC OUI 数据 ]")
    
    # 常见厂商 OUI
    mac_data = [
        {"oui": "00:00:0C", "vendor": "Cisco"},
        {"oui": "00:01:42", "vendor": "Digital Equipment"},
        {"oui": "00:01:43", "vendor": "Cisco"},
        {"oui": "00:1A:A0", "vendor": "Cisco"},
        {"oui": "00:26:86", "vendor": "Apple"},
        {"oui": "08:00:27", "vendor": "PCS Systemtechnik"},
        {"oui": "08:02:86", "vendor": "Microsystems"},
        {"oui": "52:54:00", "vendor": "QEMU"},
        {"oui": "AA:BB:CC", "vendor": "Test"},
        {"oui": "A0:E0:FF", "vendor": "Astro"},
        {"oui": "00:11:22", "vendor": "Intel"},
        {"oui": "08:94:EF", "vendor": "Apple"},
        {"oui": "00:50:F2", "vendor": "Microsoft"},
        {"oui": "00:13:10", "vendor": "Linksys"},
        {"oui": "00:1E:58", "vendor": "Nintendo"},
    ]
    
    return mac_data

def generate_all():
    """生成所有数据文件"""
    print("\n🚀 开始生成地址数据...\n")
    ensure_dir()
    print()
    
    # 生成各国数据
    data_generators = [
        ("usData.json", generate_us_data),
        ("cnData.json", generate_cn_data),
        ("hkData.json", generate_hk_data),
        ("twData.json", generate_tw_data),
        ("jpData.json", generate_jp_data),
        ("jpNamesData.json", generate_names_data),
        ("gbData.json", generate_uk_data),
        ("caData.json", generate_ca_data),
        ("inData.json", generate_in_data),
        ("sgData.json", generate_sg_data),
        ("deData.json", generate_de_data),
        ("namesData.json", generate_names_data),
        ("macOuiData.json", generate_mac_oui_data),
    ]
    
    for filename, generator in data_generators:
        try:
            data = generator()
            filepath = OUTPUT_DIR / filename
            
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"  ✓ 已保存: {filename}")
        except Exception as e:
            print(f"  ✗ 错误生成 {filename}: {e}")
        
        time.sleep(0.5)  # 避免请求过快
    
    print(f"\n✅ 完成！所有数据文件已生成到: {OUTPUT_DIR}\n")
    print("文件列表:")
    for f in sorted(OUTPUT_DIR.glob("*.json")):
        size_kb = f.stat().st_size / 1024
        print(f"  - {f.name} ({size_kb:.1f} KB)")

# 预设数据备用（如果 GeoNames 请求失败）
def _get_us_fallback():
    return [
        {"name": "New York", "admin1Code": "NY"},
        {"name": "Los Angeles", "admin1Code": "CA"},
        {"name": "Chicago", "admin1Code": "IL"},
        {"name": "Houston", "admin1Code": "TX"},
        {"name": "Phoenix", "admin1Code": "AZ"},
        {"name": "Philadelphia", "admin1Code": "PA"},
        {"name": "San Antonio", "admin1Code": "TX"},
        {"name": "San Diego", "admin1Code": "CA"},
        {"name": "Dallas", "admin1Code": "TX"},
        {"name": "San Jose", "admin1Code": "CA"},
    ]

def _get_cn_fallback():
    return [
        {"name": "Beijing", "admin1Code": "北京"},
        {"name": "Shanghai", "admin1Code": "上海"},
        {"name": "Guangzhou", "admin1Code": "广东"},
        {"name": "Shenzhen", "admin1Code": "广东"},
        {"name": "Chengdu", "admin1Code": "四川"},
        {"name": "Hangzhou", "admin1Code": "浙江"},
        {"name": "Wuhan", "admin1Code": "湖北"},
        {"name": "Nanjing", "admin1Code": "江苏"},
        {"name": "Chongqing", "admin1Code": "重庆"},
        {"name": "Xi'an", "admin1Code": "陕西"},
    ]

def _get_hk_fallback():
    return [
        {"name": "Hong Kong", "admin1Code": "HK"},
        {"name": "Kowloon", "admin1Code": "HK"},
        {"name": "New Territories", "admin1Code": "HK"},
    ]

def _get_tw_fallback():
    return [
        {"name": "Taipei", "admin1Code": "TW"},
        {"name": "Taichung", "admin1Code": "TW"},
        {"name": "Kaohsiung", "admin1Code": "TW"},
        {"name": "Tainan", "admin1Code": "TW"},
    ]

def _get_jp_fallback():
    return [
        {"name": "Tokyo", "admin1Code": "東京"},
        {"name": "Osaka", "admin1Code": "大阪"},
        {"name": "Yokohama", "admin1Code": "神奈川"},
        {"name": "Kyoto", "admin1Code": "京都"},
    ]

def _get_uk_fallback():
    return [
        {"name": "London", "admin1Code": "ENG"},
        {"name": "Manchester", "admin1Code": "ENG"},
        {"name": "Birmingham", "admin1Code": "ENG"},
        {"name": "Liverpool", "admin1Code": "ENG"},
    ]

def _get_ca_fallback():
    return [
        {"name": "Toronto", "admin1Code": "ON"},
        {"name": "Vancouver", "admin1Code": "BC"},
        {"name": "Montreal", "admin1Code": "QC"},
        {"name": "Calgary", "admin1Code": "AB"},
    ]

def _get_in_fallback():
    return [
        {"name": "Mumbai", "admin1Code": "MH"},
        {"name": "Delhi", "admin1Code": "DL"},
        {"name": "Bangalore", "admin1Code": "KA"},
        {"name": "Hyderabad", "admin1Code": "TG"},
    ]

def _get_de_fallback():
    return [
        {"name": "Berlin", "admin1Code": "be"},
        {"name": "Munich", "admin1Code": "by"},
        {"name": "Frankfurt", "admin1Code": "he"},
        {"name": "Cologne", "admin1Code": "nw"},
    ]

if __name__ == "__main__":
    try:
        generate_all()
    except KeyboardInterrupt:
        print("\n\n⚠ 操作已取消")
    except Exception as e:
        print(f"\n\n✗ 发生错误: {e}")
        import traceback
        traceback.print_exc()
