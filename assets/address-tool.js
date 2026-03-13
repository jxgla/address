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
  US: { locale: "en", dialing: "+1", postalLabel: "ZIP" },
  CN: { locale: "zh", dialing: "+86", postalLabel: "邮编" },
  JP: { locale: "ja", dialing: "+81", postalLabel: "邮编" },
  HK: { locale: "zh", dialing: "+852", postalLabel: "区号" },
  TW: { locale: "zh", dialing: "+886", postalLabel: "邮递区号" },
  GB: { locale: "en", dialing: "+44", postalLabel: "Postcode" },
  DE: { locale: "en", dialing: "+49", postalLabel: "PLZ" },
  CA: { locale: "en", dialing: "+1", postalLabel: "Postal code" },
  AU: { locale: "en", dialing: "+61", postalLabel: "Postcode" },
  SG: { locale: "en", dialing: "+65", postalLabel: "Postal code" },
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

function buildStreet(locale) {
  const streetBase = [
    "Oak",
    "Pine",
    "Maple",
    "River",
    "Cedar",
    "Liberty",
    "Sunset",
    "朝阳",
    "和平",
    "中山",
    "樱花",
    "青云",
    "中央",
    "若葉",
    "桜",
    "青葉",
  ];

  const suffixes = cache.get("data/streetTypesData.json")?.[locale] || cache.get("data/streetTypesData.json")?.en || ["Street"];
  const houseNumber = `${randomInt(11, 9879)}`;
  return `${houseNumber} ${randomItem(streetBase)}${locale === "zh" || locale === "ja" ? "" : " "}${randomItem(suffixes)}`;
}

function buildName(namesData, mode, locale) {
  const male = namesData.firstName_male || [];
  const female = namesData.firstName_female || [];
  const last = namesData.lastName || namesData.last_name || [];
  const firstPool = Math.random() > 0.48 ? male : female;

  const asiaHint = /[一-龥ぁ-んァ-ヶ]/;
  const westernHint = /[A-Za-z]/;

  const filterByMode = list => {
    if (mode === "asia") return list.filter(item => asiaHint.test(item));
    if (mode === "western") return list.filter(item => westernHint.test(item));
    return list;
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
  return `${randomInt(100000, 999999)}`;
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
  const [addressData, namesData] = await Promise.all([
    loadJson(DATA_FILES[country]),
    loadJson("data/namesData.json"),
    loadJson("data/streetTypesData.json"),
  ]);

  const locale = COUNTRY_META[country]?.locale || "en";
  const regions = normalizeRegions(addressData);

  return Array.from({ length: batchSize }, () => {
    const region = randomItem(regions);
    const city = randomItem(region?.cities || []) || region?.label || "Unknown";
    const fullName = buildName(namesData, mode, locale);
    const postalCode = buildPostalCode(country);

    return {
      country,
      fullName,
      region: region?.label || "Unknown",
      city,
      street: buildStreet(locale),
      postalCode,
      phone: buildPhone(country),
      email: buildEmail(fullName, country),
      birthDate: buildBirthDate(),
      label: COUNTRY_META[country]?.postalLabel || "Postal code",
      address: `${buildStreet(locale)}, ${city}, ${region?.label || "Unknown"}, ${country} ${postalCode}`,
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