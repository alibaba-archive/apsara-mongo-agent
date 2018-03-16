#!/usr/bin/python
# _*_ coding:UTF-8
"""

The user manager function is here
in addition to the common parameters of entry_point.py, the docker environment has additional parameters as like:

srv_opr_user_name: The user we managered
srv_opr_password: The password of the srv_opr_user_name
srv_opr_privilege: The role according to the privilege code as like:
                        1,6 ------ root@admin
                        7------- __system@admin
                        8,9------- clusterManager@admin
srv_opr_action:
             ---create
             ---modify
             ---delete
srv_opr_sys_admin_user_name: admin username
srv_opr_sys_admin_password: admin password

"""
from contextlib import contextmanager
from mongo_utils.client import RdsMongoClient
from mongo_utils.parse_docker_env import get_port_from_srv_opr_hosts
from mongo_utils import mongo_const
import pymongo

class UserManager(object):
    def __init__(self, docker_env):
        self.srv_opr_user_name = docker_env.get("srv_opr_user_name")
        self.srv_opr_user_password = docker_env.get("srv_opr_password")
        self.srv_opr_privilege = docker_env.get("srv_opr_privilege", "1")
        self.srv_opr_action = docker_env.get("srv_opr_action")

        self.port = int(get_port_from_srv_opr_hosts(docker_env))
        self.password = docker_env.get("srv_opr_sys_admin_password")
        self.user = docker_env.get("srv_opr_sys_admin_user_name")

    def do_action(self):
        print "We will %s the account: %s" % (self.srv_opr_action, self.srv_opr_user_name)
        if self.srv_opr_action == 'create':
            self.create_account()
        elif self.srv_opr_action == 'modify':
            self.modify_account()
        elif self.srv_opr_action == 'delete':
            self.delete_account()
        else:
            print "The action %s of task %s do not support" % (self.srv_opr_action, "account")

    def create_account(self):
        with self.yield_cli() as cli:
            try:
                srv_roles = mongo_const.privilege_role[self.srv_opr_privilege]
                cli.admin.add_user(self.srv_opr_user_name, self.srv_opr_user_password, roles=srv_roles)
        print "Create user for %s successful" % self.srv_opr_user_name

    def modify_account(self):
        with self.yield_cli() as cli:
            srv_roles = mongo_const.privilege_role[mongo_const.USER_PRIVILEGE]
            cli.admin.add_user(self.srv_opr_user_name, self.srv_opr_user_password, roles=srv_roles)
        print "flush account for %s successful" % self.srv_opr_user_name

    def delete_account(self):
        pass

    @contextmanager
    def yield_cli(self):
        locals_cli = RdsMongoClient.new(
            'localhost', self.port, self.user, self.password)
        try:
            yield locals_cli
        finally:
            locals_cli.close()
