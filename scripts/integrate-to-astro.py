#!/usr/bin/env python3
"""
快速集成脚本 - 将地址数据复制到 astro-paper 项目
"""

import json
import shutil
from pathlib import Path

# 路径配置
ADDRESS_DIR = Path(__file__).parent.absolute()
ASTRO_PROJECT = ADDRESS_DIR.parent / "astro-paper"
ASTRO_PUBLIC_DATA = ASTRO_PROJECT / "public" / "data" / "address"

def copy_data():
    """复制所有JSON数据到Astro项目"""
    print("\n" + "="*70)
    print("📦 快速集成到 astro-paper")
    print("="*70 + "\n")
    
    # 创建目标目录
    ASTRO_PUBLIC_DATA.mkdir(parents=True, exist_ok=True)
    print(f"✓ 目录已创建: {ASTRO_PUBLIC_DATA}\n")
    
    # 复制所有JSON文件
    copied = 0
    for json_file in sorted(ADDRESS_DIR.glob("*.json")):
        dest = ASTRO_PUBLIC_DATA / json_file.name
        shutil.copy2(json_file, dest)
        size_kb = dest.stat().st_size / 1024
        print(f"  {json_file.name:30} → {size_kb:7.1f} KB")
        copied += 1
    
    print(f"\n✓ {copied} 个数据文件已复制\n")

def create_typescript_loader():
    """创建TypeScript数据加载器"""
    loader_code = '''// src/lib/addressDataLoader.ts
/**
 * Address Data Loader - 地址数据加载器
 * Dynamically loads address data from public/data/address/
 */

export interface AddressData {
  [key: string]: {
    state?: string;
    province?: string;
    country?: string;
    region?: string;
    cities?: string[];
    [key: string]: any;
  };
}

let cachedData: { [key: string]: AddressData } = {};

export async function loadAddressData(filename: string): Promise<AddressData> {
  if (cachedData[filename]) {
    return cachedData[filename];
  }
  
  try {
    const response = await fetch(`/data/address/${filename}`);
    if (!response.ok) throw new Error(`Failed to load ${filename}`);
    const data = await response.json();
    cachedData[filename] = data;
    return data;
  } catch (error) {
    console.error(`Error loading address data: ${filename}`, error);
    return {};
  }
}

export async function getUsStates(): Promise<AddressData> {
  return loadAddressData('usData.json');
}

export async function getChinaProvinces(): Promise<AddressData> {
  return loadAddressData('cnData.json');
}

export async function getJapanPrefectures(): Promise<AddressData> {
  return loadAddressData('jpData.json');
}

export async function getAllAddressData(): Promise<{
  us: AddressData;
  cn: AddressData;
  jp: AddressData;
}> {
  return {
    us: await getUsStates(),
    cn: await getChinaProvinces(),
    jp: await getJapanPrefectures(),
  };
}
'''
    
    loader_file = ASTRO_PROJECT / "src" / "lib" / "addressDataLoader.ts"
    loader_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(loader_file, 'w', encoding='utf-8') as f:
        f.write(loader_code)
    
    print(f"✓ TypeScript Loader 已创建: {loader_file.relative_to(ASTRO_PROJECT)}\n")

