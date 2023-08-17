import subprocess

# Path to your arm-none-eabi-gdb
gdb_path = 'arm-none-eabi-gdb'

# Path to your gdb_python.py script
gdb_script_path = 'gdb_python.py'

# Path to your binary (compiled with debugging symbols)
binary_path = 'path/to/your_binary.elf'

# Commands to be run in GDB
commands = [
    f'file build/max32665.elf',            # Load the binary
    f'source gdb_python.py',      # Source the Python script
    'target remote localhost:3333',   # Connect to the target
    'monitor reset halt',             # Reset and halt the target (modify as needed)
    'load',                           # Load the binary to the target
    'monitor_variable testCounter',   # Run your custom command to monitor the variable
    'continue'                        # Continue execution
]

# Launch GDB with a command line interface
gdb_process = subprocess.Popen([gdb_path, '--interpreter=mi2'], stdin=subprocess.PIPE, universal_newlines=True)

# Run the GDB commands
for command in commands:
    gdb_process.stdin.write(f'{command}\n')
    gdb_process.stdin.flush()

# Keep the process running so you can see the printouts
gdb_process.wait()
