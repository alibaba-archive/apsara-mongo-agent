#!/usr/bin/python
# _*_ coding:UTF-8
"""
This is a docker entrypoint script.
We will parse the os.env to decide what to do.

---------------------------The Docker Env Structure-----------------------------------------------

srv_opr_type:               The type of the task, include stop, account, health_check

srv_opr_action:             The action of the task, the srv_opr_type and srv_opr_action mapper as:
                            srv_opr_type          srv_opr_action
                            stop         -------- graceful_stop
                            account      -------- (create, modify, delete)
                            health_check -------- service_check
                            backup       -------- (pre_action, post_action)
                            config       -------- (create, reload)
                            lock_ins     -------- (lock_ins_diskfull, unlock_ins)

srv_opr_timeout:            The timeout args for task

srv_opr_hosts:              The hostinfo, like this:
                                [{"ip":"", "access_port":[xxx], "physical_ins_id":xxx}]

The same type of tasks will have the same docker env, otherwise, docker env may be different.
The env above is the common part of the different task, the different part we will find in each file.

---------------------------------------------------------------------------------------------------


"""
import os
import sys
from mongo_tasks.health_check import HealthChecker
from mongo_tasks.manager_user import UserManager
from mongo_tasks.backup_instance import BackupInstance
from mongo_tasks.modify_mongo_conf import ConfManager
from mongo_tasks.stop_instance import StopInstance
from mongo_tasks.lock_instance import LockInstance

def entry(docker_env):
    srv_opr_type = docker_env.get("srv_opr_type")

    if srv_opr_type == "stop":
        stop_instance = StopInstance(docker_env)
        stop_instance.do_action()
    elif srv_opr_type == "account":
        user_manager = UserManager(docker_env)
        user_manager.do_action()
    elif srv_opr_type == "health_check":
        health_checker = HealthChecker(docker_env)
        health_checker.do_action()
    elif srv_opr_type == "backup":
        instance_backuper = BackupInstance(docker_env)
        instance_backuper.do_action()
    elif srv_opr_type == "config":
        instance_restorer = ConfManager(docker_env)
        instance_restorer.do_action()
    elif srv_opr_type == "lock_ins":
        instance_locker = LockInstance(docker_env)
        instance_locker.do_action()
    else:
        print "Not support the operator of %s type" % srv_opr_type
        sys.exit(1)

if __name__ == '__main__':
    docker_env = os.environ
    entry(docker_env)


