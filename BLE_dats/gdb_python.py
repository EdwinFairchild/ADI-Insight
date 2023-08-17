import gdb

class MonitorVariable(gdb.Breakpoint):
    def __init__(self, variable):
        super(MonitorVariable, self).__init__(variable, gdb.BP_WATCHPOINT)
        self.variable = variable

    def stop(self):
        value = gdb.parse_and_eval(self.variable)
        print(f"{self.variable} = {value}")
        return False

class SetWatchpointCommand(gdb.Command):
    def __init__(self):
        super(SetWatchpointCommand, self).__init__("monitor_variable", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        variable_to_watch = arg.strip()
        if variable_to_watch:
            MonitorVariable(variable_to_watch)
            print(f"Monitoring variable {variable_to_watch}")
        else:
            print("Please provide the variable name to monitor.")

SetWatchpointCommand()

# Replace this with your specific connection details
#gdb.execute("target remote localhost:3333")
