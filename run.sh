#!/bin/bash

# Load NVM if installed, specifically for Zsh users
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm

# Use the current working directory
CURRENT_DIR=$(pwd)

# Ensure Yarn is installed
if ! command -v yarn &> /dev/null; then
    npm install -g yarn
fi

# Function to open a new terminal tab and run a command
open_new_tab() {
    local cmd="$1"

    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS: Use iTerm2 if available, otherwise use Terminal
        if command -v osascript &>/dev/null && open -Ra "iTerm"; then
            osascript <<EOF
            tell application "iTerm"
                tell current window
                    create tab with default profile
                    tell current session
                        write text "$cmd"
                    end tell
                end tell
            end tell
EOF
        else
            osascript <<EOF
            tell application "Terminal"
                do script "$cmd"
            end tell
EOF
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Ubuntu: Use gnome-terminal
        if command -v gnome-terminal &>/dev/null; then
            gnome-terminal -- bash -c "$cmd; exec bash"
        else
            echo "gnome-terminal is not installed. Please install it to run this script on Ubuntu."
        fi
    else
        echo "Unsupported OS. This script works on macOS and Ubuntu."
    fi
}

# Start frontend server in a new tab
open_new_tab "cd '$CURRENT_DIR/frontend' && nvm install 20.17 && nvm use 20.17 && yarn install && yarn run dev"

# Check if the Neo4j container already exists
if docker ps -a --format '{{.Names}}' | grep -Eq "^neo4j-apoc$"; then
    # If it exists, check if it's running
    if docker ps --format '{{.Names}}' | grep -Eq "^neo4j-apoc$"; then
        echo "The container 'neo4j-apoc' is already running."
    else
        echo "The container 'neo4j-apoc' exists but is not running. Starting the container..."
        docker start neo4j-apoc
    fi
else
    # If it doesn't exist, run a new container in a new tab
    open_new_tab "docker run -p 7474:7474 -p 7687:7687 --name neo4j-apoc -e NEO4J_apoc_export_file_enabled=true -e NEO4J_apoc_import_file_enabled=true -e NEO4J_apoc_import_file_use__neo4j__config=true -e NEO4J_PLUGINS='[\"apoc\", \"graph-data-science\"]' neo4j"
fi

# Run backend setup and start server in another new tab
open_new_tab "cd '$CURRENT_DIR/backend' && python3 -m venv envName && source envName/bin/activate && pip install -r requirements.txt && envName/bin/uvicorn score:app --reload"
