from pyfunk.combinators import compose, curry, fnot
from pyfunk.misc import T


def test_compose():
    fn2 = compose(lambda x: x * 4, lambda x: x * 2)
    assert fn2(3) == (3 * 2 * 4)

    fn3 = compose(lambda x: x * 8, lambda x: x * 4, lambda x: x * 2)
    assert fn3(3) == (3 * 2 * 4 * 8)


def test_curry():
    add3 = curry(lambda a, b, c: a + b + c)
    assert add3(1, 2, 3) == 6
    assert add3(1, 2)(3) == 6
    assert add3(1)(2, 3) == 6
    assert add3(1)(2)(3) == 6


def test_fnot():
    twist = fnot(T)
    assert twist() is False
    assert twist(1, 2, 3) is False
