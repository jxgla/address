# 贡献指南

感谢你对本项目的关注！本文档提供了贡献流程和最佳实践的指导。

## 📋 行为准则

本项目采用 [Contributor Covenant](https://www.contributor-covenant.org/) 行为准则。

所有贡献者都应：
- 尊重不同的观点和经验
- 以建设性的方式给予和接受批评
- 关注项目和社区最好的利益
- 对他人表示同情和尊重

## 🚀 开始贡献

### 报告 Bug

在报告 bug 前，请检查 [Issue 列表](../../issues) 确保不是重复。

**好的 Bug 报告应该包括：**

- 清晰的标题和描述
- 重现 bug 的具体步骤
- 预期行为 vs 实际行为
- 截图或日志输出（如适用）
- Python 版本、操作系统等环境信息

**示例：**

```markdown
## Bug 报告：代理连接失败

### 描述
使用 Residential Proxy 时，爬虫连接超时

### 重现步骤
1. 配置 .env 文件
2. 运行 `python scripts/scrape-with-proxy.py`
3. 观察错误日志

### 预期行为
应该成功连接论代理和爬取数据

### 实际行为
每次请求都超时，3 次重试后失败

### 环境
- Python: 3.9.0
- 操作系统: Windows 10
- requests 版本: 2.28.0
```

### 功能请求

好的功能请求应该：

- 有清晰简洁的标题
- 描述是什么问题或使用场景驱动此功能
- 列出可能的实现方式
- 说明可能的优先级

**示例：**

```markdown
## 功能请求：支持更多国家/地区

### 问题描述
目前只支持少数几个国家。能否添加更多地理位置数据？

### 建议解决方案
- 添加 German 德国数据源
- 添加 France 法国数据源
- 实现归一化接口

### 额外背景
许多欧洲用户需要这些数据
```

### 提交 Pull Request

**创建 PR 前：**

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/your-feature-name`
3. 完成更改和测试
4. 提交更改：`git commit -m 'Add feature: your description'`
5. 推送分支：`git push origin feature/your-feature-name`
6. 打开 Pull Request

**PR 描述应该包括：**

```markdown
## 描述
简明扼要地描述更改内容

## 相关的 Issue
Fixes #123

## 更改类型
- [ ] Bug 修复
- [ ] 新功能
- [ ] 破坏性变更
- [ ] 文档更新

## 测试
描述你的测试步骤：
- [ ] 测试 1
- [ ] 测试 2

## 检查清单
- [ ] 代码遵循项目风格
- [ ] 自检了代码本身的变更
- [ ] 添加了适当的测试
- [ ] 更新了文档
- [ ] 提交信息清晰有意义
- [ ] 没有多余的 print 或调试代码
```

## 💻 开发指南

### 设置开发环境

```bash
# 克隆仓库
git clone https://github.com/yourusername/address-system.git
cd address

# 创建虚拟环境
python -m venv venv
source venv/bin/activate    # Linux/Mac
# 或 venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt

# 安装开发依赖
pip install -r requirements-dev.txt
```

### 代码风格

本项目遵循 [PEP 8](https://pep8.org/) 代码风格。

**关键点：**

- 缩进：4 个空格（不使用 Tab）
- 行长：不超过 120 个字符
- 命名：使用 snake_case（变量/函数）、PascalCase（类）
- 导入：按照标准库 → 第三方 → 本地的顺序组织

**示例：**

```python
#!/usr/bin/env python3
"""模块文档字符串"""

import json
from pathlib import Path
from typing import Dict, List, Optional

import requests
from dotenv import load_dotenv

from config import get_config


class DataProcessor:
    """处理地址数据的类"""
    
    def __init__(self, data_dir: Path):
        """初始化处理器
        
        Args:
            data_dir: 数据目录路径
        """
        self.data_dir = data_dir
    
    def process(self) -> Dict[str, List[str]]:
        """处理数据
        
        Returns:
            处理后的数据字典
        """
        ...
```

### 文件组织

```
address/
├── data/          # 数据文件（不修改，除非必要）
├── scripts/       # Python 脚本（主要贡献区域）
├── docs/          # 文档文件
├── tests/         # 单元测试
├── config.py      # 配置管理
└── requirements.txt
```

### 添加新脚本

创建新的 Python 脚本时：

1. 放在 `scripts/` 目录下
2. 添加模块文档字符串和函数文档
3. 包含 `if __name__ == '__main__':` 主函数块
4. 使用 Config 管理任何敏感配置
5. 添加错误处理和日志

**模板：**

```python
#!/usr/bin/env python3
"""
脚本简要描述

更详细的描述...
"""

import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import get_config


def main():
    """主函数"""
    config = get_config()
    # 你的代码


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠ 操作取消")
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
```

### 测试

添加测试以验证功能：

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_config.py

# 查看覆盖率
pytest --cov=. tests/
```

**示例测试：**

```python
import pytest
from config import get_config


class TestConfig:
    """测试配置管理"""
    
    def test_proxy_disabled_by_default(self):
        """测试默认禁用代理"""
        config = get_config()
        assert not config.use_proxy()
    
    def test_api_timeout_default(self):
        """测试 API 超时默认值"""
        config = get_config()
        assert config.get_api_timeout() == 15
    
    def test_proxy_url_masked(self):
        """测试代理 URL 掩蔽"""
        config = get_config()
        # 设置代理...
        url_str = str(config)
        assert 'password' not in url_str.lower()
```

### 提交和推送

**提交信息：**

请使用清晰、有意义的提交消息。格式：

```
<类型>: <简短描述>

<可选的详细说明>

Fixes #issue_number
```

**类型的含义：**

- `feat:` - 新功能
- `fix:` - Bug 修复
- `docs:` - 文档更改
- `style:` - 代码格式（无逻辑改变）
- `refactor:` - 代码重构
- `perf:` - 性能优化
- `test:` - 测试相关
- `chore:` - 依赖、构建等

**示例：**

```bash
git commit -m "feat: add German and French address data

- Add deData.json with German States and cities
- Add frData.json with French regions and cities
- Implement data normalization interface
- Update documentation

Fixes #42"
```

## 🔐 安全指南

### 敏感信息

**永远不要提交：**

- `.env` 文件（包含真实凭证）
- 密钥、token 或密码
- API 凭证或密钥
- 个人或机密数据

**应该提交：**

- `.env.example` 模板（无真实值）
- 配置文档和说明
- 安全最佳实践示例

### 报告安全漏洞

如果发现安全漏洞，**请勿**在 Issue 中公开。

改为：
1. 发送邮件到 security@example.com
2. 说明漏洞详情和严重程度
3. 允许 30 天修复时间

## 📚 文档指南

### 更新文档

1. 进行代码更改时，同时更新相关文档
2. 在 `docs/` 目录中编辑或创建 .md 文件
3. 使用清晰的标题和代码示例
4. 保持格式一致

### 文档风格

- 使用中文或英文（保持一致）
- 清晰的标题层次（# ## ###）
- 代码示例带语言标记
- 链接指向相关文档
- 定期检查过期内容

## 🏆 贡献者认可

所有贡献者都会被认可在：

- [CONTRIBUTORS.md](CONTRIBUTORS.md) 中列出
- GitHub 仓库的 Insights 中
- 版本发布说明中（如适用）

感谢你的贡献！

---

有问题？

- 查看 [FAQ](docs/FAQ.md)
- 搜索 [Discussions](../../discussions)
- 创建新 [Discussion](../../discussions/new)

**祝你贡献愉快！** 🎉
