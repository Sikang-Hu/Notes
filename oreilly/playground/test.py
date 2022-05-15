class MyBase:
    def __init__(self, value):
        self.value = value
    
class MyBase1(MyBase):
    def __init__(self):
        MyBase.__init__(self, 1)
        self.value += 1

class MyBase2(MyBase):
    def __init__(self):
        MyBase.__init__(self, 1)
        self.value += 2

class MyChild(MyBase1, MyBase2):
    def __init__(self):
        MyBase2.__init__(self)
        MyBase1.__init__(self)


if __name__ == '__main__':
    a = MyChild()
    print(a.__dict__)
