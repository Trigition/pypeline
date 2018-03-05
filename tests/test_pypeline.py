from pypeline.pype import Pypeline
import pytest


def test_std_creation():
    """Can we create a valid Pypeline
    """
    print(dir(p))
    print(dir(p.node))
    assert Pypeline(1) is not None


def test_do_not_allow_negative():
    """Test against negative thread count
    specifications
    """
    with pytest.raises(ValueError):
        Pypeline(-1)


def test_allow_only_ints():
    """Test against non integer inputs
    """
    with pytest.raises(ValueError):
        Pypeline(5.6)
    with pytest.raises(ValueError):
        Pypeline('This should fail')
    with pytest.raises(ValueError):
        Pypeline(['This', 'should', 'fail', 'too'])
