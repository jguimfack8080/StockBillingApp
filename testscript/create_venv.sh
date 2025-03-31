#!/bin/bash

# Check if the virtual environment already exists
if [ -d ".venv" ]; then
    echo "The virtual environment already exists."
else
    # Create the virtual environment at the root of the project
    echo "Creating the virtual environment..."
    python3 -m venv .
    echo "Virtual environment created."
fi

# Activate the virtual environment
# For Ubuntu
if [ "$(uname)" == "Linux" ]; then
    source .venv/bin/activate
    echo "Virtual environment activated (Ubuntu/Linux)."
# For Windows
elif [ "$(expr substr $(uname -s) 1 5)" == "MINGW" ]; then
    source .venv/Scripts/activate
    echo "Virtual environment activated (Windows)."
fi
