#!/bin/bash
#!/bin/bash

# Function to check Python version
check_python_version() {
    required_python_version="3.8"
    current_python_version=$(python3 -c 'import platform; print(platform.python_version())')

    if [[ $(printf '%s\n' "$required_python_version" "$current_python_version" | sort -V | head -n1) == "$required_python_version" ]]; then 
        return 0
    else
        return 1
    fi
}

# Function to check Node.js version
# Function to check Node.js version
check_node_version() {
    required_node_version=18
    current_node_version=$(node --version | grep -oP 'v\K\d+')

    if [[ "$current_node_version" -ge "$required_node_version" ]]; then
        return 0
    else
        return 1
    fi
}

# Check Python version
if check_python_version; then
    echo "Python version is 3.8 or higher."
else
    echo "Error: Python 3.8 or higher is required."
    exit 1
fi

# Check Node.js version
if check_node_version; then
    echo "Node.js version is 18 or higher."
else
    echo "Error: Node.js 18 or higher is required."
    exit 1
fi

# Install dependencies from requirements.txt
echo "Installing Python dependencies..."
cd server
pip3 install -r requirements.txt
echo "Dependencies installed successfully."
echo "Installing JS dependencies..."
cd ..
cd client/web
npm install
echo "JS dependencies installed successfully. Starting Sveltekit build and deployment..."
npm run build
pm2 start build/index.js -f
echo "Build finished. Deployed on port 3000. Starting Neural Networks and API"
cd ../..
cd server/api
SESSION_NAME="coughscan_api"
COMMAND="gunicorn -w 4 -b 0.0.0.0:5000 server.api.app:app &"


tmux new-session -d -s "$SESSION_NAME"
tmux send-keys -t "$SESSION_NAME" "$COMMAND" C-m

echo "Started tmux session '$SESSION_NAME' running '$COMMAND'"
cd ../..
echo "Note, it takes some time for the api to start up."
