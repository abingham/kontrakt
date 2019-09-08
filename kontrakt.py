class ContractError(Exception):
    """Exception raised when there is a contract violation.

    The causal exception will be explicitly chained to this, i.e. in the __cause__ attribute.
    """
    pass


class _Invocation:
    """Manage a specific invocation of a function wrapped in a contract.
    """
    def __init__(self, condition, *args, **kwargs):
        self.condition = condition
        self.args = args
        self.kwargs = kwargs
        self.result = None

    def __enter__(self):
        try:
            self.condition.precondition(*self.args, **self.kwargs)
        except Exception as exc:
            raise ContractError() from exc

        return self

    def __exit__(self, *exc):
        try:
            self.condition.postcondition(self.result, exc, *self.args, **self.kwargs)
        except Exception as exc:
            raise ContractError() from exc


class Contract:
    "Base for contracts. Not usable as a decorator."
    def __init__(self, condition):
        self.condition = condition
        self.enabled = True

    def _invoke(self, f, *args, **kwargs):
        with _Invocation(self.condition, *args, **kwargs) as inv:
            inv.result = f(*args, **kwargs)
            return inv.result


class ZeroOverheadContract(Contract):
    """A contract that checks its enabled state only once, when the decorator is applied.

    This is *almost* zero overhead. If the condition is disabled, then the only cost for using this is the application
    of the decorator; after that, the original decorated function is called directly.

    The downside to this contract is that it can't be en/disabled at runtime (after decoration). If you need to be able
    to toggle your contracts at runtime, look at `DynamicContract`.
    """
    def __call__(self, f):
        if not self.enabled:
            return f

        def wrapper(*args, **kwargs):
            self._invoke(f, *args, **kwargs)

        return wrapper


class DynamicContract(Contract):
    """A contract that can be en/disabled at run time (i.e. after decoration).
    """
    def __call__(self, f):
        def wrapper(*args, **kwargs):
            if not self.enabled:
                return f(*args, **kwargs)

            return self._invoke(f, *args, **kwargs)

        return wrapper


class Condition:
    """Specification of a pre- and post-condition pair.

    Subclass this and override `precondition` and `postcondition` to create conditions for your contracts.
    """
    def precondition(self, *args, **kwargs):
        """Called to enforce a precondition.

        Raise an exception to signal a condition failure.

        Args: 
            args: The tuple of positional args passed to the function.

            kwargs: The dict of keyword args passed to the function.
        """
        pass

    def postcondition(self, result, exc_info, *args, **kwargs):
        """Called to enforce a postcondition.

        Raise an exception to signal a condition failure.

        Args: 
            result: The return value of the function. This will be `None` if the function raised an exception. This
                will also be `None` if the function returned `None`, so you need to check `exc_info` to interpret this.

            exc_info: A tuple of `(exception-type, exception-value, exception-traceback)`. If there was no exception 
                thrown, these will be `None`. Otherwise, they will all be set. If these are `None`, then the `result` 
                argument indicates a value actually returned from the function.

            args: The tuple of positional args passed to the function.

            kwargs: The dict of keyword args passed to the function.
        """
        pass

