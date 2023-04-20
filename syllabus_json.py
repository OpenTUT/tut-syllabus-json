import os, sys, json, time
from typing import Dict

import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select

from classes import Language, Faculty, Syllabus, SyllabusEncoder
from utils import Utils


def get_syllabus(
    utils: Utils,
    language: Language,
    year: str,
    url: str,
) -> Syllabus:
    utils.driver.get(url)
    utils.wait_and_find(By.ID, "ctl00_phContents_Detail_LctInfo")

    syllabus = Syllabus(
        id=utils.get_inner_text(By.ID, "ctl00_phContents_Detail_lbl_lct_cd"),
        url=url,
        name=utils.get_inner_text(By.ID, "ctl00_phContents_Detail_lbl_sbj_name"),
        area=utils.get_inner_text(By.ID, "ctl00_phContents_Detail_lbl_sbj_area_name")
        or None,
        term=utils.get_inner_text(By.ID, "ctl00_phContents_Detail_lbl_term_name")
        or None,
        faculty=utils.get_inner_text(By.ID, "ctl00_phContents_Detail_lbl_fac_name")
        or None,
        required=utils.get_inner_text(By.ID, "ctl00_phContents_Detail_lbl_req_name")
        or None,
        units=utils.get_inner_text(By.ID, "ctl00_phContents_Detail_lbl_credits")
        or None,
        grade=utils.get_inner_text(By.ID, "ctl00_phContents_Detail_lbl_open_grad_name")
        or None,
        staff=utils.get_inner_text(By.ID, "ctl00_phContents_Detail_lbl_staff_name")
        or None,
    )

    if language == Language.EN:
        syllabus.name = utils.get_inner_text(
            By.ID, "ctl00_phContents_Detail_lbl_sbj_name_e"
        )
        if len(syllabus.name) > 0 and syllabus.name[0] == "[":
            syllabus.name = syllabus.name[1:-1]
        syllabus.staff = (
            utils.get_inner_text(By.ID, "ctl00_phContents_Detail_lbl_staff_name_e")
            or None
        )

    # 部屋情報だけ別のURLから取得
    utils.driver.get(
        f"https://kyomu.office.tut.ac.jp/portal/StudentApp/Lct/LectureList.aspx?lct_year={year}&lct_cd={syllabus.id}"
    )
    utils.wait_and_find(By.ID, "ctl00_phContents_ucLctList_ucLctHeader_tbRowHeader")
    syllabus.room = (
        utils.get_inner_text(
            By.CSS_SELECTOR,
            "#ctl00_phContents_ucLctList_gv > tbody > tr:nth-child(2) > td:nth-child(5)",
        )
        or None
    )

    return syllabus


def get_syllabuses_by_faculty(
    utils: Utils,
    language: Language,
    year: str,
    faculty: Faculty,
) -> Dict[str, Syllabus]:
    utils.driver.get("https://kyomu.office.tut.ac.jp/portal/public/syllabus/")

    # 言語選択
    if language == Language.JA:
        utils.wait_and_find(By.ID, "ctl00_bhHeader_slLanguage_imgBtnJpn").click()
    elif language == Language.EN:
        utils.wait_and_find(By.ID, "ctl00_bhHeader_slLanguage_imgBtnEng").click()

    # 年度・学部選択
    Select(utils.wait_and_find(By.ID, "ctl00_phContents_ddl_year")).select_by_value(
        year
    )
    Select(utils.wait_and_find(By.ID, "ctl00_phContents_ddl_fac")).select_by_value(
        faculty.value[1]
    )
    utils.wait_and_find(By.ID, "ctl00_phContents_ctl06_btnSearch").click()

    # シラバスURL一覧
    Select(
        utils.wait_and_find(By.ID, "ctl00_phContents_ucGrid_ddlLines")
    ).select_by_index(0)
    utils.wait_and_find(By.ID, "ctl00_phContents_ucGrid_grv")
    urls = [
        element.get_attribute("href")
        for element in driver.find_elements(
            By.CSS_SELECTOR, "#ctl00_phContents_ucGrid_grv a"
        )
    ]

    syllabuses = {}

    for url in tqdm.tqdm(urls, desc=f"{language.value}/{year}/{faculty.value[0]}"):
        syllabus = get_syllabus(utils, language, year, url)
        syllabuses[syllabus.id] = syllabus
        time.sleep(1)

    return syllabuses


driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
utils = Utils(driver, wait)
year = sys.argv[1]

# ログイン
driver.get("https://kyomu.office.tut.ac.jp/portal/")
cookies = driver.get_cookies()
while driver.current_url != "https://kyomu.office.tut.ac.jp/portal/StudentApp/Top.aspx":
    pass
utils.wait_and_find(By.ID, "ctl00_bhHeader_lnkLogout")

# 全シラバス取得・保存
for language in Language:
    os.makedirs(f"./out/{language.value}/{year}", exist_ok=True)

    for faculty in Faculty:
        syllabuses = get_syllabuses_by_faculty(utils, language, year, faculty)

        with open(f"./out/{language.value}/{year}/{faculty.value[0]}.json", "w") as f:
            json.dump(
                syllabuses,
                f,
                cls=SyllabusEncoder,
                indent=2,
                ensure_ascii=False,
            )

driver.quit()
