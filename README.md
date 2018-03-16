
ApsaraMongoAgent is a suit of docker agents used for ApsaraDB for MongoDB(https://github.com/alibaba/mongo) written in python.

It contains three docker images:
mongo_startup_docker---->will build the docker for installing and starting up a mongod instance. It contains:

                    Dockerfile              The file to build the docker
                    mongo_docker_script     The dir of docker scripts. It contains:

                                            mongo_tasks     The task of mongo according to the pengine. It contains:
                                            mongo_utils     The utils. It contains some utisl.
                    mongod_conf_template    The template of mongod.conf

mongo_manage_docker----will build the docker for managing a running mongod instance. It contains:

                    Dockerfile              The file to build the docker
                    mongo_docker_script     The dir of docker scripts. It contains:

                                            entry_point.py  Dockerfile entry_point
                                            mongo_tasks     The task of mongo according to the pengine. It contains:
                                            mongo_testcases The test cases
                                            mongo_utils     The utils. It contains some utisl.
 
mongo_perf_docker----will build the docker for collecting performance metrics from a running mongod instance. It contains:

                    Dockerfile              The file to build the docker
                    mongo_docker_script     The dir of docker scripts. It contains:

                                            perf_agent.py  Dockerfile entry_point

## How to use:
1. Build docker images. We do not provide a default base docker image for each Dockerfile. So you can select your base docker image as you like. CentOS7/RHEL7 are recommended. Likewise, we do not provide a default mongod binary in mongo_startup_docker, you can either use a community version or aliyun open src version. Please see details in Dockerfiles.
2. Run them.

Have fun!
