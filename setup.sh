#!/bin/bash

# Ensure ~/.streamlit directory exists
# mkdir -p ~/.streamlit/

# Create the Streamlit config file
# echo "[server]
# headless = true
# enableCORS = false
# " > ~/.streamlit/config.toml

# Install dependencies from requirements.txt
pip install -r requirements.txt
streamlit run app.py --server.port $PORT --server.address 0.0.0.0

