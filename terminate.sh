#!/bin/bash

# Kill the tmux session named 'coughscan_api'
if tmux has-session -t coughscan_api 2>/dev/null; then
    echo "Killing tmux session: coughscan_api"
    tmux kill-session -t coughscan_api
else
    echo "tmux session 'coughscan_api' does not exist."
fi
cd cleint/web
# Stop all PM2 processes (or specify a particular process)
echo "Stopping PM2 server..."
pm2 stop all

echo "Services stopped."
cd ../..

