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

function buildAddressLines(country, street, city, postalCode) {
  return [
    { key: "line1", label: "Address Line 1", value: street },
    { key: "city", label: "City", value: city },
    { key: "country", label: "Country", value: COUNTRY_META[country]?.label || country },
    { key: "postalCode", label: COUNTRY_META[country]?.postalLabel || "Postal code", value: postalCode },
  ];
}

function formatAddress(addressLines) {
  const lineValues = addressLines.map(line => line.value);
  return `${lineValues[0]}, ${lineValues[1]}, ${lineValues[2]} ${lineValues[3]}`;
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
  const addressText = profile.addressLines
    .map(line => `${line.label}: ${line.value}`)
    .join("\n");

  return [
    profile.fullName,
    addressText,
    `Email: ${profile.email}`,
    `Phone: ${profile.phone}`,
    `Birth date: ${profile.birthDate}`,
  ].join("\n");
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
    const addressLines = buildAddressLines(country, street, city, postalCode);

    return {
      country,
      countryLabel: COUNTRY_META[country]?.label || country,
      fullName,
      region: regionLabel,
      city,
      street,
      postalCode,
      phone: buildPhone(country),
      email: buildEmail(fullName),
      birthDate: buildBirthDate(),
      label: COUNTRY_META[country]?.postalLabel || "Postal code",
      addressLines,
      address: formatAddress(addressLines),
    };
  });
}

function renderRegion(profile) {
  if (!profile.region || profile.region === profile.countryLabel || profile.region === profile.city) {
    return "";
  }

  return `<p class="profile-region"><strong>Region:</strong> ${escapeHtml(profile.region)}</p>`;
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
              ${renderRegion(profile)}
            </div>
          </div>
          <section class="address-card-block">
            <p class="address-block-title">地址</p>
            <div class="address-stack">
              ${renderAddressLines(profile)}
            </div>
            <div class="address-row profile-phone-row">
              <div class="address-row-label">Phone number</div>
              <div class="address-row-value">${escapeHtml(profile.phone)}</div>
              <button
                type="button"
                class="line-copy"
                data-copy-text="${escapeHtml(profile.phone)}"
                data-copy-label="Phone number"
              >
                复制
              </button>
            </div>
          </section>
          <div class="profile-extra">
            <p class="profile-line"><strong>Email:</strong> ${escapeHtml(profile.email)}</p>
            <p class="profile-line"><strong>Birth date:</strong> ${escapeHtml(profile.birthDate)}</p>
          </div>
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
    resultMeta.textContent = `已生成 ${lastGenerated.length} 条 ${COUNTRY_META[country]?.label || country} 数据 · 纯静态浏览器端生成`;
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
  const text =
    format === "json"
      ? JSON.stringify(lastGenerated, null, 2)
      : lastGenerated.map(buildProfilePlainText).join("\n\n");

  await copyToClipboard(text);
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

form?.addEventListener("submit", handleGenerate);
copyButton?.addEventListener("click", copyResult);
downloadButton?.addEventListener("click", downloadJson);
outputFormatSelect?.addEventListener("change", () => {
  if (!lastGenerated.length) return;
  renderOutput(lastGenerated, outputFormatSelect.value);
});
resultCards?.addEventListener("click", handleLineCopy);
