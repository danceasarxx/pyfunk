from pyfunk.monads import Left, Right, cata
from pyfunk.misc import fid


def getT(a):
    if a < 10:
        return Left.of('Must be more than 10')
    else:
        return Right.of(a * 2)


def test_of():
    assert isinstance(Left.of(3), Left)
    assert Left.of(3)._value == 3


def test_fmap():
    left = Left.of(4)
    assert left.fmap(lambda x: x * 2) == left


def test_join():
    assert Left.of(4).fmap(lambda x: Left.of(x * 2)).join()._value == 4


def test_chain():
    assert Left.of(3).chain(lambda x: Left.of(x * 2))._value == 3


def test_either():
    g1 = getT(3)
    assert cata(fid, lambda x: x/2, g1) == 'Must be more than 10'

    g2 = getT(11)
    assert cata(lambda x: x * 2, lambda x:  x/2, g2) == 11
