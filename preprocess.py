from pathlib import Path
import json
from tqdm import tqdm
import re

DATA_PATH = Path("data")
RAW_PATH = DATA_PATH / "raw"
DEST_LANG = "zh-tw"

CONSTANT_SET = {"觀音靈籤", "解曰", "古人", "此簽", "求籤"}


def write_constants():
    constants = {}
    for constant in CONSTANT_SET:
        constants[f"{constant}_"] = constant
    dest_constants_path = DATA_PATH / DEST_LANG / "constants.json"
    with open(dest_constants_path, "w", encoding="utf-8") as f:
        json.dump(constants, f, ensure_ascii=False)


def write_preprocessed(raw_path: Path, dest_path: Path):
    with open(raw_path, "r", encoding="utf-8") as f:
        src_data = json.load(f)
    dest_data = {}
    KEYS = ["籤詩版本二", "詩  意", "解  曰", "籤詩故事一", "聖  意", "第X籤"]
    for key in KEYS:
        src_value = src_data.get(key)
        if src_value:
            dest_data[key.replace("\u00A0", "")] = src_value.replace("\t", "")
    if "解曰" in dest_data:
        dest_data["解曰"] = re.sub(r"（[^)]*\）", "", dest_data["解曰"])
    if "籤詩故事一" in dest_data:
        dest_data["古人"] = dest_data["籤詩故事一"].split("\n", 1)[0][1:]
    if "聖意" in dest_data:
        dest_data["聖意"] = dest_data["聖意"].replace("\n\n\n", "\n")
        dest_data["聖意"] = dest_data["聖意"].replace("\n", "")
        dest_data["聖意"] = dest_data["聖意"].replace(" ", "")
        dest_data["聖意"] = dest_data["聖意"].replace("\u3000", "")
        dest_data["聖意"] = dest_data["聖意"].replace("。", "")
        dest_data["詩意"] = dest_data["詩意"].replace("。", "。\n")
    if "籤詩版本二" in dest_data:
        temp = dest_data["籤詩版本二"].split("\n")
        dest_data["籤詩版本二"] = " ".join(temp[:2]) + "\n" + " ".join(temp[2:])
    second_src_key, second_src_value = list(src_data.items())[1]
    籤, 宮 = second_src_value.split("。")
    dest_data["第X籤"] = second_src_key[:-1] + 籤
    dest_data["宮"] = 宮
    with open(dest_path / raw_path.name, "w", encoding="utf-8") as f:
        json.dump(dest_data, f, ensure_ascii=False)


def main():
    write_constants()
    for raw_path in tqdm(list(RAW_PATH.glob("*.json"))):
        dest_path = DATA_PATH / DEST_LANG
        dest_path.mkdir(parents=True, exist_ok=True)
        write_preprocessed(raw_path, dest_path)


if __name__ == "__main__":
    main()
