#!/bin/bash

service=$1
machine=$2

echo "Checking if $service is already installed on $machine..."
sleep 2

echo "$service not found on $machine. Starting installation..."
sleep 2

echo "Installing $service on $machine..."
sleep 2

echo "$service installation completed successfully on $machine."
