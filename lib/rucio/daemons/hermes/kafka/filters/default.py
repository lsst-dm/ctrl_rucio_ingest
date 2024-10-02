# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import logging

class default:
    def __init__(self, logger, producer, topics):
        self.logger = logger
        self.producer = producer
        self.topics = topics

    def process(self, messages):
        to_delete = set()
        for topic in self.topics:
            d = self._process(topic, messages)
            to_delete = to_delete.union(d)
        return list(to_delete)

    def _process(self, topic, messages):
        to_delete = []
        msg_count = 0
        for message in messages:
            try: 
                self.send_message(topic, message)
                to_delete.append(message["id"])
                msg_count += 1
            except Exception as exc:
                self.logger(logging.WARN, f"error sending: {message}: {exc}")
        self.logger(logging.INFO, f"sent {msg_count} messages to Kafka")
        return to_delete

    def send_message(self, topic, message):
        d = {
            "event_type": str(message["event_type"]).lower(),
            "payload": message["payload"],
            "created_at": str(message["created_at"])
        }

        logging.debug(f"kafka sending: {message}")
        value = json.dumps(d)
        self.producer.produce(topic, key="message", value=value)
        self.producer.flush()
