#!/bin/bash
# install.sh — mock, interactive service installer
# - Prompts the user for a service name (e.g., nginx/docker/terraform)
# - Simulates check and installation steps
# - Appends messages to logs/provisioning.log
# - Does NOT perform real package installations

log_file="logs/provisioning.log"

while true; do
	read -p "Enter the service you want to install (Nginx, Docker, Terraform): " service
	
	if [ -z "$service" ]; then
		echo "Please enter a service name."
		continue
	fi
	
	echo "Checking if $service is already installed..." >> "$log_file"
	sleep 2
	
	echo "$service not found. Starting installation..." >> "$log_file"
	sleep 2
	
	echo "Installing $service..." >> "$log_file"
	sleep 2
	
	echo "$service installation completed successfully." >> "$log_file"
	echo "$service installation completed successfully."
	break
done