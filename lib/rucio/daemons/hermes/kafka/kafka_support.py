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

from confluent_kafka import Producer
import importlib
import json
import logging
import socket

from rucio.common.config import (
    config_get,
    config_get_int,
    config_get_bool,
    config_get_list,
)

mylog = None
default_filter_class_name = "rucio.daemons.hermes.kafka.filters.default"

def setup_kafka(logger):
    """
    Deliver messages to Kafka

    :param logger:             The logger object.
    """

    logger(logging.INFO, "[broker-kafka] Resolving brokers")

    # the following retrieves all rucio.cfg information

    # get broker name
    try:
        brokers = config_get("messaging-hermes-kafka", "brokers")
    except Exception:
        raise Exception("Could not load 'brokers' from configuration")

    # check to see if ssl is being used to authenticate
    logger(logging.INFO, "[broker] Checking authentication method")
    try:
        use_ssl = config_get_bool("messaging-hermes-kafka", "use_ssl")
    except Exception:
        logger(logging.INFO, "[broker] Could not find use_ssl in configuration -- update your rucio.cfg")

    # if ssl is used, get the reset of the params we'll use to authenticate
    if use_ssl:
        ca_cert = config_get_bool("messaging-hermes-kafka", "ca_cert")
        certfile = config_get_bool("messaging-hermes-kafka", "certfile")
        keyfile = config_get_bool("messaging-hermes-kafka", "keyfile")
    # get the username and password, if specified
    else:
        username = config_get("messaging-hermes-kafka", "username", raise_exception=False, default=None)
        password = config_get("messaging-hermes-kafka", "password", raise_exception=False, default=None)

    config = { 'bootstrap.servers': f'{brokers}',
               'client.id': socket.gethostname(),
             }
    
    # configure to use SSL
    if use_ssl:
        logger(logging.INFO, "[broker-kafka] use_ssl")
        producer = Producer(bootstrap_servers=f'{brokers}',
                                 security_protocol="SSL",
                                 ssl_cafile=ca_cert,
                                 ssl_certfile=certfile,
                                 ssl_keyfile=keyfile)
    elif username is not None:
        logger(logging.INFO, "[broker-kafka] username")
        producer = Producer(bootstrap_servers=f'{brokers}',
                                 sasl_username=username,
                                 sasl_password=password)
    else:
        logger(logging.INFO, f"[broker-kafka] plain {config}")
        producer = Producer(config)


    # check to see if a message filter is specified;  if it isn't, use the default
    filter_name = config_get("messaging-hermes-kafka", "message_filter", raise_exception=False, default=None)
    if filter_name is None:
        logger(logging.WARN, f'no message_filter specified, using "{default_filter_class_name}"')
        filter_name = default_filter_class_name
    else:
        logger(logging.INFO, f'message_filter set to "{filter_name}"')

    # retrieve the topic list.
    topic_list = config_get_list(
        "messaging-hermes-kafka", "topic_list", raise_exception=False, default=None
    )

    if topic_list is None:
        logger(
            logging.INFO,
            "no topic_list specified, sending to all named RSEs as topics",
        )

    # create the class used for message filtering
    message_filter = None
    try:
        message_filter_class = create_class(filter_name)
        message_filter = message_filter_class(logger, producer, topic_list)
    except Exception as e:
        logging.exception(e)

    return message_filter


def create_class(class_name):
    """Create a class specified by class_name
    """

    name = class_name.split(".")[-1]
    filter_class_name = class_name + "." + name

    dot = filter_class_name.rindex(".")
    module_name = filter_class_name[0:dot]
    _class_name = filter_class_name[dot + 1 :]

    classobj = getattr(importlib.import_module(module_name), _class_name)
    if classobj is None:
        raise RuntimeError(
            'Attempt to instantiate class "'
            + name
            + '" failed. Could not find that class.'
        )

    return classobj


def deliver_to_kafka(message_filter, messages):
    """
    Deliver messages to Kafka

    :param message_filter:     Message filtering object.
    :param messages:           The list of messages.

    :returns:                  List of message_id to delete
    """

    to_delete = message_filter.process(messages)
    return to_delete
