#!/usr/bin/python
# -*- coding:UTF-8

from ConfigParser import ConfigParser
import json
import math
import os
from mongo_utils import mongo_const


class ConfigParserUper(ConfigParser):

    def optionxform(self, optionstr):
        return optionstr


class ParamConfig(object):
    def __init__(self, docker_env, port):
        self.docker_env = docker_env
        self.storage_engine = docker_env.get("storage.engine", mongo_const.WIREDTIGER)
        self.ins_id = docker_env["ins_id"]
        self.level_params_dict = json.loads(docker_env["mycnf_dict"])
        self.port = port
        self.level_info = {key: self.docker_env.get(key) for key in mongo_const.LEVEL_INFO}
        self.type = docker_env.get("type", "x")

    def dynamic_params(self, params):
        param_value = {}
        mem_size_mb, disk_size_mb, cpu_cores = [int(i) for i in self.level_info.values()]
        print 'mem_size_mb: %s, disk_size_mb: %s, cpu_cores: %s, storage_engine: %s' % (mem_size_mb,
                disk_size_mb, cpu_cores, self.storage_engine)

        params.update(param_value)
        print "dynamic_params finished"

        remove_params = {}
        if self.storage_engine == mongo_const.ROCKSDB:
            remove_params = ['storage.directoryPerDB']
            param_value = {key: value for key, value in params.items() if mongo_const.WIREDTIGER not in key}
            param_value.update({"storage.engine": mongo_const.ROCKSDB, "storage.rocksdb.configString": ""})
        elif self.storage_engine == mongo_const.WIREDTIGER:
            param_value = {key: value for key, value in params.items() if mongo_const.ROCKSDB not in key}
            param_value.update({"storage.engine": mongo_const.WIREDTIGER})

        for item in remove_params:
            param_value.pop(item, None)
        print 'filter params completed'

        param_value.update({
            'net.port': self.port,
            'systemLog.path': os.path.join(mongo_const.MONGO_LOG_DIR, mongo_const.MONGOD_LOG_FILE),
            'processManagement.pidFilePath': os.path.join(mongo_const.MONGO_LOG_DIR, mongo_const.MONGOD_PID_FILE),
            'storage.dbPath': mongo_const.MONGO_DATA_DIR
        })
        return param_value

    def level_params(self):
        params = {key: self.level_params_dict[key] for key in mongo_const.LEVEL_PARAMS}
        return params

    @classmethod
    def template_params(cls, template_file=None):
        if not template_file:
            template_file = mongo_const.MONGOD_CONF_TEMPLATE
        parse = ConfigParserUper()
        parse.read(template_file)
        template_params = dict(parse.items("template"))
        return template_params

    def fully_build_for_install(self):
        params = {}
        params.update(self.template_params())
        params.update(self.level_params())
        params = self.dynamic_params(params)
        print "fully build for install params is: %s" % params
        return params

