from pymongo import MongoClient
from contextlib import contextmanager

class RdsMongoClient(MongoClient):

    @classmethod
    def new(cls, ip, port, user=None, pwd=None, **kwargs):
        conn_url = get_mongo_conn_url(ip, port, user, pwd)
        return cls(conn_url, connectTimeoutMS=3000, serverSelectionTimeoutMS=3000, **kwargs)


def get_mongo_conn_url(ip, port, user=None, pwd=None, set_name=None):
    url = "mongodb://"
    if user:
        if not pwd:
            pwd = user
        url += "%s:%s@" % (user, pwd)
    url += "%s:%s" % (ip, port)
    return url



