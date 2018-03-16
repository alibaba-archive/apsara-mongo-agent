#! /usr/bin/python
# coding:utf-8

"""
The file will run a resetful api
"""

import json

from flask import Flask, Response
from const import DEFAULT_FREQUENCY, COLLECTOR_CONFIG_JSON, ACCESS_PORT, TOTAL_DISK_SIZE
from env_config import EnvConfig
from collector import Collector

envConfig = EnvConfig()
collector = Collector(envConfig[ACCESS_PORT])
collector.current.data[TOTAL_DISK_SIZE] = float(envConfig.get_config(TOTAL_DISK_SIZE))

app = Flask(__name__)


@app.route('/metrics')
def collect_perf():
    collector.collect()

    return Response(collector.calculate_result.to_telegraf_json_string(), mimetype='application/json')


if __name__ == '__main__':
    perf_port = envConfig.perf_port

    # build the /var/telegraf/collector_config.json like:
    # {
    # "endpoint" : "http://localhost:5000/metrics",
    # "polling_frequency" : 120
    # }
    collector_config = dict()
    collector_config["endpoint"] = "http://localhost:%s/metrics" % perf_port
    collector_config["polling_frequency"] = DEFAULT_FREQUENCY

    collector_config_file = open(COLLECTOR_CONFIG_JSON, "w")
    json.dump(collector_config, collector_config_file)
    collector_config_file.close()

    app.run(port=perf_port)
