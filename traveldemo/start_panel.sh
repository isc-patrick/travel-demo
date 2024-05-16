#!/bin/bash

# Install jobs data
# Docker-compose cannot alone handle this without using a restart logic
# Could add this to setup during compose: https://github.com/vishnubob/wait-for-it
#python3 ../scripts/load_jobs.py

echo "pausing to let IRIS finish starting"
sleep 10
echo "Loading data"

# Todo
python3 ../scripts/load_data.py

# Start bokeh server
BOKEH_RESOURCES=cdn python3 -m panel serve app.py --allow-websocket-origin=localhost:8123 \
--address 0.0.0.0 --port 8123 --dev --autoreload --static-dirs assets=../assets

tail -f /dev/null