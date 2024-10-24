#!/usr/bin/env python3
"""
A simple caching class using Redis.
"""
import redis
import uuid
from typing import Union, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Count how many times methods of the Cache class are called."""
    @wraps(method)
    def wrapper(self, *args, **kwds) -> Any:
        """Returns the callled method"""
        if isinstance(self, Cache):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwds)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Stores the output and inputs of the called method"""
    @wraps(method)
    def wrapper(self, *args, **kwds) -> Any:
        """Stores the output and inputs of the called method"""
        input_key = "{}:inputs".format(method.__qualname__)
        output_key = "{}:outputs".format(method.__qualname__)
        if isinstance(self, Cache):
            self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwds)
        if hasattr(self, '_redis'):
            self._redis.rpush(output_key, output)
        return output
    return wrapper


def replay(method: Callable) -> None:
    """call history of a Cache class' method."""
    if method is None or not hasattr(method, '__self__'):
        return
    method_name = method.__qualname__
    input_key = "{}:inputs".format(method_name)
    output_key = "{}:outputs".format(method_name)
    redis = getattr(method.__self__, '_redis', None)
    if redis.exists(method_name):
        print("{} was called {} times".format(
            method_name, int(redis.get(method_name))))
    method_inp = redis.lrange(input_key, 0, -1)
    method_out = redis.lrange(output_key, 0, -1)
    for key, value in zip(method_inp, method_out):
        print('{}(*{}) -> {}'.format(method_name, key, value))


class Cache:
    """
    Represent an object for storing data in a Redis.
    """

    def __init__(self):
        """Initializes the Cache,
        connecting to Redis and flushing the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores data in the cache and returns the generated key."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
            self, key: str, fn: Callable = None
            ) -> Union[str, bytes, int, float]:
        """Retrives data from the storage"""
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        """Retrive str from the storage"""
        return self.get(key, lambda x: str(x))

    def get_int(self, key: str) -> int:
        """Retrive int from the data storage"""
        return self.get(key, lambda x: int(x))
