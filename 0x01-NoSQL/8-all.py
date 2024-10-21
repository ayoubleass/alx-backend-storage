#!/usr/bin/env python3
"""
This module has a function that lists all documents in a collection.
"""
import pymongo


def list_all(mongo_collection):
    """
    List a collection.
    """
    return mongo_collection.find()
