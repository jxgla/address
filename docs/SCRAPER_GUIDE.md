# 数据爬虫使用指南

## 📡 已创建的爬虫脚本

### 1. **scrape-from-sources.py** - 基础爬虫
从 GitHub 和 OpenStreetMap 获取数据
- ✓ OSM 城市坐标数据成功
- ⚠ GitHub 源需要更新 URL

**运行：**
```bash
python scrape-from-sources.py
```

**输出：**
- `osmData.json` - 世界城市坐标

---

### 2. **wikipedia-scraper.py** - Wikipedia 爬虫
从 Wikipedia API 爬取城市列表
- ✓ 美国、中国、日本、英国、印度数据增强

**运行：**
```bash
python wikipedia-scraper.py
```

**特点：**
- 稳定的 Wikipedia API
- 支持多语言
- 自动合并现有数据（不覆盖）

---

### 3. **scrape-modular.py** - 模块化爬虫（推荐）
独立运行各个数据模块

**运行：**
```bash
python scrape-modular.py
```

**包含模块：**

| 模块 | 数据源 | 状态 | 文件 |
|------|------|------|------|
| 世界国家数据 | REST Countries API | ⚠️ 受限 | worldCountriesData.json |
| 美国邮编 | 静态映射 | ✅ | usZipCodesData.json |
| 公司名称 | 手工编制 | ✅ | companiesData.json |
| 城市坐标 | 手工编制 | ✅ | citiesCoordinatesData.json |
| 街道类型 | 多语言手工 | ✅ | streetTypesData.json |

---

## 🔍 爬虫数据源对比

| 源 | 优点 | 缺点 | 推荐度 |
|----|------|------|--------|
| **Wikipedia** | 内容详细、稳定 | API 有限制、速度慢 | ⭐⭐⭐⭐ |
| **GitHub 仓库** | 数据已处理、量大 | 网络受限时容易失败 | ⭐⭐⭐ |
| **OpenStreetMap** | 准确、完整 | API 复杂 | ⭐⭐⭐⭐ |
| **REST API** | 简单、快速 | 依赖网络、有速率限制 | ⭐⭐⭐ |
| **静态生成** | 离线、快速、稳定 | 需要手工维护 | ⭐⭐⭐⭐⭐ |

---

## 🛠️ 自定义爬虫

### 修改爬虫范围

在 `scrape-modular.py` 中修改城市列表：

```python
cities_coords = {
    "Your City": {"lat": 40.0, "lng": -74.0},
    # ... 添加更多
}
```

### 添加新的爬虫模块

在 `scrape-modular.py` 中添加新方法：

```python
def scrape_new_source(self):
    """爬取新数据源"""
    print("\n[ 新数据源 ]")
    
    try:
        # 你的爬虫代码
        data = {}
        self.save_json("newData.json", data)
        return True
    except Exception as e:
        print(f"  ✗ 错误: {e}")
        return False
```

然后在 `run_all()` 中注册：

```python
modules = [
    ("你的模块", self.scrape_new_source),  # 添加这行
    # ... 其他模块
]
```

---

## 📊 已生成的补充数据

```
address/
├── 原始数据（14 个文件）
│   ├── usData.json
│   ├── cnData.json
│   ├── jpData.json
│   └── ... (其他国家)
│
└── 补充数据（5 个文件）
    ├── usZipCodesData.json      (邮编范围)
    ├── companiesData.json        (公司名)
    ├── citiesCoordinatesData.json (坐标)
    ├── streetTypesData.json      (街道类型)
    └── osmData.json              (OSM 坐标)
```

---

## 🔓 防绕过网络限制

如果爬虫因网络问题失败：

### 方案 1: 使用代理
```python
proxies = {
    "http": "http://proxy.example.com:8080",
    "https": "http://proxy.example.com:8080",
}
response = self.session.get(url, proxies=proxies, timeout=10)
```

### 方案 2: 离线生成（推荐）
```bash
python enhance-address-data.py
python enhance-regional-data.py
```

### 方案 3: 静态数据库
将数据保存为本地 JSON，直接读取，无需网络

---

## 💾 数据合并

将爬虫数据合并到现有数据：

```python
def merge_data():
    """合并所有 JSON 文件"""
    all_data = {}
    
    for json_file in OUTPUT_DIR.glob("*Data.json"):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            all_data[json_file.stem] = data
    
    with open(OUTPUT_DIR / "all-data.json", 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
```

---

## 🚀 推荐工作流

**第 1 步：快速爬虫**
```bash
python scrape-modular.py
```

**第 2 步：数据增强**
```bash
python enhance-address-data.py
python enhance-regional-data.py
```

**第 3 步：可选深度爬虫**
```bash
python wikipedia-scraper.py
```

**第 4 步：集成到 Astro**
```bash
copy address\*.json astro-paper\public\data\address\
```

---

## ❓ 常见问题

### Q: 爬虫很慢？
A: 正常，因为有请求延迟。可以修改 `time.sleep(1)` 为更小的值。

### Q: 某个 API 404？
A: REST Countries 等 API 有变化，我已在 `scrape-modular.py` 中改为静态生成，不再依赖。

### Q: 如何只爬虫某个特定模块？
A: 编辑 `run_all()` 中的 `modules` 列表，注释掉不需要的模块。

### Q: 数据重复？
A: 所有爬虫都有去重逻辑，新数据自动补充而不覆盖。

---

## 📈 下次可以爬取的数据

1. **邮编数据** - 各国的邮编规范
2. **电话号码格式** - 国际号码规范
3. **语言数据** - 各国官方语言
4. **时区数据** - 世界时区映射
5. **货币数据** - 国家与货币对应
6. **假期日期** - 各国国定假日

---

**建议：** 从 `scrape-modular.py` 开始，稳定高效，网络受限也能用。

**下一步？** 准备集成到 Astro-Paper 了吗？
