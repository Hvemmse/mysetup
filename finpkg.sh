#!/bin/bash


### 

You can run this script with the name of the package as the argument in the check_package function. It will first run the getupdate command to update the package list, and then check if the package is installed. If it is not installed, it will install the package using apt-get. Finally, it will output a success message to the user.

###



# Update package list
function getupdate() {
  sudo apt-get update
}

# Check if package is installed
function check_package() {
  if ! dpkg -s "$1" >/dev/null 2>&1; then
    # If package is not installed, install package
    sudo apt-get install -y "$1"
  fi
}

# Run getupdate command to update package list
getupdate

# Check if package is installed (replace "package-name" with actual package name)
check_package "package-name"

# Output success message to user
echo "Package-name is installed and up-to-date."
