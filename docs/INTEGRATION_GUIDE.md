# Astro-Paper 集成指南

## 🚀 快速集成步骤

### 第 1 步：复制数据文件到 Astro

```bash
# 创建数据目录
mkdir astro-paper\public\data\address\

# 复制所有 JSON 数据
copy address\*.json astro-paper\public\data\address\
```

结构应该如下：
```
astro-paper/
└── public/
    └── data/
        └── address/
            ├── usData.json
            ├── cnData.json
            ├── jpData.json
            ├── hkData.json
            ├── twData.json
            ├── gbData.json
            ├── caData.json
            ├── deData.json
            ├── inData.json
            ├── sgData.json
            ├── auData.json
            ├── namesData.json
            ├── jpNamesData.json
            ├── macOuiData.json
            ├── osmData.json
            ├── usZipCodesData.json
            ├── companiesData.json
            ├── citiesCoordinatesData.json
            └── streetTypesData.json
```

---

### 第 2 步：创建模块加载器

在 `src/lib/` 下创建新文件 `addressDataLoader.ts`：

```typescript
// src/lib/addressDataLoader.ts

interface AddressData {
  [key: string]: {
    cities?: string[];
    [key: string]: any;
  };
}

class AddressDataLoader {
  private cache: Map<string, any> = new Map();
  
  async loadData(filename: string): Promise<any> {
    if (this.cache.has(filename)) {
      return this.cache.get(filename);
    }
    
    try {
      const response = await fetch(`/data/address/${filename}`);
      const data = await response.json();
      this.cache.set(filename, data);
      return data;
    } catch (error) {
      console.error(`Failed to load ${filename}:`, error);
      return null;
    }
  }
  
  // 各国数据加载器
  async usData() { return this.loadData('usData.json'); }
  async cnData() { return this.loadData('cnData.json'); }
  async jpData() { return this.loadData('jpData.json'); }
  async hkData() { return this.loadData('hkData.json'); }
  async twData() { return this.loadData('twData.json'); }
  async gbData() { return this.loadData('gbData.json'); }
  async caData() { return this.loadData('caData.json'); }
  
  // 通用数据
  async names() { return this.loadData('namesData.json'); }
  async macOui() { return this.loadData('macOuiData.json'); }
  async cities() { return this.loadData('citiesCoordinatesData.json'); }
  async streets() { return this.loadData('streetTypesData.json'); }
  
  // 工具方法
  async getRandomCity(country: string): Promise<string> {
    const data = await this.loadData(`${country.toLowerCase()}Data.json`);
    if (!data) return 'Unknown';
    
    const states = Object.values(data) as any[];
    if (states.length === 0) return 'Unknown';
    
    const randomState = states[Math.floor(Math.random() * states.length)];
    const cities = randomState.cities || [];
    
    return cities[Math.floor(Math.random() * cities.length)] || 'Unknown';
  }
  
  async getRandomName(): Promise<{ first: string; last: string }> {
    const data = await this.names();
    if (!data) return { first: 'John', last: 'Doe' };
    
    const firstNames = data.firstName_male || [];
    const lastNames = data.lastName || [];
    
    return {
      first: firstNames[Math.floor(Math.random() * firstNames.length)],
      last: lastNames[Math.floor(Math.random() * lastNames.length)]
    };
  }
}

export const addressLoader = new AddressDataLoader();
```

---

### 第 3 步：创建 MockAddress 组件

在 `src/components/` 下创建 `MockAddressGenerator.astro`：

```astro
---
// src/components/MockAddressGenerator.astro

interface Props {
  country?: string;
  language?: 'en' | 'zh' | 'ja';
}

const { country = 'US', language = 'en' } = Astro.props;
---

<div id="mock-address-generator" class="mock-generator-container">
  <h3>Mock Address Generator</h3>
  
  <div class="controls">
    <select id="countrySelect">
      <option value="US">United States</option>
      <option value="CN">China</option>
      <option value="JP">Japan</option>
      <option value="HK">Hong Kong</option>
      <option value="TW">Taiwan</option>
      <option value="GB">United Kingdom</option>
      <option value="CA">Canada</option>
    </select>
    
    <button id="generateBtn">Generate Address</button>
    <button id="copyBtn">Copy</button>
  </div>
  
  <div id="result" class="result-box">
    <p id="addressText">Click "Generate" to create a mock address</p>
  </div>
</div>

<style>
  .mock-generator-container {
    padding: 1.5rem;
    border: 1px solid #ddd;
    border-radius: 8px;
    margin: 1rem 0;
  }
  
  .controls {
    display: flex;
    gap: 0.5rem;
    margin: 1rem 0;
  }
  
  select, button {
    padding: 0.5rem 1rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:hover {
    background: #f0f0f0;
  }
  
  .result-box {
    background: #f9f9f9;
    padding: 1rem;
    border-radius: 4px;
    margin-top: 1rem;
    font-family: monospace;
    white-space: pre-wrap;
  }
</style>

<script>
  import { addressLoader } from '../lib/addressDataLoader';
  
  const generateBtn = document.getElementById('generateBtn');
  const copyBtn = document.getElementById('copyBtn');
  const countrySelect = document.getElementById('countrySelect') as HTMLSelectElement;
  const addressText = document.getElementById('addressText')!;
  
  generateBtn?.addEventListener('click', async () => {
    const country = countrySelect.value;
    const city = await addressLoader.getRandomCity(country);
    const name = await addressLoader.getRandomName();
    
    const address = `${name.first} ${name.last}
