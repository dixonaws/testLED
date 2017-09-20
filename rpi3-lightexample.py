
'''
This is a complete device shadow document for thing "rpi3"

{
    "desired": {
        "redlight": "on",
        "greenlight": "on"
  }
}
'''

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import sys
import logging
import time
import json
import argparse
import os


class shadowCallbackContainer:
    def __init__(self, deviceShadowInstance):
        self.deviceShadowInstance = deviceShadowInstance

    # Custom Shadow callback
    def customShadowCallback_Delta(self, payload, responseStatus, token):

        # Read in command-line parameters
        # payload is a JSON string ready to be parsed using json.loads(...)
        # in both Py2.x and Py3.x
        print("Received a delta message:")
        print(payload)

        # Load the payload into a dictionary object
        dictPayload = json.loads(payload)

        for key in dictPayload["state"].keys():
            print("state keys: " + key)

        # determine which keys are present in the device shadow delta
        # for example, if the state of 'redlght' did not change, it will not be in the
        # shadow delta and thus not present in the dictPayload object
        # take action on the keys that are present in dictPayload
        if ("redlight" in dictPayload["state"]):
            if (dictPayload["state"]["redlight"] == "on"):
                sys.stdout.write("*** Turn on the red light... ")
                os.system('python redLedOn.py')
                print("done.")
            if (dictPayload["state"]["redlight"] == "off"):
                sys.stdout.write("*** Turn off the red light... ")
                os.system('python redLedOff.py')
                print("done.")

        if ("greenlight" in dictPayload["state"]):
            if (dictPayload["state"]["greenlight"] == "on"):
                sys.stdout.write("*** Turn on the green light... ")
                os.system('python greenLedOn.py')
                print("done.")
            if (dictPayload["state"]["greenlight"] == "off"):
                sys.stdout.write("*** Turn off the green light... ")
                os.system('python greenLedOff.py')
                print("done.")

        deltaMessage = json.dumps(dictPayload["state"])

        print("delta message: " + deltaMessage)
        sys.stdout.write("Request to update the reported state... ")
        newPayload = '{"state":{"reported":' + deltaMessage + '}}'
        self.deviceShadowInstance.shadowUpdate(newPayload, None, 5)
        print("sent.")

    def customCallback(self, payload, responseStatus, token):
        dictPayload = json.loads(payload)

        print dictPayload["state"].keys()


# Read in command-line parameters
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--endpoint", action="store", required=True, dest="host", help="Your AWS IoT custom endpoint")
parser.add_argument("-r", "--rootCA", action="store", required=True, dest="rootCAPath", help="Root CA file path")
parser.add_argument("-c", "--cert", action="store", dest="certificatePath", help="Certificate file path")
parser.add_argument("-k", "--key", action="store", dest="privateKeyPath", help="Private key file path")
parser.add_argument("-w", "--websocket", action="store_true", dest="useWebsocket", default=False,
                    help="Use MQTT over WebSocket")
parser.add_argument("-n", "--thingName", action="store", dest="thingName", default="rpi3", help="Targeted thing name")
parser.add_argument("-id", "--clientId", action="store", dest="clientId", default="ThingShadowEcho",
                    help="Targeted client id")

args = parser.parse_args()
host = args.host
rootCAPath = args.rootCAPath
certificatePath = args.certificatePath
privateKeyPath = args.privateKeyPath
useWebsocket = args.useWebsocket
thingName = args.thingName
clientId = args.clientId

if args.useWebsocket and args.certificatePath and args.privateKeyPath:
    parser.error("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
    exit(2)

if not args.useWebsocket and (not args.certificatePath or not args.privateKeyPath):
    parser.error("Missing credentials for authentication.")
    exit(2)

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTShadowClient
myAWSIoTMQTTShadowClient = None
if useWebsocket:
    myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(clientId, useWebsocket=True)
    myAWSIoTMQTTShadowClient.configureEndpoint(host, 443)
    myAWSIoTMQTTShadowClient.configureCredentials(rootCAPath)
else:
    myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(clientId)
    myAWSIoTMQTTShadowClient.configureEndpoint(host, 8883)
    myAWSIoTMQTTShadowClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTShadowClient configuration
myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect to AWS IoT
myAWSIoTMQTTShadowClient.connect()

# Create a deviceShadow with persistent subscription
deviceShadowHandler = myAWSIoTMQTTShadowClient.createShadowHandlerWithName(thingName, True)
shadowCallbackContainer_Bot = shadowCallbackContainer(deviceShadowHandler)

# Get the shadow in AWS IoT
print "*** Shadow in AWS IoT:"
# deviceShadowHandler.shadowGet(shadowCallbackContainer.customCallback())

# Listen on deltas
deviceShadowHandler.shadowRegisterDeltaCallback(shadowCallbackContainer_Bot.customShadowCallback_Delta)

# Loop forever
while True:
    time.sleep(1)
