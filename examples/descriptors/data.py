class DataDescriptor(object):

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __get__(self, obj, cls=None):
        if obj:
            print("Getting:", self.name)
            return self.value
        return self

    def __set__(self, obj, value):
        print("Setting:", self.name, "to", value)
        self.value = value


class A(object):
    thing = DataDescriptor("thing", 10)


a = A()
print(a.thing)

a.thing = 15
print(a.thing)
