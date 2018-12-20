"""
Probability Monad

Given a set of events of possibly differing probability, what's the probability
of all of their combinations?
"""
from cons import List
from monad import Monad


class Prob(Monad):
    @classmethod
    def unit(self, x):
        return Prob(List.from_list([(x, 1.0)]))

    def __init__(self, x):
        """
        x is a List of pairs Cons((evt1, prob1), Cons((evt2, prob2), ...
        """
        self.value = x

    def fmap(self, f):
        """
        `f` can only change the evt. It leaves the probability the same.
        """
        return Prob(self.value.fmap(lambda x: (f(x[0]), x[1])))

    def join(self, x):
        """
        x is Prob([(Prob([(evt, p1), (evt, p2)]), outerp1), (Prob([...
        """
        val = x.value.fmap(self.combine)
        return Prob(val.join(val))

    def combine(self, x):
        prob, po = x
        return prob.value.fmap(lambda e: (e[0], po * e[1]))

    def __repr__(self):
        return "Prob({!r})".format(self.value.to_list())


HEADS = 0
TAILS = 1

coin1 = Prob(List.from_list([(HEADS, 0.5), (TAILS, 0.5)]))
coin2 = Prob(List.from_list([(HEADS, 0.5), (TAILS, 0.5)]))
loaded = Prob(List.from_list([(HEADS, 0.9), (TAILS, 0.1)]))

# get probabilities for all flip combinations.
all_flips = coin1.bind(lambda x:
            coin2.bind(lambda y:
            loaded.bind(lambda z:
            Prob.unit([x, y, z]))))
