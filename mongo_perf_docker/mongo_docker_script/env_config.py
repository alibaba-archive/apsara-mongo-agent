#! /usr/bin/python
# coding:utf-8


import json
import os

from const import INS_ID, ACCESS_PORT, PERF_PORT,TOTAL_DISK_SIZE

class EnvConfig():
    env_config = {}

    def __init__(self):
        docker_env = os.environ
        self.env_config[INS_ID] = docker_env["ins_id"]

        # parse port from  port_json_str like:
        # "{\"3213\": {\"access_port\": [3083], \"link\": [3083], \"perf_port\":[3083]}}" in docker_env["port"]
        port_json_str = docker_env["port"]
        port_struct = json.loads(port_json_str)
        self.env_config[ACCESS_PORT] = port_struct[self.env_config[INS_ID]][ACCESS_PORT][0]
        self.env_config[PERF_PORT] = port_struct[self.env_config[INS_ID]][PERF_PORT][0]
        if "disk_size" in docker_env:
            self.env_config[TOTAL_DISK_SIZE] = docker_env["disk_size"]

    def __getattr__(self, name):
        try:
            return self.env_config[name]
        except KeyError:
            raise AttributeError(name)

    def __getitem__(self, item):
        try:
            return self.env_config[item]
        except KeyError:
            raise AttributeError

    def get_config(self, name):
        return self.__getattr__(name)


if __name__ == '__main__':
    envConfig = EnvConfig()
    print envConfig.get_config(INS_ID)
    print envConfig.ins_id
