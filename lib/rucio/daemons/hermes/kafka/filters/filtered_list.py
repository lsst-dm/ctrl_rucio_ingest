# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from rucio.daemons.hermes.kafka.filters.default import default
from rucio.client import Client

class filtered_list(default):

    RUBIN_BUTLER = "rubin_butler"
    RUBIN_SIDECAR = "rubin_sidecar"

    def __init__(self, logger, producer, topics):
        self.logger = logger
        self.producer = producer
        self.topics = topics
        self.client = Client()              

        self.logger(logging.INFO, f'Messages will only be sent to kafka topics: "{self.topics}"')

    def process(self, messages):
        """Process Hermes events, and send those matching the filter parameters to RSE host locations

        Parameters
        ----------
        messages : `list`
            Hermes events to process
        """
        to_delete = []
        msg_count = 0
        discard_count = 0
        # cycle through all the messages, applying the filter rules 
        # stated above.
        for message in messages:
            # if the event_type isn't 'transfer-done', then ignore this message
            # and mark it for deletion.
            if str(message['event_type']).lower() != 'transfer-done':
                discard_count += 1
                to_delete.append(message['id'])
                continue
            try:
                # get the destination RSE
                destination = str(message['payload'].get('dst-rse'))

                # check to see if the destination RSE is in the list
                # of topics we're filtering.  If it's not in the list
                # then discard it and go on to the next messages
                if self.topics is not None:
                    if destination not in self.topics:
                        # this destination RSE wasn't in the list specified
                        # in rucio.cfg, so discard it and go to the next
                        # message
                        discard_count += 1
                        to_delete.append(message['id'])
                        continue

                # get the metadata for this file
                scope = str(message['payload'].get('scope'))
                name = str(message['payload'].get('name'))
                metadata = self.client.get_metadata(plugin='ALL', scope=scope, name=name)
                self.logger(logging.INFO, f"name and metadata: {name}: {metadata}")

                # check to see if this is a intended to be ingested
                # if not, discard it
                butler_ingest = metadata.get(self.RUBIN_BUTLER)
                if butler_ingest is None:
                    discard_count += 1
                    to_delete.append(message['id'])
                    continue
                message['payload'][self.RUBIN_BUTLER] = butler_ingest

                # check to see if there's sidecar metadata, and if there is,
                # include it.
                butler_sidecar = metadata.get(self.RUBIN_SIDECAR)
                if butler_sidecar is not None:
                   message['payload'][self.RUBIN_SIDECAR] = butler_sidecar

                # send the message to Kafka
                self.send_message(topic=destination, message=message)

                to_delete.append(message['id'])
                msg_count += 1
            except Exception as exc:
                self.logger(logging.WARN, f'error sending {message}: {exc}')

        self.logger(logging.INFO, f'sent {msg_count} messages to Kafka')
        self.logger(logging.INFO, f'discarded {discard_count} filtered messages')
        return to_delete
