mkdir -p ~/ .streamlit/
echo "\
[server]\n\
port= $PORT\n\
enableCORS=false\n\
headless=true\n\
\n\
"> ~/.streamlit/config.toml
#!/bin/bash

pip install -r requirements.txt
chmod +x setup.sh

