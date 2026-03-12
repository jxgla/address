# 地址数据自动化生成系统

使用 **Faker 库** + 混合数据源生成全球城市、名字、MAC 地址数据，专为 MockAddress 项目优化。

## 📊 已生成的数据文件

```
address/
├── 美国数据
│   └── usData.json          ✅ 15+ 州，每州 12-18 个城市
├── 中国数据
│   └── cnData.json          ✅ 15+ 省份，每省 15-25 个城市
├── 亚洲数据
│   ├── hkData.json          ✅ 10 个地区，26 个城市
│   ├── twData.json          ✅ 15 个城市，38 个区域
│   ├── jpData.json          ✅ 15 个都道府县，120+ 个城市
│   ├── inData.json          ✅ 5 个邦，50+ 个城市
│   └── sgData.json          ✅ 新加坡主要城市
├── 欧洲数据
│   ├── gbData.json          ✅ 4 个区域，50+ 个城市
│   └── deData.json          ✅ 4 个州，50+ 个城市
├── 其他数据
│   ├── caData.json          ✅ 4 个省份，40+ 个城市
│   └── auData.json          ✅ 8 个州，32 个城市 (新增)
├── 人物数据
│   ├── namesData.json       ✅ 240+ 男名，240+ 女名，300+ 姓氏
│   └── jpNamesData.json     ✅ 日文名字
└── 硬件数据
    └── macOuiData.json      ✅ 49 个厂商 MAC OUI 代码
```

## 🚀 快速开始

### 已有数据 ✅
所有数据文件**已生成完毕**，位置：`e:\Antigravity\address\`

### 更新或扩展数据

```bash
# 1. 安装 Faker（如果还未安装）
pip install faker

# 2. 增强主要数据（城市、名字、MAC OUI）
python enhance-address-data.py

# 3. 补充区域数据（HK、TW、AU）
python enhance-regional-data.py
```

## 数据来源

| 数据 | 来源 | 方式 |
|------|------|------|
| 城市/地区 | Faker 库 + GeoNames 备选 | 离线生成 |
| 名字 | Faker (en/zh/ja/de) | 合成 |
| MAC OUI | IEEE 公开库 + 混合 | 手工编制 |
| HK/TW/AU | 手工数据 | 精编 |

⚠️ **网络限制友好** - 不依赖任何在线 API，完全离线运行！

## 使用生成的数据

### 方法 1：复制到 Astro 项目

```bash
# 复制数据到 Astro public 目录
cp *.json ../astro-paper/public/data/address/

# 或在 Windows 上
copy *.json ..\astro-paper\public\data\address\
```

### 方法 2：配置 MockAddress

在 Astro 组件中配置数据路径：

```javascript
import addressGenerator from './addressGenerator.js'

// 配置：指向数据目录
addressGenerator.configure({
  dataBasePath: '/data/address/',
  autoDetectPaths: false
})

// 使用
const address = addressGenerator.generateAddress('US')
```

## 数据格式示例

### 美国数据 (usData.json)
```json
{
  "NY": {
    "state": "NY",
    "cities": ["New York", "Buffalo", "Albany", "Rochester", "Syracuse", ...],
    "zip_prefix": "10"
  },
  "CA": {
    "state": "CA",
    "cities": ["Los Angeles", "San Francisco", "San Diego", ...],
    "zip_prefix": "90"
  }
}
```

### 香港数据 (hkData.json)
```json
{
  "Central & Western": {
    "district": "Central & Western",
    "cities": ["Central", "Western", "Admiralty"],
    "population": 150000
  },
  "Wan Chai": {
    "district": "Wan Chai",
    "cities": ["Wan Chai", "Causeway Bay"],
    "population": 100000
  }
}
```

### 人物名字 (namesData.json)
```json
{
  "firstName_male": ["James", "John", "Robert", "Michael", ...],
  "firstName_female": ["Mary", "Patricia", "Jennifer", ...],
  "lastName": ["Smith", "Johnson", "Williams", ...]
}
```

### MAC OUI (macOuiData.json)
```json
[
  {"oui": "00:00:0C", "vendor": "Cisco"},
  {"oui": "08:00:27", "vendor": "PCS Systemtechnik"},
  {"oui": "00:26:86", "vendor": "Apple"}
]
```

## 集成到 MockAddress/Astro

### 方法 1：复制到 Astro 项目

```bash
# Windows
copy address\*.json astro-paper\public\data\address\

# Linux/Mac
cp address/*.json astro-paper/public/data/address/
```

### 方法 2：配置 MockAddress 组件

在你的 Astro 组件中：

```javascript
import addressGenerator from './path/to/addressGenerator.js'

// 配置数据路径
addressGenerator.configure({
  dataBasePath: '/data/address/',
  autoDetectPaths: false
})

// 使用
const address = addressGenerator.generateAddress('US')
const name = generateFullName()
const mac = generateMacAddress()
```

## 数据来源与质量

| 数据 | 来源 | 方式 | 质量 |
|------|------|------|-----|
| 城市 | Faker + GeoNames 备选 | 生成 | ⭐⭐⭐⭐ |
| 名字 | Faker (en/zh/ja/de) | 合成 | ⭐⭐⭐⭐ |
| MAC OUI | IEEE 公开库 + 混合 | 手工 | ⭐⭐⭐⭐⭐ |
| HK/TW/AU | 手工编制 | 精编 | ⭐⭐⭐⭐⭐ |

**特点：**
- ✅ 100% 离线生成（无网络依赖）
- ✅ 多语言支持
- ✅ 数据量充分（1000+ 条目）
- ✅ 格式标准化
- ✅ 易于扩展

## 🔧 脚本说明

### enhance-address-data.py
增强主要国家的城市和名字数据：
- 美国：15 个主要州
- 中国：15 个主要省份
- 日本：15 个都道府县
- 英国、加拿大、德国、印度、新加坡
- 全球名字库：240+ 男名、女名，300+ 姓氏
- MAC OUI：49 个主要厂商

### enhance-regional-data.py
补充特定地区的详细数据：
- 香港：10 个分区，26 个城市/区域
- 台湾：15 个城市，38 个区
- 澳大利亚：8 个州，32 个城市

## 故障排除

### ❌ "No module named 'faker'"

```bash
pip install faker
```

### ❌ 网络请求被拦截

✅ **已解决** - 当前脚本采用 Faker 离线生成，无网络依赖

### ❌ 编码问题（中文显示乱码）

文件已保存为 UTF-8 编码，json 导出配置：
```python
json.dump(data, f, ensure_ascii=False, indent=2)
```

## 定期更新

需要新数据时运行脚本：

```bash
# 更新主要数据
python enhance-address-data.py

# 更新区域数据
python enhance-regional-data.py
```

---

**最后更新：** 2026-03-12  
**数据总量：** 14 个 JSON 文件，~35 KB，1000+ 条目  
**维护成本：** 每次需要数据更新时运行脚本 (~2 分钟)  
**技术栈：** Python 3.7+, Faker 15+
