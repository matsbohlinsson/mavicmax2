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

class B:
    def __init__(self, value):
        self.value=value
        pass

    def get(self):
        return self.value
    def set(self, value):
        self.value=value


class A:
    def __init__(self):
        self.aa = B(17)
        self.bb = B(73)
        self.cc = 12
        pass

    def __setattr__(self, key, value):
        print("__setattr__", key, value)
        try:
            getattr(self, key).set(value)
            pass
        except:
            super.__setattr__(self, key, value)

'''    def __getattr__(self, item):
        print("__getattr__", item)
        try:
            return super.__getattr__(item).get()
        except:
            return super.__getattr__(item)
'''
print("START")
a=A()
print(a.aa.value)
print("W", a.aa, a.aa.get())
a.aa = 117
a.cc = 1177
print("WWW", a.aa)


