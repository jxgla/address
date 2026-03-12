#!/usr/bin/env python3
"""
项目整理脚本 - 분类整理 address 项目文件
将混乱的文件组织成标准目录结构
"""

import os
import shutil
from pathlib import Path

def organize_project():
    """整理项目结构"""
    
    root = Path(__file__).parent.absolute()
    
    # 创建目录
    dirs = {
        'data': root / 'data',
        'scripts': root / 'scripts',
        'docs': root / 'docs',
    }
    
    for dir_name, dir_path in dirs.items():
        dir_path.mkdir(exist_ok=True)
        print(f"✓ 目录已创建: {dir_name}/")
    
    # 文件分类规则
    file_rules = {
        'data': [
            '*.json',  # 所有 JSON 数据文件
        ],
        'scripts': [
            '*.py',    # 所有 Python 脚本
        ],
        'docs': [
            '*.md',    # 所有 Markdown 文档
        ],
    }
    
    # 执行文件移动
    moved_count = 0
    skipped_count = 0
    
    for category, patterns in file_rules.items():
        target_dir = dirs[category]
        
        for pattern in patterns:
            for file in root.glob(pattern):
                # 跳过已在目标目录中的文件
                if file.parent == target_dir:
                    continue
                
                # 不移动脚本本身
                if file.name == 'organize_project.py':
                    continue
                
                try:
                    dest = target_dir / file.name
                    shutil.move(str(file), str(dest))
                    print(f"  ✓ 移动: {file.name} → {category}/")
                    moved_count += 1
                except Exception as e:
                    print(f"  ✗ 错误: {file.name} - {e}")
                    skipped_count += 1
    
    print("\n" + "="*60)
    print(f"整理完成！")
    print(f"  ✓ 移动: {moved_count} 个文件")
    print(f"  ⚠ 跳过: {skipped_count} 个文件")
    print("\n新目录结构:")
    print("""
address/
├── data/
│   ├── usData.json
│   ├── cnData.json
│   ├── jpData.json
│   ├── usTaxFreeStates.json      ← 新增！
│   └── ... (所有 .json 文件)
│
├── scripts/
│   ├── build-complete-data.py
│   ├── check-data.py
│   ├── scrape-with-proxy.py
│   └── ... (所有 .py 脚本)
│
├── docs/
│   ├── README.md
│   ├── QUICK_START.md
│   ├── SCRAPER_GUIDE.md
│   └── ... (所有文档)
│
└── organize_project.py            (本脚本)
    """)

if __name__ == "__main__":
    organize_project()
