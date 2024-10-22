#!/usr/bin/env python3
"""
This module has a function that Provides some stats about Nginx logs.
"""
from pymongo import MongoClient


def logs():
    """
    Provides some stats about Nginx logs stored in MongoDB.
    """
    http_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx
    nginx_total = nginx_collection.count_documents({})
    methods_obj = {}
    for method in http_methods:
        methods_obj[method] = nginx_collection.count_documents(
                {"method": method})
    path = nginx_collection.count_documents(
            {"method": http_methods[0], "path": "/status"})
    print("{} logs".format(nginx_total))
    print("Methods:")
    for method in http_methods:
        print(f"\tmethod {method}: {methods_obj[method]}")
    print("{} status check".format(path))


if __name__ == "__main__":
    logs()
