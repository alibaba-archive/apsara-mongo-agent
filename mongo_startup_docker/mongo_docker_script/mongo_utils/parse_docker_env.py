#!/usr/bin/python
# _*_ coding:UTF-8

"""
Parse the docker env
"""

import json
import mongo_const

def get_port_from_port_mapper(docker_env):
    """
    parse port from  port_json_str like:
    "{\"3213\": {\"access_port\": [3083], \"link\": [3083]}}" in docker_env["port"]
    :param docker_env: env from docker
    :return:
    """
    ins_id = docker_env["ins_id"]
    port_json_str = docker_env["port"]
    port_struct = json.loads(port_json_str)
    port = port_struct[ins_id][mongo_const.PORT_NAME][0]
    return port


def get_port_from_srv_opr_hosts(docker_env):
    """
    parse port from  srv_opr_hosts like:
    [{"ip":"", "external_port":[3001], "internal_port":[3001, 3002, 3003], "physical_ins_id":123}]
    :param srv_opr_hosts: srv_opr_hosts
    :return: internal_port
    """
    srv_opr_hosts = docker_env["srv_opr_hosts"]
    opr_hosts = json.loads(srv_opr_hosts)
    internal_port = opr_hosts[0].get(mongo_const.PORT_NAME)[0]
    return internal_port