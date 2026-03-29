const DATA_FILES = {
  US: "data/usData.json",
  CN: "data/cnData.json",
  JP: "data/jpData.json",
  KR: "data/krData.json",
  HK: "data/hkData.json",
  TW: "data/twData.json",
  GB: "data/gbData.json",
  DE: "data/deData.json",
  NL: "data/nlData.json",
  FR: "data/frData.json",
  ES: "data/esData.json",
  IT: "data/itData.json",
  BE: "data/beData.json",
  PT: "data/ptData.json",
  AT: "data/atData.json",
  CH: "data/chData.json",
  IE: "data/ieData.json",
  SE: "data/seData.json",
  NO: "data/noData.json",
  CA: "data/caData.json",
  AU: "data/auData.json",
  SG: "data/sgData.json",
};

const COUNTRY_META = {
  US: { label: "United States", locale: "en", dialing: "+1", postalLabel: "ZIP", nameProfile: "western" },
  CN: { label: "China", locale: "zh", dialing: "+86", postalLabel: "邮编", nameProfile: "cjk" },
  JP: { label: "Japan", locale: "ja", dialing: "+81", postalLabel: "邮编", nameProfile: "jp" },
  KR: { label: "South Korea", locale: "en", dialing: "+82", postalLabel: "Postal code", nameProfile: "western" },
  HK: { label: "Hong Kong", locale: "en", dialing: "+852", postalLabel: "Postcode", nameProfile: "western" },
  TW: { label: "Taiwan", locale: "zh", dialing: "+886", postalLabel: "邮递区号", nameProfile: "cjk" },
  GB: { label: "United Kingdom", locale: "en", dialing: "+44", postalLabel: "Postcode", nameProfile: "western" },
  DE: { label: "Germany", locale: "en", dialing: "+49", postalLabel: "PLZ", nameProfile: "western" },
  NL: { label: "Netherlands", locale: "en", dialing: "+31", postalLabel: "Postcode", nameProfile: "western" },
  FR: { label: "France", locale: "en", dialing: "+33", postalLabel: "Code postal", nameProfile: "western" },
  ES: { label: "Spain", locale: "en", dialing: "+34", postalLabel: "Codigo postal", nameProfile: "western" },
  IT: { label: "Italy", locale: "en", dialing: "+39", postalLabel: "CAP", nameProfile: "western" },
  BE: { label: "Belgium", locale: "en", dialing: "+32", postalLabel: "Postal code", nameProfile: "western" },
  PT: { label: "Portugal", locale: "en", dialing: "+351", postalLabel: "Codigo postal", nameProfile: "western" },
  AT: { label: "Austria", locale: "en", dialing: "+43", postalLabel: "Postleitzahl", nameProfile: "western" },
  CH: { label: "Switzerland", locale: "en", dialing: "+41", postalLabel: "PLZ", nameProfile: "western" },
  IE: { label: "Ireland", locale: "en", dialing: "+353", postalLabel: "Eircode", nameProfile: "western" },
  SE: { label: "Sweden", locale: "en", dialing: "+46", postalLabel: "Postcode", nameProfile: "western" },
  NO: { label: "Norway", locale: "en", dialing: "+47", postalLabel: "Postnummer", nameProfile: "western" },
  CA: { label: "Canada", locale: "en", dialing: "+1", postalLabel: "Postal code", nameProfile: "western" },
  AU: { label: "Australia", locale: "en", dialing: "+61", postalLabel: "Postcode", nameProfile: "western" },
  SG: { label: "Singapore", locale: "en", dialing: "+65", postalLabel: "Postal code", nameProfile: "mixed" },
};

const LOCALIZED_OUTPUT_COUNTRIES = new Set(["JP", "TW"]);
const DIGITS = "0123456789";

const DISPLAY_LABELS = {
  default: {
    region: "Region",
    nativeName: "Native name",
    englishName: "English name",
    line1: "Address Line 1",
    city: "City",
    country: "Country",
    postalCode: "Postal code",
    oneLineAddress: "One-line address",
    phone: "Phone number",
    email: "Email",
    birthDate: "Birth date",
    addressSection: "Address",
    nativeOutputBadge: "Native output",
    englishOutputBadge: "English output",
    nativeOneLineAddress: "Native one-line address",
    englishOneLineAddress: "English one-line address",
  },
  nativeLocalized: {
    region: "地区",
    nativeName: "本地名字",
    englishName: "English name",
    line1: "地址第一行",
    city: "城市",
    country: "国家",
    postalCode: "邮编",
    oneLineAddress: "一行地址",
    phone: "电话号码",
    email: "邮箱",
    birthDate: "出生日期",
    addressSection: "地址",
    nativeOutputBadge: "本地输出",
    englishOutputBadge: "English 输出",
    nativeOneLineAddress: "本地一行地址",
    englishOneLineAddress: "English 一行地址",
  },
  english: {
    region: "Region",
    nativeName: "Native name",
    englishName: "English name",
    line1: "Address Line 1",
    city: "City",
    country: "Country",
    postalCode: "Postal code",
    oneLineAddress: "One-line address",
    phone: "Phone number",
    email: "Email",
    birthDate: "Birth date",
    addressSection: "Address",
    nativeOutputBadge: "Native output",
    englishOutputBadge: "English output",
    nativeOneLineAddress: "Native one-line address",
    englishOneLineAddress: "English one-line address",
  },
};

const POSTAL_LABEL_OVERRIDES = {
  JP: {
    native: "邮编",
    english: "Postal code",
  },
  TW: {
    native: "郵遞區號",
    english: "Postal code",
  },
};

