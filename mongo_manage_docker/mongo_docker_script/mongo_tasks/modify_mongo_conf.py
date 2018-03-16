import os
import yaml
from mongo_utils import mongo_const
from mongo_utils.param_config import ParamConfig
from mongo_utils.parse_docker_env import get_access_port_from_srv_opr_host_ip, get_flush_param_values, get_flush_param_actions
from mongo_utils.client import RdsMongoClient
from mongo_utils.os_utils import chown_paths
from contextlib import contextmanager
import json


class ConfManager(object):
    def __init__(self, docker_env):
        self.port = str(get_access_port_from_srv_opr_host_ip(docker_env))
        self.srv_opr_action = docker_env.get("srv_opr_action")
        self.docker_env = docker_env
        self.user = self.docker_env.get("srv_opr_sys_admin_user_name")
        self.password = self.docker_env.get("srv_opr_sys_admin_password")

    def do_action(self):
        if self.srv_opr_action == 'create':
            self.generate_conf_for_build()
        elif self.srv_opr_action == 'reload':
            self.flush_params()
        else:
            print "ERROR: The action %s of task %s do not support" % (self.srv_opr_action, "config")

    def generate_conf_for_build(self):
        mongod_conf_file = os.path.join(mongo_const.MONGO_CONF_DIR, mongo_const.MONGOD_CONF_FILE)
        if not os.path.exists(mongod_conf_file):
            build_mongod_conf(mongod_conf_file, self.port, self.docker_env)

    def flush_params(self):
        param_values = get_flush_param_values(self.docker_env)
        if param_values is None:
            print "param_values can not be None!"
        else:
            self.flush_param_to_conf(param_values)
        param_actions = get_flush_param_actions(self.docker_env)
        if param_actions:
            for param_name, param_value in param_values.items():
                self.flush_param_on_ins(param_name, param_value, param_actions)

    def flush_param_to_conf(self, param_values):
        cfg_path = os.path.join(mongo_const.MONGO_CONF_DIR, mongo_const.MONGOD_CONF_FILE)
        self.assert_exists(cfg_path)
        with open(cfg_path) as f:
            mongo_cfg = yaml.load(f)
            for param_name, new_value in param_values.items():
                try:
                    new_value = json.loads(new_value)
                except:
                    pass
                item = mongo_cfg
                keys = param_name.split('.')
                for key in keys[0: len(keys) - 1]:
                    if not item.has_key(key):
                        item[key] = {}
                    item = item[key]
                item[keys[len(keys) - 1]] = new_value
        with open(cfg_path, 'w') as f:
            f.write(gen_yaml_config(mongo_cfg))

    def assert_exists(self, path):
        if not os.path.exists(path):
            raise " %s is not exists!!!" % path

    def flush_param_on_ins(self, param_name, param_value, param_actions):
        flush_method = param_actions.get(param_name, None)
        if param_name in ('operationProfiling.mode', 'operationProfiling.slowOpThresholdMs'):
            self.set_profiling_on_ins(param_name, param_value)
        elif 'reload' == flush_method:
            param_name = param_name.split('.')[-1]
            self.reload_param_on_ins(param_name, param_value)
        elif 'setParameter' == flush_method:
            param_name = param_name.split('.')[-1]
            self.set_parameter_on_ins(param_name, param_value)
        else:
            print "param %s do not config to flush on ins" % param_name

    @contextmanager
    def yield_local_cli(self):
        local_cli = RdsMongoClient.new(
            "localhost",
            self.port,
            self.user,
            self.password)
        try:
            yield local_cli
        finally:
            local_cli.close()

    def set_profiling_on_ins(self, param_name, param_value):
        if param_name == 'operationProfiling.mode':
            profiling_mode = param_value
            profiling_threshold = self.get_param_from_conf('operationProfiling.slowOpThresholdMs')
            with self.yield_local_cli() as local_cli:
                local_cli.set_profiling_level(profiling_mode, profiling_threshold)
        if param_name == 'operationProfiling.slowOpThresholdMs':
            profiling_mode = self.get_param_from_conf('operationProfiling.mode')
            profiling_threshold = param_value
            with self.yield_local_cli() as local_cli:
                local_cli.set_profiling_level(profiling_mode, profiling_threshold)

    def reload_param_on_ins(self, param, param_value):
        with self.yield_local_cli() as local_cli:
            local_cli.reload_param(param, param_value)

    def get_param_from_conf(self, name):
        cfg_path = os.path.join(mongo_const.MONGO_CONF_DIR, mongo_const.MONGOD_CONF_FILE)
        self.assert_exists(cfg_path)
        with open(cfg_path) as f:
            mongo_cfg = yaml.load(f)
            keys = name.split('.')
            return reduce(lambda x, y: x[y], [mongo_cfg] + keys)

    def set_parameter_on_ins(self, param, param_value):
        with self.yield_local_cli() as local_cli:
            local_cli.set_parameter(param, param_value)


def update2dict(d, val, left):
    items = left.split('.', 1)
    if len(items) == 1:
        if hasattr(val, 'isdigit') and val.isdigit():
            val = int(val)
        if val == 'true' or val == 'false':
            val = val == 'true'
        d[left] = val
    else:
        d.setdefault(items[0], {})
        update2dict(d[items[0]], val, items[1])


def cfg2dict(cfg_list):
    result = {}
    for (k, v) in cfg_list:
        update2dict(result, v, k)
    return result


def gen_yaml_config(params):
    cfg_dict = cfg2dict(params.items())
    return yaml.safe_dump(cfg_dict, default_flow_style=False)


def build_mongod_conf(mongod_conf_file, port, docker_env):
    param_config = ParamConfig(docker_env, port)
    params = param_config.fully_build_for_install()

    with open(mongod_conf_file, 'w') as out_file:
        out_file.write(gen_yaml_config(params))
    # tool docker and kernel docker may have different user namespace
    #chown_paths([mongod_conf_file], mongo_const.MONGO_USER, mongo_const.MONGO_GROUP)
