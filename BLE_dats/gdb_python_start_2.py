import subprocess
import time

def send_command(process, command):
    process.stdin.write(f'{command}\n')
    process.stdin.flush()

def print_call_stack(process):
    send_command(process, 'backtrace')

def print_core_registers(process):
    send_command(process, 'info registers')

def run_gdb(variables_to_watch):
    # Path to your arm-none-eabi-gdb, gdb_python.py script, and binary
    gdb_path = 'arm-none-eabi-gdb'
    gdb_script_path = 'gdb_python.py'
    binary_path = 'path/to/your_binary.elf'

    # Launch GDB with a command line interface
    gdb_process = subprocess.Popen([gdb_path, '--interpreter=mi2'], stdin=subprocess.PIPE, universal_newlines=True)

    # Run the initial setup commands
    send_command(gdb_process, f'file {binary_path}')
    send_command(gdb_process, f'source {gdb_script_path}')
    send_command(gdb_process, 'target remote localhost:3333')
    send_command(gdb_process, 'monitor reset halt')
    send_command(gdb_process, 'load')

    # Add the initial watchpoints
    for variable in variables_to_watch:
        send_command(gdb_process, f'monitor_variable {variable}')

    # Continue execution
    send_command(gdb_process, 'continue')

    # Simulate waiting for a few seconds (e.g., user interaction in GUI)
    time.sleep(5)

    # Pause execution (you can modify this based on your specific setup)
    send_command(gdb_process, 'interrupt')

    # Add a new variable to watch
    send_command(gdb_process, 'monitor_variable another_variable')

    # Resume execution
    send_command(gdb_process, 'continue')

    # Simulate keeping GDB running (e.g., waiting for user interaction in GUI)
    time.sleep(5)

    # Terminate GDB when done (or when user chooses to exit in GUI)
    gdb_process.terminate()

# List of variables to watch initially
variables_to_watch = ['my_variable']

# Run GDB with the initial variables
run_gdb(variables_to_watch)