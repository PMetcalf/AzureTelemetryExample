'''

Device Simulator

Generates and sends signals to Azure IoT backend.

'''

# Module Importations
import random
import time
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse

# The device connection string to authenticate the device with your IoT hub.
# Using the Azure CLI:
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
connection_string = "HostName=AzureTelemetryExampleHub.azure-devices.net;DeviceId=simulatedDevice;SharedAccessKey=qfc+fv2lxxXvwTcYjZYMaEC6B4mEZXd6Cf4RXFnNrUI="

# Define the JSON message to send to IoT Hub.
temperature_C = 10.0
humidity_percent = 50
message_body = '{{"temperature": {temperature},"humidity": {humidity}}}'

# Interval is used to set reporting frequency.
interval = 1

# Method creates the IoT Hub client.
def iothub_client_init():
    client = IoTHubDeviceClient.create_from_connection_string(connection_string)
    return client


# Method sets up a listening function for hub responses.
def listen_for_hub_response(device_client):
    
    global interval

    while True:

        # Set the device to receive messages from the hub.
        method_request = device_client.receive_method_request()
        print("\nMethod callback called with:\nmethodName = {method_name}\npayload = {payload}".format(
            method_name = method_request.name,
            payload = method_request.payload))

        # Manage the response contained in the message body.
        if method_request.name == "SetTelemetryInterval":
            try:
                interval = int(method_request.payload)
            except ValueError:
                response_payload = {"Response:": "Invalid parameter"}
                response_status = 400
            else:
                response_payload = {"Response:": "Executed direct method {}".format(method_request.name)}
                response_status = 200
        else:
            response_payload = {"Response:": "Direct method {} not defined}".format(method_request.name)}
            response_status = 404

        # Return a message to the hub.
        method_response = MethodResponse(method_request.request_id, response_status, payload = responseresponse_payload)
        device_client.send_method_response(method_response)


# Method creates and runs client.
def iothub_client_telemetry_sample_run():

    # Try-catch in use as web service may fail.
    try:
        # Initialise the client.
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

        while True:
            # Build the message with simulated telemetry values.
            temperature = temperature_C + (random.random() * 10)
            humidity = humidity_percent + (random.random() * 20)
            msg_txt_formatted = message_body.format(temperature=temperature, humidity=humidity)
            message = Message(msg_txt_formatted)

            # Add a custom application property to the message.
            # An IoT hub can filter on these properties without access to the message body.
            if temperature > 15:
              message.custom_properties["temperatureAlert"] = "true"
            else:
              message.custom_properties["temperatureAlert"] = "false"

            # Send the message.
            print( "Sending message: {}".format(message) )
            client.send_message(message)
            print ( "Message successfully sent" )
            time.sleep(1)

    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    print ( "IoT Hub Quickstart #1 - Simulated device" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run()

