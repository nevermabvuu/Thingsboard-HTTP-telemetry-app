from ._anvil_designer import ThingsBoardInterfaceTemplate
from anvil import *
import anvil.server
 
class ThingsBoardInterface(ThingsBoardInterfaceTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        # Any code you write here will run before the form opens.

    # Read data from ThingsBoard when the button is clicked
    def btnWriteData_click(self, **event_args):
        print("Button clicked!")  # This should show up in Anvil's app logs
        temperature = self.temperature_input.text
        
        # Prepare data in the format ThingsBoard expects
        data = {
            "temperature": float(temperature),
        }
        
        # Call the server function to send data
        result = anvil.server.call('write_device_data', data)
        
        if 'error' in result:
            alert(result['error'])
        else:
            alert("Data sent successfully!")

    # Event handler for the button to fetch data
    def btnFetchData_click(self, **event_args):
        print("Fetching data...")
        
        username = "nevermabvuu@gmail.com"  # Replace with your actual ThingsBoard username
        password = "NaleTaps@21"  # Replace with your actual password

        try:
            # Call the server function with username and password
            result = anvil.server.call('fetch_device_data', username, password)
            
            if 'error' in result:
                alert(result['error'])
            else:
                temperature = result.get("temperature")
                
                # Display the fetched value on the form
                self.temperature_label.text = f"Temperature: {temperature}°C" if temperature is not None else "Temperature: N/A"
        
        except Exception as e:
            print("Error fetching data:", e)  # Handle any exceptions that occur during the call
            alert("An error occurred while fetching data.")
