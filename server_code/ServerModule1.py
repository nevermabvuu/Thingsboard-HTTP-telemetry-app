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
import anvil.server
import requests

@anvil.server.callable
def fetch_device_data(username, password):
    # Authenticate to get the JWT token
    auth_url = "https://thingsboard.cloud/api/auth/login"
    auth_payload = {
        "username": username,
        "password": password
    }
    
    # Authenticate and get the JWT token
    try:
        auth_response = requests.post(auth_url, json=auth_payload)
        auth_response.raise_for_status()  # Raise an error for bad responses
        jwt_token = auth_response.json().get("token")  # Extract the JWT token
        print(f"JWT Token: {jwt_token}")  # Optionally log the JWT token for debugging
    except requests.exceptions.HTTPError as http_err:
        print(f"Authentication failed: {http_err}")
        return {"error": "Authentication failed. Check your username and password."}
    except Exception as err:
        print(f"An error occurred: {err}")
        return {"error": "An unexpected error occurred."}

    # Now, using the access token and device ID to fetch telemetry data
    device_id = "5e0437d0-8574-11ef-bb30-8bb8e87dad7e"  # Replace with your actual device ID
    access_token = "ydzn45p30ps6n8a1n3yg"  # Replace with your actual device access token
    telemetry_url = f"https://thingsboard.cloud/api/v1/{access_token}/telemetry/{device_id}"
    
    headers = {
        "Content-Type": "application/json"
    }

    # Fetch telemetry data
    try:
        telemetry_response = requests.get(telemetry_url, headers=headers)
        telemetry_response.raise_for_status()  # Raise an error for bad responses
        telemetry_data = telemetry_response.json()  # Parse the JSON response
        return telemetry_data  # Return the telemetry data to the client
    except requests.exceptions.HTTPError as http_err:
        print(f"Failed to fetch telemetry data: {http_err}")
        return {"error": "Failed to fetch telemetry data."}
    except Exception as err:
        print(f"An error occurred: {err}")
        return {"error": "An unexpected error occurred."}
