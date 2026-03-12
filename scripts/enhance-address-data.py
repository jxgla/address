#!/usr/bin/env python3
"""
使用 Faker 库增强地址数据
- 扩展已有的城市数据
- 补充缺失的字段
- 生成真实感的邮编、地址等
"""

import json
from pathlib import Path
from faker import Faker
from collections import defaultdict
import random

OUTPUT_DIR = Path(__file__).parent.absolute()

# 各国 Faker 本地化代码
LOCALES = {
    "US": "en_US",
    "CN": "zh_CN",
    "HK": "zh_HK",
    "TW": "zh_TW",
    "JP": "ja_JP",
    "GB": "en_GB",
    "CA": "en_CA",
    "DE": "de_DE",
    "IN": "en_IN",
    "SG": "en_SG",
}

# 州/省映射（用于补充邮编等）
US_STATES = {
    "NY": "New York", "CA": "California", "TX": "Texas", "FL": "Florida",
    "IL": "Illinois", "PA": "Pennsylvania", "OH": "Ohio", "MI": "Michigan",
    "NC": "North Carolina", "GA": "Georgia", "NJ": "New Jersey", "VA": "Virginia",
    "WA": "Washington", "AZ": "Arizona", "MA": "Massachusetts", "CO": "Colorado",
    "MN": "Minnesota", "MO": "Missouri", "MD": "Maryland", "HI": "Hawaii"
}

CN_PROVINCES = {
    "北京": "Beijing", "上海": "Shanghai", "广东": "Guangdong", "四川": "Sichuan",
    "浙江": "Zhejiang", "湖北": "Hubei", "江苏": "Jiangsu", "重庆": "Chongqing",
    "陕西": "Shaanxi", "福建": "Fujian", "天津": "Tianjin", "安徽": "Anhui",
    "山东": "Shandong", "河北": "Hebei", "河南": "Henan", "湖南": "Hunan",
    "云南": "Yunnan", "辽宁": "Liaoning", "黑龙江": "Heilongjiang", "吉林": "Jilin"
}

