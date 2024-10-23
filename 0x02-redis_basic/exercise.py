#!/usr/bin/env python3
"""
A simple caching class using Redis.
"""
import redis
import uuid
from typing import Union, Callable


class Cache:
    """
    Represent an object for storing data in a Redis.
    """

    def __init__(self):
        """Initializes the Cache,
        connecting to Redis and flushing the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores data in the cache and returns the generated key."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
            self, key: str, fn: Callable
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
