from pyfunk import combinators as _
from pyfunk import collections as __


@_.curry
def maybe(x, fn, mb):
    '''
    Extract a Maybe's value providing a default if Nothing
    @sig maybe :: b -> (a -> b) -> Maybe a -> b
    '''
    return x if mb.nothing() else fn(mb._value)


@_.curry
def maybify(nullify, f):
    '''
    Creates a function that returns Maybe. Also accepts a Nonifier
    that checks that transforms falsy value to None. One can use
    misc.F if there is no need to nonify.
    @sig maybify :: (a -> Bool) -> (a -> b) -> (a -> Maybe b)
    '''
    return _.compose(lambda a: Maybe.of(None if nullify(a) else a), f)


@_.curry
def either(f, g, e):
    '''
    Extracts the values from either for transformation there f is for
    Left and g for Right
    @sig either :: Either a b => (a -> c) -> (b -> c) -> Either a b -> c
    '''
    if isinstance(e, Left):
        return f(e._value)
    elif isinstance(e, Right):
        return g(e._value)


def join(m):
    '''
    Unbound version of join
    @sig join :: Monad m => m (m a) -> m a
    '''
    return m.join()


@_.curry
def chain(fn, m):
    '''
    Unbound version of chain
    @sig chain :: Monad m => (a -> m b) -> m a -> m b
    '''
    return m.chain(fn)


def mcompose(*fns):
    '''
    Composes functions that produce monads
    @sig mcompose :: Monad m => ((b -> m c), (a -> m b)) -> (a -> m c)
    '''
    first = fns[-1:]
    rest = __.fmap(fns[:-1], chain)
    return _.compose(*(rest + (first,)))


class Container(object):

    def __init__(self, x):
        '''
        Create new Container
        @sig a -> Container a
        '''
        self._value = x

    @classmethod
    def of(cls, x):
        '''
        Factory for creating new container
        @sig of :: a -> Container a
        '''
        return cls(x)

    def fmap(self, fn):
        '''
        Transforms the value of the container using the given function
        @sig map :: Container a => (a -> b) -> Container b
        '''
        return self.of(fn(self._value))

    def join(self):
        '''
        Lifts a container out of another
        @sig join :: Container c => c (c a) -> c a
        '''
        return self._value

    def chain(self, fn):
        '''
        Transforms the value of the container using a function to a monad
        @sig chain :: Container a -> (a -> Container b) -> Container b
        '''
        return self.fmap(fn).join()


class Left(object):

    def __init__(self, x):
        '''
        Create new Left monad
        @sig a -> Left
        '''
        self._value = x

    @classmethod
    def of(cls, x):
        '''
        Factory for creating new Left monad
        @sig of :: a -> Left
        '''
        return cls(x)

    def fmap(self, fn):
        '''
        Does nothing
        @sig map :: Left => (a -> b) -> Left
        '''
        return self

    def join(self):
        '''
        Lifts a Left monad out of another
        @sig join :: Left l => _ -> Left
        '''
        return self

    def chain(self, fn):
        '''
        Does the same as join
        @sig chain :: Left -> (a -> Left) -> Left
        '''
        return self.fmap(fn).join()


Right = Container


class IO(object):

    def __init__(self, fn):
        '''
        Create new IO Monad
        @sig a -> IO a
        '''
        self.unsafeIO = fn

    @classmethod
    def of(cls, x):
        '''
        Factory for creating new IO monad
        @sig of :: a -> IO a
        '''
        return cls(lambda: x)

    def fmap(self, fn):
        '''
        Transforms the value of the IO monad using the given function
        @sig map :: IO a => (a -> b) -> IO b
        '''
        return IO(_.compose(fn, self.unsafeIO))

    def join(self):
        '''
        Lifts an IO monad out of another
        @sig join :: IO i => i (i a) -> c a
        '''
        return IO(lambda: self.unsafeIO().unsafeIO())

    def chain(self, fn):
        '''
        Transforms the value of the IO monad using a function to a monad
        @sig chain :: IO a -> (a -> IO b) -> IO b
        '''
        return self.fmap(fn).join()


class Maybe(object):

    def __init__(self, x):
        '''
        Create new Maybe Monad
        @sig a -> Maybe a
        '''
        self._value = x

    @classmethod
    def of(cls, x):
        '''
        Factory for creating new Maybe monad
        @sig of :: a -> Maybe a
        '''
        return Maybe(x)

    def nothing(self):
        '''
        Checks if the value of this Maybe is None.
        @sig nothing :: Maybe a => _ -> Bool
        '''
        return self._value is None

    def fmap(self, fn):
        '''
        Transforms the value of the Maybe monad using the given function
        @sig map :: Maybe a => (a -> b) -> Maybe b
        '''
        return Maybe.of(None) if self.nothing() \
            else Maybe.of(fn(self._value))

    def join(self):
        '''
        Lifts an Maybe monad out of another
        @sig join :: Maybe i => i (i a) -> c a
        '''
        return Maybe.of(None) if self.nothing() \
            else self._value

    def chain(self, fn):
        '''
        Transforms the value of the Maybe monad using a function to a monad
        @sig chain :: Maybe a -> (a -> Maybe b) -> Maybe b
        '''
        return self.fmap(fn).join()


class Task(object):

    def __init__(self, fn):
        '''
        Create new Container
        @sig a -> Task a b
        '''
        self.fork = fn

    @classmethod
    def of(cls, x):
        '''
        Factory for creating new resolved task
        @sig of :: b -> Task _ b
        '''
        return Task(lambda _, resolve: resolve(x))

    @classmethod
    def rejected(cls, x):
        '''
        Factory for creating a rejected task
        @sig rejected :: a -> Task a _
        '''
        return Task(lambda reject, _: reject(x))

    def fmap(self, fn):
        '''
        Transforms the resolved value of the task using the given function
        @sig map :: Task a b => (b -> c) -> Task a c
        '''
        return Task(lambda rej, res: self.fork(rej, _.compose(res, fn)))

    def join(self):
        '''
        Lifts a Task out of another
        @sig join :: Task a b => Task a Task b c -> Task a c
        '''
        return Task(lambda rej, res: self.fork(rej,
                    lambda x: x.fork(rej, res)))

    def chain(self, fn):
        '''
        Transforms the resolved value of the Task using a function to a monad
        @sig chain :: Task a -> (a -> Container b) -> Container b
        '''
        self.fmap(fn).join()

    def or_else(self, fn):
        '''
        Helps the use of making task even when dealing with rcover
        @sig or_else :: Task [a b] => (a -> Task [c b]) -> Task [c b]
        '''
        return Task(lambda rej, res: self.fork(
                    lambda x: x.fork(rej, res), res))
