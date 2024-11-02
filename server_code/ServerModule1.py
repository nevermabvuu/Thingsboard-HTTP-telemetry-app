import anvil.server

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

import requests

# Define ThingsBoard URL and Device Token
THINGSBOARD_URL = "https://thingsboard.cloud"  # replace with your instance URL
DEVICE_TOKEN = "your_device_token_here"  # replace with your ThingsBoard device token

# Function to read data from ThingsBoard
@anvil.server.callable
def read_device_data():
    url = f"{THINGSBOARD_URL}/api/v1/{DEVICE_TOKEN}/telemetry"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # returns the telemetry data
    else:
        return {"error": "Failed to retrieve data"}

# Function to write data to ThingsBoard
@anvil.server.callable
def write_device_data(data):
    url = f"{THINGSBOARD_URL}/api/v1/{DEVICE_TOKEN}/telemetry"
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return {"status": "Success"}
    else:
        return {"error": "Failed to send data"}
