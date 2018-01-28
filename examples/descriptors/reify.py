import requests


class reify(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, cls=None):
        if obj is None:
            return self

        print("Fetching google")
        value = self.func(obj)
        setattr(obj, self.func.__name__, value)
        return value


class A(object):
    @reify
    def google(self):
        return requests.get("http://www.google.com").text


a = A()
print(len(a.google))
print(len(a.google))
print(len(a.google))
print(len(a.google))
print(len(a.google))
