"""
Maybe is like exception handling when you don't care about the details. If you
have a sequence of operations and want the final value to be Nothing if any
of them returns Nothing, then use Maybe. It factors out the "null check" after
every function call in a sequence.
"""
from monad import Monad


class Maybe(Monad):
    @classmethod
    def unit(cls, x):
        return Just(x)

    def join(self, x):
        if isinstance(x, Nothing):
            return Nothing()
        return x.value


class Just(Maybe):
    def __init__(self, value):
        self.value = value

    def fmap(self, func):
        return Just(func(self.value))

    def __repr__(self):
        return "Just({!r})".format(self.value)


class Nothing(Maybe):
    def fmap(self, func):
        return Nothing()

    def __repr__(self):
        return "Nothing"


result = Just(4).bind(lambda x:
         Just(3).bind(lambda y:
         Maybe.unit(x * y)))
