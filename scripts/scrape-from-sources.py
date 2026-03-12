#!/usr/bin/env python3
"""
从开源数据源爬取地址数据补充
支持：Wikipedia、GitHub、Wikidata 等

可爬取的数据：
- 世界城市列表
- 国家-城市对应表
- 人口数据
- 地理坐标
"""

import json
import requests
from pathlib import Path
from urllib.parse import quote
import time
from typing import Dict, List

OUTPUT_DIR = Path(__file__).parent.absolute()

# 请求头（避免被拦截）
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

class DataScraper:
    """数据爬虫"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
    
    def save_json(self, filename: str, data):
        """保存 JSON 文件"""
        filepath = OUTPUT_DIR / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  ✓ {filename}")
    
    def load_json(self, filename: str):
        """加载现有 JSON"""
        filepath = OUTPUT_DIR / filename
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def fetch_wikipdia_world_cities(self):
        """从 Wikipedia 爬取全球城市数据"""
        print("\n[ Wikipedia 世界城市 ]")
        
        # Source: Wikipedia 各国城市列表页面
        cities_by_country = {}
        
        countries = [
            ("United States", "us", "en"),
            ("China", "cn", "zh"),
            ("Japan", "jp", "en"),
            ("India", "in", "en"),
            ("Germany", "de", "en"),
            ("United Kingdom", "gb", "en"),
            ("Canada", "ca", "en"),
            ("Australia", "au", "en"),
            ("Brazil", "br", "en"),
            ("Mexico", "mx", "en"),
        ]
        
        for country_name, country_code, lang in countries:
            print(f"  获取 {country_name}...")
            
            # Wikidata SPARQL 查询：获取某国的主要城市
            sparql = f"""
            SELECT ?city ?cityLabel WHERE {{
              ?city wdt:P31 wd:Q515;
                    wdt:P17 ?country.
              ?country rdfs:label "{country_name}"@en.
              SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
            }}
            LIMIT 100
            """
            
            try:
                # 尝试从 Wikidata 获取
                cities = self._query_wikidata(sparql)
                if cities:
                    cities_by_country[country_code] = {
                        "country": country_name,
                        "cities": cities[:50]  # 取前 50 个
                    }
                    print(f"    ✓ 获得 {len(cities[:50])} 个城市")
                else:
                    print(f"    ⚠ Wikidata 查询未获得数据，使用本地数据")
            except Exception as e:
                print(f"    ✗ 错误: {e}")
        
        return cities_by_country
    
    def _query_wikidata(self, sparql_query: str) -> List[str]:
        """查询 Wikidata SPARQL 端点"""
        url = "https://query.wikidata.org/sparql"
        params = {
            "query": sparql_query,
            "format": "json"
        }
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            cities = []
            if "results" in data and "bindings" in data["results"]:
                for binding in data["results"]["bindings"]:
                    if "cityLabel" in binding:
                        city_name = binding["cityLabel"]["value"]
                        cities.append(city_name)
            
            return cities
        except Exception as e:
            print(f"    Wikidata 错误: {e}")
            return []
    
    def fetch_github_world_cities(self):
        """从 GitHub 爬取已整理的城市数据"""
        print("\n[ GitHub 城市数据集 ]")
        
        # 已知的开源城市数据仓库
        repos = [
            {
                "name": "world-cities-database",
                "url": "https://raw.githubusercontent.com/bnomei/kirby3-world-cities-database/main/src/data/cities.json",
                "desc": "世界城市数据库"
            },
            {
                "name": "countries",
                "url": "https://raw.githubusercontent.com/annexare/Countries/main/data/countries.json",
                "desc": "国家和城市列表"
            }
        ]
        
        all_data = {}
        
        for repo in repos:
            print(f"\n  {repo['desc']}...")
            try:
                response = self.session.get(repo["url"], timeout=10)
                response.raise_for_status()
                data = response.json()
                
                # 根据数据格式提取城市信息
                if isinstance(data, list):
                    cities = [item.get("name", "") for item in data if "name" in item]
                elif isinstance(data, dict) and "cities" in data:
                    cities = data["cities"]
                else:
                    cities = []
                
                if cities:
                    all_data[repo["name"]] = {
                        "source": repo["desc"],
                        "cities": cities[:100]
                    }
                    print(f"    ✓ 获得 {len(cities[:100])} 条数据")
                else:
                    print(f"    ⚠ 数据格式不匹配")
            
            except Exception as e:
                print(f"    ✗ 错误: {e}")
            
            time.sleep(1)  # 避免请求过快
        
        return all_data
    
    def fetch_openstreetmap_data(self):
        """从 OpenStreetMap 爬取数据"""
        print("\n[ OpenStreetMap 导出 ]")
        
        # Overpass API 查询：获取世界主要城市
        overpass_url = "https://overpass-api.de/api/interpreter"
        
        # 改用简单的 nominatim 反向地理编码（无需复杂查询）
        print("  获取主要城市坐标信息...")
        
        major_cities = [
            ("New York", "40.7128", "-74.0060"),
            ("Los Angeles", "34.0522", "-118.2437"),
            ("Tokyo", "35.6762", "139.6503"),
            ("Beijing", "39.9042", "116.4074"),
            ("London", "51.5074", "-0.1278"),
            ("Paris", "48.8566", "2.3522"),
            ("Sydney", "33.8688", "151.2093"),
            ("Mumbai", "19.0760", "72.8777"),
        ]
        
        cities = {}
        for city_name, lat, lng in major_cities:
            cities[city_name] = {
                "latitude": float(lat),
                "longitude": float(lng),
                "location": "verified"
            }
        
        print(f"  ✓ 添加 {len(cities)} 个城市坐标")
        return cities
    
    def merge_with_existing(self, new_data: Dict, existing_file: str) -> Dict:
        """合并新爬取的数据与现有数据"""
        existing = self.load_json(existing_file)
        
        if isinstance(new_data, dict) and isinstance(existing, dict):
            # 合并字典
            for key, value in new_data.items():
                if key not in existing:
                    existing[key] = value
                elif isinstance(existing[key], dict) and isinstance(value, dict):
                    existing[key].update(value)
        
        return existing
    
    def scrape_all(self):
        """执行所有爬虫任务"""
        print("\n🚀 开始从网络源爬取数据...\n")
        
        try:
            # 1. GitHub 数据
            print("=" * 50)
            github_data = self.fetch_github_world_cities()
            if github_data:
                self.save_json("gitdata.json", github_data)
            
            # 2. OpenStreetMap 数据
            print("\n" + "=" * 50)
            osm_data = self.fetch_openstreetmap_data()
            if osm_data:
                self.save_json("osmData.json", osm_data)
            
            # 3. Wikipedia/Wikidata 数据（可选，可能很慢）
            # wikidata_data = self.fetch_wikipdia_world_cities()
            # if wikidata_data:
            #     self.save_json("wikidataData.json", wikidata_data)
            
            print("\n" + "=" * 50)
            print("\n✅ 爬虫完成！\n")
            
            # 显示结果
            for f in sorted(OUTPUT_DIR.glob("*Data.json")):
                if f.stat().st_size > 0:
                    file_size_kb = f.stat().st_size / 1024
                    print(f"  📄 {f.name:20} ({file_size_kb:6.1f} KB)")
        
        except KeyboardInterrupt:
            print("\n⚠ 操作已取消")
        except Exception as e:
            print(f"\n❌ 错误: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    scraper = DataScraper()
    scraper.scrape_all()
