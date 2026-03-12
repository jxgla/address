#!/usr/bin/env python3
"""
直接构建完整美国数据 - 不走网络爬虫，直接扩充现有数据
"""

import json
from pathlib import Path
from faker import Faker

OUTPUT_DIR = Path(__file__).parent.absolute()

# 所有 50 州及其真实城市样本（从维基百科知识库）
REAL_US_CITIES = {
    "AL": {"state": "Alabama", "cities": ["Birmingham", "Montgomery", "Mobile", "Huntsville", "Tuscaloosa", "Auburn", "Gadsden", "Dothan", "Bessemer", "Anniston"]},
    "AK": {"state": "Alaska", "cities": ["Anchorage", "Juneau", "Fairbanks", "Ketchikan", "Sitka", "Kodiak", "Palmer", "Kenai", "Bethel", "Wasilla"]},
    "AZ": {"state": "Arizona", "cities": ["Phoenix", "Mesa", "Chandler", "Scottsdale", "Glendale", "Gilbert", "Tempe", "Peoria", "Surprise", "Tucson"]},
    "AR": {"state": "Arkansas", "cities": ["Little Rock", "Fort Smith", "Fayetteville", "Springdale", "Jonesboro", "North Little Rock", "Conway", "Rogers", "Pine Bluff", "Bentonville"]},
    "CA": {"state": "California", "cities": ["Los Angeles", "San Diego", "San Jose", "San Francisco", "Fresno", "Long Beach", "Sacramento", "Oakland", "Stockton", "Irvine"]},
    "CO": {"state": "Colorado", "cities": ["Denver", "Colorado Springs", "Aurora", "Fort Collins", "Lakewood", "Longmont", "Greeley", "Boulder", "Arvada", "Fountain"]},
    "CT": {"state": "Connecticut", "cities": ["Bridgeport", "New Haven", "Hartford", "Stamford", "Waterbury", "Danbury", "New Britain", "West Hartford", "Norwalk", "Meriden"]},
    "DE": {"state": "Delaware", "cities": ["Wilmington", "Dover", "Newark", "Smyrna", "Elsmere", "New Castle", "Middletown", "Milford", "Seaford", "Georgetown"]},
    "FL": {"state": "Florida", "cities": ["Jacksonville", "Miami", "Tampa", "Orlando", "St. Petersburg", "Hialeah", "Fort Lauderdale", "Tallahassee", "Port Saint Lucie", "Cape Coral"]},
    "GA": {"state": "Georgia", "cities": ["Atlanta", "Augusta", "Columbus", "Savannah", "Athens", "Sandy Springs", "Marietta", "Roswell", "Macon", "Alpharetta"]},
    "HI": {"state": "Hawaii", "cities": ["Honolulu", "Pearl City", "Kailua", "Kaneohe", "Waipahu", "Mililani", "Kahului", "Hilo", "Kapolei", "Wailea"]},
    "ID": {"state": "Idaho", "cities": ["Boise", "Meridian", "Pocatello", "Idaho Falls", "Nampa", "Caldwell", "Coeur d'Alene", "Twin Falls", "Rexburg", "Moscow"]},
    "IL": {"state": "Illinois", "cities": ["Chicago", "Aurora", "Rockford", "Joliet", "Naperville", "Springfield", "Peoria", "Elgin", "Waukegan", "Champaign"]},
    "IN": {"state": "Indiana", "cities": ["Indianapolis", "Fort Wayne", "Evansville", "South Bend", "Mishawaka", "Bloomington", "Lafayette", "Carmel", "Muncie", "Anderson"]},
    "IA": {"state": "Iowa", "cities": ["Des Moines", "Cedar Rapids", "Davenport", "Sioux City", "Iowa City", "Waterloo", "Council Bluffs", "Dubuque", "Ames", "Urbandale"]},
    "KS": {"state": "Kansas", "cities": ["Kansas City", "Wichita", "Overland Park", "Topeka", "Olathe", "Lawrence", "Shawnee", "Salina", "Manhattan", "Leawood"]},
    "KY": {"state": "Kentucky", "cities": ["Louisville", "Lexington", "Bowling Green", "Covington", "Owensboro", "Hopkinsville", "Louisville Metro", "Richmond", "Newport", "Paducah"]},
    "LA": {"state": "Louisiana", "cities": ["New Orleans", "Baton Rouge", "Shreveport", "Lafayette", "Lake Charles", "Kenner", "Alexandria", "Monroe", "Metairie", "Houma"]},
    "ME": {"state": "Maine", "cities": ["Portland", "Lewiston", "Bangor", "Augusta", "Auburn", "Biddeford", "Sanford", "Waterville", "Brewer", "Westbrook"]},
    "MD": {"state": "Maryland", "cities": ["Baltimore", "Columbia", "Hagerstown", "Annapolis", "Gaithersburg", "Bowie", "Frederick", "Salisbury", "Glen Burnie", "Takoma Park"]},
    "MA": {"state": "Massachusetts", "cities": ["Boston", "Worcester", "Springfield", "Lowell", "Cambridge", "New Bedford", "Brockton", "Quincy", "Lynn", "Fall River"]},
    "MI": {"state": "Michigan", "cities": ["Detroit", "Grand Rapids", "Warren", "Sterling Heights", "Ann Arbor", "Lansing", "Flint", "Dearborn", "Livonia", "Westland"]},
    "MN": {"state": "Minnesota", "cities": ["Minneapolis", "Saint Paul", "Rochester", "Duluth", "Saint Cloud", "Bloomington", "Brooklyn Park", "Plymouth", "Maple Grove", "Coon Rapids"]},
    "MS": {"state": "Mississippi", "cities": ["Jackson", "Gulfport", "Biloxi", "Hattiesburg", "Meridian", "Vicksburg", "Ridgeland", "Greenville", "Tupelo", "Southaven"]},
    "MO": {"state": "Missouri", "cities": ["Kansas City", "St. Louis", "Springfield", "Independence", "Columbia", "St. Peters", "Lee's Summit", "St. Charles", "Joplin", "O'Fallon"]},
    "MT": {"state": "Montana", "cities": ["Billings", "Missoula", "Great Falls", "Butte", "Bozeman", "Helena", "Kalispell", "Havre", "Miles City", "Anaconda"]},
    "NE": {"state": "Nebraska", "cities": ["Omaha", "Lincoln", "Bellevue", "Grand Island", "Kearney", "Fremont", "Norfolk", "Hastings", "North Platte", "Columbus"]},
    "NV": {"state": "Nevada", "cities": ["Las Vegas", "Henderson", "North Las Vegas", "Reno", "Paradise", "Sunrise Manor", "Spring Valley", "Enterprise", "Sparks", "Elko"]},
    "NH": {"state": "New Hampshire", "cities": ["Manchester", "Nashua", "Concord", "Rochester", "Dover", "Durham", "Keene", "Newington", "Laconia", "Lebanon"]},
    "NJ": {"state": "New Jersey", "cities": ["Newark", "Jersey City", "Elizabeth", "Paterson", "Trenton", "Atlantic City", "Asbury Park", "Camden", "Clifton", "Passaic"]},
    "NM": {"state": "New Mexico", "cities": ["Albuquerque", "Las Cruces", "Santa Fe", "Rio Rancho", "Lynn", "Clovis", "Roswell", "Gallup", "Hobbs", "Farmington"]},
    "NY": {"state": "New York", "cities": ["New York City", "Buffalo", "Rochester", "Yonkers", "Syracuse", "Albany", "Utica", "New Rochelle", "Troy", "Cortland"]},
    "NC": {"state": "North Carolina", "cities": ["Charlotte", "Raleigh", "Greensboro", "Durham", "Winston-Salem", "Fayetteville", "Cary", "Wilmington", "High Point", "Greenville"]},
    "ND": {"state": "North Dakota", "cities": ["Bismarck", "Fargo", "Grand Forks", "Minot", "Williston", "Ward", "Dickinson", "Mandan", "Jamestown", "Watford City"]},
    "OH": {"state": "Ohio", "cities": ["Columbus", "Cleveland", "Cincinnati", "Toledo", "Akron", "Dayton", "Parma", "Canton", "Youngstown", "Gahanna"]},
    "OK": {"state": "Oklahoma", "cities": ["Oklahoma City", "Tulsa", "Norman", "Broken Arrow", "Edmond", "Moore", "Lawton", "Enid", "Muskogee", "Shawnee"]},
    "OR": {"state": "Oregon", "cities": ["Portland", "Eugene", "Salem", "Gresham", "Hillsboro", "Beaverton", "Bend", "Medford", "Springfield", "Corvallis"]},
    "PA": {"state": "Pennsylvania", "cities": ["Philadelphia", "Pittsburgh", "Allentown", "Erie", "Reading", "Scranton", "Bethlehem", "Lancaster", "Harrisburg", "Altoona"]},
    "RI": {"state": "Rhode Island", "cities": ["Providence", "Warwick", "Cranston", "Pawtucket", "Woonsocket", "Newport", "Central Falls", "West Warwick", "Coventry", "Westerly"]},
    "SC": {"state": "South Carolina", "cities": ["Charleston", "Columbia", "Greenville", "Spartanburg", "Sumter", "Rock Hill", "Myrtle Beach", "Florence", "Goose Creek", "Wilmington"]},
    "SD": {"state": "South Dakota", "cities": ["Sioux Falls", "Rapid City", "Aberdeen", "Watertown", "Brookings", "Pierre", "Mitchell", "Yankton", "Vermillion", "Huron"]},
    "TN": {"state": "Tennessee", "cities": ["Memphis", "Nashville", "Knoxville", "Chattanooga", "Clarksville", "Murfreesboro", "Franklin", "Johnson City", "Collegedale", "Germantown"]},
    "TX": {"state": "Texas", "cities": ["Houston", "Phoenix", "San Antonio", "Dallas", "Austin", "Fort Worth", "El Paso", "Arlington", "Corpus Christi", "Plano"]},
    "UT": {"state": "Utah", "cities": ["Salt Lake City", "Provo", "West Valley City", "Orem", "Sandy", "Ogden", "St. George", "Layton", "Taylorsville", "Lehi"]},
    "VT": {"state": "Vermont", "cities": ["Burlington", "Rutland", "South Burlington", "Montpelier", "Barre", "Benningon", "Brattleboro", "Derby", "Northfield", "Winooski"]},
    "VA": {"state": "Virginia", "cities": ["Virginia Beach", "Norfolk", "Richmond", "Alexandria", "Newport News", "Hampton", "Arlington", "Blacksburg", "Roanoke", "Lynchburg"]},
    "WA": {"state": "Washington", "cities": ["Seattle", "Spokane", "Tacoma", "Vancouver", "Bellevue", "Kent", "Everett", "Renton", "Federal Way", "Kirkland"]},
    "WV": {"state": "West Virginia", "cities": ["Charleston", "Huntington", "Parkersburg", "Morgantown", "Wheeling", "Fairmont", "Weirton", "Beckley", "Bluefield", "Princeton"]},
    "WI": {"state": "Wisconsin", "cities": ["Milwaukee", "Madison", "Green Bay", "Kenosha", "Racine", "Appleton", "Waukesha", "Eau Claire", "La Crosse", "Oshkosh"]},
    "WY": {"state": "Wyoming", "cities": ["Cheyenne", "Laramie", "Casper", "Gillette", "Rock Springs", "Sheridan", "Cody", "Jackson Hole", "Evanston", "Green River"]},
}

