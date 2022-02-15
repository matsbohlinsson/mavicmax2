
class A:
    def __init__(self):
        print("A created")

    def __del__(self):
        print("A deleted")



class B:
    def __init__(self):
        print("B created")
        self.a = A()
    def __del__(self):
        print("B deleted")

b=B()
c = b
del b

print("q", c)

