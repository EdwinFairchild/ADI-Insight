from pyocd.core.helpers import ConnectHelper
#from target_max32655 import MAX32655  # Make sure this import corresponds to the actual location of your custom target file
import time
import logging
logging.basicConfig(level=logging.DEBUG)

def monitor_variables(target, addresses):
    previous_value = None
    while True:
        for address in addresses:
            value = target.read32(address)
            if value != previous_value:
                previous_value = value
                print(f"Variable at {address:x}: {value}")
        time.sleep(0.1)  # Adjust the refresh rate as needed

def main():
    session_options = {
    "halt_on_connect": False,
     "connect_mode": "attach", # Use 'attach' instead of 'under_reset' or other modes
}
    # Connect to the probe
    probe = ConnectHelper.session_with_chosen_probe(return_first=True, target_override="MAX32660", session_options=session_options)
    
    # Make sure to handle the case where no probe is found
    if probe is None:
        print("No probe found!")
        return

    with probe:
        target = probe.target
        target.resume() # Add this line
       #variable_addresses = [0x20001374, 0x20000008]  # Replace with actual addresses
       # address of counter varaible in wsf timer
       
        variable_addresses = [0x20001374]  # Replace with actual addresses
        monitor_variables(target, variable_addresses)

        print("Connected to target, CPU ID:", target.core.cpu_id)

if __name__ == "__main__":
    main()
