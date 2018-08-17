#!/usr/bin/env python

import logging
import os
import sys
import time
import json

from dxlclient.callbacks import EventCallback
from dxlclient.client import DxlClient
from dxlclient.client_config import DxlClientConfig
from dxlclient.message import Event, Request

logging.getLogger().setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

CONFIG_FILE = "path to dxlclient.config file"
config = DxlClientConfig.create_dxl_config_from_file(CONFIG_FILE)

with DxlClient(config) as client:

    client.connect()

    class MyEventCallback(EventCallback):
        def on_event(self, event):
            try:
                query = event.payload.decode()
                query = query[:query.rfind('}')+1]
                query = json.loads(query)

                try:
		    ips = query['Summary']['Dst IP']
		    if not ips:
                        pass
                    else:
                        ipv4 = ips
                        print ipv4
                        os.system('python ib_push.py ip ' + ipv4)
                except: pass

		try:
                    for ips in query['Summary']['Ips']:
                        ipv4 = ips['Ipv4']
                        print ipv4
                        if not ipv4: pass
                        else:
                            os.system('python ib_push.py ip ' + ipv4)
                except: pass

		try:
		    for urls in query['Summary']['Urls']:
                        url = urls['Url']
                        print url
                        if not url: pass
                        else:
                            os.system('python ib_push.py domain ' + url)
                except: pass

            except Exception as e:
                print e

        @staticmethod
        def worker_thread(req):
            client.sync_request(req)

    # Register the callback with the client
    client.add_event_callback('#', MyEventCallback(), subscribe_to_topic=False)
    client.subscribe("/mcafee/event/atd/file/report")

    # Wait forever
    while True:
        time.sleep(60)
