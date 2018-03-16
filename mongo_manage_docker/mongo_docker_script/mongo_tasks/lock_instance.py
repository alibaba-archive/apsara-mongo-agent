from mongo_utils.client import RdsMongoClient
from mongo_utils.parse_docker_env import get_port_from_srv_opr_hosts
from mongo_utils import mongo_const
from mongo_tasks.modify_mongo_conf import ConfManager
from contextlib import contextmanager
import json

class LockInstance(object):
    def __init__(self, docker_env):
        self.docker_env = docker_env
        self.parse_docker_env(docker_env)
        self.srv_opr_action = docker_env.get("srv_opr_action")
        self.port = str(get_port_from_srv_opr_hosts(docker_env))
        self.ip = "127.0.0.1"

    def parse_docker_env(self, docker_env):
        pass

    def do_action(self):
        if self.srv_opr_action == mongo_const.LOCK_INS_DISKFULL:
            self.lock_ins_diskfull()
        elif self.srv_opr_action == mongo_const.UNLOCK_INS_DISKFULL:
            self.unlock_ins_diskfull()
        else:
            print "ERROR: The action %s of task %s do not support" % (self.srv_opr_action, "lock_ins")

    def lock_ins_diskfull(self):
        self.flush_param()
        with self.yield_local_cli() as local_cli:
            local_cli.set_readonly_on()

    def unlock_ins_diskfull(self):
        self.flush_param()
        with self.yield_local_cli() as local_cli:
            local_cli.set_readonly_off()

    @contextmanager
    def yield_local_cli(self):
        cli = RdsMongoClient.new(
            self.ip,
            self.port)
        try:
            yield cli
        finally:
            cli.close()

    def flush_param(self):
        self.docker_env["srv_opr_host_ip"] = json.dumps({"access_port": [self.port]})
        confmanager = ConfManager(self.docker_env)
        if self.srv_opr_action == mongo_const.LOCK_INS_DISKFULL:
            param_value = {"security.readonly.durationSecond": -1}
            confmanager.flush_param_to_conf(param_value)
        elif self.srv_opr_action == mongo_const.UNLOCK_INS_DISKFULL:
            param_value = {"security.readonly.durationSecond": 0}
            confmanager.flush_param_to_conf(param_value)

