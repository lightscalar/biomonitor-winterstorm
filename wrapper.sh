#!/bin/bash

# ------------------------

# Wrapper script for the biomonitor system.

# Starts the frontend Vue.js web server through
# a python http server, as well as the backend
# python server.

# ------------------------

# Start the backend.
python /app/api/server.py &

python /app/api/frontend_server.py

echo "All done, servers started!"