def expand_cities_with_faker():
    """使用 Faker 为每个州补充城市"""
    fake = Faker('en_US')
    
    print_text = "\n" + "="*70
    print_text += "\n🏙️  扩充美国所有50州城市数据\n"
    print_text += "="*70 + "\n"
    
    us_data = {}
    total_new = 0
    
    for state_code, state_info in REAL_US_CITIES.items():
        state_name = state_info["state"]
        cities = state_info["cities"].copy()
        
        # 用 Faker 再补充 10 个城市
        for _ in range(10):
            city = fake.city()
            if city not in cities:
                cities.append(city)
        
        us_data[state_code] = {
            "state": state_name,
            "cities": cities[:25]  # 限制到 25 个
        }
        
        total_new += len(cities)
        print_text += f"  {state_code}: {state_name:20} → {len(cities):3} cities\n"
    
    # 保存
    output_file = OUTPUT_DIR / "usData.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(us_data, f, ensure_ascii=False, indent=2)
    
    size_kb = output_file.stat().st_size / 1024
    print_text += "\n" + "="*70
    print_text += f"\n✅ 美国数据已保存: {size_kb:.1f} KB\n"
    print_text += f"   • 50 个州\n   • {total_new} 个城市\n"
    print_text += "="*70 + "\n"
    
    print(print_text)
    return us_data

