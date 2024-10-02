from confluent_kafka import Consumer
import socket
from typing import Dict
import yaml
from lsst.ctrl.rucio.ingest.rse_mapper import RseMapper
from lsst.ctrl.rucio.ingest.message import RSE_KEY, URL_KEY, Message

rse_map = RseMapper("ingest.yaml")
group_id = rse_map.group_id()
brokers = rse_map.brokers()
topics = rse_map.topics()

conf = { 'bootstrap.servers': 'localhost:9092', 'client.id': socket.gethostname, 'group.id': group_id, 'auto.offset.reset': 'earliest', 'enable.auto.commit': False }
        
consumer = Consumer(conf)
consumer.subscribe(topics)

msgs = consumer.consume(num_messages=1)

for msg in msgs:
    # print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition, message.offset, message.key, message.value))
    message = Message(msg)
    rse, url = message.extract_rse_info()
    s = rse_map.resplice( rse, url)
    print("url: %s, new url: %s" % (url, s))
    print()

