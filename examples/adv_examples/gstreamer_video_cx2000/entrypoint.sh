#!/bin/bash
set -e

# Start SSHD in the background
/usr/sbin/sshd

# Now launch your application
# exec /app/launcher.sh
exec $*
