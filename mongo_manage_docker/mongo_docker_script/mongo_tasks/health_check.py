#!/usr/bin/python
# _*_ coding:UTF-8
"""
This file support health check

in addition to the common parameters of entry_point.py, the docker environment has additional parameters as like:

srv_opr_action:
             ---service_check

"""
import sys
from contextlib import contextmanager
from mongo_utils.parse_docker_env import get_port_from_srv_opr_hosts
from mongo_utils.client import RdsMongoClient


class HealthChecker(object):
    def __init__(self, docker_env):
        self.srv_opr_action = docker_env["srv_opr_action"]
        self.port = int(get_port_from_srv_opr_hosts(docker_env))
        self.password = docker_env.get("password")
        self.user = docker_env.get("user")

    def do_action(self):
        if self.srv_opr_action == 'service_check':
            print "We will check the service."
            self.service_check()
        else:
            print "ERROR: The action %s of task %s do not support" % (self.srv_opr_action, "health_check")

    def service_check(self):
        try:
            with self.yield_cli() as cli:
                result = cli.admin.command('ping')
        except Exception, e:
            print "Exceptiong is :%s" % str(e)
            sys.exit(-1)

        if result["ok"] == 1:
            print "The custins is healthy"
        else:
            print "The custins is not healthy: %s" % result
            sys.exit(-1)

    @contextmanager
    def yield_cli(self):
        locals_cli = RdsMongoClient.new(
            'localhost', self.port, self.user, self.password)
        try:
            yield locals_cli
        finally:
            locals_cli.close()


