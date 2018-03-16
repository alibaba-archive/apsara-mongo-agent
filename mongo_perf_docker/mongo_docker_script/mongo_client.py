#! /usr/bin/python
# coding:utf-8

from pymongo import MongoClient


class RDSMongoClient():
    def __init__(self, port=27017, host="localhost", username=None, password=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client = MongoClient(self.get_mongo_conn_url(host, port, username, password),
                                  connectTimeoutMS=3000,
                                  serverSelectionTimeoutMS=3000)

    def reconnect(self):
        self.client = MongoClient(self.get_mongo_conn_url(self.host, self.port, self.username, self.password),
                                  connectTimeoutMS=3000,
                                  serverSelectionTimeoutMS=3000)

    def try_run_command(self, db, command):
        try:
            return self.client.get_database(db).command(command)
        except:
            self.reconnect()
            return self.client.get_database(db).command(command)

    def get_mongo_conn_url(self, ip, port, user=None, pwd=None, set_name=None):
        url = 'mongodb://'
        if user is not None:
            if pwd is None:
                pwd = user
            url += '%s:%s@' % (user, pwd)
        url += '%s:%s' % (ip, port)
        if set_name is not None:
            url += '/?replicaSet=%s' % set_name
        return url
