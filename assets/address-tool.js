const DATA_FILES = {
  US: "data/usData.json",
  CN: "data/cnData.json",
  JP: "data/jpData.json",
  HK: "data/hkData.json",
  TW: "data/twData.json",
  GB: "data/gbData.json",
  DE: "data/deData.json",
  CA: "data/caData.json",
  AU: "data/auData.json",
  SG: "data/sgData.json",
};

const COUNTRY_META = {
  US: { locale: "en", dialing: "+1", postalLabel: "ZIP", nameProfile: "western" },
  CN: { locale: "zh", dialing: "+86", postalLabel: "邮编", nameProfile: "cjk" },
  JP: { locale: "ja", dialing: "+81", postalLabel: "邮编", nameProfile: "jp" },
  HK: { locale: "zh", dialing: "+852", postalLabel: "区号", nameProfile: "cjk" },
  TW: { locale: "zh", dialing: "+886", postalLabel: "邮递区号", nameProfile: "cjk" },
  GB: { locale: "en", dialing: "+44", postalLabel: "Postcode", nameProfile: "western" },
  DE: { locale: "en", dialing: "+49", postalLabel: "PLZ", nameProfile: "western" },
  CA: { locale: "en", dialing: "+1", postalLabel: "Postal code", nameProfile: "western" },
  AU: { locale: "en", dialing: "+61", postalLabel: "Postcode", nameProfile: "western" },
  SG: { locale: "en", dialing: "+65", postalLabel: "Postal code", nameProfile: "mixed" },
};

const STREET_BASE = {
  western: ["Oak", "Pine", "Maple", "River", "Cedar", "Liberty", "Sunset", "Hill", "Lake", "Washington"],
  cjk: ["朝阳", "和平", "中山", "人民", "建设", "长安", "新华", "文化", "解放", "幸福"],
  jp: ["若葉", "桜", "青葉", "中央", "緑", "旭", "山手", "白川", "花園", "日の出"],
};

const STRICT_NAME_FILTERS = {
  western: item => /[A-Za-z]/.test(item) && !/[一-龥]/.test(item) && !/[ぁ-んァ-ヶ]/.test(item),
  cjk: item => /[一-龥]/.test(item) && !/[A-Za-z]/.test(item),
  jp: item => /[ぁ-んァ-ヶ一-龥]/.test(item) && !/[A-Za-z]/.test(item),
  mixed: item => Boolean(item),
};

const cache = new Map();
let lastGenerated = [];

const form = document.querySelector("#generator-form");
const countrySelect = document.querySelector("#country-select");
const batchSizeInput = document.querySelector("#batch-size");
const outputFormatSelect = document.querySelector("#output-format");
const profileModeSelect = document.querySelector("#profile-mode");
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

function pad(value, length = 2) {
  return String(value).padStart(length, "0");
}

function normalizeRegions(rawData) {
  if (Array.isArray(rawData)) {
    return rawData.map((entry, index) => ({
      key: String(index),
      label: entry.state || entry.province || entry.region || entry.city || `Region ${index + 1}`,
      cities: entry.cities || entry.districts || entry.areas || [],
    }));
  }

  return Object.entries(rawData).map(([key, value]) => ({
    key,
    label: value.state || value.province || value.region || value.city || key,
    cities: value.cities || value.districts || value.areas || [],
  }));
}

function buildStreet(country, locale) {
  const profile = COUNTRY_META[country]?.nameProfile || "mixed";
  const streetBase = STREET_BASE[profile] || STREET_BASE.western;
  const suffixes = cache.get("data/streetTypesData.json")?.[locale] || cache.get("data/streetTypesData.json")?.en || ["Street"];
  const houseNumber = `${randomInt(11, 9879)}`;

  if (locale === "zh" || locale === "ja") {
    return `${randomItem(streetBase)}${randomItem(suffixes)}${houseNumber}号`;
  }

  return `${houseNumber} ${randomItem(streetBase)} ${randomItem(suffixes)}`;
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
  const male = pools.male;
  const female = pools.female;
  const last = pools.last;
  const firstPool = Math.random() > 0.48 ? male : female;

  const profile = COUNTRY_META[country]?.nameProfile || "mixed";
  const strictFilter = STRICT_NAME_FILTERS[profile] || STRICT_NAME_FILTERS.mixed;
  const asiaFilter = item => /[一-龥ぁ-んァ-ヶ]/.test(item) && !/[A-Za-z]/.test(item);
  const westernFilter = item => /[A-Za-z]/.test(item) && !/[一-龥ぁ-んァ-ヶ]/.test(item);

  const filterByCountry = list => {
    return list.filter(strictFilter);
  };

  const filterByMode = list => {
    const countryFiltered = filterByCountry(list);
    const base = countryFiltered.length ? countryFiltered : list;
    if (mode === "asia") return base.filter(asiaFilter);
    if (mode === "western") return base.filter(westernFilter);
    return base;
  };

  const filteredFirst = filterByMode(firstPool);
  const filteredLast = filterByMode(last);
  const firstName = randomItem(filteredFirst.length ? filteredFirst : firstPool) || "Alex";
  const lastName = randomItem(filteredLast.length ? filteredLast : last) || "Taylor";

  if (locale === "zh" || locale === "ja") {
    return `${lastName}${firstName}`;
  }
  return `${firstName} ${lastName}`;
}

