from examples.decorators.dr import component


@component()
def two():
    return 2


@component()
def three():
    return 3


@component([two, three])
def add(a, b):
    return a + b


class Common(object):
    def __init__(self, obj):
        self.obj = obj

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.obj)


@component([add])
class A(Common):
    pass


@component([add])
class B(Common):
    pass


@component(["c"])
class C(Common):
    pass
