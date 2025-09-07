#!/bin/bash

# サンプルアプリケーションを起動するスクリプト

echo "Starting sample application..."
uv run --directory apps/sample streamlit run simple_app.py --server.port 8502