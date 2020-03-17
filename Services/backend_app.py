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
connection_string = "HostName=AzureTelemetryExampleHub.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=glElhyl7qcPnjnBZYUTQob98kdzZRa97svoJO3c/0RQ="
device_id = "simulatedDevice"

# Details of Direct Method to call.
method_name = "SetTelemetryInterval"
method_payload = "10"

# Routine updates telemetry interval via hub
def iot_device_updatetelemetry_interval():
    
    # Try-except in use as webservice may fail
    try:

        # Create registry manager
        registry_manager = IoTHubRegistryManager(connection_string)

        # Call the direct method
        device_method = CloudToDeviceMethod(method_name = method_name, 
                                            payload = method_payload)
        device_response = registry_manager.invoke_device_method(device_id, device_method)

        # Provide feedback to user
        print("")
        print("Device Method Called")
        print("Device Method Name     : {0}".format(method_name))
        print("Device Method Payload  : {0}".format(method_payload))
        
        print("Device Response")
        print("Response Status        : {0}".format(device_response.status))
        print("Response Payload        : {0}".format(device_response.payload))

        # Allow user to close service connection
        input("Press Enter to continue ...\n")

    except Exception as ex:
        print("Unexpected error")
        return

    except KeyboardInterrupt:
        print("Device Instruction stopped")

# Main method calls routine to update telemetry interval