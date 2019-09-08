from kontrakt import Condition, ContractError, ZeroOverheadContract
import pytest


class NonDecreasing(Condition):
    def precondition(self, *args):
        if not all(a <= b for a, b in zip(args, args[1:])):
            raise ValueError()


non_decreasing = ZeroOverheadContract(NonDecreasing())


@non_decreasing
def sum_three(a, b, c):
    return a + b + c


def test_precondition_allows_correct_invocations():
    sum_three(1, 2, 3)
    sum_three(1, 1, 1)


def test_precondition_failure_raises_ContractError():
    with pytest.raises(ContractError):
        sum_three(3, 2, 1)


def test_ContractError_includes_cause():
    try:
        sum_three(3, 2, 1)
    except ContractError as exc:
        assert isinstance(exc.__cause__, ValueError)


def test_direct_function_access():
    contract = ZeroOverheadContract(Condition())
    contract.enabled = False

    def foo():
        pass

    decorated = contract(foo)

    assert decorated is foo


def test_decorated_function_access():
    contract = ZeroOverheadContract(Condition())
    contract.enabled = True

    def foo():
        pass

    decorated = contract(foo)

    assert decorated is not foo
