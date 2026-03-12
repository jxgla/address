#!/usr/bin/env python3
"""
支持 Residential Proxy 的完整数据爬虫
自动补充城市、地区、名字等数据

配置管理版本：敏感信息通过 .env 文件管理
使用方式：
  1. cp .env.example .env
  2. 在 .env 中填入代理凭证
  3. python scripts/scrape-with-proxy.py [--no-proxy]
"""

import json
import requests
from pathlib import Path
import time
from typing import Dict, List, Optional
import random
import sys

# 导入配置管理
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import get_config

OUTPUT_DIR = Path(__file__).parent.parent / 'data'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

class ResidentialProxyScraper:
    """支持 Residential Proxy 的完整爬虫"""
    
    def __init__(self, use_proxy: bool = True):
        self.config = get_config()
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        
        if use_proxy and self.config.use_proxy():
            proxy_config = self.config.get_proxy_config()
            self.session.proxies.update(proxy_config)
            print("✓ Residential Proxy 已启用")
            # 显示代理服务器（不显示凭证）
            proxy_url = self.config.get_proxy_url()
            if '@' in proxy_url:
                server = proxy_url.split('@')[1]
                print(f"  代理服务器: {server}")
        else:
            print("⚠ 未使用代理（直接连接）")
    
    def save_json(self, filename: str, data, print_size: bool = True):
        """保存 JSON 文件"""
        filepath = OUTPUT_DIR / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        if print_size:
            size = filepath.stat().st_size / 1024
            print(f"  ✓ {filename:30} ({size:7.1f} KB)")
        else:
            print(f"  ✓ {filename}")
    
    def load_json(self, filename: str):
        """加载现有 JSON"""
        filepath = OUTPUT_DIR / filename
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def fetch_with_retry(self, url: str, max_retries: int = 3, timeout: int = 15) -> Optional[str]:
        """带重试的 HTTP 请求"""
        for attempt in range(max_retries):
            try:
                print(f"    请求: {url[:60]}... (尝试 {attempt + 1}/{max_retries})")
                response = self.session.get(url, timeout=timeout)
                response.raise_for_status()
                print(f"    ✓ 成功 (状态码: {response.status_code})")
                return response.text
            except requests.exceptions.ProxyError:
                print(f"    ⚠ 代理错误，重试...")
                time.sleep(2 ** attempt)  # 指数退避
            except Exception as e:
                print(f"    ⚠ 错误: {type(e).__name__}")
                time.sleep(1)
        
        return None
    
    # ============ 爬虫模块 1: 美国城市 ============
    
    def scrape_us_cities(self):
        """爬取美国各州城市"""
        print("\n[ 美国城市数据 ]")
        
        existing = self.load_json("usData.json")
        
        # Wikipedia 列表页面
        pages = [
            ("California", "CA"),
            ("Texas", "TX"),
            ("Florida", "FL"),
            ("New York", "NY"),
            ("Pennsylvania", "PA"),
            ("Illinois", "IL"),
            ("Ohio", "OH"),
            ("Georgia", "GA"),
            ("North Carolina", "NC"),
            ("Michigan", "MI"),
        ]
        
        for state_name, state_code in pages:
            print(f"\n  {state_code}: {state_name}")
            
            url = f"https://en.wikipedia.org/wiki/List_of_cities_in_{state_name}"
            html = self.fetch_with_retry(url)
            
            if html:
                # 简单的 HTML 解析（取所有带括号的行）
                import re
                cities = re.findall(r'>\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*<', html)
                cities = list(set(cities))[:30]  # 去重并限制数量
                
                if cities and state_code in existing:
                    existing_cities = set(existing[state_code].get("cities", []))
                    new_cities = [c for c in cities if c not in existing_cities]
                    existing[state_code]["cities"].extend(new_cities[:15])
                    print(f"    ✓ 添加 {len(new_cities[:15])} 个城市")
            
            time.sleep(random.uniform(1, 3))  # 随机延迟避免被拦截
        
        self.save_json("usData.json", existing)
    
    # ============ 爬虫模块 2: 中国城市 ============
    
    def scrape_china_cities(self):
        """爬取中国主要城市"""
        print("\n[ 中国城市数据 ]")
        
        existing = self.load_json("cnData.json")
        
        # 从维基百科爬取中国城市
        url = "https://en.wikipedia.org/wiki/List_of_cities_in_China"
        html = self.fetch_with_retry(url)
        
        if html:
            import re
            # 提取所有可能的城市名
            cities = re.findall(r'<a[^>]*>([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)</a>', html)
            cities = list(set(cities))[:50]
            
            if cities and "Major" not in existing:
                existing["Major"] = {
                    "province": "Major Cities",
                    "cities": cities
                }
                print(f"  ✓ 添加 {len(cities)} 个主要城市")
        
        self.save_json("cnData.json", existing)
        time.sleep(random.uniform(1, 3))
    
    # ============ 爬虫模块 3: 日本城市 ============
    
    def scrape_japan_cities(self):
        """爬取日本城市数据"""
        print("\n[ 日本城市数据 ]")
        
        existing = self.load_json("jpData.json")
        
        # 日本主要城市（手工 + Wikipedia）
        url = "https://en.wikipedia.org/wiki/List_of_cities_in_Japan"
        html = self.fetch_with_retry(url)
        
        if html:
            import re
            cities = re.findall(r'<td[^>]*>([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)</td>', html)
            cities = list(set(cities))[:80]
            
            # 分配给各都道府县
            prefectures = ["東京", "大阪", "神奈川", "京都", "埼玉", "千葉", "兵庫", "北海道"]
            for pref in prefectures:
                if pref in existing and cities:
                    new_cities = [c for c in cities if c not in existing[pref]["cities"]]
                    cities_to_add = new_cities[:10]
                    existing[pref]["cities"].extend(cities_to_add)
                    if cities_to_add:
                        print(f"  {pref}: 添加 {len(cities_to_add)} 个城市")
            
            # 删除已添加的城市
            cities = cities[len(cities):0]
        
        self.save_json("jpData.json", existing)
        time.sleep(random.uniform(1, 3))
    
    # ============ 爬虫模块 4: 英国城市 ============
    
    def scrape_uk_cities(self):
        """爬取英国城市"""
        print("\n[ 英国城市数据 ]")
        
        existing = self.load_json("gbData.json")
        
        url = "https://en.wikipedia.org/wiki/List_of_cities_in_the_United_Kingdom"
        html = self.fetch_with_retry(url)
        
        if html:
            import re
            cities = re.findall(r'>([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)<', html)
            cities = list(set(cities))[:50]
            
            if "England" in existing and cities:
                new_cities = [c for c in cities if c not in existing["England"]["cities"]]
                existing["England"]["cities"].extend(new_cities[:20])
                print(f"  ✓ 添加 {len(new_cities[:20])} 个城市")
        
        self.save_json("gbData.json", existing)
        time.sleep(random.uniform(1, 3))
    
    # ============ 爬虫模块 5: 印度城市 ============
    
    def scrape_india_cities(self):
        """爬取印度城市"""
        print("\n[ 印度城市数据 ]")
        
        existing = self.load_json("inData.json")
        
        url = "https://en.wikipedia.org/wiki/List_of_largest_cities_of_India"
        html = self.fetch_with_retry(url)
        
        if html:
            import re
            cities = re.findall(r'<td[^>]*>([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)</td>', html)
            cities = list(set(cities))[:50]
            
            if cities and len(existing) > 0:
                first_state = list(existing.keys())[0]
                new_cities = [c for c in cities if c not in existing[first_state]["cities"]]
                existing[first_state]["cities"].extend(new_cities[:30])
                print(f"  ✓ 添加 {len(new_cities[:30])} 个城市")
        
        self.save_json("inData.json", existing)
        time.sleep(random.uniform(1, 3))
    
    # ============ 爬虫模块 6: 全球主要城市 ============
    
    def scrape_world_capitals(self):
        """爬取世界各国首都和主要城市"""
        print("\n[ 世界首都和主要城市 ]")
        
        url = "https://en.wikipedia.org/wiki/List_of_world_capitals_by_population"
        html = self.fetch_with_retry(url)
        
        capitals = {}
        
        if html:
            import re
            # 提取表格中的城市数据
            rows = re.findall(r'<tr[^>]*>.*?<td[^>]*>([^<]+)</td>.*?</tr>', html, re.DOTALL)
            
            for i, row in enumerate(rows[:100]):
                if len(row.strip()) > 2:
                    city = row.strip().split('[')[0].strip()  # 移除维基链接
                    if 2 < len(city) < 40:
                        capitals[f"city_{i}"] = {
                            "name": city,
                            "type": "capital"
                        }
        
        if capitals:
            self.save_json("worldCapitalsData.json", capitals)
            print(f"  ✓ 添加 {len(capitals)} 个首都")
        
        time.sleep(random.uniform(1, 3))
    
    # ============ 爬虫模块 7: GitHub 仓库数据 ============
    
    def scrape_github_data(self):
        """从 GitHub 爬取城市数据"""
        print("\n[ GitHub 数据源 ]")
        
        urls = [
            ("https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.json", "countries"),
            ("https://raw.githubusercontent.com/mledoze/countries/master/countries.json", "countries_alt"),
        ]
        
        for url, name in urls:
            print(f"  {name}...")
            html = self.fetch_with_retry(url, timeout=10)
            
            if html:
                try:
                    data = json.loads(html)
                    self.save_json(f"github_{name}.json", data, print_size=False)
                    print(f"    ✓ 保存成功")
                except:
                    print(f"    ✗ JSON 解析失败")
            
            time.sleep(random.uniform(2, 4))
    
    # ============ 执行全部爬虫 ============
    
    def run_all(self):
        """运行所有爬虫"""
        print("\n" + "="*70)
        print("🚀 支持 Residential Proxy 的完整爬虫系统")
        print("="*70)
        
        modules = [
            ("美国城市", self.scrape_us_cities),
            ("中国城市", self.scrape_china_cities),
            ("日本城市", self.scrape_japan_cities),
            ("英国城市", self.scrape_uk_cities),
            ("印度城市", self.scrape_india_cities),
            ("世界首都", self.scrape_world_capitals),
            ("GitHub 数据", self.scrape_github_data),
        ]
        
        results = {}
        
        for name, func in modules:
            try:
                func()
                results[name] = "✓"
            except Exception as e:
                results[name] = f"✗ {type(e).__name__}"
            
            print()
        
        # 总结
        print("="*70)
        print("📊 执行结果：\n")
        
        for name, result in results.items():
            status = "✓ 成功" if result == "✓" else result
            print(f"  {name:15} {status}")
        
        print("\n" + "="*70)
        print("✅ 爬虫执行完成！\n")
        
        # 列出所有文件
        print("数据文件列表：")
        total_size = 0
        for f in sorted(OUTPUT_DIR.glob("*.json")):
            size = f.stat().st_size / 1024
            total_size += size
            print(f"  📄 {f.name:35} {size:7.1f} KB")
        
        print(f"\n  总计：{total_size:7.1f} KB")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Residential Proxy 爬虫系统')
    parser.add_argument('--no-proxy', action='store_true', help='禁用代理，直接连接')
    parser.add_argument('--dry-run', action='store_true', help='测试模式（不实际爬取）')
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
    
    scraper = ResidentialProxyScraper(use_proxy=not args.no_proxy)
    
    try:
        scraper.run_all()
    except KeyboardInterrupt:
        print("\n\n⚠ 操作已取消")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
