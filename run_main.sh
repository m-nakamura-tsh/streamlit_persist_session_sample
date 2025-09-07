#!/bin/bash

# メインアプリケーションを起動するスクリプト

echo "Starting main application..."
uv run --directory apps/main streamlit run app.py --server.port 8501