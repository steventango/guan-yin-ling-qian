from googletrans import Translator, LANGUAGES


from pathlib import Path
import json
from tqdm import tqdm


def translate(data_path: Path, src_lang: str, dest_lang: str):
    translator = Translator()
    dest_path = data_path / dest_lang
    dest_path.mkdir(parents=True, exist_ok=True)

    for src_path in tqdm(list(data_path.glob(f"{src_lang}/*.json"))):
        output_path = dest_path / src_path.name
        if output_path.exists():
            continue
        with open(src_path, "r", encoding="utf-8") as f:
            src_data = json.load(f)
        dest_data = {}
        translations = translator.translate(list(src_data.values()), src=src_lang, dest=dest_lang)
        for key, translation in zip(src_data.keys(), translations):
            dest_data[key] = translation.text
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(dest_data, f)


def main():
    DATA_PATH = Path("data")
    SRC_LANG = "zh-tw"
    for dest_lang in tqdm(LANGUAGES):
        if dest_lang == SRC_LANG:
            continue
        translate(DATA_PATH, SRC_LANG, dest_lang)


if __name__ == "__main__":
    main()
