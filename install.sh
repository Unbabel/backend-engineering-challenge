#!/bin/sh

set -e

# Define the name of your program
PROGRAM_NAME="unbabel_cli"

# Define the location where the program will be installed
INSTALL_DIRECTORY="/usr/local/bin"

# Remove go mod if existing
rm go.mod || true

# Initialize Go module
go mod init "$PROGRAM_NAME"

# Build the Go program
go build -o "$PROGRAM_NAME"

# Install the program to the desired location
sudo mv "$PROGRAM_NAME" "$INSTALL_DIRECTORY/$PROGRAM_NAME"

# Make the program executable
sudo chmod +x "$INSTALL_DIRECTORY/$PROGRAM_NAME"

# Confirm that the program is installed
echo "Successfully installed $PROGRAM_NAME to $INSTALL_DIRECTORY"