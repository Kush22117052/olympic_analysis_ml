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
if [ -z "$PORT" ]; then
  PORT=8501
fi

# Run the Streamlit app with the correct server port and address
streamlit run app.py --server.port $PORT --server.address 0.0.0.0

