
from typing import List


class Foo():
    def __init__(self,attr1,attr2) -> None:
        self.attr1 = attr1
        self.attr1 = attr2
        pass

test = []
test.append([Foo(1,2),Foo(3,4)])
#del(test[0][1])
print(test[0][1].attr1)