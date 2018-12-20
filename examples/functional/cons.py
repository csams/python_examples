"""
Lists can represent uncertainty in calculations. They allow functions to
return several values instead of just one. Each of those values get fed to
the next function, which returns it's own list of possible values for each
input.
"""
from monad import Monad


class List(Monad):
    @classmethod
    def unit(cls, x):
        return Cons(x)

    def join(self, x):
        """ x is Nil or a List(List a). Flatten it out. """
        if isinstance(x, Nil):
            return Nil()

        if isinstance(x.head, Nil):
            return Nil()

        return Cons.mappend(x.head, self.join(x.tail))

    @classmethod
    def from_list(cls, l):
        if not l:
            return Nil()
        return Cons(l[0], List.from_list(l[1:]))

    def to_list(self):
        p = self
        results = []
        while not isinstance(p, Nil):
            results.append(p.head)
            p = p.tail
        return results


class Nil(List):
    def fmap(self, func):
        return Nil()

    def mappend(self, value):
        return value

    def __repr__(self):
        return "Nil"


class Cons(List):
    def __init__(self, head, tail=None):
        self.head = head
        self.tail = tail or Nil()

    def fmap(self, func):
        return Cons(func(self.head), self.tail.fmap(func))

    def mappend(self, y):
        return Cons(self.head, self.tail.mappend(y))

    def __repr__(self):
        return repr(self.to_list())


# Just collect all combinations of x, y, and z.
combinations = List.from_list([1, 2, 3]).bind(lambda x:
               List.from_list([5, 6, 7]).bind(lambda y:
               List.from_list([8, 9, 0]).bind(lambda z:
               List.unit((x, y, z)))))