const JP_NAME_ROMAJI = {
  first: {
    太郎: "Taro",
    翔太: "Shota",
    大輝: "Daiki",
    蓮: "Ren",
    悠真: "Yuma",
    陽斗: "Haruto",
    直樹: "Naoki",
    健太: "Kenta",
    颯太: "Sota",
    拓海: "Takumi",
    大和: "Yamato",
    海斗: "Kaito",
    圭介: "Keisuke",
    雄大: "Yudai",
    一樹: "Kazuki",
    結衣: "Yui",
    葵: "Aoi",
    美咲: "Misaki",
    陽菜: "Hina",
    莉子: "Riko",
    彩花: "Ayaka",
    さくら: "Sakura",
    優奈: "Yuna",
    愛: "Ai",
    七海: "Nanami",
    真央: "Mao",
    花音: "Kanon",
    美月: "Mizuki",
    琴音: "Kotone",
    遥: "Haruka",
  },
  last: {
    佐藤: "Sato",
    鈴木: "Suzuki",
    高橋: "Takahashi",
    田中: "Tanaka",
    伊藤: "Ito",
    渡辺: "Watanabe",
    山本: "Yamamoto",
    中村: "Nakamura",
    小林: "Kobayashi",
    加藤: "Kato",
    吉田: "Yoshida",
    山田: "Yamada",
    佐々木: "Sasaki",
    山口: "Yamaguchi",
    松本: "Matsumoto",
  },
};

const TW_NAME_POOL = {
  male: [
    { native: "志明", english: "Zhiming" },
    { native: "建宏", english: "Jianhong" },
    { native: "冠宇", english: "Guanyu" },
    { native: "柏翰", english: "Bohan" },
    { native: "宇翔", english: "Yuxiang" },
    { native: "俊傑", english: "Junjie" },
    { native: "承恩", english: "Chengen" },
    { native: "家豪", english: "Jiahao" },
    { native: "哲維", english: "Zhewei" },
    { native: "子軒", english: "Zixuan" },
  ],
  female: [
    { native: "雅婷", english: "Yating" },
    { native: "怡君", english: "Yijun" },
    { native: "佳穎", english: "Jiaying" },
    { native: "佩珊", english: "Peishan" },
    { native: "思妤", english: "Siyu" },
    { native: "欣怡", english: "Xinyi" },
    { native: "婉婷", english: "Wanting" },
    { native: "詩涵", english: "Shihan" },
    { native: "郁婷", english: "Yuting" },
    { native: "心妤", english: "Xinyu" },
  ],
  last: [
    { native: "陳", english: "Chen" },
    { native: "林", english: "Lin" },
    { native: "王", english: "Wang" },
    { native: "張", english: "Zhang" },
    { native: "李", english: "Li" },
    { native: "黃", english: "Huang" },
    { native: "吳", english: "Wu" },
    { native: "蔡", english: "Cai" },
    { native: "劉", english: "Liu" },
    { native: "楊", english: "Yang" },
  ],
};

