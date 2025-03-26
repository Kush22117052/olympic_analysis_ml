#!/bin/bash

# Ensure ~/.streamlit directory exists
mkdir -p ~/.streamlit/

# Create the Streamlit config file with proper environment variable for $PORT
echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
" > ~/.streamlit/config.toml

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Make sure setup.sh is executable
chmod +x setup.sh
