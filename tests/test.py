from kafka import KafkaConsumer
from typing import Dict
import yaml
from rse_mapper import RseMapper
from message import RSE_KEY, URL_KEY, Message

rse_map = RseMapper("ingest.yaml")
brokers = rse_map.brokers()
topics = rse_map.topics()
        
consumer = KafkaConsumer(*topics, bootstrap_servers=brokers, auto_offset_reset='earliest', enable_auto_commit=False)

for msg in consumer:
    # print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition, message.offset, message.key, message.value))
    message = Message(msg)
    rse, url = message.extract_rse_info()
    s = rse_map.resplice( rse, url)
    print("url: %s, new url: %s" % (url, s))
    print()
