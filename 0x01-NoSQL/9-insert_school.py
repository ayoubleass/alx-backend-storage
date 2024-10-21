#!/usr/bin/env python3
"""
This module has a function that inserts
a new document in a collection based on kwargs.
"""
import pymongo


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a collection based on kwargs
    """
    docs = mongo_collection.insert_one(kwargs)
    return docs.inserted_id