const LOCALIZED_OUTPUT_META = {
  JP: {
    country: { native: "日本", english: "Japan" },
    regions: {
      Japan: { native: "日本", english: "Japan" },
      Tokyo: { native: "東京都", english: "Tokyo" },
      "Osaka Prefecture": { native: "大阪府", english: "Osaka Prefecture" },
      "Kanagawa Prefecture": { native: "神奈川県", english: "Kanagawa Prefecture" },
      "Aichi Prefecture": { native: "愛知県", english: "Aichi Prefecture" },
      "Saitama Prefecture": { native: "埼玉県", english: "Saitama Prefecture" },
      "Chiba Prefecture": { native: "千葉県", english: "Chiba Prefecture" },
      Hokkaido: { native: "北海道", english: "Hokkaido" },
      "Fukuoka Prefecture": { native: "福岡県", english: "Fukuoka Prefecture" },
      "Kyoto Prefecture": { native: "京都府", english: "Kyoto Prefecture" },
      "Hyogo Prefecture": { native: "兵庫県", english: "Hyogo Prefecture" },
    },
    cities: {
      Tokyo: { native: "東京", english: "Tokyo" },
      Yokohama: { native: "横浜", english: "Yokohama" },
      Osaka: { native: "大阪", english: "Osaka" },
      Nagoya: { native: "名古屋", english: "Nagoya" },
      Sapporo: { native: "札幌", english: "Sapporo" },
      Fukuoka: { native: "福岡", english: "Fukuoka" },
      Kyoto: { native: "京都", english: "Kyoto" },
      Kobe: { native: "神戸", english: "Kobe" },
      Hachioji: { native: "八王子", english: "Hachioji" },
      Machida: { native: "町田", english: "Machida" },
      Fuchu: { native: "府中", english: "Fuchu" },
      Chofu: { native: "調布", english: "Chofu" },
      Sakai: { native: "堺", english: "Sakai" },
      Higashiosaka: { native: "東大阪", english: "Higashiosaka" },
      Toyonaka: { native: "豊中", english: "Toyonaka" },
      Takatsuki: { native: "高槻", english: "Takatsuki" },
      Kawasaki: { native: "川崎", english: "Kawasaki" },
      Sagamihara: { native: "相模原", english: "Sagamihara" },
      Fujisawa: { native: "藤沢", english: "Fujisawa" },
      Yokosuka: { native: "横須賀", english: "Yokosuka" },
      Toyota: { native: "豊田", english: "Toyota" },
      Okazaki: { native: "岡崎", english: "Okazaki" },
      Ichinomiya: { native: "一宮", english: "Ichinomiya" },
      Toyohashi: { native: "豊橋", english: "Toyohashi" },
      Saitama: { native: "埼玉", english: "Saitama" },
      Kawaguchi: { native: "川口", english: "Kawaguchi" },
      Kawagoe: { native: "川越", english: "Kawagoe" },
      Tokorozawa: { native: "所沢", english: "Tokorozawa" },
      Koshigaya: { native: "越谷", english: "Koshigaya" },
      Chiba: { native: "千葉", english: "Chiba" },
      Funabashi: { native: "船橋", english: "Funabashi" },
      Matsudo: { native: "松戸", english: "Matsudo" },
      Kashiwa: { native: "柏市", english: "Kashiwa" },
      Ichikawa: { native: "市川", english: "Ichikawa" },
      Asahikawa: { native: "旭川", english: "Asahikawa" },
      Hakodate: { native: "函館", english: "Hakodate" },
      Kushiro: { native: "釧路", english: "Kushiro" },
      Otaru: { native: "小樽", english: "Otaru" },
      Kitakyushu: { native: "北九州", english: "Kitakyushu" },
      Kurume: { native: "久留米", english: "Kurume" },
      Omuta: { native: "大牟田", english: "Omuta" },
      Iizuka: { native: "飯塚", english: "Iizuka" },
      Uji: { native: "宇治", english: "Uji" },
      Kameoka: { native: "亀岡", english: "Kameoka" },
      Maizuru: { native: "舞鶴", english: "Maizuru" },
      Fukuchiyama: { native: "福知山", english: "Fukuchiyama" },
      Himeji: { native: "姫路", english: "Himeji" },
      Nishinomiya: { native: "西宮", english: "Nishinomiya" },
      Amagasaki: { native: "尼崎", english: "Amagasaki" },
      Akashi: { native: "明石", english: "Akashi" },
    },
    streetBases: [
      { native: "若葉", english: "Wakaba" },
      { native: "青葉", english: "Aoba" },
      { native: "中央", english: "Chuo" },
      { native: "緑丘", english: "Midorigaoka" },
      { native: "日向", english: "Hyuga" },
      { native: "山手", english: "Yamate" },
      { native: "白川", english: "Shirakawa" },
      { native: "花園", english: "Hanazono" },
      { native: "桜丘", english: "Sakuragaoka" },
      { native: "浜町", english: "Hamacho" },
    ],
    streetTypes: [
      { native: "通り", english: "dori" },
      { native: "通", english: "Ave" },
      { native: "道", english: "Rd" },
      { native: "町", english: "cho" },
      { native: "北通り", english: "Kita-dori" },
      { native: "南通り", english: "Minami-dori" },
      { native: "東通り", english: "Higashi-dori" },
      { native: "西通り", english: "Nishi-dori" },
    ],
  },
  TW: {
    country: { native: "台灣", english: "Taiwan" },
    regions: {
      台北: { native: "臺北市", english: "Taipei City" },
      新北: { native: "新北市", english: "New Taipei City" },
      台中: { native: "臺中市", english: "Taichung City" },
      台南: { native: "臺南市", english: "Tainan City" },
      高雄: { native: "高雄市", english: "Kaohsiung City" },
      桃园: { native: "桃園市", english: "Taoyuan City" },
      新竹: { native: "新竹市", english: "Hsinchu City" },
      苗栗: { native: "苗栗縣", english: "Miaoli County" },
      彰化: { native: "彰化縣", english: "Changhua County" },
      南投: { native: "南投縣", english: "Nantou County" },
      云林: { native: "雲林縣", english: "Yunlin County" },
      嘉义: { native: "嘉義縣", english: "Chiayi County" },
      花莲: { native: "花蓮縣", english: "Hualien County" },
      台东: { native: "臺東縣", english: "Taitung County" },
      宜兰: { native: "宜蘭縣", english: "Yilan County" },
    },
    cities: {
      大安: { native: "大安區", english: "Da'an District" },
      信义: { native: "信義區", english: "Xinyi District" },
      松山: { native: "松山區", english: "Songshan District" },
      中山: { native: "中山區", english: "Zhongshan District" },
      板桥: { native: "板橋區", english: "Banqiao District" },
      中和: { native: "中和區", english: "Zhonghe District" },
      永和: { native: "永和區", english: "Yonghe District" },
      新庄: { native: "新莊區", english: "Xinzhuang District" },
      西屯: { native: "西屯區", english: "Xitun District" },
      南屯: { native: "南屯區", english: "Nantun District" },
      北屯: { native: "北屯區", english: "Beitun District" },
      东区: { native: "東區", english: "East District" },
      中西区: { native: "中西區", english: "West Central District" },
      南区: { native: "南區", english: "South District" },
      前金: { native: "前金區", english: "Qianjin District" },
      苓雅: { native: "苓雅區", english: "Lingya District" },
      新兴: { native: "新興區", english: "Xinxing District" },
      鼓山: { native: "鼓山區", english: "Gushan District" },
      中坜: { native: "中壢區", english: "Zhongli District" },
      平镇: { native: "平鎮區", english: "Pingzhen District" },
      龙潭: { native: "龍潭區", english: "Longtan District" },
      北区: { native: "北區", english: "North District" },
      香山: { native: "香山區", english: "Xiangshan District" },
      竹南: { native: "竹南鎮", english: "Zhunan Township" },
      头份: { native: "頭份市", english: "Toufen City" },
      彰化: { native: "彰化市", english: "Changhua City" },
      員林: { native: "員林市", english: "Yuanlin City" },
      南投: { native: "南投市", english: "Nantou City" },
      埔里: { native: "埔里鎮", english: "Puli Township" },
      斗六: { native: "斗六市", english: "Douliu City" },
      虎尾: { native: "虎尾鎮", english: "Huwei Township" },
      嘉义: { native: "嘉義市", english: "Chiayi City" },
      太保: { native: "太保市", english: "Taibao City" },
      花莲: { native: "花蓮市", english: "Hualien City" },
      台东: { native: "臺東市", english: "Taitung City" },
      宜兰: { native: "宜蘭市", english: "Yilan City" },
    },
    streetBases: [
      { native: "中山", english: "Zhongshan" },
      { native: "和平", english: "Heping" },
      { native: "民生", english: "Minsheng" },
      { native: "民權", english: "Minquan" },
      { native: "建國", english: "Jianguo" },
      { native: "忠孝", english: "Zhongxiao" },
      { native: "光復", english: "Guangfu" },
      { native: "仁愛", english: "Ren'ai" },
      { native: "復興", english: "Fuxing" },
      { native: "信義", english: "Xinyi" },
    ],
    streetTypes: [
      { native: "路", english: "Rd" },
      { native: "街", english: "St" },
      { native: "巷", english: "Ln" },
      { native: "大道", english: "Boulevard" },
      { native: "北路", english: "N Rd" },
      { native: "南路", english: "S Rd" },
      { native: "東路", english: "E Rd" },
      { native: "西路", english: "W Rd" },
    ],
  },
};

const STREET_BASE = {
  western: ["Oak", "Pine", "Maple", "River", "Cedar", "Liberty", "Sunset", "Hill", "Lake", "Washington"],
  cjk: ["朝阳", "和平", "中山", "人民", "建设", "长安", "新华", "文化", "解放", "幸福"],
  jp: ["若叶", "青叶", "中央", "绿丘", "日向", "山手", "白川", "花园", "樱丘", "滨町"],
};

