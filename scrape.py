import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


RAW_PATH = Path("data/raw/")


def main():
    RAW_PATH.mkdir(parents=True, exist_ok=True)
    for n in tqdm(range(1, 101)):
        data_dict = {}
        response = requests.get(f"http://www.0961223888.com/kannon/Kannon{n}.htm")
        response.encoding = response.apparent_encoding

        if response.status_code != 200:
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.find_all("tr")
        for row in rows:
            columns = row.find_all("td")
            key = columns[0].text.strip()
            value = None
            if len(columns) > 1:
                value = columns[1].text.strip()
            data_dict[key] = value

        with open(RAW_PATH / f"{n}.json", "w", encoding="utf-8") as json_file:
            json.dump(data_dict, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
