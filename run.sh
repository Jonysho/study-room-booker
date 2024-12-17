#!/bin/bash

# Prompt the user for username and password
read -p "Enter your username: " USERNAME
read -sp "Enter your password: " PASSWORD
echo

# Export the username and password as environment variables
export USERNAME
export PASSWORD

# Install required Python packages
# pip install -r requirements.txt

# Run the Python script
python3 navigater.py