#!/usr/bin/env python3
"""
Residential Proxy 爬虫 - 安全版本
使用配置管理敏感信息

使用方式：
  1. 复制 .env.example → .env
  2. 在 .env 中填入你的代理凭证
  3. python scripts/scrape-with-proxy.py
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
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}


class ResidentialProxyScraper:
    """支持 Residential Proxy 的完整爬虫"""
    
    def __init__(self, use_proxy: bool = True):
        """
        初始化爬虫
        
        Args:
            use_proxy: 是否启用代理（默认 True）
        """
        self.config = get_config()
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        
        if use_proxy and self.config.use_proxy():
            proxy_config = self.config.get_proxy_config()
            self.session.proxies.update(proxy_config)
            print("✓ Residential Proxy 已启用")
            print(f"  代理服务器: {self.config.get_proxy_url().split('@')[1]}")
        else:
            print("⚠ 未使用代理（直接连接）")
    
    def save_json(self, filename: str, data, print_size: bool = True):
        """保存 JSON 文件"""
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        filepath = OUTPUT_DIR / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        if print_size:
            size = filepath.stat().st_size / 1024
            print(f"  ✓ {filename:35} {size:7.1f} KB")
    
    def load_json(self, filename: str):
        """读取 JSON 文件"""
        filepath = OUTPUT_DIR / filename
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def fetch_with_retry(self, url: str, max_retries: int = 3, timeout: int = 15) -> Optional[str]:
        """
        带重试的 HTTP 请求
        
        Args:
            url: 请求 URL
            max_retries: 最大重试次数
            timeout: 超时时间
            
        Returns:
            响应文本或 None
        """
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=timeout)
                if response.status_code == 200:
                    return response.text
                print(f"  ⚠ HTTP {response.status_code}")
            except requests.exceptions.ProxyError:
                delay = 2 ** attempt
                print(f"  ↻ 代理错误，{delay}s 后重试 ({attempt + 1}/{max_retries})")
                time.sleep(delay)
            except requests.exceptions.Timeout:
                print(f"  ↻ 连接超时，重试... ({attempt + 1}/{max_retries})")
            except requests.exceptions.RequestException as e:
                print(f"  ⚠ 请求错误: {type(e).__name__}")
            
            time.sleep(random.uniform(0.5, 2))
        
        return None
    
    def scrape_us_major_cities(self):
        """爬取美国主要城市"""
        print("\n[ 美国城市数据 ]")
        
        existing = self.load_json('usData.json')
        
        states = [
            ("California", "CA"), ("Texas", "TX"), ("Florida", "FL"),
            ("New York", "NY"), ("Pennsylvania", "PA"), ("Illinois", "IL"),
        ]
        
        count = 0
        for state_name, state_code in states:
            if len(existing.get(state_code, {}).get('cities', [])) < 15:
                url = f"https://en.wikipedia.org/wiki/List_of_cities_in_{state_name}"
                
                html = self.fetch_with_retry(url)
                if html:
                    import re
                    cities = re.findall(r'>([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)<', html)
                    cities = list(set(cities))[:20]
                    
                    if state_code not in existing:
                        existing[state_code] = {'state': state_name, 'cities': []}
                    
                    new = [c for c in cities if c not in existing[state_code]['cities']]
                    existing[state_code]['cities'].extend(new[:15])
                    
                    print(f"  {state_code}: 添加 {len(new[:15])} 个城市")
                    count += len(new[:15])
                else:
                    print(f"  {state_code}: 请求失败")
                
                time.sleep(random.uniform(1, 3))
        
        self.save_json('usData.json', existing)
        print(f"\n  总计添加: {count} 个城市")
    
    def run_all(self):
        """运行所有爬虫"""
        print("\n" + "="*70)
        print("🕷️  Residential Proxy 爬虫 (安全版本)")
        print("="*70)
        
        try:
            self.scrape_us_major_cities()
            
            print("\n" + "="*70)
            print("✅ 爬虫执行完成！")
            print("="*70)
        
        except KeyboardInterrupt:
            print("\n⚠ 爬虫已暂停（可重新运行）")
        except Exception as e:
            print(f"\n❌ 错误: {e}")
            import traceback
            traceback.print_exc()


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Residential Proxy 爬虫')
    parser.add_argument('--no-proxy', action='store_true', help='禁用代理，直接连接')
    parser.add_argument('--dry-run', action='store_true', help='测试模式（不保存文件）')
    args = parser.parse_args()
    
    # 检查配置
    config = get_config()
    if not config.use_proxy() and not args.no_proxy:
        print("⚠ 警告: 代理未配置")
        print("   请复制 .env.example 到 .env 并填入代理凭证")
        print("   或使用 --no-proxy 选项禁用代理")
        return
    
    # 运行爬虫
    scraper = ResidentialProxyScraper(use_proxy=not args.no_proxy)
    scraper.run_all()


if __name__ == '__main__':
    main()
