from pyocd.probe.pydapaccess import DAPAccess

# Get a list of all connected debug probes
probes = DAPAccess.get_connected_devices()

# Print the details of each probe
for probe in probes:
    print("Probe ID: %s, Vendor: %s, Product: %s" % (probe._unique_id, probe.vendor_name, probe.product_name))
