## Monads, Python Style

The code here is meant to illustrate concepts. I wouldn't actually write python
code in this way.

Monads are a type of object and a way of composing functions that handle objects
of that type.

Here's regular function composition, read "f after g." The output of g directly
matches the input of f.
```python
def compose(f, g):
    def inner(x):
        res = g(x)
        return f(res)
    return inner

def one(a):
    return a + 1

def two(a):
    return a + 2

three = compose(one, two)
five = compose(three, two)
```

Say we want the notion of "Maybe" having a value. If we have it, it's Just
the value. If we don't, it's Nothing. It's like an exception except you don't
care aboue the details when something blows up.
```python
class Maybe(object):
    pass

class Just(Maybe):
    def __init__(self, value):
        self.value = value

class Nothing(Maybe):
    pass

a = Just(4)
b = Just(5)
c = Nothing()
```

Now say we have a function that returns a valid value on all inputs but zero.
```python
def i_hate_zero(a):
    if a == 0:
        return Nothing()
    return Just(a)
```

And we have another function that hates ones.
```python
def i_hate_one(a):
    if a == 1:
        return Nothing()
    return Just(a)
```

And we want to compose i_hate_zero with i_hate_one to make a function that
hates both.

We can't just `compose(i_hate_zero, i_hate_one)`. They both take regular values
and return a `Maybe`.

So.. just redefine function composition for functions that do that.
```python
def maybe_compose(f, g):
    def inner(x):
        res = g(x)
        if isinstance(res, Nothing):
            return Nothing()
    return f(res.value)

i_hate_zero_and_one = compose(i_hate_zero, i_hate_one)
```

We took two functions from `thing -> Maybe thing` and made a third one.

And that's the big insight behind Monads. They're objects like Maybe and a way
of combining functions that return them. There also are a bunch of laws that
they must obey, but those laws aren't written with the above intuition in mind.

The way we normally see monads comes from factoring boilerplate out of the
`maybe_compose` function above. `compose` is normally implemented in terms of
another function called `bind`, which is itself implemented in terms of a
function called `join`. Here's another version of `compose`:
```python
def maybe_compose(f, g):
    def inner(x):
        res = g(x)
        return maybe_bind(res, f)
    return inner
```

We're just factoring out the isinstance business. Notice that the type of `bind`
is `bind(Maybe thing, (f(thing): Maybe thing)): Maybe thing`. It takes a `Maybe`
and a function and returns a `Maybe`. The function takes a thing and returns a
`Maybe`.
```python
def maybe_bind(res, f):
    if isinstance(res, Nothing):
        return Nothing()
    return f(res.value)
```

But even `maybe_bind` has some boilerplate if `Maybe` is a `Functor`. Note that
`fmap` sneaks a function inside a `Functor` to modify its contents.
```python
def maybe_fmap(f, m):
    if isinstance(m, Nothing):
        return Nothing()
    return Just(f(m.value))
```

maybe_bind can now be defined as
```python
def maybe_bind(res, f):
    return maybe_fmap(f, res)
```

Well, almost. That will give you a `Just(Just(value))`. `fmap` gets you into the
`Maybe` that is res, but `f` itself returns a `Maybe`. That means `f` might drop
a `Just` inside the existing `Just`. We need a way to flatten that out.

It's called `join`:
```python
def maybe_join(m):
    if isinstance(m, Nothing):
        return Nothing()
    return m.value
```

now `maybe_bind` can be fully defined like this:
```python
def maybe_bind(res, f):
    return maybe_join(maybe_fmap(f, res))
```

So, if python handled dispatch of polymorphic functions in a different way you
could define compose and bind just once for all Monads like this:
```python
def compose(f, g):
    def inner(x):
        res = g(x)
        return bind(res, f)
    return inner


def bind(res, f):
    return join(fmap(f, res))
```

If you lean on duck typing and have your `Monad` instances subclass an actual
`Monad` class that requires `fmap` and `join` to be written in them, you can do
this:
```python
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
```

Most languages that use `Monads` have a particular operator for `bind` and are
very functional. Languages like `Haskell` even have `do-notation` for bind that
make using it look more imperative, even though it isn't. The same is true of
scala's "for / yield" construct. It's a lot like Haskell `do-notation`.

If I make up some monad syntax for python and pretend return works differently,
this
```python
result = Just(4).bind(lambda x:
         Just(3).bind(lambda y:
         Maybe.unit(x * y)))

```

might look like this
```python
result = {
    x <- Just(4)
    y <- Just(3)
    return (x * y)
}
```

And this
```python
combinations = List.from_list([1, 2, 3]).bind(lambda x:
               List.from_list([5, 6, 7]).bind(lambda y:
               List.from_list([8, 9, 0]).bind(lambda z:
               List.unit((x, y, z)))))
```

might look like this:
```python
results = {
    x <- [1, 2, 3]
    y <- [5, 6, 7]
    z <- [8, 9, 0]
    return (x, y, z)
}
```

Check out the code in this package to see some of the `python` versions of those
examples.
