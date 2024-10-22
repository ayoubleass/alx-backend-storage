#!/usr/bin/env python3
"""
Thais module has a function that
returns the list of school having a specific topic.
"""
import pymongo


def schools_by_topic(mongo_collection, topic):
    """
     Find and returns the list of school having a specific topic.
    """
    return mongo_collection.find({"topics": topic})
