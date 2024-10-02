ARG RUCIO_DAEMONS_VERSION
FROM rucio/rucio-daemons:${RUCIO_DAEMONS_VERSION}

ARG CONFLUENT_KAFKA_VERSION
RUN pip install confluent_kafka==${CONFLUENT_KAFKA_VERSION}
RUN pip install retrying

RUN mkdir -p /etc/grid-security/certificates
RUN mkdir /usr/local/lib/python3.9/site-packages/rucio/daemons/hermes/kafka
COPY bin/rucio-hermesk /usr/local/bin/rucio-hermesk
COPY lib/rucio/common/constants.py /usr/local/lib/python3.9/site-packages/rucio/common/constants.py
COPY ./lib/rucio/daemons/hermes/kafka /usr/local/lib/python3.9/site-packages/rucio/daemons/hermes/kafka/

# ENTRYPOINT ["/start-daemon.sh"]
