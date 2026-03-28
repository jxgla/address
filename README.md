# Address Generator

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)

> Inspired by [hotbob011/real-random-taxfree-address](https://github.com/hotbob011/real-random-taxfree-address). Thanks for the inspiration.

精准的全球地址生成系统，内置多国地址生成、爬虫采集和数据增强能力。完全支持代理配置和开源友好的环境变量管理。

## 🌟 主要特性

- 🌍 **全球地址覆盖**：50+ 美国城市、中国省份、日本都道府县、英国地区、印度邦
- 🎯 **美国税务优化**：专门的零税率州和低税率州分类（MT, NH, OR, DE, AK 等）
- 🤖 **合成身份生成**：TypeScript/Python 双语支持的完整身份生成系统
- 🕷️ **智能网页爬虫**：支持 Residential Proxy，带自动重试和错误处理
- 🔐 **安全配置管理**：环境变量 + .env 文件方案，完全隔离敏感信息
- 📦 **即插即用**：预加载 20+ JSON 数据文件，零配置即可使用
- 🚀 **生产就绪**：Docker 支持、完整日志、健康检查

## 📋 目录结构

```
address/
├── data/                       # 数据文件（20+ JSON）
│   ├── usData.json            # 美国 50 个州 + 城市
│   ├── cnData.json            # 中国各省份 + 城市
│   ├── jpData.json            # 日本都道府县
│   ├── gbData.json            # 英国地区
│   ├── inData.json            # 印度邦
│   ├── usTaxFreeStates.json   # ⭐ 零税/低税州（新增）
│   ├── namesData.json         # 常用人名
│   ├── macOuiData.json        # MAC 地址前缀
│   └── ... (12 more files)
│
├── scripts/                    # Python 爬虫和工具脚本
│   ├── scrape-with-proxy.py   # 主爬虫（支持 Residential Proxy）
│   ├── build-complete-data.py # 数据构建和验证
│   ├── enhance-address-data.py # 数据增强工具
│   ├── check-data.py          # 数据检查和统计
│   └── ... (8 more utilities)
│
├── docs/                       # 文档和指南
│   ├── README.md
│   ├── QUICK_START.md
│   ├── SCRAPER_GUIDE.md
│   └── ...
│
├── config.py                   # 🔑 配置管理核心（支持 .env）
├── .env.example               # 配置模板（复制为 .env）
├── requirements.txt           # Python 依赖
├── .gitignore                 # Git 规则（保护 .env）
└── README.md                  # 本文件
```

## 🚀 快速开始

### 1. 安装依赖

```bash
# 克隆仓库
git clone https://github.com/jxgla/address-system.git
cd address

# 安装 Python 依赖
pip install -r requirements.txt
```

### 2. 配置环境（可选：仅在需要代理时）

```bash
# 复制示例配置
cp .env.example .env

# 编辑 .env，填入代理凭证（两种方法任选其一）
# 方法 1：直接代理 URL
PROXY_URL=http://username:password@proxy.server:port

# 方法 2：代理组件
PROXY_USERNAME=your_username
PROXY_PASSWORD=your_password
PROXY_HOST=proxy.server
PROXY_PORT=10000
```

### 3. 立即使用

```bash
# 直接连接（不使用代理）
python scripts/check-data.py

# 或使用代理【需要先配置 .env】
python scripts/scrape-with-proxy.py

# 禁用代理进行测试
python scripts/scrape-with-proxy.py --no-proxy
```

## 💻 使用示例

### Python 中加载地址数据

```python
import json
from pathlib import Path

# 加载美国数据
data_dir = Path('data')
with open(data_dir / 'usData.json', 'r', encoding='utf-8') as f:
    us_data = json.load(f)

# 访问特定州
california_cities = us_data['CA']['cities']
print(california_cities)  # ['Los Angeles', 'San Francisco', ...]

# 加载零税州数据
with open(data_dir / 'usTaxFreeStates.json', 'r', encoding='utf-8') as f:
    tax_free = json.load(f)

zero_tax_states = tax_free['taxFreeStates']['states']
# MT, NH, OR, DE, AK
```

### 使用配置管理

```python
from config import get_config, get_proxy_config

# 获取配置
config = get_config()

# 检查是否启用代理
if config.use_proxy():
    print(f"Proxy: {config.get_proxy_url()}")
    
    # 用于 requests
    import requests
    proxies = config.get_proxy_config()
    response = requests.get('https://example.com', proxies=proxies)
else:
    print("Direct connection (no proxy)")

# 获取 API 配置
timeout = config.get_api_timeout()        # 15 秒
max_retries = config.get_max_retries()    # 3 次
retry_delay = config.get_retry_delay()    # 1 秒
```

## 📊 数据统计

| 数据文件 | 类型 | 覆盖范围 | 记录数 |
|---------|------|---------|--------|
| usData.json | 地理 | 美国 50 州 + 城市 | 500+ |
| cnData.json | 地理 | 中国 31 省 + 城市 | 300+ |
| jpData.json | 地理 | 日本 47 都道府县 | 400+ |
| usTaxFreeStates.json | ⭐ 新 | 零税/低税州 | 8 州 |
| namesData.json | 人名 | 常用人名 | 1000+ |
| macOuiData.json | 网络 | MAC 厂商前缀 | 5000+ |

## 🕷️ 爬虫使用指南

### 基础爬虫

```bash
# 爬取所有数据（自动使用 .env 中的代理）
python scripts/scrape-with-proxy.py

# 禁用代理（直接连接）
python scripts/scrape-with-proxy.py --no-proxy

# 测试模式
python scripts/scrape-with-proxy.py --dry-run
```

### 带代理的爬虫

爬虫支持 **Residential Proxy**（如 proxy-seller.com），通过环境变量安全配置：

```env
# .env 文件示例
PROXY_URL=http://username:password@res.proxy-seller.com:10000
# 或分开配置
PROXY_USERNAME=your_username
PROXY_PASSWORD=your_password
PROXY_HOST=res.proxy-seller.com
PROXY_PORT=10000

# API 设置
API_TIMEOUT=15
MAX_RETRIES=3
RETRY_DELAY=1
```

### 爬虫功能

- ✅ 美国城市爬取（Wikipedia）
- ✅ 中国城市爬取
- ✅ 日本都市爬取
- ✅ 英国城市爬取
- ✅ 印度城市爬取
- ✅ 世界首都爬取
- ✅ GitHub 开源数据源集成

### 错误处理和重试

爬虫内置智能重试机制：

```
代理错误 → 指数退避重试 (1s, 2s, 4s...)
连接超时 → 自动重试（3 次）
HTTP 错误 → 记录并继续
```

## 🔐 安全特性

### 敏感信息隔离

- ✅ **无硬编码凭证**：所有敏感信息从 `.env` 读取
- ✅ **.gitignore 保护**：`.env` 从不提交到 Git
- ✅ **环境变量支持**：CI/CD 友好
- ✅ **凭证掩蔽**：日志中自动隐藏密码

### 推荐配置

```bash
# 生产环境：使用环境变量（不使用 .env）
export PROXY_URL="http://user:pass@proxy.com:10000"
python scripts/scrape-with-proxy.py

# 开发环境：使用 .env 文件（已在 .gitignore 中）
cp .env.example .env
# 编辑 .env 填入凭证
python scripts/scrape-with-proxy.py
```

## 📦 依赖

- Python 3.7+
- requests (2.28+)
- python-dotenv (0.20+)
- faker (13+)

完整列表见 [requirements.txt](requirements.txt)

## 🛠️ 数据增强工具

### 构建完整数据集

```bash
python scripts/build-complete-data.py
```

### 验证数据完整性

```bash
python scripts/check-data.py
```

### 增强地址数据

```bash
python scripts/enhance-address-data.py
```

## ☁️ Cloudflare Pages 部署

Pages 发布目录默认使用 `dist/pages`，避免误把整个仓库内容直接公开到线上。

```bash
python scripts/prepare-pages-deploy.py
wrangler.cmd pages deploy dist/pages --project-name address-lab
```

打包脚本当前只会复制这些公开运行时资源：

- `index.html`
- `_headers`
- `assets/`
- `data/`

这样 `scripts/`、`docs/`、临时日志和其他仓库内部文件就不会被误发布。

## 📖 文档

完整文档位于 `docs/` 目录：

- [快速开始](docs/QUICK_START.md) - 5 分钟快速上手
- [爬虫指南](docs/SCRAPER_GUIDE.md) - 详细爬虫配置
- [集成指南](docs/INTEGRATION_GUIDE.md) - 与其他系统集成
- [系统总结](docs/SYSTEM_SUMMARY.md) - 技术架构概览

## 🎯 使用场景

- 📍 **地址验证**：验证和标准化地址格式
- 🎲 **测试数据**：生成逼真的测试地址
- 📊 **数据分析**：地理信息分析和可视化
- 💼 **业务应用**：物流、房产、税务等行业应用
- 🏦 **合规**：自动查询零/低税州信息

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

```bash
# Fork 仓库
# 创建特性分支: git checkout -b feature/amazing-feature
# 提交更改: git commit -m 'Add amazing feature'
# 推送分支: git push origin feature/amazing-feature
# 打开 Pull Request
```

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙋 支持

遇到问题？

1. 查看 [常见问题](docs/FAQ.md)
2. 搜索 [Issue](https://github.com/jxgla/address-system/issues)
3. 新建 [Issue](https://github.com/jxgla/address-system/issues/new)

## 📝 更新日志

### v1.2.0 - 2026-03-12

- ✨ 新增：美国税务优化数据（零税州 + 低税州）
- 🔐 改进：完整的配置管理系统（.env 支持）
- 🎯 改进：自动项目组织和清理
- 📚 改进：强化文档和示例

### v1.1.0 - 2026-03-08

- ✨ 新增：Residential Proxy 支持
- 🐛 修复：爬虫重试逻辑
- 📊 新增：数据验证工具

### v1.0.0 - 2026-03-01

- 🎉 初始版本发布

---

**Made with ❤️ for the open-source community**

如果这个项目对你有帮助，请考虑给个 ⭐ Star！
