import dataclasses


class Select:
    def __init__(self, value, list_of_strings:[str]):
        self.list_of_strings = list_of_strings
        self.value = value

    def set(self, x):
        self.value = x

    def __repr__(self):
        print("WW")
        return self.value

s=Select('mats', ['mats', 'anders', 'nils'])


@dataclasses.dataclass
class MyClass(object):
    name:str = Select('mats', ['mats', 'anders', 'nils'])

    def __repr__(self):
        print("QQ")
        return self.name

    def __setattr__(self, name, value):
        print(f'__setattr__(self, {name}, {value})')
        print("dict", self.__dict__)
        if name in self.__dict__:
            self.__dict__[name].set(value)
        else:
            self.__dict__.update({name:value})


a=MyClass()
print(1,a.name)
a.name='ander'
print(2, a.name)


class Meta:
    pass

class MetaDataMinMax:
    def __init__(self, min, max):
        pass
    pass

class MetaDataSelect:
    def __init__(self, str_list):
        pass
    pass

@dataclasses.dataclass
class Input(Meta):
    speed_x: int  = 12
    speed_x_meta: MetaDataMinMax = MetaDataMinMax(min=10, max=30)
    mode: str = 'NORMAL'
    mode_meta: MetaDataSelect = MetaDataSelect(str_list=['NORMAL', 'SPORT', 'ATTI'])

