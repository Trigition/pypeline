import pytest

import utils
from pypeline.pype import Pypeline

def test_std_creation():
    """Can we create a valid Pypeline
    """
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


def test_singleton():
    """Tests adding 1 lone function
    :returns: TODO

    """
    pype = Pypeline(2)
    pype.link(lambda x: print(x))


def test_linear_chain():
    """Tests aligning functions into pipeline
    """
    pype = Pypeline(2)
    src = lambda x: 2*x
    pype.link(src)
    pype.link(src, lambda y: print(y))

def test_linear_runtime():
    """Tests running simple multiplication pypeline
    """
    pype = Pypeline(2)
    #f1 = lambda x: 2*x
    #f2 = lambda x: 3*x
    f1 = utils.mul_by_2
    f2 = utils.mul_by_3
    pype.link(f1)
    pype.link(f1, f2)
    test_input = [0,1,2,3,4,5]
    pype.load_data(test_input)
    result = pype.run()
    print(test_input)
    print(result[f2])
    assert [i*6 for i in test_input] == result[f2]
