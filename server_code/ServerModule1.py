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
import anvil.server
import requests

THINGSBOARD_URL = "http://thingsboard.cloud"
DEVICE_TOKEN = "ydzn45p30ps6n8a1n3yg"  # Replace with your actual device token

@anvil.server.callable
def write_device_data(data):
    url = f"{THINGSBOARD_URL}/api/v1/{DEVICE_TOKEN}/telemetry"
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        return {"status": "Success"}
    else:
        return {"error": f"Failed to send data. Status code: {response.status_code}"}

@anvil.server.callable
def fetch_device_data(username, password):
    # Step 1: Authenticate
    auth_url = "https://thingsboard.cloud/api/auth/login"
    auth_response = requests.post(auth_url, json={"username": username, "password": password})
    
    if auth_response.status_code != 200:
        return {"error": "Authentication failed: " + auth_response.json().get('message', '')}

    token = auth_response.json().get('token')

    # Step 2: Fetch telemetry data
    device_id = "5e0437d0-8574-11ef-bb30-8bb8e87dad7e"  # Replace with your actual device ID
    telemetry_url = f"https://thingsboard.cloud/api/v1/{token}/telemetry/{device_id}"
    
    telemetry_response = requests.get(telemetry_url)

    # Log the response to check for error messages
    print("Telemetry response:", telemetry_response.json())  # Log the response to see what the API returns

    if telemetry_response.status_code != 200:
        return {"error": "Failed to fetch telemetry data: " + telemetry_response.json().get('message', '')}
    
    return telemetry_response.json()
