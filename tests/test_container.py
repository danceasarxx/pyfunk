from pyfunk.functors import Container


def test_of():
    assert isinstance(Container.of(3), Container)
    assert Container.of(3)._value == 3


def test_fmap():
    assert Container.of(4).fmap(lambda x: x * 2)._value == 8


def test_join():
    assert Container.of(4).fmap(lambda x: Container.of(x * 2)).join()._value == 8


def test_chain():
    assert Container.of(3).chain(lambda x: Container.of(x * 2))._value == 6
