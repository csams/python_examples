import logging

from examples.util import get_name

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

# Demystifying Decorators

# But first, some background...


# Functions and classes in python are first class citizens. They can be passed
# as arguments, created in any environment, and returned as values.

def square(x):
    return x * x


def mymap(func, args):
    return [func(a) for a in args]


print "mymap(square, range(5))"
print mymap(square, range(5))


class A(object):
    def __init__(self, obj):
        self.obj = obj

    def __repr__(self):
        return "A(%s)" % self.obj


print "mymap(A, range(5))"
print mymap(A, range(5))


def make_multiplier(n):
    def inner(x):
        return n * x
    return inner


mul_four = make_multiplier(4)
print "mul_four(3)"
print mul_four(3)


# Q: What is a decorator?
# A: Any single argument callable.

# Better Q: What is decorator syntax?
# A: Syntactic sugar for a special kind of invocation and assignment idiom.

# The decorator operator invokes a callable against a function or class at the
# point the function or class is defined and assigns the result of the
# invocation to the function or class symbol.


# Example:
# "simple_decorator" is our decorator.

def simple_decorator(obj):
    """ This is a simple decorator. It accepts some object as its only parameter
        and returns that same object as its value. This function is called only
        once per decorated object at the time the object is defined.
    """
    log.info("Calling %s with %s" % (get_name(simple_decorator), get_name(obj)))
    return obj


# without decorator syntax, we just define a function and then explicitly
# call the decorator with it as an argument.
def times_two(a):
    return 2 * a


times_two = simple_decorator(times_two)

# THIS IS ALL A DECORATOR IS.
# All the other complexity around decorators comes from other standard python
# language features.


# Example with decorator syntax.
# The "@" symbol handles the invocation.
@simple_decorator
def times_three(a):
    return 3 * a

# Since decorator syntax is just sugar for a special kind of call and
# assignment, it can be used against anything that can be defined in-place.
# Note that simple_decorator isn't explicitly called. e.g., there are no
# parens after the name: @simple_decorator and not @simple_decorator()
# The @ operator takes care of calling the decorator function against the
# decorated object. @simple_decorator() would first explicitly call simple_decorator
# and then the @ operator would implicitly call the result of that call.


# Here is an example using a class:
@simple_decorator
class B(object):
    pass
