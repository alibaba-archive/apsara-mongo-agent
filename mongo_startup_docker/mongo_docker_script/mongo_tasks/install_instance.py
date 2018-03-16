#!/usr/bin/python
# _*_ coding:UTF-8
"""
This is a install instance script. In this file, we just do:

1. create os user: mongodb:mongodb
2. chown DATA, LOG to mongodb user
3. build mongod.conf
4. start the mongod

The docker env as follow:

ins_id: The instance id

port: The list of port:
                      {\"205\": {\"access_port\": [3001], \"link\": [3001]}
                      The key of the dict is instance id 205
                      The port dict can get by the key portname. In mongodb, the portname is access_port and
                      the link indicate the port which will check custins
"""

import os
import sys
import shutil
import yaml

from mongo_tasks.modify_mongo_conf import build_mongod_conf
from mongo_utils import mongo_const
from mongo_utils.parse_docker_env import get_port_from_port_mapper
from mongo_utils.os_utils import add_os_user
from mongo_utils.os_utils import chown_paths
from mongo_utils.os_utils import delete_file_exclude


def get_storage_engine_from_conf():
    mongod_conf_file = os.path.join(mongo_const.MONGO_CONF_DIR, mongo_const.MONGOD_CONF_FILE)
    conf = yaml.load(open(mongod_conf_file, 'r'))
    storage_engine = conf['storage']['engine']
    return storage_engine


def install_instance(docker_env):

    port = docker_env["PORT"] = str(get_port_from_port_mapper(docker_env))
    ins_id = docker_env["ins_id"]
    create_type = docker_env.get("create_type", mongo_const.INSTALL)

    add_os_user(mongo_const.MONGO_USER, mongo_const.MONGO_GROUP)
    need_chown_dirs = [mongo_const.MONGO_DATA_DIR, mongo_const.MONGO_LOG_DIR]
    chown_paths(need_chown_dirs, mongo_const.MONGO_USER, mongo_const.MONGO_GROUP)

    mongod_conf_file = os.path.join(mongo_const.MONGO_CONF_DIR, mongo_const.MONGOD_CONF_FILE)

    if create_type == mongo_const.INSTALL:
        if not os.path.exists(mongod_conf_file):
            build_mongod_conf(mongod_conf_file, port, docker_env)

    elif create_type == mongo_const.RESTORE:
        storage_engine = get_storage_engine_from_conf()
        if storage_engine == mongo_const.WIREDTIGER:
            build_mongod_conf(mongod_conf_file, port, docker_env)
            print "finish to rebuild conf file"
        elif storage_engine == mongo_const.ROCKSDB:
            backup_file_path = mongo_const.ROCKSDB_BAK_DIR
            new_backup_file_path = mongo_const.ROCKSDB_DATA_DIR
            if os.path.exists(backup_file_path):
                delete_file_exclude(mongo_const.MONGO_DATA_DIR, os.path.basename(mongo_const.ROCKSDB_BAK_DIR))
                os.rename(backup_file_path, new_backup_file_path)
                print "finish to rename db_bak dir"

                build_mongod_conf(mongod_conf_file, port, docker_env)
                print "finish to rebuild conf file"
        else:
            print "no supported storage engine: %s" % storage_engine
    else:
        print "unknown create_type %s" % create_type

    print "start mongodb"
    os.system(" ".join(sys.argv[1:]))


if __name__ == '__main__':
    docker_env = os.environ
    install_instance(docker_env)

