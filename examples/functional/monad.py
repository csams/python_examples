class Functor(object):
    def fmap(self, f):
        raise NotImplemented()


class Monad(Functor):
    @classmethod
    def return_(cls, value):
        raise NotImplemented()

    def bind(self, f):
        return self.join(self.fmap(f))

    def join(self, x):
        raise NotImplemented()


def compose(f, g):
    def inner(x):
        res = g(x)
        return res.bind(f)
    return inner


def bind(res, f):
    return join(fmap(f, res))


def fmap(f, xs):
    return xs.fmap(f)


def join(x):
    return x.join(x)
