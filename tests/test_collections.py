from pyfunk import collections as _
from pyfunk.misc import T


def test_fmap():
    oresult = _.fmap(lambda x: x * 2, {'a': 1, 'b': 2})
    assert oresult['a'] == 2
    assert oresult['b'] == 4

    aresult = _.fmap(lambda x: x * 2, [1, 2])
    assert aresult[0] == 2
    assert aresult[1] == 4


def test_fslice():
    aresult = _.fslice(0, 2, [0, 1, 2, 3])
    assert aresult[0] == 0
    assert len(aresult) == 2

    tresult = _.fslice(0, 2, (0, 1, 2, 3))
    assert tresult[0] == 0
    assert len(tresult) == 2

    sresult = _.fslice(0, 5, 'helloworld')
    assert sresult == 'hello'

    allresult = _.fslice(0, None, [0, 1, 2, 3])
    assert len(allresult) == 4


def test_ffilter():
    oresult = _.ffilter(T, {'a': 1, 'b': 2})
    assert len(oresult) == 2

    aresult = _.ffilter(lambda x: x < 3, [0, 1, 2, 3])
    assert len(aresult) == 3


def test_prop():
    assert _.prop('b', {'a': 1, 'b': 2}) == 2


def test_concat():
    assert len(_.concat((1, 2), (3, 4))) == 4
    assert len(_.concat([1, 2], [3, 4])) == 4
    assert _.concat('hello', 'world') == 'helloworld'


def test_index_of():
    assert _.index_of(lambda x: x == 3, [1, 2, 3, 4, 5]) == 2
    assert _.index_of(lambda x: x == 6, [1, 2, 3, 4, 5]) == -1


def test_array_get():
    assert _.array_get(3, [1, 2, 3, 4, 5]) == 4
    assert _.array_get(24, [1, 2, 3, 4, 5]) is None


def test_first():
    assert _.first(lambda x: x > 4, [1, 2, 3, 4, 5]) == 5


def test_head():
    assert _.head([1, 2, 3, 4, 5]) == 1


def test_take_while():
    assert len(_.take_while(lambda x: x < 3, [1, 2, 3, 4, 5])) == 2
    assert len(_.take_while(lambda x: x > 8, [1, 2, 3, 4, 5])) == 0


def test_drop_while():
    assert len(_.drop_while(lambda x: x < 3, [1, 2, 3, 4, 5, 6])) == 4
    assert len(_.drop_while(lambda x: x < 8, [1, 2, 3, 4, 5])) == 0
