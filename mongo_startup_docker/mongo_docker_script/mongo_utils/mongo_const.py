#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
define constants about mongodb
"""

# path
MONGO_DATA_DIR = "/data"
MONGO_LOG_DIR = "/log"
# TODO use /conf
MONGO_CONF_DIR = "/data"
MONGO_USER = "mongodb"
MONGO_GROUP = "mongodb"
MONGOD_CONF_TEMPLATE = "/mongod_conf_template"
MONGOD_CONF_FILE = "mongod.conf"
MONGOD_PID_FILE = "mongod.pid"
MONGOD_LOG_FILE = "mongod.log"
PORT_NAME = "access_port"

# const
DB_TYPE_MONGODB = "mongodb"
DB_VERSION = "3.4"

# create type
INSTALL = "install"
RESTORE = "restore"

# storage engine
WIREDTIGER = "wiredTiger"
ROCKSDB = "rocksdb"

# character type
NORMAL = "normal"

# level
LEVEL_INFO = ["mem_size", "disk_size", "cpu_cores"]

LEVEL_PARAMS = ['net.maxIncomingConnections', 'storage.wiredTiger.engineConfig.cacheSizeGB',
                'storage.rocksdb.cacheSizeGB']

# restore
ROCKSDB_DATA_DIR = '/data/db'
ROCKSDB_BAK_DIR = '/data/db_bak'