${city}, ${country}`;
    
    addressText.textContent = address;
  });
  
  copyBtn?.addEventListener('click', () => {
    navigator.clipboard.writeText(addressText.textContent || '');
    alert('Copied!');
  });
</script>
```

---

### 第 4 步：在 Tools 页面中使用

在 `src/pages/tools/index.astro` 中添加：

```astro
---
import MockAddressGenerator from '../../components/MockAddressGenerator.astro'
---

<div class="tool-card">
  <h2>Mock Address Generator</h2>
  <MockAddressGenerator client:load country="US" />
</div>
```

---

### 第 5 步：测试

```bash
cd astro-paper
npm run dev
```

访问 `http://localhost:3000/tools/` 测试

---

## 📋 集成检查清单

- [ ] 数据文件复制到 `public/data/address/`
- [ ] 确认所有 19 个 JSON 文件都存在
- [ ] 创建 `src/lib/addressDataLoader.ts`
- [ ] 创建 `src/components/MockAddressGenerator.astro`
- [ ] 在 tools 页面中引入组件
- [ ] 运行 `npm run dev` 测试
- [ ] 检查浏览器控制台是否有错误
- [ ] 验证数据正确加载

---

## 🔧 高级配置

### 使用 Environment Variables

```env
# .env
PUBLIC_ADDRESS_DATA_PATH=/data/address/
PUBLIC_ADDRESS_CACHE_TTL=3600000
```

### 添加更多功能

```typescript
// 生成完整地址
async generateFullAddress(country: string) {
  const city = await this.getRandomCity(country);
  const name = await this.getRandomName();
  const streets = await this.streets();
  
  return `${name.first} ${name.last}
123 ${streets.en[0]} Street
${city}, ${country} 12345`;
}

// 生成 SIM 卡号
async generateSimCard() {
  return '86' + Math.random().toString().substring(2, 12);
}

// 生成虚拟 MAC 地址
async generateMacAddress() {
  const mac = await this.macOui();
  if (!mac || mac.length === 0) return '00:00:00:00:00:00';
  
  const oui = mac[Math.floor(Math.random() * mac.length)].oui;
  const last3 = Array(3).fill(0)
    .map(() => Math.floor(Math.random() * 256)
      .toString(16)
      .padStart(2, '0'))
    .join(':');
  
  return `${oui}:${last3}`;
}
```

---

## 📊 性能优化

**缓存策略：**

```typescript
// 使用 browser caching
const CACHE_KEY = 'address_data_v1';
const CACHE_TTL = 24 * 60 * 60 * 1000; // 24 小时

async loadData(filename: string): Promise<any> {
  const cacheKey = `${CACHE_KEY}_${filename}`;
  const cached = localStorage.getItem(cacheKey);
  
  if (cached) {
    const { data, timestamp } = JSON.parse(cached);
    if (Date.now() - timestamp < CACHE_TTL) {
      return data;
    }
  }
  
  const data = await fetch(`/data/address/${filename}`).then(r => r.json());
  localStorage.setItem(cacheKey, JSON.stringify({
    data,
    timestamp: Date.now()
  }));
  
  return data;
}
```

---

## ✅ 验证清单

运行后检查：

```bash
# 1. 检查文件是否存在
ls -la astro-paper/public/data/address/*.json

# 2. 运行构建
cd astro-paper && npm run build

# 3. 检查输出日志中是否有错误
npm run dev 2>&1 | grep -i error

# 4. 在浏览器开发者工具中检查网络请求
# Network 标签 → Filter by XHR → 应该能看到对 JSON 文件的请求
```

---

## 🎉 完成！

现在你的 Astro-Paper 已经集成了完整的 MockAddress 数据系统，可以：

✅ 生成虚拟地址  
✅ 随机请求城市和名字  
✅ 提供多国数据  
✅ 支持 MAC 地址生成  
✅ 完全离线运行  

**接下来？** 可以继续扩展功能，比如：
- 与 MockAddress 引擎集成
- 添加邮编生成
- 集成电话号码格式
- 添加 UI 主题选择

---

**如有问题？** 检查 [SCRAPER_GUIDE.md](SCRAPER_GUIDE.md) 了解如何更新数据。
