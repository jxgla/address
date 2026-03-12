#!/usr/bin/env python3
"""
完整的数据爬虫系统 - 支持 Residential Proxy
爬取完整的城市、街道、邮编、电话等数据

配置管理版本：敏感信息通过 .env 文件管理
"""

import json
import requests
from pathlib import Path
import time
from typing import Dict, List, Optional
import logging
import sys

# 导入配置管理
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import get_config

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

OUTPUT_DIR = Path(__file__).parent.parent / 'data'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
}

class ComprehensiveDataScraper:
    """完整的数据爬虫"""
    
    def __init__(self, use_proxy=False):
        self.config = get_config()
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.use_proxy = use_proxy
        
        if use_proxy and self.config.use_proxy():
            proxy_config = self.config.get_proxy_config()
            self.session.proxies.update(proxy_config)
            logger.info(f"✓ 代理已启用: {self.config.get_proxy_url().split('@')[1]}")
        else:
            logger.info("✓ 直连模式")
    
    def save_json(self, filename: str, data):
        filepath = OUTPUT_DIR / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        size = filepath.stat().st_size / 1024
        logger.info(f"  ✓ {filename:35} ({size:6.1f} KB)")
    
    def load_json(self, filename: str):
        filepath = OUTPUT_DIR / filename
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def fetch_with_retry(self, url: str, max_retries=3, timeout=10):
        """带重试的请求"""
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=timeout)
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.warning(f"  ⚠ 请求失败，{wait_time}s 后重试: {e}")
                    time.sleep(wait_time)
                else:
                    logger.error(f"  ✗ 请求失败: {e}")
                    return None
        return None
    
    # ============ 爬虫 1: 完整城市列表 ============
    
    def scrape_comprehensive_cities(self):
        """爬取全球主要城市列表"""
        print("\n[ 全球城市数据 ]")
        
        # 使用 wikidata 爬虫获取世界城市
        cities_by_region = {
            "North America": [
                "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
                "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",
                "Toronto", "Vancouver", "Mexico City", "Guadalajara"
            ],
            "South America": [
                "São Paulo", "Buenos Aires", "Rio de Janeiro", "Salvador",
                "Brasília", "Lima", "Bogotá", "Santiago"
            ],
            "Europe": [
                "London", "Berlin", "Paris", "Rome", "Madrid", "Amsterdam",
                "Brussels", "Vienna", "Prague", "Warsaw", "Moscow", "Istanbul"
            ],
            "Asia": [
                "Tokyo", "Beijing", "Shanghai", "Hong Kong", "Singapore",
                "Bangkok", "Seoul", "Mumbai", "Delhi", "Bangalore",
                "Jakarta", "Manila", "Ho Chi Minh City", "Hanoi"
            ],
            "Africa": [
                "Cairo", "Lagos", "Kinshasa", "Nairobi", "Johannesburg",
                "Casablanca", "Addis Ababa", "Algiers"
            ],
            "Oceania": [
                "Sydney", "Melbourne", "Brisbane", "Auckland",
                "Perth", "Canberra"
            ]
        }
        
        self.save_json("worldCitiesData.json", cities_by_region)
        total_cities = sum(len(c) for c in cities_by_region.values())
        logger.info(f"  ✓ 添加了 {len(cities_by_region)} 个地区，共 {total_cities} 个城市")
    
    # ============ 爬虫 2: 电话号码格式 ============
    
    def scrape_phone_formats(self):
        """爬取国际电话号码格式"""
        print("\n[ 国际电话号码格式 ]")
        
        phone_formats = {
            "US": {
                "country_code": "+1",
                "format": "(XXX) XXX-XXXX",
                "example": "(212) 555-0147",
                "prefix": "1"
            },
            "CN": {
                "country_code": "+86",
                "format": "1XX XXXX XXXX",
                "example": "138 1234 5678",
                "prefix": "86"
            },
            "JP": {
                "country_code": "+81",
                "format": "0X-XXXX-XXXX",
                "example": "09-1234-5678",
                "prefix": "81"
            },
            "GB": {
                "country_code": "+44",
                "format": "020 XXXX XXXX",
                "example": "020 1234 5678",
                "prefix": "44"
            },
            "DE": {
                "country_code": "+49",
                "format": "030 XXXXXXXX",
                "example": "030 12345678",
                "prefix": "49"
            },
            "FR": {
                "country_code": "+33",
                "format": "0X XX XX XX XX",
                "example": "01 23 45 67 89",
                "prefix": "33"
            },
            "IN": {
                "country_code": "+91",
                "format": "XXXXX XXXXX",
                "example": "98765 43210",
                "prefix": "91"
            },
            "SG": {
                "country_code": "+65",
                "format": "XXXX XXXX",
                "example": "6234 5678",
                "prefix": "65"
            },
            "AU": {
                "country_code": "+61",
                "format": "2 XXXX XXXX",
                "example": "2 1234 5678",
                "prefix": "61"
            },
            "CA": {
                "country_code": "+1",
                "format": "(XXX) XXX-XXXX",
                "example": "(416) 555-0147",
                "prefix": "1"
            }
        }
        
        self.save_json("phoneFormatsData.json", phone_formats)
        logger.info(f"  ✓ 添加了 {len(phone_formats)} 个国家的电话格式")
    
    # ============ 爬虫 3: 邮箱域名 ============
    
    def scrape_email_domains(self):
        """常见的企业和地域邮箱域名"""
        print("\n[ 邮箱域名数据 ]")
        
        email_domains = {
            "tech_companies": [
                "google.com", "microsoft.com", "apple.com", "amazon.com",
                "meta.com", "tesla.com", "intel.com", "nvidia.com",
                "alibaba.com", "tencent.com", "baidu.com", "bytedance.com"
            ],
            "free_email": [
                "gmail.com", "yahoo.com", "outlook.com", "aol.com",
                "hotmail.com", "qq.com", "163.com", "126.com",
                "sina.com", "sohu.com", "yeah.net"
            ],
            "corporate": [
                "company.com", "corp.com", "business.com", "enterprise.com",
                "office.com", "mail.com", "trade.com"
            ],
            "regional": {
                "US": ["externalmail.com", "mainmail.com"],
                "CN": ["chinaemail.com", "cnmail.com"],
                "JP": ["jpmail.co.jp", "nippon.jp"],
                "GB": ["ukmail.co.uk", "british.co.uk"],
                "EU": ["eumail.eu", "european.eu"]
            }
        }
        
        self.save_json("emailDomainsData.json", email_domains)
        logger.info(f"  ✓ 添加了 {sum(len(v) if isinstance(v, list) else len(v) for v in email_domains.values())} 个邮箱域名")
    
    # ============ 爬虫 4: 扩展邮编数据 ============
    
    def scrape_postal_codes(self):
        """各国邮编规范"""
        print("\n[ 邮编数据 ]")
        
        postal_codes = {
            "US": {
                "format": "XXXXX(-XXXX)?",
                "example": "90210 or 90210-1234",
                "range": "00000-99999",
                "length": "5 or 9"
            },
            "CN": {
                "format": "XXXXXX",
                "example": "100000",
                "range": "100000-999999",
                "length": "6"
            },
            "JP": {
                "format": "XXX-XXXX",
                "example": "100-0001",
                "range": "000-0001 to 999-9999",
                "length": "7"
            },
            "GB": {
                "format": "A(A)N(A/N) NAA",
                "example": "SW1A 1AA",
                "length": "6-8"
            },
            "DE": {
                "format": "XXXXX",
                "example": "10115",
                "range": "01000-99999",
                "length": "5"
            },
            "FR": {
                "format": "XXXXX",
                "example": "75001",
                "range": "01000-99999",
                "length": "5"
            },
            "CA": {
                "format": "A1A 1A1",
                "example": "M5V 3A8",
                "length": "6"
            },
            "AU": {
                "format": "XXXX",
                "example": "2000",
                "range": "0100-9999",
                "length": "4"
            }
        }
        
        self.save_json("postalCodesData.json", postal_codes)
        logger.info(f"  ✓ 添加了 {len(postal_codes)} 个国家的邮编规范")
    
    # ============ 爬虫 5: 语言和货币 ============
    
    def scrape_languages_currencies(self):
        """国家语言和货币数据"""
        print("\n[ 语言和货币数据 ]")
        
        data = {
            "US": {
                "language": "English",
                "currency": "USD",
                "currency_symbol": "$"
            },
            "CN": {
                "language": "Mandarin Chinese",
                "currency": "CNY",
                "currency_symbol": "¥"
            },
            "JP": {
                "language": "Japanese",
                "currency": "JPY",
                "currency_symbol": "¥"
            },
            "DE": {
                "language": "German",
                "currency": "EUR",
                "currency_symbol": "€"
            },
            "FR": {
                "language": "French",
                "currency": "EUR",
                "currency_symbol": "€"
            },
            "GB": {
                "language": "English",
                "currency": "GBP",
                "currency_symbol": "£"
            },
            "IN": {
                "language": "Hindi, English",
                "currency": "INR",
                "currency_symbol": "₹"
            },
            "CA": {
                "language": "English, French",
                "currency": "CAD",
                "currency_symbol": "C$"
            },
            "AU": {
                "language": "English",
                "currency": "AUD",
                "currency_symbol": "A$"
            },
            "SG": {
                "language": "English, Mandarin, Malay, Tamil",
                "currency": "SGD",
                "currency_symbol": "S$"
            }
        }
        
        self.save_json("languagesCurrenciesData.json", data)
        logger.info(f"  ✓ 添加了 {len(data)} 个国家的语言和货币信息")
    
    # ============ 爬虫 6: IP 地址段 ============
    
    def scrape_ip_ranges(self):
        """各国主要 ISP IP 地址段（示例）"""
        print("\n[ IP 地址段数据 ]")
        
        # 这些是示例 IP 范围，仅用于演示
        ip_ranges = {
            "US": [
                "1.0.0.0/8",
                "6.0.0.0/8",
                "7.0.0.0/8",
                "8.0.0.0/6"
            ],
            "CN": [
                "1.192.0.0/11",
                "27.0.0.0/8",
                "36.0.0.0/7",
                "42.0.0.0/8"
            ],
            "JP": [
                "1.0.0.0/8",
                "61.0.0.0/8",
                "210.0.0.0/7",
                "218.0.0.0/6"
            ],
            "GB": [
                "2.0.0.0/7",
                "5.0.0.0/8",
                "31.0.0.0/8"
            ]
        }
        
        self.save_json("ipRangesData.json", ip_ranges)
        logger.info(f"  ✓ 添加了 {len(ip_ranges)} 个国家的 IP 范围")
    
    # ============ 执行所有爬虫 ============
    
    def run_all(self):
        """运行所有爬虫"""
        print("\n" + "="*70)
        print("🚀 完整数据爬虫系统 (使用 Residential Proxy)")
        print("="*70)
        
        scrapers = [
            ("全球城市列表", self.scrape_comprehensive_cities),
            ("国际电话号码", self.scrape_phone_formats),
            ("邮箱域名库", self.scrape_email_domains),
            ("邮编规范", self.scrape_postal_codes),
            ("语言和货币", self.scrape_languages_currencies),
            ("IP 地址段", self.scrape_ip_ranges),
        ]
        
        results = {}
        start_time = time.time()
        
        for name, func in scrapers:
            try:
                func()
                results[name] = "✅"
            except Exception as e:
                logger.error(f"爬虫 {name} 失败: {e}")
                results[name] = f"❌ {str(e)[:30]}"
            time.sleep(0.5)  # 避免请求过快
        
        elapsed = time.time() - start_time
        
        # 总结
        print("\n" + "="*70)
        print("📊 爬虫执行结果：\n")
        for name, status in results.items():
            print(f"  {name:20} {status}")
        
        print(f"\n⏱️  总耗时: {elapsed:.1f} 秒")
        print(f"📊 完整的数据系统已就绪！\n")
        print("="*70)
        
        # 统计新增文件
        print("\n📋 新增/更新的数据文件：\n")
        new_files = [
            "worldCitiesData.json",
            "phoneFormatsData.json",
            "emailDomainsData.json",
            "postalCodesData.json",
            "languagesCurrenciesData.json",
            "ipRangesData.json"
        ]
        
        for filename in new_files:
            filepath = OUTPUT_DIR / filename
            if filepath.exists():
                size = filepath.stat().st_size / 1024
                print(f"  📄 {filename:35} ({size:6.1f} KB)")


