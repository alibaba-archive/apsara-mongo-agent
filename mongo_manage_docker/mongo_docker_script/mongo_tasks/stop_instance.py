#!/usr/bin/python
# _*_ coding:UTF-8
"""

The instance stop function is here
in addition to the common parameters of entry_point.py, the docker environment has additional parameters as like:

srv_opr_action:
             ---graceful_stop 
srv_opr_conf: /conf  
srv_opr_log: /log

"""
import os
import time
import yaml
from mongo_utils import mongo_const
from mongo_utils.mongo_path import MongoPathHelp
from mongo_utils.network import check_port_exists
from mongo_utils.command import execute_command


class StopInstance(object):
    def __init__(self, docker_env):
        self.srv_opr_action = docker_env.get("srv_opr_action")
        self.port = self.get_port_from_conf()
        self.path_help = MongoPathHelp(self.port, docker_env.get("srv_opr_conf"), docker_env.get("srv_opr_log"))

    def get_port_from_conf(self):
        mongod_conf_file = os.path.join(mongo_const.MONGO_CONF_DIR, mongo_const.MONGOD_CONF_FILE)
        conf = yaml.load(open(mongod_conf_file, 'r'))
        port = conf['net']['port']
        return port

    def do_action(self):
        if self.srv_opr_action == 'graceful_stop':
            print "We will stop the instance gracefully!"
            self.stop_instance()
            print 'mongodb port(%s) is not existed.' % self.port
        else:
            print "ERROR: The action %s of task %s do not support" % (self.srv_opr_action, "stop")

    def stop_instance(self, timeout_check_shutdown=300, check_interval=5):
        process_pid = self.get_process()
        port_existed = check_port_exists(int(self.port))
        if not process_pid and not port_existed:
            print "The port %s is not used, mongodb instance is stopped." % self.port
            return
        self.path_help.stop_instance()

        for _ in range(timeout_check_shutdown / check_interval):
            process_pid = self.get_process()
            port_existed = check_port_exists(int(self.port))
            if process_pid or port_existed:
                time.sleep(check_interval)
            else:
                print "mongodb instance %s stop now" % self.port
                return
        else:
            raise Exception("Cannot kill mongodb %s process after retried." % self.port)

    def get_process(self):
        cmd = ["ps -eo pid,comm |grep mongod|awk '{print $1}'"]
        status, output = execute_command(cmd)
        if status == 0:
            pid = output.strip()
            return pid
        else:
            raise Exception('graceful stop mongo fail: %s, %s' % (status, output))
