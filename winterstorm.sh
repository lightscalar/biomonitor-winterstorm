#!/bin/bash

# Executable to download and run the biomonitor app.

cd ~

# Kill all of the docker processes executing on
# the machine currently.  This should definitely
# be removed if this is going anywhere with other
# docker images!
echo "\n---> Killing all docker instances"
docker kill $(docker ps -q)

# Try to find the biomonitor directory. If it isn't there,
# grab it from Matt's github repo.
if [ ! -d "biomonitor-winterstorm" ]; then
    echo "\n---> Cloning into the winterstorm repo since it doesn't exist here.\n"
    git clone https://github.com/lightscalar/biomonitor-winterstorm.git
fi

cd ~/biomonitor-winterstorm

# Start the application!
echo "\n--->>> Starting the image and running the webservers!\n"
sh start_image.sh
