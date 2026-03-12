#!/usr/bin/env python3
"""
模块化数据爬虫系统 - 快速补充不同类型的数据
可独立运行各个爬虫模块
"""

import json
import requests
from pathlib import Path
import time
from typing import Dict, List

OUTPUT_DIR = Path(__file__).parent.absolute()

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

class CityDataScraper:
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
    
    def save_json(self, filename: str, data):
        filepath = OUTPUT_DIR / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        size = filepath.stat().st_size / 1024
        print(f"✓ {filename:20} ({size:6.1f} KB)")
    
    def load_json(self, filename: str):
        filepath = OUTPUT_DIR / filename
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    # ============ 子模块 1: 世界大城市坐标 ============
    
    def scrape_world_major_cities(self):
        """爬取世界主要城市的坐标和人口数据"""
        print("\n[ 世界主要城市 ]")
        
        # 从 REST Countries API 获取国家数据
        try:
            url = "https://restcountries.com/v3.1/all"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            countries = response.json()
            
            major_cities = {}
            for country in countries:
                country_name = country.get("name", {}).get("common", "")
                if country_name:
                    major_cities[country_name] = {
                        "capital": country.get("capital", [""])[0],
                        "region": country.get("region", ""),
                        "population": country.get("population", 0)
                    }
            
            print(f"  ✓ 获得 {len(major_cities)} 个国家数据")
            self.save_json("worldCountriesData.json", major_cities)
            return True
        
        except Exception as e:
            print(f"  ✗ 错误: {e}")
            return False
    
    # ============ 子模块 2: 邮编数据 ============
    
    def scrape_us_zip_codes(self):
        """爬取美国邮编数据"""
        print("\n[ 美国邮编数据 ]")
        
        try:
            # Zippopotamus 免费 ZIP 码 API
            url = "https://www.zippopotam.us/us/{state}/{city}"
            
            existing = self.load_json("usData.json")
            
            # 为几个州示范
            states = ["CA", "TX", "NY", "FL"]
            
            zip_data = {}
            for state in states:
                # 这个 API 限制较多，仅示范
                print(f"  获取 {state} 数据...")
                
                # 由于 API 限制，这里用静态映射替代
                zip_data[state] = {
                    "state": state,
                    "zip_ranges": {
                        "CA": "90001-96199",
                        "TX": "73301-88999",
                        "NY": "10001-14999",
                        "FL": "32004-34999"
                    }.get(state, "")
                }
                time.sleep(0.5)
            
            print(f"  ✓ 获得 {len(zip_data)} 个州的邮编范围")
            self.save_json("usZipCodesData.json", zip_data)
            return True
        
        except Exception as e:
            print(f"  ✗ 错误: {e}")
            return False
    
    # ============ 子模块 3: 企业/机构数据 ============
    
    def scrape_company_names(self):
        """生成常见公司名称数据（作为备选地址内容）"""
        print("\n[ 公司/机构名称 ]")
        
        companies = {
            "tech": [
                "Google", "Microsoft", "Apple", "Amazon", "Meta", 
                "Tesla", "Intel", "Nvidia", "Oracle", "Adobe",
                "Alibaba", "Tencent", "Baidu", "ByteDance", "Xiaomi"
            ],
            "finance": [
                "Goldman Sachs", "JP Morgan", "Bank of America", "Wells Fargo",
                "ICBC", "Agricultural Bank", "Bank of China", "China Construction Bank"
            ],
            "energy": [
                "ExxonMobil", "Shell", "Chevron", "BP",
                "PetroChina", "Sinopec", "State Grid", "Saudi Aramco"
            ],
            "manufacturing": [
                "Boeing", "Airbus", "Toyota", "Volkswagen", "BMW",
                "Shanghai Auto", "Geely", "BYD", "SAIC"
            ]
        }
        
        self.save_json("companiesData.json", companies)
        print(f"  ✓ 添加 {sum(len(v) for v in companies.values())} 个公司")
        return True
    
    # ============ 子模块 4: 地理坐标数据 ============
    
    def scrape_geographic_coordinates(self):
        """添加地理坐标数据"""
        print("\n[ 地理坐标 ]")
        
        # 来自已知的坐标数据
        cities_coords = {
            "Beijing": {"lat": 39.9042, "lng": 116.4074},
            "Shanghai": {"lat": 31.2304, "lng": 121.4737},
            "Guangzhou": {"lat": 23.1291, "lng": 113.2644},
            "New York": {"lat": 40.7128, "lng": -74.0060},
            "London": {"lat": 51.5074, "lng": -0.1278},
            "Paris": {"lat": 48.8566, "lng": 2.3522},
            "Tokyo": {"lat": 35.6762, "lng": 139.6503},
            "Sydney": {"lat": -33.8688, "lng": 151.2093},
            "Toronto": {"lat": 43.6629, "lng": -79.3957},
            "Mumbai": {"lat": 19.0760, "lng": 72.8777},
            "Singapore": {"lat": 1.3521, "lng": 103.8198},
            "Hong Kong": {"lat": 22.3193, "lng": 114.1694},
            "Bangkok": {"lat": 13.7563, "lng": 100.5018},
            "Seoul": {"lat": 37.5665, "lng": 126.9780},
            "Berlin": {"lat": 52.5200, "lng": 13.4050},
            "Dubai": {"lat": 25.2048, "lng": 55.2708},
        }
        
        self.save_json("citiesCoordinatesData.json", cities_coords)
        print(f"  ✓ 添加 {len(cities_coords)} 个城市坐标")
        return True
    
    # ============ 子模块 5: 街道类型数据 ============
    
    def create_street_types(self):
        """创建街道类型数据（用于地址生成）"""
        print("\n[ 街道类型 ]")
        
        street_types = {
            "en": [
                "Street", "Avenue", "Boulevard", "Road", "Drive", "Lane",
                "Court", "Circle", "Park", "Place", "Square", "Terrace",
                "Trail", "Tower", "View", "Way", "Broadway", "Walk"
            ],
            "zh": [
                "路", "街", "道", "巷", "里", "弄", "号",
                "北路", "南路", "东路", "西路", "中路", "新路"
            ],
            "ja": [
                "通り", "道", "街", "路", "線", "丁目", "番地",
                "北通", "南通", "東通", "西通"
            ]
        }
        
        self.save_json("streetTypesData.json", street_types)
        print(f"  ✓ 添加 {sum(len(v) for v in street_types.values())} 个街道类型")
        return True
    
    # ============ 执行 ============
    
    def run_all(self):
        """运行所有爬虫"""
        print("\n" + "="*60)
        print("🚀 模块化数据爬虫系统")
        print("="*60)
        
        modules = [
            ("世界国家数据", self.scrape_world_major_cities),
            ("美国邮编范围", self.scrape_us_zip_codes),
            ("公司机构名称", self.scrape_company_names),
            ("城市地理坐标", self.scrape_geographic_coordinates),
            ("街道类型库", self.create_street_types),
        ]
        
        results = {}
        for name, func in modules:
            try:
                result = func()
                results[name] = "✓ 成功" if result else "✗ 失败"
            except Exception as e:
                results[name] = f"✗ {e}"
            time.sleep(1)
        
        # 总结
        print("\n" + "="*60)
        print("📊 执行结果：\n")
        for name, result in results.items():
            print(f"  {name:15} {result}")
        
        print("\n" + "="*60)
        print("\n✅ 爬虫执行完成！\n")
        
        # 列出所有新文件
        print("新增/更新的数据文件：")
        new_files = ["worldCountriesData.json", "usZipCodesData.json", 
                    "companiesData.json", "citiesCoordinatesData.json", 
                    "streetTypesData.json"]
        
        for f in new_files:
            filepath = OUTPUT_DIR / f
            if filepath.exists():
                size = filepath.stat().st_size / 1024
                print(f"  📄 {f:30} ({size:6.1f} KB)")

if __name__ == "__main__":
    scraper = CityDataScraper()
    scraper.run_all()
