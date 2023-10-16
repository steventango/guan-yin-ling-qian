const TABLE = document.getElementById('table');
const TITLE = document.querySelector('title');
const SELECT_TL = document.getElementById('translation-language');
const NUMBER_TL = document.getElementById('number');
const BUTTON = document.getElementById('求籤_');


async function updateData() {
  const urlParams = new URLSearchParams(window.location.search);
  const tl = urlParams.get('tl') || 'zh-tw';
  const n = urlParams.get('n');

  if (['zh-tw', 'zh-cn', 'ja', 'ko'].includes(tl)) {
    TABLE.classList.add('vertical');
  } else {
    TABLE.classList.remove('vertical');
  }

  const response_constants = await fetch(`./data/${tl}/constants.json`, { cache: "force-cache" });
  const data_tl_constants = await response_constants.json();

  const entries = [...Object.entries(data_tl_constants)];

  TITLE.textContent = `${data_tl_constants['觀音靈籤_']}`;
  if (n && n.length) {
    const response_tl_n = await fetch(`./data/${tl}/${n}.json`, { cache: "force-cache" });
    const data_tl_n = await response_tl_n.json();
    entries.push(...Object.entries(data_tl_n));
    TABLE.style.display = 'table';
    if (data_tl_n['第X籤']) {
      TITLE.textContent += ` - ${data_tl_n['第X籤']}`;
    }
  } else {
    TABLE.style.display = 'none';
  }

  for (const [key, value] of entries) {
    const element = document.getElementById(key);
    if (!element) {
      continue;
    }
    let text = value.replaceAll("\n", "<br>");
    element.innerHTML = text || '';
  }
}

function updateUrlParams() {
  const tl = SELECT_TL.value;
  const n = NUMBER_TL.value;
  const searchParams = new URLSearchParams();
  if (tl) {
    searchParams.set('tl', tl);
  }
  if (n) {
    searchParams.set('n', n);
  }
  history.replaceState(null, '', `?${searchParams.toString()}`);
  updateData();
}

function 求籤() {
  let n = NUMBER_TL.value;
  while (n == NUMBER_TL.value) {
    n = Math.floor(Math.random() * 100) + 1;
  }
  NUMBER_TL.value = n;
  NUMBER_TL.options[n].selected = true;
  updateUrlParams();
}

function initializeSelects() {
  const urlParams = new URLSearchParams(window.location.search);
  const n = urlParams.get('n');
  if (n) {
    NUMBER_TL.value = n;
    NUMBER_TL.options[n].selected = true;
  }
  const tl = urlParams.get('tl');
  if (tl) {
    SELECT_TL.value = tl;
    for (const option of SELECT_TL.options) {
      option.selected = option.value === tl;
    }
  }
}

function main() {
  SELECT_TL.addEventListener('change', updateUrlParams);
  NUMBER_TL.addEventListener('change', updateUrlParams);
  BUTTON.addEventListener('click', 求籤);

  initializeSelects();
  updateData();
}

main();
