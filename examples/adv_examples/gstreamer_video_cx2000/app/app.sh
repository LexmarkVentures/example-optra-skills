#!/bin/bash
set -e

# If VIDEO_FILE is not provided, sleep for debugging purposes.
if [ -z "$VIDEO_FILE" ]; then
    echo "VIDEO_FILE environment variable is not set. Sleeping indefinitely for debugging."
    sleep infinity
    exit 1
fi

# Environment configuration
. /app/app.env

exec cmdloop "playvideo $VIDEO_FILE"
