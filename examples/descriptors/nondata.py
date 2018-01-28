
class NonDataDescriptor(object):

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __get__(self, obj, cls=None):
        if obj:
            print("Getting:", self.name)
            return self.value
        return self


class A(object):
    thing = NonDataDescriptor("thing", 10)


a = A()
print(a.thing)

a.thing = 15
print(a.thing)
