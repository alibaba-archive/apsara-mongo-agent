#!/usr/bin/python
# _*_ coding:UTF-8
"""
modify the mongod.conf
"""
import os
import sys
import json
import yaml
from mongo_utils.param_config import ParamConfig
from mongo_utils import mongo_const
from mongo_utils.os_utils import chown_paths

def update2dict(d, val, left):
    items = left.split('.', 1)
    if len(items) == 1:
        if hasattr(val, 'isdigit') and val.isdigit():
            val = int(val)
        if val == 'true' or val == 'false':
            val = val == 'true'
        d[left] = val
    else:
        d.setdefault(items[0], {})
        update2dict(d[items[0]], val, items[1])

def cfg2dict(cfg_list):
    result = {}
    for (k, v) in cfg_list:
        update2dict(result, v, k)
    return result


def gen_yaml_config(params):
    cfg_dict = cfg2dict(params.items())
    return yaml.safe_dump(cfg_dict, default_flow_style=False)


def build_mongod_conf(mongod_conf_file, port, docker_env):
    param_config = ParamConfig(docker_env, port)
    params = param_config.fully_build_for_install()

    with open(mongod_conf_file, 'w') as out_file:
        out_file.write(gen_yaml_config(params))
    chown_paths([mongod_conf_file], mongo_const.MONGO_USER, mongo_const.MONGO_GROUP)



