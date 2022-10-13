import requests
import json
import time
import sys

# Simple Zenitel Link application demo using Requests HTTP library for Python

def main():
    print("Simple Zenitel Link Test/Demo written in Python")
    # define IP and port of the Connect Server
    ip = sys.argv[1]
    username = sys.argv[2]
    password =  sys.argv[3]
    port = "80"
    CONNECT_SERVER = "http://" + ip + ":" + port + "/"
    
    print("Login to Connect and get token")
    response = requests.post(CONNECT_SERVER + "api/auth/login",  auth=requests.auth.HTTPBasicAuth(username, password))
    if response.status_code != 200:
        print("Error, Could not authenticate! ")
        
    # store access token for later use
    token = response.json()['access_token']
    
    # get all reachable devices
    response = requests.get(CONNECT_SERVER + "api/system/device_accounts", headers={'Authorization': 'Bearer ' + token})
    if response.status_code != 200:
        print("Error, Could not get reachable devices!")
        
    print("Devices found :" + str(response.json()))
    print("Let's make a call!")
    print("Enter 'From' Dirno : ")
    from_dir = input()
    print("Enter 'To' Dirno : ")
    to_dir = input()
    
    callbody = {'from_dirno':from_dir, 'to_dirno':to_dir}
    response = requests.post(CONNECT_SERVER + "api/calls", headers={'Authorization': 'Bearer ' + token}, json=callbody)
    if response.status_code != 202:
        print("Error, Could not call device : " + str(response.json()))
    else:
        time.sleep(0.1)
        response = requests.get(CONNECT_SERVER + "api/calls", headers={'Authorization': 'Bearer ' + token})
        print("Calls :" + str(response.json()))
    print("Press enter to hangup...")
    input()
    response = requests.delete(CONNECT_SERVER + "api/calls?dirno=" + from_dir, headers={'Authorization': 'Bearer ' + token})
    if response.status_code != 200:
        print("Error, Could not hang up device :" + str(response.json()))
    else:
        response = requests.get(CONNECT_SERVER + "api/calls", headers={'Authorization': 'Bearer ' + token})
        print("Calls :" + str(response.json()))
        
    print("That's it!")
    
    
        
if __name__ == "__main__":
    main()
    
