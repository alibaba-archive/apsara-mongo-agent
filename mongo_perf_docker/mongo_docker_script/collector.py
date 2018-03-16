#! /usr/bin/python
# coding:utf-8

from mongo_client import RDSMongoClient
from util import DeepFilterMap
from const import LOCAL_TIME, SHOW, ORIGINAL, CMD, OPERATION, OP_AVERAGE, OP_DEFAULT, METRIC_NAME_MAPPING, \
    EXPRESSION_METRIC_MAPPING,CMD_METRIC_MAPPING, REPL_LAG, RESULT_FORMAT_CONFIG, NAME, FIELDS
from datetime import datetime
import re
import json
import commands
"""
get the result of the request like this:

{
"timestamp": "2016-12-12T10:04:23Z",  # 可选，缺省为当前时间
"metrics": [{
    "timestamp": "2016-12-12T10:04:23Z",  # 可选，缺省为上一级timestamp时间
    "name": "multi_fields",
    "fields": {
        "f1": 23,
        "f2": 234.1
    },
    "tags": {
        "foo": "bar",
        "real": true,
        "fake": 1
    }
}, {
    "timestamp": "2016-12-12T10:04:23Z",  # 可选，缺省为上一级timestamp时间
    "name": "one_field",
    "fields": {
        "f": 23
    },
    "tags": {
        "foo": "bar",
        "real": true
    }
}, {
    "timestamp": "2016-12-12T10:04:23Z",  # 可选，缺省为上一级timestamp时间
    "name": "one_field",
    "fields": {
        "f": 23
    },
    "tags": {
        "hello": "world",
        "real": false
    }
}]
}

"""

reg = re.compile("\$\w*")


class DataModel():
    def __init__(self):
        self.timestamp = datetime.utcnow()
        self.data = {}

    def to_telegraf_json_string(self):
        result_dict = {}
        result_dict["timestamp"] = self.timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
        result_dict["metrics"] = []
        for fm in RESULT_FORMAT_CONFIG:
            single_metric = {"name": fm[NAME], "fields": {}}
            for field in fm[FIELDS]:
                single_metric["fields"][field] = self.data.get(field, 0)
            result_dict["metrics"] += [single_metric]

        return json.dumps(result_dict)


class Collector():
    last = DataModel()
    current = DataModel()
    calculate_result = DataModel()

    def __init__(self, port):
        self.conn = RDSMongoClient(port=port)

    def collect(self):
        result = DeepFilterMap(self.conn.try_run_command("test", {"serverStatus": 1}))

        self.last = self.current
        self.current = DataModel()

        self.current.timestamp = result.pick_value(LOCAL_TIME)
        self.calculate_result.timestamp = self.current.timestamp
        # collect simple metrics
        for metric_obj in METRIC_NAME_MAPPING:
            self.current.data[metric_obj[SHOW]] = result.pick_value(metric_obj[ORIGINAL].split("|"))
            self.cal_metric(metric_obj[SHOW], metric_obj[OPERATION])
        # collect metrics using bash command
        for metric_obj in CMD_METRIC_MAPPING:
            status, text = commands.getstatusoutput(metric_obj[CMD])
            if status == 0:
                metrics = metric_obj[SHOW].split(";")
                values = text.split("\n")
                kv_pair = zip(metrics, values)
                for k,v in kv_pair:
                    self.current.data[k] = int(v.strip())
                    self.cal_metric(k, metric_obj[OPERATION])
        # collect extra metrics,ex. repl_lag
        # self.collect_extra()
        # collect statistical metrics
        for metric_obj in EXPRESSION_METRIC_MAPPING:
            self.cal_metric(metric_obj[SHOW], metric_obj[OPERATION])

    def cal_metric(self, show_metric, op):
        if op == OP_DEFAULT:
            self.calculate_result.data[show_metric] = self.current.data[show_metric]
            return
        elif op == OP_AVERAGE:
            time_delta_seconds = (self.current.timestamp - self.last.timestamp).total_seconds()
            if show_metric in self.last.data:
                if time_delta_seconds > 0:
                    self.calculate_result.data[show_metric] = \
                        int((self.current.data[show_metric] - self.last.data[show_metric]) / time_delta_seconds)

        else:
            variables = reg.findall(op)
            value = -1
            for v in variables:
                metric = v[1:]
                if self.calculate_result.data.get(metric, None) is None:
                    value = 0
                    break
                else:
                    op = op.replace(v, str(self.calculate_result.data[metric]), -1)

            if value == -1:
                value = eval(op)
            self.calculate_result.data[show_metric] = value

    def collect_extra(self):
        result = self.conn.try_run_command("admin", {"replSetGetStatus": 1})
        my_time = None
        pri_time = None
        for member in result["members"]:
            if member.get("self", False):
                my_time = member["optimeDate"]
            if member["stateStr"] == "PRIMARY":
                pri_time = member["optimeDate"]
        if my_time and pri_time:
            time_delta_seconds = (pri_time - my_time).total_seconds()
            self.current.data[REPL_LAG] = time_delta_seconds if time_delta_seconds > 0 else 0
            self.calculate_result.data[REPL_LAG] = self.current.data[REPL_LAG]
