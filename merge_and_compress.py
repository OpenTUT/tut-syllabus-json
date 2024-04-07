import json
import os
import pathlib
import sys

from classes import Faculty, Language, SyllabusEncoder

year = "2024"

# 全シラバス取得
for language in Language:
    os.makedirs(f"./out/{language.value}/{year}", exist_ok=True)
    all_syllabuses = {}

    json_files = list(
        filter(
            lambda x: x.name != "all.min.json",
            pathlib.Path(f"./out/{language.value}/{year}").glob("*.json"),
        )
    )

    for json_file in json_files:
        with open(json_file, "r") as f:
            all_syllabuses.update(json.load(f))

    # minifyしたJSONを保存
    with open(f"./out/{language.value}/{year}/all.min.json", "w") as f:
        json.dump(
            all_syllabuses,
            f,
            cls=SyllabusEncoder,
            separators=(",", ":"),
        )