const STRICT_NAME_FILTERS = {
  western: item => /[A-Za-z]/.test(item) && !/[\u4e00-\u9fff]/.test(item) && !/[\u3040-\u30ff]/.test(item),
  cjk: item => /[\u4e00-\u9fff]/.test(item) && !/[A-Za-z]/.test(item),
  jp: item => /[\u3040-\u30ff\u4e00-\u9fff]/.test(item) && !/[A-Za-z]/.test(item),
  mixed: item => Boolean(item),
};

const cache = new Map();
let lastGenerated = [];

const form = document.querySelector("#generator-form");
const countrySelect = document.querySelector("#country-select");
const batchSizeInput = document.querySelector("#batch-size");
const outputFormatSelect = document.querySelector("#output-format");
const profileModeSelect = document.querySelector("#profile-mode");
const localizationModeSelect = document.querySelector("#localization-mode");
const localizationNote = document.querySelector("#localization-note");
const resultMeta = document.querySelector("#result-meta");
const emptyState = document.querySelector("#empty-state");
const resultCards = document.querySelector("#result-cards");
const resultJson = document.querySelector("#result-json");
const copyButton = document.querySelector("#copy-result");
const downloadButton = document.querySelector("#download-json");

async function loadJson(path) {
  if (cache.has(path)) return cache.get(path);
  const response = await fetch(path);
  if (!response.ok) throw new Error(`Failed to load ${path}`);
  const data = await response.json();
  cache.set(path, data);
  return data;
}

function randomItem(items) {
  if (!Array.isArray(items) || items.length === 0) return "";
  return items[Math.floor(Math.random() * items.length)];
}

function randomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function randomChars(charset, count) {
  return Array.from({ length: count }, () => charset[randomInt(0, charset.length - 1)]).join("");
}

function randomDigits(count) {
  return randomChars(DIGITS, count);
}

