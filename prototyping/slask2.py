import dataclasses
from enum import Enum


@dataclasses.dataclass
class AA:
    a: int = 1
    aa: str = "asdfg"
    _a: int=2


def filter_dict(d:dict, startswith:str='_') -> dict:
    return dict(filter(lambda elem: not elem[0].startswith(startswith), d.items()))



print(AA().__dict__)
print(filter_dict(AA().__dict__))


class Select(Enum):
    SPORT = 1
    MANUAL = 2
    GPS = 2


def makeEnumDict(o):
    return {i.name: i.value for i in o}

print("QQQ", makeEnumDict(Select))

print(round(12.346,2))





print("WW", 3<<2)

print("", 0b00011 | 0b00011)
