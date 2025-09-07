#!/bin/bash

# 初期セットアップスクリプト

echo "Setting up Streamlit Persist Session Sample..."

# Create data directories
echo "Creating data directories..."
mkdir -p data/processes
mkdir -p data/processes/deleted
mkdir -p data/logs

# Create .gitkeep files
touch data/processes/.gitkeep
touch data/logs/.gitkeep

# Install dependencies with uv
echo "Installing dependencies..."
if command -v uv &> /dev/null; then
    uv sync
else
    echo "Error: uv is not installed. Please install it first:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Make run scripts executable
chmod +x run_main.sh
chmod +x run_sample.sh
chmod +x scripts/clean_data.py

echo "Setup complete!"
echo ""
echo "To run the main app: ./run_main.sh"
echo "To run the sample app: ./run_sample.sh"