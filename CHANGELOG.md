# Change Log

所有重要的项目变更都会记录在此文件中。

格式参考 [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)，
版本号遵循 [Semantic Versioning](https://semver.org/spec/v2.0.0.html)。

## [Unreleased]

### Added
- 计划中的功能和特性

### Changed
- 计划中的改进

### Deprecated
- 已废弃的 API

### Fixed
- 已修复的 Bug

### Security
- 安全相关更新

---

## [1.2.0] - 2024-01-15

### Added
- ✨ **美国税务优化数据**
  - 新增 `data/usTaxFreeStates.json` 包含 5 个零税州（MT, NH, OR, DE, AK）
  - 新增 3 个低税州（CO, GA, LA）数据
  - 包含 20+ 个城市样本数据

- ✨ **完整的配置管理系统**
  - 新增 `config.py` 模块（680+ 行）
  - 支持环境变量和 .env 文件混合配置
  - 自动凭证掩蔽以保护敏感信息
  - API 超时/重试配置
  - 代理配置建造生成器

- ✨ **环境文件和安全**
  - 新增 `.env.example` 配置模板
  - 新增 `.gitignore` 保护敏感文件
  - 安全最佳实践文档

### Changed
- 🔄 **爬虫脚本现代化**
  - 将 `scrape-with-proxy.py` 重构为使用 Config 管理
  - 移除所有硬编码凭证
  - 改进命令行参数支持

- 🔄 **项目结构重组**
  - 自动化项目组织脚本 `organize_project.py`
  - 37 个文件移入对应目录：data/、scripts/、docs/
  - 清晰的目录层级结构

- 📝 **文档增强**
  - 专业的 GitHub 风格 README.md
  - 更新 QUICK_START.md 和 SCRAPER_GUIDE.md
  - 数据统计表格
  - 使用场景示例

### Fixed
- 🐛 代理配置不一致问题
- 🐛 路径相关的跨平台兼容性问题
- 🐛 爬虫超时处理的稳定性

### Security
- 🔐 移除硬编码代理凭证（CRITICAL）
- 🔐 实施环境变量配置管理
- 🔐 自动凭证掩蔽在日志输出中
- 🔐 增强 .gitignore 规则

---

## [1.1.0] - 2024-01-10

### Added
- ✨ **Residential Proxy 支持**
  - 完整的代理配置系统
  - 自动重试和指数退避
  - 代理连接验证

- ✨ **数据爬虫工具**
  - `scrape-with-proxy.py` - 主爬虫脚本
  - 支持多个数据源（Wikipedia, GitHub 等）
  - 智能城市数据提取

- ✨ **数据增强工具**
  - `enhance-address-data.py` - 数据增强
  - `build-complete-data.py` - 数据构建
  - `check-data.py` - 数据验证

- 📚 **初始文档**
  - QUICK_START.md
  - SCRAPER_GUIDE.md
  - INTEGRATION_GUIDE.md

### Changed
- 📝 改进爬虫的错误处理
- 📝 简化数据加载 API
- 📝 优化网络请求性能

### Fixed
- 🐛 修复爬虫超时问题
- 🐛 改进 HTML 解析稳定性
- 🐛 修复 JSON 编码问题

---

## [1.0.0] - 2024-01-01

### Added
- 🎉 **初始版本发布**
  
- 📦 **核心数据集**
  - usData.json - 美国 50 个州 + 1000+ 城市
  - cnData.json - 中国 31 省 + 300+ 城市
  - jpData.json - 日本 47 都道府县 + 400+ 城市
  - gbData.json - 英国全区域
  - inData.json - 印度各邦
  - namesData.json - 1000+ 常用人名
  - macOuiData.json - 5000+ MAC 地址前缀
  - 以及 13 个其他数据文件

- 🐍 **Python 工具套件**
  - 12 个实用脚本
  - 数据验证和检查
  - 数据导出功能

- 📚 **完整文档**
  - 项目 README
  - 快速开始指南
  - API 参考文档

---

## 版本对比

| 版本 | 发布日期 | 主要特性 | 状态 |
|------|---------|---------|------|
| 1.2.0 | 2024-01-15 | 税务数据 + 配置管理 | ✅ 当前 |
| 1.1.0 | 2024-01-10 | Proxy 爬虫 + 工具 | ✅ 稳定 |
| 1.0.0 | 2024-01-01 | 初始发布 | ✅ 存档 |

---

## 迁移指南

### 从 v1.1.0 升级到 v1.2.0

```bash
git pull origin main

# 配置环境变量（如果使用代理）
cp .env.example .env
# 编辑 .env 填入代理凭证

# 测试新配置
python scripts/scrape-with-proxy.py --no-proxy
```

**破坏性变更：** 无

### 从 v1.0.0 升级到 v1.1.0

```bash
git pull origin main
pip install -r requirements.txt

# 使用新的爬虫脚本
python scripts/scrape-with-proxy.py
```

**破坏性变更：** 无

---

## 贡献

欢迎提交 PR 来改进此项目！请参考 [CONTRIBUTING.md](CONTRIBUTING.md)

## 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

**最后更新：** 2024-01-15
**维护者：** [Your Name]
**联系方式：** [your-email@example.com]