def load_json(filepath):
    """加载现有 JSON 文件"""
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_json(filepath, data):
    """保存 JSON 文件"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ {filepath.name}")

def enhance_us_data():
    """扩展美国数据"""
    print("[ 美国数据 ]")
    fake = Faker("en_US")
    data = load_json(OUTPUT_DIR / "usData.json")
    
    # 为每个州补充更多城市和邮编
    for state_code, state_name in list(US_STATES.items())[:15]:  # 前15个州
        if state_code not in data:
            data[state_code] = {"state": state_name, "cities": []}
        
        # 补充城市数量到 10-15 个
        existing_cities = set(data[state_code].get("cities", []))
        while len(existing_cities) < random.randint(12, 18):
            city = fake.city().split()[0]  # 取第一个词作为城市名
            if city not in existing_cities:
                existing_cities.add(city)
        
        data[state_code]["cities"] = sorted(list(existing_cities))
        # 补充邮编范围
        data[state_code]["zip_prefix"] = f"{random.randint(10, 99)}{random.randint(100, 999)}"
    
    save_json(OUTPUT_DIR / "usData.json", data)

def enhance_cn_data():
    """扩展中国数据"""
    print("[ 中国数据 ]")
    fake = Faker("zh_CN")
    data = load_json(OUTPUT_DIR / "cnData.json")
    
    # 为每个省份补充更多城市
    for province_code, province_name in list(CN_PROVINCES.items())[:15]:
        if province_code not in data:
            data[province_code] = {"province": province_name, "cities": []}
        
        existing_cities = set(data[province_code].get("cities", []))
        while len(existing_cities) < random.randint(15, 25):
            city = fake.city()
            if city not in existing_cities and len(city) < 10:
                existing_cities.add(city)
        
        data[province_code]["cities"] = sorted(list(existing_cities))
    
    save_json(OUTPUT_DIR / "cnData.json", data)

def enhance_jp_data():
    """扩展日本数据"""
    print("[ 日本数据 ]")
    fake = Faker("ja_JP")
    data = load_json(OUTPUT_DIR / "jpData.json")
    
    prefectures = ["東京", "大阪", "神奈川", "京都", "埼玉", "千葉", "兵庫", "北海道", 
                   "福岡", "愛知", "静岡", "広島", "岡山", "福島", "新潟"]
    
    for pref in prefectures:
        if pref not in data:
            data[pref] = {"prefecture": pref, "cities": []}
        
        existing_cities = set(data[pref].get("cities", []))
        while len(existing_cities) < random.randint(8, 12):
            city = fake.city()
            if city not in existing_cities:
                existing_cities.add(city)
        
        data[pref]["cities"] = sorted(list(existing_cities))
    
    save_json(OUTPUT_DIR / "jpData.json", data)

def enhance_other_countries():
    """增强其他国家数据"""
    countries = [
        ("GB", "en_GB", ["England", "Scotland", "Wales", "Northern Ireland"]),
        ("CA", "en_CA", ["Ontario", "Quebec", "British Columbia", "Alberta"]),
        ("DE", "de_DE", ["Bavaria", "North Rhine-Westphalia", "Baden-Württemberg", "Hesse"]),
        ("IN", "en_IN", ["Maharashtra", "Uttar Pradesh", "West Bengal", "Karnataka"]),
        ("SG", "en_US", ["Singapore"]),
    ]
    
    for country_code, locale, regions in countries:
        print(f"[ {country_code} 数据 ]")
        fake = Faker(locale)
        filename = f"{country_code.lower()}Data.json"
        data = load_json(OUTPUT_DIR / filename)
        
        for region in regions:
            if region not in data:
                data[region] = {"region": region, "cities": []}
            
            existing_cities = set(data[region].get("cities", []))
            while len(existing_cities) < random.randint(8, 15):
                city = fake.city()
                city = city.split()[0]  # 取第一个词
                if city not in existing_cities:
                    existing_cities.add(city)
            
            data[region]["cities"] = sorted(list(existing_cities))
        
        save_json(OUTPUT_DIR / filename, data)

def enhance_names_data():
    """扩展名字数据"""
    print("[ 通用名字数据 ]")
    
    fakes = {
        "en": Faker("en_US"),
        "zh": Faker("zh_CN"),
        "ja": Faker("ja_JP"),
        "de": Faker("de_DE"),
    }
    
    data = load_json(OUTPUT_DIR / "namesData.json")
    
    # 扩展男名
    for _ in range(20):
        for locale_key, fake in fakes.items():
            name = fake.first_name_male()
            if name not in data.get("firstName_male", []):
                data.setdefault("firstName_male", []).append(name)
    
    # 扩展女名
    for _ in range(20):
        for locale_key, fake in fakes.items():
            name = fake.first_name_female()
            if name not in data.get("firstName_female", []):
                data.setdefault("firstName_female", []).append(name)
    
    # 扩展姓氏
    for _ in range(20):
        for locale_key, fake in fakes.items():
            name = fake.last_name()
            if name not in data.get("lastName", []):
                data.setdefault("lastName", []).append(name)
    
    # 确保有足够数量
    while len(data.get("firstName_male", [])) < 80:
        data.setdefault("firstName_male", []).append(fakes["en"].first_name_male())
    while len(data.get("firstName_female", [])) < 80:
        data.setdefault("firstName_female", []).append(fakes["en"].first_name_female())
    while len(data.get("lastName", [])) < 100:
        data.setdefault("lastName", []).append(fakes["en"].last_name())
    
    # 去重
    data["firstName_male"] = list(set(data["firstName_male"]))
    data["firstName_female"] = list(set(data["firstName_female"]))
    data["lastName"] = list(set(data["lastName"]))
    
    save_json(OUTPUT_DIR / "namesData.json", data)

def enhance_mac_oui_data():
    """扩展 MAC OUI 数据"""
    print("[ MAC OUI 数据 ]")
    
    data = load_json(OUTPUT_DIR / "macOuiData.json")
    if not isinstance(data, list):
        data = []
    
    # 常见厂商补充
    vendors = [
        "Broadcom", "Realtek", "Qualcomm", "MediaTek", "Marvell", "Atheros",
        "Intel", "AMD", "NVIDIA", "Samsung", "Sony", "LG", "Philips", "Sharp",
        "Panasonic", "Toshiba", "Hitachi", "NEC", "Fujitsu", "Siemens",
        "Ericsson", "Nokia", "Motorola", "Huawei", "ZTE", "Xiaomi", "OPPO",
        "Vivo", "OnePlus", "Google", "Amazon", "Meta", "Apple", "Microsoft"
    ]
    
    existing_ouids = {item.get("oui") for item in data}
    
    for i, vendor in enumerate(vendors):
        oui = f"{i:02x}:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}"
        if oui not in existing_ouids:
            data.append({"oui": oui, "vendor": vendor})
            existing_ouids.add(oui)
    
    save_json(OUTPUT_DIR / "macOuiData.json", data)

def generate_all():
    """生成所有增强数据"""
    print("\n🚀 开始增强地址数据...\n")
    
    try:
        enhance_us_data()
        enhance_cn_data()
        enhance_jp_data()
        enhance_other_countries()
        enhance_names_data()
        enhance_mac_oui_data()
        
        print("\n✅ 完成！所有数据已增强\n")
        print("统计信息:")
        
        # 统计各文件
        for json_file in sorted(OUTPUT_DIR.glob("*.json")):
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    size = len(data)
                elif isinstance(data, list):
                    size = len(data)
                else:
                    size = 0
                file_size_kb = json_file.stat().st_size / 1024
                print(f"  📄 {json_file.name:20} - {size:4} 条目 ({file_size_kb:6.1f} KB)")
    
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    generate_all()
