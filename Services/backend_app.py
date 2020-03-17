'''

Backend Application

Application simulates backend, on-cloud service used to update simulated device.

'''

# Module importations
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod, CloudToDeviceMethodResult
from builtins import input
import sys

# Service connection string used to authenticate with the device hub.
CONNECTION_STRING = ""
DEVICE_ID = ""

# Details of Direct Method to call.
METHOD_NAME = "SetTelemetryInterval"
METHOD_PAYLOAD = "10"

# Routine updates telemetry interval via hub
def iot_device_updatetelemetry_interval():
    pass

# Main method calls routine to update telemetry interval