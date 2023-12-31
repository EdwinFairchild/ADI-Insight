from pyocd.core.helpers import ConnectHelper
#from target_max32655 import MAX32655  # Make sure this import corresponds to the actual location of your custom target file
import time
import logging
import subprocess
logging.basicConfig(level=logging.DEBUG)

def mass_erase():
    command = ["pyocd", "erase", "--mass"]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print("Mass erase failed:", result.stderr.decode())
    else:
        print("Mass erase completed.")



def print_core_registers(target):
    # Define the list of core registers you want to read
    reg_list = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r10', 'r11', 'r12', 'sp', 'lr', 'pc', 'xpsr']

    #halt tagert
    target.halt()
    # Get the core registers
    core_registers = target.read_core_registers_raw(reg_list)
    #resume target
    target.resume()
    
    # Print the core registers
    print("Core Registers:")
    for reg, value in zip(reg_list, core_registers):
        print(f"{reg}: {value:08x}")



def monitor_variables(target, addresses):
    previous_value = None
    currentTime = time.time()
    while True:
        for address in addresses:
            value = target.read32(address)
            if value != previous_value:
                previous_value = value
                print(f"Variable at {address:x}: {value}")
        time.sleep(0.1)  # Adjust the refresh rate as needed
        # after 10 seconds do a mass erase
        if time.time() - currentTime > 5:
            target.halt()
            target.disconnect()  # Disconnect before erase
            mass_erase()
            print("Mass erase completed.")
            break;

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
        # Call the method to print core registers
        print_core_registers(target)
        variable_addresses = [0x20001374]  # Replace with actual addresses
        monitor_variables(target, variable_addresses)
        print("All done!")
       # print("Connected to target, CPU ID:", target.cores.cpu_id)

if __name__ == "__main__":
    main()
