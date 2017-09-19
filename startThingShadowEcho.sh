#!/usr/bin/env bash

# stop script on error
set -e

# Check to see if root CA file exists, download if not
if [ ! -f ~/connect_device_package/root-CA.crt ]; then
  printf "\nDownloading AWS IoT Root CA certificate from Symantec...\n"
  curl https://www.symantec.com/content/en/us/enterprise/verisign/roots/VeriSign-Class%203-Public-Primary-Certification-Authority-G5.pem > /home/jpdixon/connect_device_package/root-CA.crt
fi

# install AWS Device SDK for Python if not already installed
if [ ! -d ~/connect_device_package/aws-iot-device-sdk-python ]; then
  printf "\nInstalling AWS SDK...\n"
  cd /home/jpdixon/connect_device_package
  git clone https://github.com/aws/aws-iot-device-sdk-python.git
  pushd aws-iot-device-sdk-python
  python setup.py install
  popd
fi

# run pub/sub sample app using certificates downloaded in package
printf "\nRunning thingShadowEcho sample application...\n"
python ThingShadowEcho.py -e a30xablwjaar4w.iot.us-east-1.amazonaws.com -r /home/jpdixon/connect_device_package/root-CA.crt -c /home/jpdixon/connect_device_package/rpi3.cert.pem -k /home/jpdixon/connect_device_package/rpi3.private.key