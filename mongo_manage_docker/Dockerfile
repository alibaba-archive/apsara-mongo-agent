
# TODO: add your base image here as you like
FROM xxx
ENV PYTHONPATH /docker_script
ENTRYPOINT ["python", "/docker_script/entry_point.py"]
COPY get-pip.py /
RUN rpm --rebuilddb \
    && python get-pip.py \
    && python -m pip install pymongo \
    && python -m pip install PyYAML
COPY mongod_conf_template /
COPY mongo_docker_script /docker_script
RUN chmod -R +x /docker_script 