function pad(value, length = 2) {
  return String(value).padStart(length, "0");
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function normalizeRegions(rawData) {
  if (Array.isArray(rawData)) {
    return rawData.map((entry, index) => ({
      key: String(index),
      label: entry.state || entry.province || entry.district || entry.region || entry.city || `Region ${index + 1}`,
      cities: entry.cities || entry.districts || entry.areas || [],
    }));
  }

  return Object.entries(rawData).map(([key, value]) => ({
    key,
    label: value.state || value.province || value.district || value.region || value.city || key,
    cities: value.cities || value.districts || value.areas || [],
  }));
}

function isAggregateCountryRegion(country, region) {
  const countryLabel = COUNTRY_META[country]?.label || country;
  return region?.key === country || region?.label === countryLabel;
}

function getGeneratorRegions(country, regions) {
  const filteredRegions = regions.filter(region => !isAggregateCountryRegion(country, region));
  return filteredRegions.length ? filteredRegions : regions;
}

function supportsLocalizedOutput(country) {
  return LOCALIZED_OUTPUT_COUNTRIES.has(country);
}

function getRequestedOutputLanguage(country) {
  if (!supportsLocalizedOutput(country)) {
    return "native";
  }

  return localizationModeSelect?.value || "native";
}

function localizeMappedValue(country, bucket, value, language) {
  if (!value) return "";

  const meta = LOCALIZED_OUTPUT_META[country];
  const mappedValue = meta?.[bucket]?.[value];
  if (!mappedValue) return value;

  return mappedValue[language] || value;
}

function getLabelPack(country, displayLanguage = "native") {
  const basePack = !supportsLocalizedOutput(country)
    ? DISPLAY_LABELS.default
    : displayLanguage === "english"
      ? DISPLAY_LABELS.english
      : DISPLAY_LABELS.nativeLocalized;

  const postalCode =
    POSTAL_LABEL_OVERRIDES[country]?.[displayLanguage] ||
    COUNTRY_META[country]?.postalLabel ||
    basePack.postalCode;

  return {
    ...basePack,
    postalCode,
  };
}

function buildCountryVariants(country) {
  if (!supportsLocalizedOutput(country)) {
    const label = COUNTRY_META[country]?.label || country;
    return { native: label, english: label };
  }

  const meta = LOCALIZED_OUTPUT_META[country];
  return {
    native: meta?.country?.native || COUNTRY_META[country]?.label || country,
    english: meta?.country?.english || COUNTRY_META[country]?.label || country,
  };
}

function buildLocationVariants(country, region, city) {
  if (!supportsLocalizedOutput(country)) {
    return {
      region: { native: region, english: region },
      city: { native: city, english: city },
    };
  }

  return {
    region: {
      native: localizeMappedValue(country, "regions", region, "native"),
      english: localizeMappedValue(country, "regions", region, "english"),
    },
    city: {
      native: localizeMappedValue(country, "cities", city, "native"),
      english: localizeMappedValue(country, "cities", city, "english"),
    },
  };
}

function buildStreet(country, locale) {
  const profile = COUNTRY_META[country]?.nameProfile || "mixed";
  const streetBase = STREET_BASE[profile] || STREET_BASE.western;
  const streetTypes = cache.get("data/streetTypesData.json");
  const suffixes = streetTypes?.[locale] || streetTypes?.en || ["Street"];
  const houseNumber = `${randomInt(11, 9879)}`;

  if (locale === "zh") {
    return `${randomItem(streetBase)}${randomItem(suffixes)}${houseNumber}号`;
  }

  if (locale === "ja") {
    return `${randomItem(streetBase)}${randomItem(suffixes)}${houseNumber}番`;
  }

  return `${houseNumber} ${randomItem(streetBase)} ${randomItem(suffixes)}`;
}

function buildLocalizedStreetVariants(country) {
  const meta = LOCALIZED_OUTPUT_META[country];
  const streetBase = randomItem(meta?.streetBases || []);
  const streetType = randomItem(meta?.streetTypes || []);
  const houseNumber = `${randomInt(11, 9879)}`;

  if (!streetBase || !streetType) {
    return { native: buildStreet(country, COUNTRY_META[country]?.locale || "en"), english: buildStreet(country, "en") };
  }

  if (country === "JP") {
    const englishStreet =
      streetType.english.includes("dori") || streetType.english === "cho"
        ? `${houseNumber} ${streetBase.english}-${streetType.english}`
        : `${houseNumber} ${streetBase.english} ${streetType.english}`;

    return {
      native: `${streetBase.native}${streetType.native}${houseNumber}番`,
      english: englishStreet,
    };
  }

  return {
    native: `${streetBase.native}${streetType.native}${houseNumber}號`,
    english: `${houseNumber} ${streetBase.english} ${streetType.english}`.replace(/\s+/g, " ").trim(),
  };
}

function buildStreetVariants(country, locale) {
  if (supportsLocalizedOutput(country)) {
    return buildLocalizedStreetVariants(country);
  }

  const street = buildStreet(country, locale);
  return { native: street, english: street };
}

function getNamePools(namesData, jpNamesData, country) {
  if (country === "JP") {
    return {
      male: jpNamesData.firstName_male || [],
      female: jpNamesData.firstName_female || [],
      last: jpNamesData.lastName || jpNamesData.last_name || [],
    };
  }

  return {
    male: namesData.firstName_male || [],
    female: namesData.firstName_female || [],
    last: namesData.lastName || namesData.last_name || [],
  };
}

function buildName(namesData, jpNamesData, mode, country, locale) {
  const pools = getNamePools(namesData, jpNamesData, country);
  const firstPool = Math.random() > 0.48 ? pools.male : pools.female;
  const profile = COUNTRY_META[country]?.nameProfile || "mixed";
  const strictFilter = STRICT_NAME_FILTERS[profile] || STRICT_NAME_FILTERS.mixed;
  const asiaFilter = item => /[\u4e00-\u9fff\u3040-\u30ff]/.test(item) && !/[A-Za-z]/.test(item);
  const westernFilter = item => /[A-Za-z]/.test(item) && !/[\u4e00-\u9fff\u3040-\u30ff]/.test(item);

  const filterByCountry = list => list.filter(strictFilter);
  const filterByMode = list => {
    const countryFiltered = filterByCountry(list);
    const base = countryFiltered.length ? countryFiltered : list;

    if (mode === "asia") return base.filter(asiaFilter);
    if (mode === "western") return base.filter(westernFilter);
    return base;
  };

  const filteredFirst = filterByMode(firstPool);
  const filteredLast = filterByMode(pools.last);
  const firstName = randomItem(filteredFirst.length ? filteredFirst : firstPool) || "Alex";
  const lastName = randomItem(filteredLast.length ? filteredLast : pools.last) || "Taylor";

  if (locale === "zh" || locale === "ja") {
    return `${lastName}${firstName}`;
  }

  return `${firstName} ${lastName}`;
}

function buildTaiwanNameVariants() {
  const firstPool = Math.random() > 0.48 ? TW_NAME_POOL.male : TW_NAME_POOL.female;
  const firstName = randomItem(firstPool) || { native: "志明", english: "Zhiming" };
  const lastName = randomItem(TW_NAME_POOL.last) || { native: "陳", english: "Chen" };

  return {
    native: `${lastName.native}${firstName.native}`,
    english: `${firstName.english} ${lastName.english}`,
  };
}

function buildJapanNameVariants(jpNamesData) {
  const firstPool = Math.random() > 0.48 ? jpNamesData.firstName_male || [] : jpNamesData.firstName_female || [];
  const lastPool = jpNamesData.lastName || jpNamesData.last_name || [];
  const firstName = randomItem(firstPool) || "太郎";
  const lastName = randomItem(lastPool) || "佐藤";

  return {
    native: `${lastName}${firstName}`,
    english: `${JP_NAME_ROMAJI.first[firstName] || firstName} ${JP_NAME_ROMAJI.last[lastName] || lastName}`,
  };
}

function buildNameVariants(namesData, jpNamesData, mode, country, locale) {
  if (country === "JP") {
    return buildJapanNameVariants(jpNamesData);
  }

  if (country === "TW") {
    return buildTaiwanNameVariants();
  }

  const fullName = buildName(namesData, jpNamesData, mode, country, locale);
  return { native: fullName, english: fullName };
}

function buildPostalCode(country) {
  const canadaLetters = "ABCEGHJKLMNPRSTVXY";

  if (country === "US" || country === "DE" || country === "FR" || country === "ES" || country === "IT" || country === "KR") {
    return `${randomInt(10000, 99999)}`;
  }

  if (country === "AT" || country === "CH" || country === "NO") {
    return `${randomInt(1000, 9999)}`;
  }

  if (country === "CA") {
    return `${randomChars(canadaLetters, 1)}${randomInt(1, 9)}${randomChars(canadaLetters, 1)} ${randomInt(1, 9)}${randomChars(canadaLetters, 1)}${randomInt(1, 9)}`;
  }

  if (country === "GB") {
    return `${randomChars("ABCDEFGHJKLMNPRSTUVWXYZ", 1)}${randomInt(1, 9)} ${randomInt(1, 9)}${randomChars("ABCDEFGHJKPSTUW", 2)}`;
  }

  if (country === "NL") {
    return `${randomInt(1000, 9999)} ${randomChars("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 2)}`;
  }

  if (country === "BE") {
    return `${randomInt(1000, 9999)}`;
  }

  if (country === "PT") {
    return `${randomInt(1000, 9999)}-${randomInt(100, 999)}`;
  }

  if (country === "IE") {
    return `${randomChars("ACDEFHKNPRTVWXY", 1)}${randomInt(1, 9)}${randomChars("0123456789ACDEFHKNPRTVWXY", 1)} ${randomChars("0123456789ACDEFHKNPRTVWXY", 4)}`;
  }

  if (country === "SE") {
    return `${randomInt(100, 999)} ${randomInt(10, 99)}`;
  }

  if (country === "JP") {
    return `${randomInt(100, 999)}-${randomInt(1000, 9999)}`;
  }

  if (country === "AU") {
    return `${randomInt(1000, 9999)}`;
  }

  if (country === "TW") {
    return `${randomInt(100, 999)}`;
  }

  if (country === "HK") {
    return "N/A";
  }

  return `${randomInt(100000, 999999)}`;
}

function buildAddressLines(country, street, city, countryLabel, postalCode, displayLanguage) {
  const labels = getLabelPack(country, displayLanguage);

  return [
    { key: "line1", label: labels.line1, value: street },
    { key: "city", label: labels.city, value: city },
    { key: "country", label: labels.country, value: countryLabel },
    { key: "postalCode", label: labels.postalCode, value: postalCode },
  ];
}

function formatAddress(addressLines, region = "") {
  const lineValues = addressLines.map(line => line.value);
  const cityLine = lineValues[1];
  const countryLine = lineValues[2];
  const postalLine = lineValues[3];
  const locality =
    region && region !== cityLine && region !== countryLine ? `${cityLine}, ${region}` : cityLine;
  const countryAndPostal = postalLine && postalLine !== "N/A" ? `${countryLine} ${postalLine}` : countryLine;

  return [lineValues[0], locality, countryAndPostal].filter(Boolean).join(", ");
}

function buildPhone(country) {
  const prefix = COUNTRY_META[country]?.dialing || "+00";

  if (country === "US" || country === "CA") {
    return `${prefix} ${randomInt(201, 989)} ${randomInt(200, 989)} ${randomInt(1000, 9999)}`;
  }

  if (country === "CN") {
    return `${prefix} 1${randomInt(3, 9)}${randomInt(0, 9)} ${randomInt(1000, 9999)} ${randomInt(1000, 9999)}`;
  }

  if (country === "JP") {
    return `${prefix} 90 ${randomInt(1000, 9999)} ${randomInt(1000, 9999)}`;
  }

  if (country === "KR") {
    return `${prefix} 10 ${randomInt(1000, 9999)} ${randomInt(1000, 9999)}`;
  }

  if (country === "HK") {
    return `${prefix} ${randomInt(5, 9)}${randomDigits(3)} ${randomDigits(4)}`;
  }

  if (country === "TW") {
    return `${prefix} 9${randomInt(10, 99)} ${randomDigits(3)} ${randomDigits(3)}`;
  }

  if (country === "GB") {
    return `${prefix} 7${randomDigits(3)} ${randomDigits(6)}`;
  }

  if (country === "DE") {
    return `${prefix} 15${randomInt(0, 9)} ${randomDigits(7)}${randomInt(0, 9)}`;
  }

  if (country === "NL") {
    return `${prefix} 6 ${randomDigits(4)} ${randomDigits(4)}`;
  }

  if (country === "FR") {
    return `${prefix} 6 ${randomInt(10, 99)} ${randomInt(10, 99)} ${randomInt(10, 99)} ${randomInt(10, 99)}`;
  }

  if (country === "ES") {
    return `${prefix} 6${randomDigits(2)} ${randomDigits(3)} ${randomDigits(3)}`;
  }

  if (country === "IT") {
    return `${prefix} 3${randomDigits(2)} ${randomDigits(3)} ${randomDigits(4)}`;
  }

  if (country === "BE") {
    return `${prefix} 4${randomDigits(2)} ${randomDigits(2)} ${randomDigits(2)} ${randomDigits(2)}`;
  }

  if (country === "PT") {
    return `${prefix} 9${randomDigits(2)} ${randomDigits(3)} ${randomDigits(3)}`;
  }

  if (country === "AT") {
    return `${prefix} 6${randomDigits(2)} ${randomDigits(3)} ${randomDigits(4)}`;
  }

  if (country === "CH") {
    return `${prefix} 79 ${randomDigits(3)} ${randomDigits(2)} ${randomDigits(2)}`;
  }

  if (country === "IE") {
    return `${prefix} 8${randomInt(3, 9)} ${randomDigits(3)} ${randomDigits(4)}`;
  }

  if (country === "SE") {
    return `${prefix} 70 ${randomDigits(3)} ${randomDigits(2)} ${randomDigits(2)}`;
  }

  if (country === "NO") {
    return `${prefix} ${randomDigits(4)} ${randomDigits(4)}`;
  }

  if (country === "AU") {
    return `${prefix} 4${randomDigits(2)} ${randomDigits(3)} ${randomDigits(3)}`;
  }

  if (country === "SG") {
    return `${prefix} ${randomInt(8, 9)}${randomDigits(3)} ${randomDigits(4)}`;
  }

  return `${prefix} ${randomInt(100, 999)} ${randomInt(1000, 9999)} ${randomInt(1000, 9999)}`;
}

function buildBirthDate() {
  const year = randomInt(1980, 2004);
  const month = pad(randomInt(1, 12));
  const day = pad(randomInt(1, 28));
  return `${year}-${month}-${day}`;
}

function buildEmail(name) {
  const normalized =
    name
      .toLowerCase()
      .replace(/[^a-z0-9\u4e00-\u9fa5\u3040-\u30ff]+/gi, "")
      .slice(0, 14) || "user";
  const domain = ["gmail.com", "outlook.com", "proton.me", "icloud.com"];
  return `${normalized}${randomInt(11, 999)}@${randomItem(domain)}`;
}

async function copyToClipboard(text) {
  if (navigator.clipboard?.writeText) {
    await navigator.clipboard.writeText(text);
    return;
  }

  const textArea = document.createElement("textarea");
  textArea.value = text;
  textArea.setAttribute("readonly", "");
  textArea.style.position = "absolute";
  textArea.style.left = "-9999px";
  document.body.appendChild(textArea);
  textArea.select();
  document.execCommand("copy");
  document.body.removeChild(textArea);
}

function buildProfilePlainText(profile) {
  const alternateName =
    profile.supportsLocalizedOutput && profile.fullNameNative !== profile.fullNameEnglish
      ? profile.displayLanguage === "english"
        ? `${profile.labels.nativeName}: ${profile.fullNameNative}`
        : `${profile.labels.englishName}: ${profile.fullNameEnglish}`
      : "";
  const alternateOneLineAddress =
    profile.supportsLocalizedOutput && profile.addressOneLineNative !== profile.addressOneLineEnglish
      ? profile.displayLanguage === "english"
        ? `${profile.labels.nativeOneLineAddress}: ${profile.addressOneLineNative}`
        : `${profile.labels.englishOneLineAddress}: ${profile.addressOneLineEnglish}`
      : "";
  const addressText = profile.addressLines
    .map(line => `${line.label}: ${line.value}`)
    .join("\n");

  return [
    profile.fullName,
    alternateName,
    `${profile.labels.oneLineAddress}: ${profile.addressOneLine}`,
    alternateOneLineAddress,
    addressText,
    `${profile.labels.email}: ${profile.email}`,
    `${profile.labels.phone}: ${profile.phone}`,
    `${profile.labels.birthDate}: ${profile.birthDate}`,
  ]
    .filter(Boolean)
    .join("\n");
}

function buildAddressVariants(country, countryVariants, locationVariants, streetVariants, postalCode) {
  const nativeAddressLines = buildAddressLines(
    country,
    streetVariants.native,
    locationVariants.city.native,
    countryVariants.native,
    postalCode,
    "native"
  );
  const englishAddressLines = buildAddressLines(
    country,
    streetVariants.english,
    locationVariants.city.english,
    countryVariants.english,
    postalCode,
    "english"
  );

  return {
    native: {
      lines: nativeAddressLines,
      oneLine: formatAddress(nativeAddressLines, locationVariants.region.native),
    },
    english: {
      lines: englishAddressLines,
      oneLine: formatAddress(englishAddressLines, locationVariants.region.english),
    },
  };
}

function toDisplayProfile(profile, requestedLanguage) {
  const displayLanguage = supportsLocalizedOutput(profile.country) ? requestedLanguage : "native";
  const address = profile.addressVariants[displayLanguage] || profile.addressVariants.native;
  const labels = getLabelPack(profile.country, displayLanguage);

  return {
    country: profile.country,
    countryLabel: profile.countryVariants[displayLanguage],
    fullName: profile.nameVariants[displayLanguage],
    fullNameNative: profile.nameVariants.native,
    fullNameEnglish: profile.nameVariants.english,
    region: profile.locationVariants.region[displayLanguage],
    regionNative: profile.locationVariants.region.native,
    regionEnglish: profile.locationVariants.region.english,
    city: profile.locationVariants.city[displayLanguage],
    cityNative: profile.locationVariants.city.native,
    cityEnglish: profile.locationVariants.city.english,
    street: profile.streetVariants[displayLanguage],
    streetNative: profile.streetVariants.native,
    streetEnglish: profile.streetVariants.english,
    postalCode: profile.postalCode,
    phone: profile.phone,
    email: profile.email,
    birthDate: profile.birthDate,
    label: COUNTRY_META[profile.country]?.postalLabel || "Postal code",
    addressLines: address.lines,
    addressLinesNative: profile.addressVariants.native.lines,
    addressLinesEnglish: profile.addressVariants.english.lines,
    addressOneLine: address.oneLine,
    addressOneLineNative: profile.addressVariants.native.oneLine,
    addressOneLineEnglish: profile.addressVariants.english.oneLine,
    address: address.oneLine,
    displayLanguage,
    labels,
    supportsLocalizedOutput: supportsLocalizedOutput(profile.country),
  };
}

function getDisplayProfiles(profiles = lastGenerated) {
  return profiles.map(profile => toDisplayProfile(profile, getRequestedOutputLanguage(profile.country)));
}

function buildResultMetaText(country, count) {
  const language =
    supportsLocalizedOutput(country) && getRequestedOutputLanguage(country) === "english"
      ? " · English 名字 / 地址输出"
      : supportsLocalizedOutput(country)
        ? " · 本地名字 / 地址输出"
        : "";

  return `已生成 ${count} 条 ${COUNTRY_META[country]?.label || country} 数据 · 纯静态浏览器端生成${language}`;
}

function updateLocalizationControl() {
  const country = countrySelect?.value || "US";
  const enabled = supportsLocalizedOutput(country);

  if (localizationModeSelect) {
    localizationModeSelect.disabled = !enabled;
  }

  if (localizationNote) {
    localizationNote.textContent = enabled
      ? "当前国家支持本地名字 / 地址与 English 名字 / 地址之间即时切换。"
      : "仅对日本和台湾生效，其他国家保持默认输出。";
  }
}

async function generateProfiles({ country, batchSize, mode }) {
  const [addressData, namesData, jpNamesData] = await Promise.all([
    loadJson(DATA_FILES[country]),
    loadJson("data/namesData.json"),
    loadJson("data/jpNamesData.json"),
    loadJson("data/streetTypesData.json"),
  ]);

  const locale = COUNTRY_META[country]?.locale || "en";
  const regions = normalizeRegions(addressData);
  const generatorRegions = getGeneratorRegions(country, regions);

  return Array.from({ length: batchSize }, () => {
    const region = randomItem(generatorRegions);
    const city = randomItem(region?.cities || []) || region?.label || "Unknown";
    const nameVariants = buildNameVariants(namesData, jpNamesData, mode, country, locale);
    const postalCode = buildPostalCode(country);
    const streetVariants = buildStreetVariants(country, locale);
    const regionLabel = region?.label || "Unknown";
    const countryVariants = buildCountryVariants(country);
    const locationVariants = buildLocationVariants(country, regionLabel, city);
    const addressVariants = buildAddressVariants(country, countryVariants, locationVariants, streetVariants, postalCode);
    const email = buildEmail(nameVariants.english || nameVariants.native);

    return {
      country,
      countryVariants,
      nameVariants,
      locationVariants,
      streetVariants,
      postalCode,
      regionRaw: regionLabel,
      cityRaw: city,
      phone: buildPhone(country),
      email,
      birthDate: buildBirthDate(),
      label: COUNTRY_META[country]?.postalLabel || "Postal code",
      addressVariants,
    };
  });
}

function renderRegion(profile) {
  if (!profile.region || profile.region === profile.countryLabel || profile.region === profile.city) {
    return "";
  }

  return `<p class="profile-region"><strong>${escapeHtml(profile.labels.region)}:</strong> ${escapeHtml(profile.region)}</p>`;
}

function renderNameNote(profile) {
  if (!profile.supportsLocalizedOutput || profile.fullNameNative === profile.fullNameEnglish) {
    return "";
  }

  const label = profile.displayLanguage === "english" ? profile.labels.nativeName : profile.labels.englishName;
  const value = profile.displayLanguage === "english" ? profile.fullNameNative : profile.fullNameEnglish;

  return `<p class="profile-name-note"><strong>${escapeHtml(label)}:</strong> ${escapeHtml(value)}</p>`;
}

function renderOutputBadge(profile) {
  if (!profile.supportsLocalizedOutput) {
    return "";
  }

  const badgeLabel = profile.displayLanguage === "english" ? profile.labels.englishOutputBadge : profile.labels.nativeOutputBadge;
  return `<span class="profile-output-badge">${escapeHtml(badgeLabel)}</span>`;
}

function renderAddressLines(profile) {
  return profile.addressLines
    .map(
      line => `
        <div class="address-row">
          <div class="address-row-label">${escapeHtml(line.label)}</div>
          <div class="address-row-value">${escapeHtml(line.value)}</div>
          <button
            type="button"
            class="line-copy"
            data-copy-text="${escapeHtml(line.value)}"
            data-copy-label="${escapeHtml(line.label)}"
          >
            复制
          </button>
        </div>
      `
    )
    .join("");
}

function renderCards(profiles) {
  resultCards.innerHTML = profiles
    .map(
      profile => `
        <article class="profile-card">
          <div class="profile-head">
            <div>
              <h3>${escapeHtml(profile.fullName)}</h3>
              ${renderNameNote(profile)}
              ${renderRegion(profile)}
            </div>
            ${renderOutputBadge(profile)}
          </div>
          <section class="address-card-block">
            <p class="address-block-title">${escapeHtml(profile.labels.addressSection)}</p>
            <div class="address-stack">
              ${renderAddressLines(profile)}
            </div>
            <div class="address-row profile-address-summary">
              <div class="address-row-label">${escapeHtml(profile.labels.oneLineAddress)}</div>
              <div class="address-row-value">${escapeHtml(profile.addressOneLine)}</div>
              <button
                type="button"
                class="line-copy"
                data-copy-text="${escapeHtml(profile.addressOneLine)}"
                data-copy-label="${escapeHtml(profile.labels.oneLineAddress)}"
              >
                复制
              </button>
            </div>
            <div class="address-row profile-phone-row">
              <div class="address-row-label">${escapeHtml(profile.labels.phone)}</div>
              <div class="address-row-value">${escapeHtml(profile.phone)}</div>
              <button
                type="button"
                class="line-copy"
                data-copy-text="${escapeHtml(profile.phone)}"
                data-copy-label="${escapeHtml(profile.labels.phone)}"
              >
                复制
              </button>
            </div>
          </section>
          <div class="profile-extra">
            <p class="profile-line"><strong>${escapeHtml(profile.labels.email)}:</strong> ${escapeHtml(profile.email)}</p>
            <p class="profile-line"><strong>${escapeHtml(profile.labels.birthDate)}:</strong> ${escapeHtml(profile.birthDate)}</p>
          </div>
        </article>
      `
    )
    .join("");
}

function renderOutput(profiles, format) {
  const displayProfiles = getDisplayProfiles(profiles);
  emptyState.hidden = true;

  if (format === "json") {
    resultCards.hidden = true;
    resultJson.hidden = false;
    resultJson.textContent = JSON.stringify(displayProfiles, null, 2);
    return;
  }

  resultJson.hidden = true;
  resultCards.hidden = false;
  renderCards(displayProfiles);
}

async function handleGenerate(event) {
  event.preventDefault();
  const country = countrySelect.value;
  const batchSize = Math.max(1, Math.min(12, Number(batchSizeInput.value) || 1));
  const format = outputFormatSelect.value;
  const mode = profileModeSelect.value;

  resultMeta.textContent = "生成中...";

  try {
    lastGenerated = await generateProfiles({ country, batchSize, mode });
    renderOutput(lastGenerated, format);
    resultMeta.textContent = buildResultMetaText(country, lastGenerated.length);
    copyButton.disabled = false;
    downloadButton.disabled = false;
  } catch (error) {
    console.error(error);
    resultMeta.textContent = "加载本地 JSON 失败，请确认 data 目录已和静态页面一起部署。";
  }
}

async function copyResult() {
  if (!lastGenerated.length) return;

  const format = outputFormatSelect.value;
  const displayProfiles = getDisplayProfiles();
  const text =
    format === "json"
      ? JSON.stringify(displayProfiles, null, 2)
      : displayProfiles.map(buildProfilePlainText).join("\n\n");

  await copyToClipboard(text);
  resultMeta.textContent = `已复制 ${lastGenerated.length} 条结果。`;
}

function downloadJson() {
  if (!lastGenerated.length) return;

  const displayProfiles = getDisplayProfiles();
  const blob = new Blob([JSON.stringify(displayProfiles, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `address-lab-${Date.now()}.json`;
  link.click();
  URL.revokeObjectURL(url);
}

async function handleLineCopy(event) {
  const button = event.target.closest(".line-copy");
  if (!button) return;

  const copyText = button.dataset.copyText || "";
  const copyLabel = button.dataset.copyLabel || "这一行";
  const originalText = button.textContent;

  try {
    await copyToClipboard(copyText);
    button.textContent = "已复制";
    resultMeta.textContent = `已复制 ${copyLabel}。`;

    window.setTimeout(() => {
      button.textContent = originalText;
    }, 1200);
  } catch (error) {
    console.error(error);
    resultMeta.textContent = "复制失败，请重试。";
  }
}

function handleLocalizationChange() {
  if (!lastGenerated.length) return;

  renderOutput(lastGenerated, outputFormatSelect.value);
  resultMeta.textContent = buildResultMetaText(lastGenerated[0].country, lastGenerated.length);
}

updateLocalizationControl();
form?.addEventListener("submit", handleGenerate);
copyButton?.addEventListener("click", copyResult);
downloadButton?.addEventListener("click", downloadJson);
countrySelect?.addEventListener("change", updateLocalizationControl);
localizationModeSelect?.addEventListener("change", handleLocalizationChange);
outputFormatSelect?.addEventListener("change", () => {
  if (!lastGenerated.length) return;
  renderOutput(lastGenerated, outputFormatSelect.value);
});
resultCards?.addEventListener("click", handleLineCopy);
