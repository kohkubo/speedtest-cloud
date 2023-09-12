from dataclasses import dataclass


@dataclass
class FileDetails:
    path: str
    size: float
    time: float
    speed: float
