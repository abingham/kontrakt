
from kontrakt import Condition, ZeroOverheadContract


# 1. Create a Condition class.
class NonDecreasing(Condition):
    def precondition(self, *args):
        if not all(a <= b for a, b in zip(args, args[1:])):
            raise ValueError('Arguments must be non-descending')


# 2. Instantiate a contract using the condition.
non_decreasing = ZeroOverheadContract(NonDecreasing())


# 3. Apply the contract to a function
@non_decreasing
def my_func(a, b, c):
    return a + b + c


# Use the function.
my_func(1, 2, 3)
my_func(1, 1, 1)
my_func(3, 2, 1) # Will throw