def create_astro_component():
    """创建Astro组件"""
    component_code = '''---
// src/components/AddressGenerator.astro
/**
 * Address Generator Component
 * Mock address generator using local address data
 */

import type { AddressData } from '../lib/addressDataLoader';

interface Props {
  country?: 'US' | 'CN' | 'JP';
  style?: string;
}

const { country = 'US' } = Astro.props;
---

<div class="address-generator" data-country={country}>
  <h2>📍 Address Generator</h2>
  
  <div class="generator-form">
    <label>
      <span>Country:</span>
      <select id="country-select">
        <option value="US">United States</option>
        <option value="CN">China</option>
        <option value="JP">Japan</option>
      </select>
    </label>
    
    <label>
      <span>State/Province:</span>
      <select id="state-select">
        <option>Select a state...</option>
      </select>
    </label>
    
    <label>
      <span>City:</span>
      <select id="city-select">
        <option>Select a city...</option>
      </select>
    </label>
    
    <button id="generate-btn" class="btn-primary">Generate Address</button>
  </div>
  
  <div id="result" class="result-box" style="display: none;">
    <h3>Generated Address:</h3>
    <pre id="address-output"></pre>
    <button id="copy-btn" class="btn-secondary">📋 Copy</button>
  </div>
</div>

<style>
  .address-generator {
    max-width: 600px;
    margin: 2rem auto;
    padding: 2rem;
    border: 2px solid var(--color-primary, #007bff);
    border-radius: 8px;
    background: var(--bg-secondary, #f8f9fa);
  }
  
  .generator-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin: 1.5rem 0;
  }
  
  label {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    font-weight: 500;
  }
  
  select, input, button {
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
  }
  
  button {
    cursor: pointer;
    background: var(--color-primary, #007bff);
    color: white;
    border: none;
    margin-top: 1rem;
  }
  
  button:hover {
    opacity: 0.9;
  }
  
  .result-box {
    margin-top: 2rem;
    padding: 1.5rem;
    background: white;
    border-radius: 4px;
    border-left: 4px solid var(--color-primary, #007bff);
  }
  
  pre {
    background: #f5f5f5;
    padding: 1rem;
    border-radius: 4px;
    overflow-x: auto;
    font-size: 0.9rem;
  }
</style>

<script>
  // Dynamic loading of address data
  async function initAddressGenerator() {
    const countrySelect = document.getElementById('country-select') as HTMLSelectElement;
    const stateSelect = document.getElementById('state-select') as HTMLSelectElement;
    const citySelect = document.getElementById('city-select') as HTMLSelectElement;
    const generateBtn = document.getElementById('generate-btn');
    const resultBox = document.getElementById('result');
    const addressOutput = document.getElementById('address-output');
    const copyBtn = document.getElementById('copy-btn');
    
    let currentData: Record<string, any> = {};
    
    // Load initial data
    async function loadCountryData(country: string) {
      let filename = 'usData.json';
      if (country === 'CN') filename = 'cnData.json';
      if (country === 'JP') filename = 'jpData.json';
      
      try {
        const response = await fetch(`/data/address/${filename}`);
        currentData = await response.json();
        
        // Update state select
        stateSelect.innerHTML = '<option>Select a state...</option>';
        Object.keys(currentData).forEach(key => {
          const option = document.createElement('option');
          option.value = key;
          option.textContent = currentData[key].state || currentData[key].province || key;
          stateSelect.appendChild(option);
        });
        
        citySelect.innerHTML = '<option>Select a city...</option>';
      } catch (error) {
        console.error('Failed to load data:', error);
      }
    }
    
    // Update cities when state changes
    stateSelect.addEventListener('change', () => {
      const state = stateSelect.value;
      citySelect.innerHTML = '<option>Select a city...</option>';
      
      if (state && currentData[state]) {
        const cities = currentData[state].cities || [];
        cities.forEach((city: string) => {
          const option = document.createElement('option');
          option.value = city;
          option.textContent = city;
          citySelect.appendChild(option);
        });
      }
    });
    
    // Generate address
    generateBtn?.addEventListener('click', () => {
      const country = countrySelect.value;
      const state = stateSelect.value;
      const city = citySelect.value;
      
      if (!state || !city) {
        alert('Please select state and city');
        return;
      }
      
      const address = `${city}, ${currentData[state].state || currentData[state].province || state}, ${country}`;
      
      if (addressOutput) {
        addressOutput.textContent = address;
      }
      
      if (resultBox) {
        resultBox.style.display = 'block';
      }
    });
    
    // Copy to clipboard
    copyBtn?.addEventListener('click', () => {
      const text = addressOutput?.textContent;
      if (text) {
        navigator.clipboard.writeText(text).then(() => {
          copyBtn.textContent = '✅ Copied!';
          setTimeout(() => {
            copyBtn.textContent = '📋 Copy';
          }, 2000);
        });
      }
    });
    
    // Initialize with US data
    await loadCountryData('US');
    
    // Handle country change
    countrySelect.addEventListener('change', () => {
      loadCountryData(countrySelect.value);
    });
  }
  
  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAddressGenerator);
  } else {
    initAddressGenerator();
  }
</script>
'''
    
    component_file = ASTRO_PROJECT / "src" / "components" / "AddressGenerator.astro"
    component_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(component_file, 'w', encoding='utf-8') as f:
        f.write(component_code)
    
    print(f"✓ Astro 组件已创建: {component_file.relative_to(ASTRO_PROJECT)}\n")

