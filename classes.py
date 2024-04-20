import json
from enum import Enum
from dataclasses import dataclass
from typing import Any, Optional


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
