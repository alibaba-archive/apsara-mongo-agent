
# TODO: add your base image here as you like
FROM xxx
ENV PYTHONPATH /docker_script
ENTRYPOINT ["python", "/docker_script/mongo_tasks/install_instance.py"]

# TODO: replace your/path/to/mongod with your mongod path
CMD ["su", "-l", "mongodb", "-c", "\"/your/path/to/mongod -f /data/mongod.conf\""]
COPY get-pip.py /

# TODO: replace your_mongodb_package with your mongodb package install cmd
RUN rpm --rebuilddb \
    && yum install your_mongodb_package -y \
    && python get-pip.py \
    && python -m pip install pymongo \
    && python -m pip install PyYAML
COPY mongod_conf_template /
COPY mongo_docker_script /docker_script
RUN chmod -R +x /docker_script 
VOLUME ["/data", "/log"]
HEALTHCHECK --interval=30s --retries=3 --timeout=3s CMD python /docker_script/mongo_tasks/health_check.py || exit 1
