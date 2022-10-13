#!/usr/bin/env python

# WAMP, call setup and cancel

import txaio
txaio.use_asyncio()
from autobahn.asyncio.component import Component, run
from autobahn.wamp.types import RegisterOptions
from asyncio import sleep
import requests
import asyncio
import json
import time
import sys


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

@component.on_join
async def joined(session, details):
    print("session ready")
    try:
        res = await session.call(u'com.zenitel.system.device_accounts')
        print("Devices found: {}".format(res))
    except Exception as e:
        print("call error: {0}".format(e))

    print("Let's make a call!")
    print("Enter 'From' Dirno : ")
    from_dir = input()
    print("Enter 'To' Dirno : ")
    to_dir = input()
    
    callbody = {'from_dirno':from_dir, 'to_dirno':to_dir}
    try:
        res = await session.call(u'com.zenitel.calls.post',callbody)
        print("Call between: {}".format(res))
    except Exception as e:
        print("call error: {0}".format(e))
    time.sleep(0.2)
    try:
        res = await session.call(u'com.zenitel.calls')
        print("Call between: {}".format(res))
    except Exception as e:
        print("call error: {0}".format(e))

    print("Press enter to hangup...")
    input()
    callbody = {'dirno':from_dir}
    try:
        res = await session.call(u'com.zenitel.calls.delete',callbody)
        print("Call cancelled: {}".format(res))
    except Exception as e:
        print("call error: {0}".format(e))
    time.sleep(0.2)
    try:
        res = await session.call(u'com.zenitel.calls')
        print("Call between: {}".format(res))
    except Exception as e:
        print("call error: {0}".format(e))

    print("Press CTRL-C to exit")

run([component])