function buildPostalCode(country) {
  if (country === "US") return `${randomInt(10000, 99999)}`;
  if (country === "CA") return `A${randomInt(1, 9)}A ${randomInt(1, 9)}A${randomInt(1, 9)}`;
  if (country === "GB") return `E${randomInt(1, 9)} ${randomInt(1, 9)}AA`;
  if (country === "JP") return `${randomInt(100, 999)}-${randomInt(1000, 9999)}`;
  if (country === "HK") return `${randomInt(100000, 999999)}`;
  if (country === "TW") return `${randomInt(100, 999)}`;
  return `${randomInt(100000, 999999)}`;
}

function formatAddress({ country, street, city, regionLabel, postalCode }) {
  if (country === "CN" || country === "HK" || country === "TW") {
    return `${regionLabel}${city}${street}，${postalCode}`;
  }

  if (country === "JP") {
    return `${regionLabel}${city}${street} 〒${postalCode}`;
  }

  return `${street}, ${city}, ${regionLabel}, ${country} ${postalCode}`;
}

function buildPhone(country) {
  const prefix = COUNTRY_META[country]?.dialing || "+00";
  return `${prefix} ${randomInt(100, 999)} ${randomInt(1000, 9999)} ${randomInt(1000, 9999)}`;
}

function buildBirthDate() {
  const year = randomInt(1980, 2004);
  const month = pad(randomInt(1, 12));
  const day = pad(randomInt(1, 28));
  return `${year}-${month}-${day}`;
}

function buildEmail(name, country) {
  const normalized = name
    .toLowerCase()
    .replace(/[^a-z0-9\u4e00-\u9fa5\u3040-\u30ff]+/gi, "")
    .slice(0, 14) || "user";
  const domain = ["gmail.com", "outlook.com", "proton.me", "icloud.com"];
  return `${normalized}${randomInt(11, 999)}@${randomItem(domain)}`;
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

  return Array.from({ length: batchSize }, () => {
    const region = randomItem(regions);
    const city = randomItem(region?.cities || []) || region?.label || "Unknown";
    const fullName = buildName(namesData, jpNamesData, mode, country, locale);
    const postalCode = buildPostalCode(country);
    const street = buildStreet(country, locale);
    const regionLabel = region?.label || "Unknown";

    return {
      country,
      fullName,
      region: regionLabel,
      city,
      street,
      postalCode,
      phone: buildPhone(country),
      email: buildEmail(fullName, country),
      birthDate: buildBirthDate(),
      label: COUNTRY_META[country]?.postalLabel || "Postal code",
      address: formatAddress({ country, street, city, regionLabel, postalCode }),
    };
  });
}

function renderCards(profiles) {
  resultCards.innerHTML = profiles
    .map(
      profile => `
        <article class="profile-card">
          <h3>${profile.fullName}</h3>
          <p class="profile-line"><strong>Address:</strong> ${profile.address}</p>
          <p class="profile-line"><strong>Email:</strong> ${profile.email}</p>
          <p class="profile-line"><strong>Phone:</strong> ${profile.phone}</p>
          <p class="profile-line"><strong>Birth date:</strong> ${profile.birthDate}</p>
        </article>
      `
    )
    .join("");
}

function renderOutput(profiles, format) {
  emptyState.hidden = true;
  if (format === "json") {
    resultCards.hidden = true;
    resultJson.hidden = false;
    resultJson.textContent = JSON.stringify(profiles, null, 2);
    return;
  }

  resultJson.hidden = true;
  resultCards.hidden = false;
  renderCards(profiles);
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
    resultMeta.textContent = `已生成 ${lastGenerated.length} 条 ${country} 数据 · 纯静态浏览器端生成`; 
    copyButton.disabled = false;
    downloadButton.disabled = false;
  } catch (error) {
    console.error(error);
    resultMeta.textContent = "加载本地 JSON 失败，请确认 data 目录已随静态页面一起部署。";
  }
}

async function copyResult() {
  if (!lastGenerated.length) return;
  const format = outputFormatSelect.value;
  const text = format === "json"
    ? JSON.stringify(lastGenerated, null, 2)
    : lastGenerated
        .map(item => `${item.fullName}\n${item.address}\n${item.email}\n${item.phone}`)
        .join("\n\n");
  await navigator.clipboard.writeText(text);
  resultMeta.textContent = `已复制 ${lastGenerated.length} 条结果。`;
}

function downloadJson() {
  if (!lastGenerated.length) return;
  const blob = new Blob([JSON.stringify(lastGenerated, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `address-lab-${Date.now()}.json`;
  link.click();
  URL.revokeObjectURL(url);
}

form?.addEventListener("submit", handleGenerate);
copyButton?.addEventListener("click", copyResult);
downloadButton?.addEventListener("click", downloadJson);