#!/usr/bin/python
# _*_ coding:UTF-8

"""
This file define action to backup a instance
"""
import os
import sys
import json
import shutil
import yaml

from mongo_utils.parse_docker_env import get_port_from_srv_opr_hosts
from contextlib import contextmanager
from mongo_utils.client import RdsMongoClient
from mongo_utils import mongo_const


class BackupInstance(object):
    def __init__(self, docker_env):
        self.parse_docker_env(docker_env)

    def parse_docker_env(self, docker_env):
        self.srv_opr_action = docker_env.get("srv_opr_action")
        self.storage_engine = self.get_storage_engine_from_conf()
        self.port = str(get_port_from_srv_opr_hosts(docker_env))
        self.ip = "127.0.0.1"
        self.rocksdb_bak_dir = mongo_const.ROCKSDB_BAK_DIR

    def get_storage_engine_from_conf(self):
        mongod_conf_file = os.path.join(mongo_const.MONGO_CONF_DIR, mongo_const.MONGOD_CONF_FILE)
        conf = yaml.load(open(mongod_conf_file, 'r'))
        storage_engine = conf['storage']['engine']
        return storage_engine

    def do_action(self):
        if self.srv_opr_action == 'pre_action':
            self.start_backup()
        elif self.srv_opr_action == 'post_action':
            self.stop_backup()
        else:
            print "ERROR: The action %s of task %s do not support" % (self.srv_opr_action, "backup")
            sys.exit(-1)


    def start_backup(self):
        self.stop_backup()

        with self.yield_local_cli() as local_client:
            if self.storage_engine == mongo_const.WIREDTIGER:
                pass
            elif self.storage_engine == mongo_const.ROCKSDB:
                local_client.admin.command("setParameter", rocksdbBackup=self.rocksdb_bak_dir)


    def stop_backup(self):
        with self.yield_local_cli() as local_client:
            if self.storage_engine == mongo_const.WIREDTIGER:
                pass
            elif self.storage_engine == mongo_const.ROCKSDB:
                if os.path.exists(self.rocksdb_bak_dir):
                    shutil.rmtree(self.rocksdb_bak_dir)


    @contextmanager
    def yield_local_cli(self):
        cli = RdsMongoClient.new(
            self.ip,
            self.port)
        try:
            yield cli
        finally:
            cli.close()

