#!/usr/bin/python
# _*_ coding:UTF-8

"""

"""

import unittest
from entry_point import entry
from mongo_utils import mongo_const


class TestEntryPoint(unittest.TestCase):
    def setUp(self):
        pass

    def test_generate_conf(self):
        docker_env = {"srv_opr_action": "create", "srv_opr_type": "flush_params", "srv_opr_timeout": "300",
                      "srv_opr_hosts": '[{"ip": "", "access_port": [3083]}]'}
        entry(docker_env)
        print "Pass create conf test case successfully"

    def test_reload_conf(self):
        pass

    def test_lockins_diskfull(self):
        docker_env = {"srv_opr_action": mongo_const.LOCK_INS_DISKFULL, "srv_opr_type":"lock_ins",
                      "srv_opr_hosts":"[{\"ip\":\"\", \"access_port\":[3083], \"physical_ins_id\":3213}]"}
        entry(docker_env)

    def test_unlockins_diskfull(self):
        docker_env = {"srv_opr_action": mongo_const.UNLOCK_INS_DISKFULL, "srv_opr_type":"unlock_ins",
                      "srv_opr_hosts":"[{\"ip\":\"\", \"access_port\":[3083], \"physical_ins_id\":3213}]"}
        entry(docker_env)

    def test_health_check(self):
        docker_env = {"srv_opr_action": "service_check", "srv_opr_type": "health_check",
                      "srv_opr_hosts": '[{"ip": "", "access_port": [3083]}]'}
        entry(docker_env)
        print "Pass health check test case successfully"

    def test_flush_params(self):
        docker_env = {"srv_opr_action":"reload", "srv_opr_type":"config",
                      "srv_opr_host_ip":"{\"link\": [3002], \"physical_hostins_id\": 1072, \"ip\": \"10.125.59.51\",\"access_port\": [3002], \"perf_port\": [3001], \"physical_ins_id\": 1072}",
                      "srv_opr_sys_admin_user_name": "wang", "srv_opr_sys_admin_password":"wang",
                      "param_values":"[{\"auditLog.authSuccess\":\"true\",\"setParameter.cursorTimeoutMillis\":\"650000\"}]",
                      "param_actions":"[{\"auditLog.authSuccess\":\"reload\",\"setParameter.cursorTimeoutMillis\":\"setParameter\"}]"}
        entry(docker_env)
        print "Pass flush params case successfully"

