#!/bin/sh

mkdir -p ~/.streamlit/


echo "\
[server]
headless = true
enableCORS=false
port = $PORT
" > ~/.streamlit/config.toml

streamlit run app.py
