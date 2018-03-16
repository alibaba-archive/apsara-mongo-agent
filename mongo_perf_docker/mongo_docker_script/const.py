#! /usr/bin/python
# coding:utf-8

DEFAULT_FREQUENCY = 60
COLLECTOR_CONFIG_JSON = "/var/telegraf/collector_config.json"
# docker environment
INS_ID = "ins_id"
ACCESS_PORT = "access_port"
PERF_PORT = "perf_port"
TOTAL_DISK_SIZE = "total_disk_size"
# collector config
LOCAL_TIME = "localTime"
REPL_LAG = "repl_lag"
ORIGINAL = "original"
SHOW = "show"
CMD = "cmd"
OPERATION = "op"
# collector operation
OP_AVERAGE = "average"
OP_DEFAULT = ""
# result format config
NAME = "name"
FIELDS = "fields"
### bash command template
CMD_GET_DIR_SIZE = "du -sb %s | awk -F' ' '{print $ 1}'"

METRIC_NAME_MAPPING = [
    {ORIGINAL: "opcounters|insert", SHOW: "insert", OPERATION: OP_AVERAGE},
    {ORIGINAL: "opcounters|query", SHOW: "query", OPERATION: OP_AVERAGE},
    {ORIGINAL: "opcounters|update", SHOW: "update", OPERATION: OP_AVERAGE},
    {ORIGINAL: "opcounters|delete", SHOW: "delete", OPERATION: OP_AVERAGE},
    {ORIGINAL: "opcounters|getmore", SHOW: "getmore", OPERATION: OP_AVERAGE},
    {ORIGINAL: "opcounters|command", SHOW: "command", OPERATION: OP_AVERAGE},
    {ORIGINAL: "asserts|regular", SHOW: "regular", OPERATION: OP_AVERAGE},
    {ORIGINAL: "asserts|warning", SHOW: "warning", OPERATION: OP_AVERAGE},
    {ORIGINAL: "asserts|msg", SHOW: "msg", OPERATION: OP_AVERAGE},
    {ORIGINAL: "asserts|user", SHOW: "user", OPERATION: OP_AVERAGE},
    {ORIGINAL: "mem|resident", SHOW: "resident", OPERATION: OP_DEFAULT},
    {ORIGINAL: "mem|virtual", SHOW: "virtual", OPERATION: OP_DEFAULT},
    {ORIGINAL: "mem|mapped", SHOW: "mapped", OPERATION: OP_DEFAULT},
    {ORIGINAL: "connections|current", SHOW: "current_conn", OPERATION: OP_DEFAULT},
    {ORIGINAL: "connections|available", SHOW: "available_conn", OPERATION: OP_DEFAULT},
    {ORIGINAL: "connections|internal_current", SHOW: "current_internal_conn", OPERATION: OP_DEFAULT},
    {ORIGINAL: "connections|internal_available", SHOW: "available_internal_conn", OPERATION: OP_DEFAULT},
    {ORIGINAL: "metrics|cursor|open|total", SHOW: "total_open", OPERATION: OP_DEFAULT},
    {ORIGINAL: "metrics|cursor|timedOut", SHOW: "timed_out", OPERATION: OP_AVERAGE},
    {ORIGINAL: "network|bytesIn", SHOW: "bytes_in", OPERATION: OP_AVERAGE},
    {ORIGINAL: "network|bytesOut", SHOW: "bytes_out", OPERATION: OP_AVERAGE},
    {ORIGINAL: "network|numRequests", SHOW: "num_requests", OPERATION: OP_AVERAGE},
    {ORIGINAL: "mem|virtual", SHOW: "non_mapped_virtual_memory", OPERATION: OP_DEFAULT},
    {ORIGINAL: "globalLock|currentQueue|total", SHOW: "gl_cq_total", OPERATION: OP_DEFAULT},
    {ORIGINAL: "globalLock|currentQueue|readers", SHOW: "gl_cq_readers", OPERATION: OP_DEFAULT},
    {ORIGINAL: "globalLock|currentQueue|writers", SHOW: "gl_cq_writers", OPERATION: OP_DEFAULT},
    {ORIGINAL: "extra_info|page_faults", SHOW: "page_faults", OPERATION: OP_DEFAULT},
    {ORIGINAL: "wiredTiger|cache|bytes currently in the cache", SHOW: "bytes_currently_in_the_cache",
     OPERATION: OP_DEFAULT},
    {ORIGINAL: "wiredTiger|cache|bytes read into cache", SHOW: "bytes_read_into_cache", OPERATION: OP_DEFAULT},
    {ORIGINAL: "wiredTiger|cache|bytes written from cache", SHOW: "bytes_written_from_cache", OPERATION: OP_DEFAULT},
    {ORIGINAL: "wiredTiger|cache|maximum bytes configured", SHOW: "maximum_bytes_configured", OPERATION: OP_DEFAULT},
    {ORIGINAL: "wiredTiger|concurrentTransactions|write|out", SHOW: "write_concurrent_trans_out",
     OPERATION: OP_DEFAULT},
    {ORIGINAL: "wiredTiger|concurrentTransactions|write|available", SHOW: "write_concurrent_trans_available",
     OPERATION: OP_DEFAULT},
    {ORIGINAL: "wiredTiger|concurrentTransactions|read|out", SHOW: "read_concurrent_trans_out", OPERATION: OP_DEFAULT},
    {ORIGINAL: "wiredTiger|concurrentTransactions|read|available", SHOW: "read_concurrent_trans_available",
     OPERATION: OP_DEFAULT},
    {ORIGINAL: "metrics|repl|iocheck|cost", SHOW: "iocheck_cost", OPERATION: OP_DEFAULT},
    # {ORIGINAL: "systemInfo|oplog used size", SHOW: "oplog_used_size", OPERATION: OP_DEFAULT},
    # {ORIGINAL: "systemInfo|oplog max size", SHOW: "oplog_max_size", OPERATION: OP_DEFAULT},
    {ORIGINAL: "systemInfo|system cpu usage per 10 thousand", SHOW: "cpu_sys", OPERATION: OP_DEFAULT},
    {ORIGINAL: "systemInfo|user cpu usage per 10 thousand", SHOW: "cpu_user", OPERATION: OP_DEFAULT},

]
# cmd metric format:
# SHOW: key1[;key2[;key3]]
# CMD result: value1[\nvalue2[\nvalue3]]
CMD_METRIC_MAPPING = [
    {SHOW: "disk_size", CMD: CMD_GET_DIR_SIZE % "/data/", OPERATION: OP_DEFAULT},
]

