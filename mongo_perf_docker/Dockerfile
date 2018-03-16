
# TODO: add your base image here as you like
FROM xxx
ENV PYTHONPATH $PYTHONPATH:/docker_script
LABEL apsara.collector.http.mongodb="/var/telegraf/collector_config.json"
ENTRYPOINT ["python", "/docker_script/perf_agent.py"]
COPY get-pip.py /
RUN rpm --rebuilddb\
    && python get-pip.py \
    && python -m pip install pymongo \
    && python -m pip install flask
COPY mongo_docker_script /docker_script
RUN chmod -R +x /docker_script \
    && mkdir -p /var/telegraf/
