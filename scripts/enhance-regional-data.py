#!/usr/bin/env python3
"""补充 HK、TW、AU 等地区的数据"""

import json
from pathlib import Path
from faker import Faker

OUTPUT_DIR = Path(__file__).parent.absolute()

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def enhance_hk_data():
    """增强香港数据"""
    print("[ 香港数据 ]")
    fake_en = Faker("en_US")
    fake_zh = Faker("zh_CN")
    
    hk_districts = {
        "Central & Western": ["Central", "Western", "Admiralty"],
        "Wan Chai": ["Wan Chai", "Causeway Bay"],
        "East": ["Quarry Bay", "Tai Koo", "Shau Kei Wan"],
        "South": ["Aberdeen", "Repulse Bay", "Stanley"],
        "Yau Tsim Mong": ["Mong Kok", "Tsim Sha Tsui", "Yau Ma Tei"],
        "Sham Shui Po": ["Sham Shui Po", "Cheung Sha Wan"],
        "Kowloon City": ["Hung Hom", "To Kwa Wan"],
        "Wong Tai Sin": ["Wong Tai Sin", "Tseung Kwan O"],
        "Kwun Tong": ["Kwun Tong", "Lam Tin"],
        "New Territories": ["Shatin", "Tai Po", "Tuen Mun", "Yuen Long"],
    }
    
    data = {}
    for district, cities in hk_districts.items():
        data[district] = {
            "district": district,
            "cities": cities,
            "population": len(cities) * 50000
        }
    
    save_json(OUTPUT_DIR / "hkData.json", data)
    print(f"  ✓ 添加了 {len(data)} 个地区，共 {sum(len(v['cities']) for v in data.values())} 个城市")

def enhance_tw_data():
    """增强台湾数据"""
    print("[ 台湾数据 ]")
    
    tw_cities = {
        "台北": ["大安", "信义", "松山", "中山"],
        "新北": ["板桥", "中和", "永和", "新庄"],
        "台中": ["西屯", "南屯", "北屯", "东区"],
        "台南": ["中西区", "东区", "南区"],
        "高雄": ["前金", "苓雅", "新兴", "鼓山"],
        "桃园": ["中坜", "平镇", "龙潭"],
        "新竹": ["东区", "北区", "香山"],
        "苗栗": ["竹南", "头份"],
        "彰化": ["彰化", "員林"],
        "南投": ["南投", "埔里"],
        "云林": ["斗六", "虎尾"],
        "嘉义": ["嘉义", "太保"],
        "花莲": ["花莲"],
        "台东": ["台东"],
        "宜兰": ["宜兰"],
    }
    
    data = {}
    for city, districts in tw_cities.items():
        data[city] = {
            "city": city,
            "districts": districts,
            "population": len(districts) * 100000
        }
    
    save_json(OUTPUT_DIR / "twData.json", data)
    print(f"  ✓ 添加了 {len(data)} 个城市，共 {sum(len(v['districts']) for v in data.values())} 个区")

def enhance_au_data():
    """补充澳大利亚数据"""
    print("[ 澳大利亚数据 ]")
    fake = Faker("en_AU")
    
    au_states = {
        "NSW": ["Sydney", "Newcastle", "Wollongong", "Central Coast", "Canberra"],
        "VIC": ["Melbourne", "Geelong", "Ballarat", "Bendigo", "Shepparton"],
        "QLD": ["Brisbane", "Gold Coast", "Sunshine Coast", "Cairns", "Townsville"],
        "WA": ["Perth", "Fremantle", "Mandurah", "Bunbury", "Port Hedland"],
        "SA": ["Adelaide", "Gawler", "Mount Gambier", "Whyalla"],
        "TAS": ["Hobart", "Launceston", "Devonport"],
        "ACT": ["Canberra", "Queanbeyan"],
        "NT": ["Darwin", "East Arm", "Palmerston"],
    }
    
    data = {}
    for state, cities in au_states.items():
        data[state] = {
            "state": state,
            "cities": cities
        }
    
    save_json(OUTPUT_DIR / "auData.json", data)
    print(f"  ✓ 添加了 {len(data)} 个州，共 {sum(len(v['cities']) for v in data.values())} 个城市")

def generate_all():
    print("\n🚀 补充地区数据...\n")
    try:
        enhance_hk_data()
        enhance_tw_data()
        enhance_au_data()
        print("\n✅ 所有地区数据已补充！\n")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    generate_all()
