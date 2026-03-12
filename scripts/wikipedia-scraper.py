#!/usr/bin/env python3
"""
从 Wikipedia 和其他开源 API 爬取城市、地区数据
更稳定、更详细的数据补充方案
"""

import json
import requests
from pathlib import Path
import time
from typing import Dict, List
import re

OUTPUT_DIR = Path(__file__).parent.absolute()

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

class WikipediaScraper:
    """Wikipedia 爬虫"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
    
    def save_json(self, filename: str, data):
        filepath = OUTPUT_DIR / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  ✓ {filename}")
    
    def load_json(self, filename: str):
        filepath = OUTPUT_DIR / filename
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def fetch_wikipedia_list(self, page_title: str) -> List[str]:
        """从 Wikipedia 的列表页爬取数据"""
        url = "https://en.wikipedia.org/w/api.php"
        
        params = {
            "action": "query",
            "titles": page_title,
            "prop": "extracts",
            "explaintext": True,
            "format": "json"
        }
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if "query" in data and "pages" in data["query"]:
                page = list(data["query"]["pages"].values())[0]
                if "extract" in page:
                    text = page["extract"]
                    # 简单的正则提取（可能不完美，但足够用）
                    lines = text.split('\n')
                    cities = [line.strip() for line in lines 
                             if line.strip() and len(line.strip()) < 50
                             and not line.startswith('=')]
                    return cities[:100]
            
            return []
        except Exception as e:
            print(f"    ✗ {e}")
            return []
    
    def fetch_us_states_cities(self):
        """爬取美国各州城市列表"""
        print("\n[ 美国城市数据增强 ]")
        
        existing = self.load_json("usData.json")
        
        # Wikipedia "List of cities in [State]" 页面列表
        pages = [
            ("List of cities in California", "CA"),
            ("List of cities in Texas", "TX"),
            ("List of cities in Florida", "FL"),
            ("List of cities in New York", "NY"),
            ("List of cities in Pennsylvania", "PA"),
        ]
        
        for page_title, state_code in pages:
            print(f"  {state_code}: {page_title}...")
            cities = self.fetch_wikipedia_list(page_title)
            
            if state_code in existing and cities:
                # 补充城市
                existing_cities = set(existing[state_code].get("cities", []))
                new_cities = [c for c in cities if c not in existing_cities]
                existing[state_code]["cities"].extend(new_cities[:10])
                print(f"    ✓ 添加 {len(new_cities[:10])} 个城市")
            
            time.sleep(1)
        
        self.save_json("usData.json", existing)
    
    def fetch_china_cities(self):
        """爬取中国城市数据（英文 Wikipedia）"""
        print("\n[ 中国城市数据增强 ]")
        
        existing = self.load_json("cnData.json")
        
        pages = [
            ("List of cities in China", None),
        ]
        
        for page_title, _ in pages:
            print(f"  爬取: {page_title}...")
            cities = self.fetch_wikipedia_list(page_title)
            
            if cities:
                # 把所有城市按首字母分组到 "Major" 类别
                if "Major" not in existing:
                    existing["Major"] = {
                        "province": "Major Cities",
                        "cities": []
                    }
                
                new_cities = [c for c in cities if c not in existing["Major"]["cities"]]
                existing["Major"]["cities"].extend(new_cities[:30])
                print(f"    ✓ 添加 {len(new_cities[:30])} 个主要城市")
            
            time.sleep(1)
        
        self.save_json("cnData.json", existing)
    
    def fetch_jp_cities(self):
        """爬取日本城市数据"""
        print("\n[ 日本城市数据增强 ]")
        
        existing = self.load_json("jpData.json")
        
        # 日本各都道府县的主要城市
        major_cities_jp = {
            "東京": ["Tokyo", "Shinjuku", "Shibuya", "Chiyoda", "Minato"],
            "大阪": ["Osaka", "Kobe", "Kyoto", "Sakai"],
            "神奈川": ["Yokohama", "Kawasaki", "Sagamihara"],
            "埼玉": ["Saitama", "Kawagoe", "Omiya"],
            "千葉": ["Chiba", "Funabashi", "Matsudo"],
        }
        
        for prefecture, cities in major_cities_jp.items():
            if prefecture in existing:
                new_cities = [c for c in cities if c not in existing[prefecture]["cities"]]
                existing[prefecture]["cities"].extend(new_cities)
                print(f"  {prefecture}: 添加 {len(new_cities)} 个城市")
        
        self.save_json("jpData.json", existing)
    
    def fetch_uk_cities(self):
        """爬取英国城市数据"""
        print("\n[ 英国城市数据增强 ]")
        
        existing = self.load_json("gbData.json")
        
        pages = [
            ("List of cities in the United Kingdom", None),
            ("List of cities in England", "England"),
        ]
        
        for page_title, region in pages:
            print(f"  {page_title}...")
            cities = self.fetch_wikipedia_list(page_title)
            
            if cities and "England" in existing:
                new_cities = [c for c in cities if c not in existing["England"]["cities"]]
                existing["England"]["cities"].extend(new_cities[:20])
                print(f"    ✓ 添加 {len(new_cities[:20])} 个城市")
            
            time.sleep(1)
        
        self.save_json("gbData.json", existing)
    
    def fetch_india_cities(self):
        """爬取印度城市数据"""
        print("\n[ 印度城市数据增强 ]")
        
        existing = self.load_json("inData.json")
        
        pages = [
            ("List of cities in India", None),
        ]
        
        for page_title, _ in pages:
            print(f"  {page_title}...")
            cities = self.fetch_wikipedia_list(page_title)
            
            if cities and len(existing) > 0:
                # 添加到第一个邦
                first_state = list(existing.keys())[0]
                new_cities = [c for c in cities if c not in existing[first_state]["cities"]]
                existing[first_state]["cities"].extend(new_cities[:30])
                print(f"    ✓ 添加 {len(new_cities[:30])} 个城市")
            
            time.sleep(1)
        
        self.save_json("inData.json", existing)
    
    def enrich_all(self):
        """执行所有增强操作"""
        print("\n🚀 从 Wikipedia 爬取补充数据...\n")
        
        try:
            self.fetch_us_states_cities()
            time.sleep(2)
            
            self.fetch_china_cities()
            time.sleep(2)
            
            self.fetch_jp_cities()
            time.sleep(2)
            
            self.fetch_uk_cities()
            time.sleep(2)
            
            self.fetch_india_cities()
            
            print("\n" + "=" * 50)
            print("✅ 数据增强完成！\n")
            
            # 显示更新后的统计
            print("更新后的数据：")
            for f in sorted(OUTPUT_DIR.glob("*Data.json")):
                with open(f, 'r', encoding='utf-8') as fp:
                    data = json.load(fp)
                    if isinstance(data, dict):
                        total_items = sum(len(v.get("cities", [])) if isinstance(v, dict) else 0 
                                         for v in data.values())
                    elif isinstance(data, list):
                        total_items = len(data)
                    else:
                        total_items = 0
                    
                    file_size_kb = f.stat().st_size / 1024
                    print(f"  📄 {f.name:20} - {total_items:4} 条目 ({file_size_kb:6.1f} KB)")
        
        except KeyboardInterrupt:
            print("\n⚠ 操作已取消")
        except Exception as e:
            print(f"\n❌ 错误: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    scraper = WikipediaScraper()
    scraper.enrich_all()
