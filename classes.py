import json
from enum import Enum
from dataclasses import dataclass
from typing import Any, Optional

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement


class Language(Enum):
    JA = "ja"
    EN = "en"


class Faculty(Enum):
    UNDERGRADUATE = ("undergraduate", "10")
    MASTER = ("master", "20")
    DOCTOR = ("doctor", "30")


@dataclass
class Syllabus:
    id: str
    url: str
    name: str
    area: Optional[str] = None
    term: Optional[str] = None
    faculty: Optional[str] = None
    required: Optional[str] = None
    units: Optional[str] = None
    grade: Optional[str] = None
    staff: Optional[str] = None
    room: Optional[str] = None


# Syllabus→JSON
class SyllabusEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Syllabus):
            return o.__dict__
        return json.JSONEncoder.default(self, o)


class Utils:
    def __init__(self, driver: WebDriver, wait: WebDriverWait):
        self.driver = driver
        self.wait = wait

    def wait_and_find(self, by: str, value: Any) -> WebElement:
        return self.wait.until(EC.presence_of_element_located((by, value)))

    def get_inner_text(self, by: str, value: Any) -> Optional[str]:
        try:
            return self.driver.find_element(by, value).text.strip()
        except:
            return None