EXPRESSION_METRIC_MAPPING = [
    {SHOW: "qps", OPERATION: "$insert + $update + $delete + $query + $getmore + $command"},
    {SHOW: "conn_usage", OPERATION: "int($current_conn / ($current_conn + $available_conn) * 100)"},
    # {SHOW: "oplog_used_size_mb", OPERATION: "int($oplog_used_size / (1024 * 1024))"},
    # {SHOW: "oplog_max_size_mb", OPERATION: "int($oplog_max_size / (1024 * 1024))"},
    {SHOW: "cpu_usage", OPERATION: "$cpu_sys + $cpu_user"},
    {SHOW: "data_size", OPERATION: "$disk_size"},
    {SHOW: "disk_usage", OPERATION: "$disk_size / 1024.0 / 1024.0 / $"+TOTAL_DISK_SIZE}
]

RESULT_FORMAT_CONFIG = [
    {NAME: "opcounters", FIELDS: ["insert", "query", "update", "delete", "getmore", "command"]},
    {NAME: "mg_asserts", FIELDS: ["regular", "warning", "msg", "user"]},
    {NAME: "mem", FIELDS: ["resident", "virtual", "mapped"]},
    {NAME: "connections", FIELDS: ["current_conn"]},
    {NAME: "cursors", FIELDS: ["total_open", "timed_out"]},
    {NAME: "network", FIELDS: ["bytes_in", "bytes_out", "num_requests"]},
    {NAME: "non_mapped_virtual_memory", FIELDS: ["non_mapped_virtual_memory"]},
    {NAME: "global_lock_current_queue", FIELDS: ["gl_cq_total", "gl_cq_readers", "gl_cq_writers"]},
    {NAME: "page_faults", FIELDS: ["page_faults"]},
    ##
    {NAME: "detailed_disk_space", FIELDS: ["ins_size", "data_size", "log_size"]},
    #{NAME: "mem_usage", FIELDS: ["mem_usage"]},
    {NAME: "conn_usage", FIELDS: ["conn_usage"]},
    {NAME: "wt_concurrent_trans",
     FIELDS: ["write_concurrent_trans_out", "write_concurrent_trans_available", "read_concurrent_trans_out",
              "read_concurrent_trans_available"]},
    {NAME: "qps", FIELDS: ["qps"]},
    {NAME: "internal_connections", FIELDS: ["current_internal_conn"]},
    {NAME: "iocheck_cost", FIELDS: ["iocheck_cost"]},
    {NAME: "disk_usage", FIELDS: ["disk_size","data_size","disk_usage"]}
    # {NAME: "oplog_size", FIELDS: ["oplog_used_size_mb", "oplog_max_size_mb"]},
]
