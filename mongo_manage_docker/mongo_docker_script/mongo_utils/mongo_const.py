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

# storage engine
WIREDTIGER = "wiredTiger"
ROCKSDB = "rocksdb"

# character type
NORMAL = "normal"

# level
LEVEL_INFO = ["mem_size", "disk_size", "cpu_cores"]

LEVEL_PARAMS = ['net.maxIncomingConnections', 'storage.wiredTiger.engineConfig.cacheSizeGB',
                'storage.rocksdb.cacheSizeGB']

# white list
USERWHITELISTPATH = "/conf/mg%s"
ADMINWHITELISTPATH = "/conf/admin"


# privilege role map
privilege_role = {'9': [{"role": "__system", "db": "admin"}], '8': [{"role": "__system", "db": "admin"}], '7': \
            [{"role": "clusterManager", "db": "admin"}], '1': [{"role": "root", "db": "admin"}], \
            '6': [{"role": "root", "db": "admin"}]}

PROFILING_MODE = {"off": 0, "slowOp": 1, "all": 2}

USER_PRIVILEGE = '6'

# some environ keys
LOCK_INS_DISKFULL = 'lock_ins_diskfull'
UNLOCK_INS_DISKFULL = 'unlock_ins'

# backup
ROCKSDB_BAK_DIR = '/data/db_bak'

# error code
ERRCODE_UNAUTHORIZED = 13