def create_integration_guide():
    """创建集成指南"""
    guide = '''# 🏙️ Address Generator Integration Guide

## Status: ✅ Ready to Use

Your address database has been successfully set up and is ready to integrate into astro-paper.

### Quick Start

#### 1. Use in Astro Pages

```astro
---
// src/pages/tools/address-generator.astro
import AddressGenerator from '../../components/AddressGenerator.astro';
---

<layout title="Address Generator">
  <AddressGenerator client:load />
</layout>
```

#### 2. Use in React Components

```typescript
// src/components/AddressGeneratorReact.tsx
import { useState, useEffect } from 'react';
import { loadAddressData } from '../lib/addressDataLoader';

export default function AddressGeneratorReact() {
  const [data, setData] = useState({});
  
  useEffect(() => {
    loadAddressData('usData.json').then(setData);
  }, []);
  
  // ... rest of component
}
```

### Available Data Files

```
public/data/address/
├── usData.json          (50 states × 20 cities = 1000 entries)
├── cnData.json          (7 provinces × 2-6 cities = 43 entries)
├── jpData.json          (5 prefectures × 4-5 cities = 22 entries)
├── gbData.json          (10 major cities)
├── deData.json          (46 cities)
├── inData.json          (49 cities)
├── caData.json          (44 cities)
├── auData.json          (32 cities)
├── hkData.json          (26 districts)
└── ... (other countries)
```

### Data Format

```json
{
  "AL": {
    "state": "Alabama",
    "cities": ["Birmingham", "Montgomery", "Mobile", ...]
  },
  "AK": {
    "state": "Alaska",
    "cities": ["Anchorage", "Juneau", ...]
  }
}
```

### Performance Tips

1. **Lazy Load by Country**: Only fetch the data you need
   ```typescript
   const usData = await loadAddressData('usData.json');
   ```

2. **Cache Data**: The loader automatically caches loaded data
   - First load: API request from /data/address/
   - Subsequent loads: From memory

3. **Pre-load in Static Pages**: For better UX
   ```astro
   ---
   const usData = fetch('/data/address/usData.json')
     .then(r => r.json());
   ---
   ```

### Customization

To add more countries or cities:

1. Edit the data JSON files directly in `public/data/address/`
2. Or re-run the data builder:
   ```bash
   cd address
   python build-complete-data.py
   ```

### Deployment

1. Ensure `public/data/address/` is included in your build
2. For Netlify/Vercel: No special config needed
3. For self-hosted: Verify public folder is served correctly

### Support

For questions or to enhance the data:
- Add more cities: Edit JSON files directly
- Generate more data: Run `python build-complete-data.py`
- Use proxy scraper: Run `python scrape-with-proxy.py`

---

**Data updated**: 2024
**Total entries**: 1,286+ cities
**Coverage**: 11+ countries/regions
'''
    
    guide_file = ASTRO_PROJECT / "ADDRESS_INTEGRATION.md"
    
    with open(guide_file, 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print(f"✓ 集成指南已创建: {guide_file.relative_to(ASTRO_PROJECT)}\n")

def main():
    print(f"\n当前项目位置: {ASTRO_PROJECT.relative_to(ASTRO_PROJECT.parent)}\n")
    
    if not ASTRO_PROJECT.exists():
        print(f"❌ 错误: 找不到 astro-paper 项目")
        print(f"   期望位置: {ASTRO_PROJECT}")
        return
    
    copy_data()
    create_typescript_loader()
    create_astro_component()
    create_integration_guide()
    
    print("="*70)
    print("✅ 集成完成！")
    print("="*70)
    print("\n📝 后续步骤：\n")
    print("1. 在 astro-paper 页面中导入组件：")
    print("   import AddressGenerator from '@/components/AddressGenerator.astro';")
    print("\n2. 使用组件：")
    print("   <AddressGenerator client:load />")
    print("\n3. 在浏览器中打开 http://localhost:3000/tools/address-generator")
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()
