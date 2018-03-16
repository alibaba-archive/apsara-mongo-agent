import os
from mongo_utils.mongo_const import MONGO_CONF_DIR, MONGO_LOG_DIR, MONGOD_CONF_FILE, MONGOD_PID_FILE
from mongo_utils.command import execute_command


class MongoPathHelp(object):
    def __init__(self, port, conf_path=None, log_path=None, timeout=300):
        self.port = port
        self.srv_opr_timeout = timeout
        self.conf_path = conf_path if conf_path else MONGO_CONF_DIR
        self.log_path = log_path if log_path else MONGO_LOG_DIR
        self.pid_file = os.path.join(self.log_path, MONGOD_PID_FILE)
        self.conf_file_path = os.path.join(self.conf_path, MONGOD_CONF_FILE)

    def stop_instance(self):
        pid_file = self.pid_file
        with open(pid_file, 'r') as f:
            pid = f.read().strip()
        cmd = "kill %s" % pid
        status, output = execute_command(cmd)
        if status == 0:
            return output.strip()
        else:
            raise Exception('graceful stop mongo fail: %s, %s' % (status, output))
