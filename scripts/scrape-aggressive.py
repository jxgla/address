#!/usr/bin/env python3
"""
激进数据爬虫 - 通过 Residential Proxy 大量爬取数据
支持暂停和恢复

配置管理版本：敏感信息通过 .env 文件管理
"""

import json
import requests
from pathlib import Path
import time
import random
from typing import Dict, List
import sys

# 导入配置管理
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import get_config

OUTPUT_DIR = Path(__file__).parent.parent / 'data'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

class AggressiveScraper:
    
    def __init__(self):
        self.config = get_config()
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        
        if self.config.use_proxy():
            proxy_config = self.config.get_proxy_config()
            self.session.proxies.update(proxy_config)
            print("✓ Residential Proxy 已启用")
        else:
            print("⚠ 未使用代理")

    
    def save_json(self, filename: str, data):
        filepath = OUTPUT_DIR / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        size = filepath.stat().st_size / 1024
        print(f"  ✓ {filename:35} {size:7.1f} KB")
    
    def load_json(self, filename: str):
        filepath = OUTPUT_DIR / filename
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def aggressive_us_scrape(self):
        """大量爬取美国所有州的城市"""
        print("\n[ 美国所有州城市爬虫 ]")
        
        existing = self.load_json("usData.json")
        
        # 所有 50 州
        states = [
            ("Alabama", "AL"), ("Alaska", "AK"), ("Arizona", "AZ"), ("Arkansas", "AR"),
            ("California", "CA"), ("Colorado", "CO"), ("Connecticut", "CT"), ("Delaware", "DE"),
            ("Florida", "FL"), ("Georgia", "GA"), ("Hawaii", "HI"), ("Idaho", "ID"),
            ("Illinois", "IL"), ("Indiana", "IN"), ("Iowa", "IA"), ("Kansas", "KS"),
            ("Kentucky", "KY"), ("Louisiana", "LA"), ("Maine", "ME"), ("Maryland", "MD"),
            ("Massachusetts", "MA"), ("Michigan", "MI"), ("Minnesota", "MN"), ("Mississippi", "MS"),
            ("Missouri", "MO"), ("Montana", "MT"), ("Nebraska", "NE"), ("Nevada", "NV"),
            ("New Hampshire", "NH"), ("New Jersey", "NJ"), ("New Mexico", "NM"), ("New York", "NY"),
            ("North Carolina", "NC"), ("North Dakota", "ND"), ("Ohio", "OH"), ("Oklahoma", "OK"),
            ("Oregon", "OR"), ("Pennsylvania", "PA"), ("Rhode Island", "RI"), ("South Carolina", "SC"),
            ("South Dakota", "SD"), ("Tennessee", "TN"), ("Texas", "TX"), ("Utah", "UT"),
            ("Vermont", "VT"), ("Virginia", "VA"), ("Washington", "WA"), ("West Virginia", "WV"),
            ("Wisconsin", "WI"), ("Wyoming", "WY")
        ]
        
        count = 0
        for state_name, state_code in states:
            if state_code not in existing:
                existing[state_code] = {"state": state_name, "cities": []}
            
            # 只爬取还没有数据的州
            if len(existing[state_code]["cities"]) < 10:
                url = f"https://en.wikipedia.org/wiki/List_of_cities_in_{state_name}"
                
                try:
                    response = self.session.get(url, timeout=10)
                    if response.status_code == 200:
                        # 简单提取
                        import re
                        cities = re.findall(r'>([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)<', response.text)
                        cities = list(set(cities))[:25]
                        
                        new_cities = [c for c in cities if c not in existing[state_code]["cities"]]
                        existing[state_code]["cities"].extend(new_cities[:20])
                        
                        print(f"  {state_code:2} ({state_name:15}): 添加 {len(new_cities[:20]):2} 个城市")
                        count += len(new_cities[:20])
                    
                except Exception as e:
                    print(f"  {state_code}: ✗ {type(e).__name__}")
                
                time.sleep(random.uniform(0.5, 2))
        
        self.save_json("usData.json", existing)
        print(f"\n  总计添加：{count} 个城市")
    
    def aggressive_china_scrape(self):
        """大量爬取中国各省城市"""
        print("\n[ 中国各省城市爬虫 ]")
        
        existing = self.load_json("cnData.json")
        
        provinces = [
            ("Anhui", "安徽"), ("Fujian", "福建"), ("Gansu", "甘肃"), ("Guangdong", "广东"),
            ("Guangxi", "广西"), ("Guizhou", "贵州"), ("Hainan", "海南"), ("Hebei", "河北"),
            ("Henan", "河南"), ("Heilongjiang", "黑龙江"), ("Hubei", "湖北"), ("Hunan", "湖南"),
            ("Inner Mongolia", "内蒙古"), ("Jiangsu", "江苏"), ("Jiangxi", "江西"), 
            ("Jilin", "吉林"), ("Liaoning", "辽宁"), ("Ningxia", "宁夏"), ("Qinghai", "青海"),
            ("Shaanxi", "陕西"), ("Shandong", "山东"), ("Shanxi", "山西"), ("Sichuan", "四川"),
            ("Tibet", "西藏"), ("Xinjiang", "新疆"), ("Yunnan", "云南"), ("Zhejiang", "浙江")
        ]
        
        count = 0
        for eng_name, cn_name in provinces:
            if cn_name not in existing:
                existing[cn_name] = {"province": cn_name, "cities": []}
            
            if len(existing[cn_name]["cities"]) < 15:
                url = f"https://en.wikipedia.org/wiki/{eng_name}#Cities"
                
                try:
                    response = self.session.get(url, timeout=10)
                    if response.status_code == 200:
                        import re
                        cities = re.findall(r'>([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)<', response.text)
                        cities = list(set(cities))[:30]
                        
                        new_cities = [c for c in cities if c not in existing[cn_name]["cities"]]
                        existing[cn_name]["cities"].extend(new_cities[:20])
                        
                        print(f"  {cn_name:6}: 添加 {len(new_cities[:20]):2} 个城市")
                        count += len(new_cities[:20])
                
                except Exception as e:
                    print(f"  {cn_name}: ✗ {type(e).__name__}")
                
                time.sleep(random.uniform(0.5, 2))
        
        self.save_json("cnData.json", existing)
        print(f"\n  总计添加：{count} 个城市")
    
    def aggressive_european_scrape(self):
        """爬取欧洲国家城市"""
        print("\n[ 欧洲城市爬虫 ]")
        
        # 各欧洲国家及对应数据文件
        countries = {
            "gbData.json": [("England", "England"), ("Scotland", "Scotland"), ("Wales", "Wales")],
            "deData.json": [("Bavaria", "Bayern"), ("North Rhine-Westphalia", "Nordrhein")],
            "frData.json": [("Île-de-France", "Île-de-France"), ("Provence", "Provence")],
        }
        
        count = 0
        for data_file, regions in countries.items():
            data = self.load_json(data_file)
            
            for region_en, region_key in regions:
                url = f"https://en.wikipedia.org/wiki/List_of_cities_in_{region_en}"
                
                try:
                    response = self.session.get(url, timeout=10)
                    if response.status_code == 200:
                        import re
                        cities = re.findall(r'>([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)<', response.text)
                        cities = list(set(cities))[:30]
                        
                        if region_en not in data:
                            data[region_en] = {"region": region_en, "cities": []}
                        
                        new_cities = [c for c in cities if c not in data[region_en]["cities"]]
                        data[region_en]["cities"].extend(new_cities[:15])
                        
                        print(f"  {region_en:30}: 添加 {len(new_cities[:15]):2} 个城市")
                        count += len(new_cities[:15])
                
                except Exception as e:
                    print(f"  {region_en}: ✗ {type(e).__name__}")
                
                time.sleep(random.uniform(0.5, 2))
            
            if data_file not in ["gbData.json"]:  # 不覆盖已有文件，新建
                self.save_json(data_file, data)
        
        print(f"\n  总计添加：{count} 个城市")
    
    def aggressive_asia_scrape(self):
        """爬取亚洲城市"""
        print("\n[ 亚洲城市爬虫 ]")
        
        countries = [
            ("Japan", "jpData.json"),
            ("South Korea", "krData.json"),
            ("Thailand", "thData.json"),
            ("Vietnam", "vnData.json"),
            ("Philippines", "phData.json"),
            ("Indonesia", "idData.json"),
            ("Malaysia", "myData.json"),
        ]
        
        count = 0
        for country_name, data_file in countries:
            url = f"https://en.wikipedia.org/wiki/List_of_cities_in_{country_name}"
            data = self.load_json(data_file)
            
            try:
                response = self.session.get(url, timeout=10)
                if response.status_code == 200:
                    import re
                    cities = re.findall(r'>([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)<', response.text)
                    cities = list(set(cities))[:50]
                    
                    key = "cities"
                    if key not in data:
                        data[key] = cities
                    else:
                        new = [c for c in cities if c not in data[key]]
                        data[key].extend(new[:30])
                    
                    print(f"  {country_name:20}: 添加 {len(cities):2} 个城市")
                    count += len(cities)
                    
                    self.save_json(data_file, data)
            
            except Exception as e:
                print(f"  {country_name}: ✗ {type(e).__name__}")
            
            time.sleep(random.uniform(0.5, 2))
        
        print(f"\n  总计添加：{count} 个城市")
    
    def run_all(self):
        """执行所有激进爬虫"""
        print("\n" + "="*70)
        print("🚀 激进数据爬虫 (Residential Proxy)")
        print("="*70)
        
        try:
            self.aggressive_us_scrape()
            time.sleep(3)
            
            self.aggressive_china_scrape()
            time.sleep(3)
            
            self.aggressive_european_scrape()
            time.sleep(3)
            
            self.aggressive_asia_scrape()
            
            print("\n" + "="*70)
            print("✅ 激进爬虫完成！\n")
            
            # 总统计
            print("最终数据统计：")
            total_size = 0
            file_count = 0
            for f in sorted(OUTPUT_DIR.glob("*.json")):
                size = f.stat().st_size / 1024
                total_size += size
                file_count += 1
            
            print(f"  📊 {file_count} 个数据文件，总计 {total_size:.1f} KB")
        
        except KeyboardInterrupt:
            print("\n⚠ 爬虫已暂停（可重新运行继续）")
        except Exception as e:
            print(f"\n❌ 错误: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='激进数据爬虫')
    parser.add_argument('--no-proxy', action='store_true', help='禁用代理，直接连接')
    args = parser.parse_args()
    
    # 验证配置
    config = get_config()
    if not args.no_proxy and not config.use_proxy():
        print("⚠ 警告: 代理未配置")
        print("   请执行以下步骤：")
        print("   1. 复制配置文件: cp .env.example .env")
        print("   2. 编辑 .env 文件，填入代理凭证")
        print("   3. 重新运行此脚本")
        print()
        print("   或使用 --no-proxy 选项禁用代理")
        sys.exit(1)
    
    scraper = AggressiveScraper()
    try:
        scraper.run_all()
    except KeyboardInterrupt:
        print("\n⚠ 操作已取消")

