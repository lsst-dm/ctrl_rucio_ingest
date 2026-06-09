# -*- coding: utf-8 -*-

# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