def enhance_other_countries():
    """补充其他国家数据"""
    print("🌍 补充其他国家数据...\n")
    
    # 中国各省主要城市（补充现有数据）
    cn_major = {
        "北京": ["北京", "朝阳", "东城", "西城", "海淀", "丰台", "石景山"],
        "上海": ["上海", "黄浦", "浦东", "静安", "徐汇", "长宁"],
        "广东": ["广州", "深圳", "珠海", "汕头", "韶关", "佛山"],
        "浙江": ["杭州", "宁波", "嘉兴", "湖州", "绍兴", "金华"],
        "江苏": ["南京", "苏州", "南通", "扬州", "镇江", "常州"],
        "四川": ["成都", "自贡", "攀枝花", "泸州", "德阳", "绵阳"],
        "福建": ["福州", "厦门", "漳州", "泉州", "龙岩", "三明"],
    }
    
    cn_data = {}
    for province, cities in cn_major.items():
        cn_data[province] = {"province": province, "cities": cities}
    
    cn_file = OUTPUT_DIR / "cnData.json"
    with open(cn_file, 'w', encoding='utf-8') as f:
        json.dump(cn_data, f, ensure_ascii=False, indent=2)
    
    print(f"  ✓ China: 7 provinces, {sum(len(c) for c in cn_data.values())} cities")
    
    # 日本各都道府县主要城市
    jp_major = {
        "東京": ["東京", "新宿", "渋谷", "品川", "千代田"],
        "大阪": ["大阪", "梅田", "心斎橋", "難波", "北新地"],
        "神奈川": ["横浜", "川崎", "相模原", "横須賀"],
        "京都": ["京都", "伏見", "右京", "左京"],
        "兵庫": ["神戸", "姫路", "尼崎", "明石"],
    }
    
    jp_data = {}
    for pref, cities in jp_major.items():
        jp_data[pref] = {"prefecture": pref, "cities": cities}
    
    jp_file = OUTPUT_DIR / "jpData.json"
    with open(jp_file, 'w', encoding='utf-8') as f:
        json.dump(jp_data, f, ensure_ascii=False, indent=2)
    
    print(f"  ✓ Japan: {len(jp_data)} prefectures")
    
    # 英国主要城市
    gb_cities = {
        "cities": ["London", "Manchester", "Birmingham", "Leeds", "Glasgow", "Liverpool", "Bristol", "York", "Oxford", "Cambridge"]
    }
    
    gb_file = OUTPUT_DIR / "gbData.json"
    with open(gb_file, 'w', encoding='utf-8') as f:
        json.dump(gb_cities, f, ensure_ascii=False, indent=2)
    
    print(f"  ✓ UK: 10 major cities")

if __name__ == "__main__":
    print("\n🚀 构建完整地址数据库\n")
    
    expand_cities_with_faker()
    enhance_other_countries()
    
    print("\n📊 最终统计：")
    import subprocess
    result = subprocess.run(
        ["python", "check-data.py"],
        cwd=OUTPUT_DIR,
        capture_output=True,
        text=True
    )
    print(result.stdout)
