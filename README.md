# kontrakt

An outline of how you might implement almost-zero-overhead
contracts in Python. 

The basic idea is that you apply contracts by decorating functions. The contracts can be en/disabled in various ways.
The most interesting type of contract is the "zero-overhead" one which - if disabled at the point of decoration - will
simply return the decorated function.

NB: This is mostly a sketch. Don't rely on it or believe it without looking at it yourself!

## Tests

There are a few unit tests you can run like this::

    pip install -r requirements.txt
    pytest .