import json
from pathlib import Path

output_dir = Path(__file__).parent
data_dir = output_dir

print("\n📊 数据统计报告\n" + "="*50)

total_cities = 0
total_names = 0
total_files = 0
total_bytes = 0

for json_file in sorted(data_dir.glob("*.json")):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    size_kb = json_file.stat().st_size / 1024
    total_bytes += json_file.stat().st_size
    total_files += 1
    
    # 计数
    if isinstance(data, dict):
        if "cities" in data:
            count = len(data["cities"])
        else:
            count = sum(len(v.get("cities", [])) if isinstance(v, dict) else 0 for v in data.values())
            if count == 0 and "provinces" in data:
                count = len(data.get("provinces", []))
        
        if "names" in json_file.name.lower():
            total_names += len(data.get("male", [])) + len(data.get("female", []))
        else:
            total_cities += count
        
        print(f"{json_file.name:30} {size_kb:8.1f} KB  ({count:5} items)")
    else:
        print(f"{json_file.name:30} {size_kb:8.1f} KB")

print("\n" + "="*50)
print(f"总文件数: {total_files}")
print(f"总数据量: {total_bytes / 1024:.1f} KB")
print(f"总城市数: {total_cities}")
print(f"总名字数: {total_names}")
print("="*50)

# 详细检查美国数据
print("\n🇺🇸 美国州数据详情：")
with open(data_dir / "usData.json", 'r', encoding='utf-8') as f:
    us_data = json.load(f)

states = list(us_data.keys())
print(f"  州数量: {len(states)}")
print(f"  首个州 ({states[0]}): {len(us_data[states[0]]['cities'])} 个城市")
if len(states) > 1:
    print(f"  最后一州 ({states[-1]}): {len(us_data[states[-1]]['cities'])} 个城市")
sample_state = states[2]
print(f"\n样本州 ({sample_state}):")
print(f"  {us_data[sample_state]['cities'][:5]}")
