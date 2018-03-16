from pymongo import MongoClient
from mongo_utils import mongo_const

class RdsMongoClient(MongoClient):

    @classmethod
    def new(cls, ip, port, user=None, password=None, **kwargs):
        conn_url = get_mongo_conn_url(ip, port, user, password)
        return cls(conn_url, connectTimeoutMS=3000, serverSelectionTimeoutMS=3000, **kwargs)

    def set_readonly_on(self):
        result = self.admin.command("setReadOnly", duration=-1)
        if result["ok"] != 1 or result["readOnly"] != 'enable':
            print("""failed to run db.runCommand({ setReadOnly: 1, duration: -1 }),
                            result: %s!""" % result)
        else:
            print "successfully to set readonly on for client!"

    def set_readonly_off(self):
        result = self.admin.command("setReadOnly", duration=0)
        if int(result["ok"]) != 1 or result["readOnly"] != 'disable':
            print """failed to run db.runCommand({ setReadOnly: 1, duration: 0 }),
                            result: %s!""" % result
        else:
            print "successfully to set readonly off for client!"

    def reload_param(self, param_name, param_value):
        cmd = dict(reload=param_name, param=self.format_param_value(param_value))
        result = self.admin.command(cmd)
        if int(result["ok"]) == 1:
            print "successfully to call %s" % cmd
        else:
            print "failed to call %s" % cmd

    def format_param_value(self, param_value):
        if param_value.isdigit():
            return int(param_value)
        elif param_value.lower() == 'true':
            return True
        elif param_value.lower() == 'false':
            return False
        else:
            return param_value

    def set_profiling_level(self, profiling_mode, profiling_threshold):
        result = self.admin.command({"profile": mongo_const.PROFILING_MODE[profiling_mode],
                                     "slowms": int(profiling_threshold)})
        if int(result["ok"]) == 1:
            print ("successfully to set profiling mode, profiling_mode: %s, profiling_threshold: %s!"
                     % (profiling_mode, profiling_threshold))
        else:
            print ("failed to set profiling mode, profiling_mode: %s, profiling_threshold: %s!"
                            % (profiling_mode, profiling_threshold))

    def set_parameter(self, param, param_value):
        cmd = {param: self.format_param_value(param_value)}
        result = self.admin.command("setParameter", **cmd)
        if int(result["ok"]) == 1:
            print "successfully to call %s" % cmd
        else:
            print "failed to call %s" % cmd


def get_mongo_conn_url(ip, port, user=None, pwd=None, set_name=None):
    url = "mongodb://"
    if user:
        if not pwd:
            pwd = user
        url += "%s:%s@" % (user, pwd)
    url += "%s:%s" % (ip, port)
    return url
