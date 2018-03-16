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

def get_access_port_from_srv_opr_host_ip(docker_env):
    """
    parse port from  port_json_str like:
    "srv_opr_host_ip":"{\"link\": [3002], \"physical_hostins_id\": 1072, \"ip\": \"10.125.59.51\",\"access_port\": [3002],
     \"perf_port\": [3001], \"physical_ins_id\": 1072}"
    :param docker_env: env from docker
    :return:
    """
    srv_opr_host_ip = json.loads(docker_env["srv_opr_host_ip"])
    port = srv_opr_host_ip[mongo_const.PORT_NAME][0]
    return port

def get_flush_param_values(docker_env):
    """
    parse param_values from  param_values like:
    "param_values":[{\"security.authorization\":\"enabled\",...}]
    :param docker_env: env from docker
    :return: param_values
    """
    param_values = docker_env.get("param_values")
    if param_values is not None:
        param_values = json.loads(param_values)[0]
    return param_values

def get_flush_param_actions(docker_env):
    """
    parse param_actions from  param_value like:
    "param_actions":[{\"auditLog.authSuccess\":\"reload\",...}]
    :param docker_env: env from docker
    :return: param_actions
    """
    param_actions = docker_env.get("param_actions")
    if param_actions is not None:
        param_actions = json.loads(param_actions)[0]
    return param_actions