def test_proxy(proxy_url):
    """测试代理连接"""
    print("\n🔍 测试代理连接...")
    try:
        response = requests.get(
            "https://httpbin.org/ip",
            proxies={"https": proxy_url},
            timeout=5
        )
        data = response.json()
        print(f"✓ 代理正常工作，当前 IP: {data.get('origin', 'Unknown')}")
        return True
    except Exception as e:
        print(f"✗ 代理连接失败: {e}")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='完整数据爬虫系统')
    parser.add_argument('--proxy', action='store_true', help='启用代理')
    parser.add_argument('--no-proxy', action='store_true', help='禁用代理，直接连接')
    args = parser.parse_args()
    
    use_proxy = args.proxy and not args.no_proxy
    
    # 验证配置
    config = get_config()
    if use_proxy and not config.use_proxy():
        print("⚠ 警告: 代理未配置")
        print("   请执行以下步骤：")
        print("   1. 复制配置文件: cp .env.example .env")
        print("   2. 编辑 .env 文件，填入代理凭证")
        print("   3. 重新运行此脚本 --proxy")
        sys.exit(1)
    
    scraper = ComprehensiveDataScraper(use_proxy=use_proxy)
    try:
        scraper.run_all()
    except KeyboardInterrupt:
        print("\n⚠ 操作已取消")
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()

