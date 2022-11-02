import os, sys, json

from classes import Language, Faculty, SyllabusEncoder

year = sys.argv[1]

# 全シラバス取得
for language in Language:
    os.makedirs(f"./out/{language.value}/{year}", exist_ok=True)
    all_syllabuses = {}

    for faculty in Faculty:
        with open(f"./out/{language.value}/{year}/{faculty.value[0]}.json", "r") as f:
            all_syllabuses |= json.load(f)

    # minifyしたJSONを保存
    with open(f"./out/{language.value}/{year}/all.min.json", "w") as f:
        json.dump(
            all_syllabuses,
            f,
            cls=SyllabusEncoder,
            separators=(",", ":"),
        )
