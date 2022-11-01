#!/usr/bin/env python

# Script for subscribing to WAMP topics

import txaio
txaio.use_asyncio()
from autobahn.asyncio.component import Component, run
from autobahn.wamp.types import RegisterOptions
from asyncio import sleep
import requests
import asyncio
import json
import sys


##
# CONFIG
##

ip = sys.argv[1]
username = sys.argv[2]
password =  sys.argv[3]
restapi = "http://" + ip + "/"

##
# WAMP SETUP
##
print("Login to ICX and get token as " + username + ':' + password)
response = requests.post(restapi + "api/auth/login", auth=requests.auth.HTTPBasicAuth(username, password))
if response.status_code != 200 and assert_success == False :
    print("No response from Zenitel Connect")
    exit()

token = response.json()['access_token']

# WAMP socket setup
component = Component(
    transports=[
        {
            "type": "websocket",
            "url": "ws://"+ip+":8087/wamp",
            "max_retries": 1,
            "options": {
                "open_handshake_timeout": 100,
            }
        },
    ],
    realm="zenitel",
    authentication={
            "ticket": {
                "authid": username,
                "ticket": token
            }
    },
)

component.events_received = []

@component.on_disconnect
def disconnect():
    print("Disconnected")
    asyncio.get_event_loop().stop()

##
# TOPICS
# Add more topics, maybe make it possible to select wich ones to subscribe to
##
@component.subscribe(u"com.zenitel.system.device_account")
def onreg(info):
    print("com.zenitel.system.device_account:")
    print(json.dumps(info, indent=4, sort_keys=True))
    component.events_received.append(info)

@component.subscribe(u"com.zenitel.call")
def oncall(info):
    print("com.zenitel.call:")
    print(json.dumps(info, indent=4, sort_keys=True))
    component.events_received.append(info)

@component.subscribe(u"com.zenitel.call_leg")
def oncallleg(info):
    print("com.zenitel.call_leg:")
    print(json.dumps(info, indent=4, sort_keys=True))
    component.events_received.append(info)

@component.subscribe(u"com.zenitel.system.open_door")
def onopendoor(info):
    print("com.zenitel.system.open_door:")
    print(json.dumps(info, indent=4, sort_keys=True))
    component.events_received.append(info)

##
# EVENT LOOP
##
@component.on_join
async def join(session, details):
    print("joined {}: {}".format(session, details))

    print("")
    print("")
    print("--------------Starting Connect WAMP monitor--------------")
    timer = 0
    while True:
        await sleep(60)
        timer = timer + 60
        print("Running for: " + str(timer) + " seconds")
        print("Press CTRL-C to exit")
        # Runs forever and prints events continuously

    session.leave()
    asyncio.get_event_loop().stop()



# Event loops stop here until it is stopped from inside
run([component])
