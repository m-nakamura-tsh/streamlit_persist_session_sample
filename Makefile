# Makefile for Streamlit Persist Session Sample

.PHONY: help setup install run-main run-sample test format lint clean

help:
	@echo "Available commands:"
	@echo "  make setup      - Initial setup"
	@echo "  make install    - Install dependencies"
	@echo "  make run-main   - Run main application"
	@echo "  make run-sample - Run sample application"
	@echo "  make test       - Run tests"
	@echo "  make format     - Format code with ruff"
	@echo "  make lint       - Lint code with ruff"
	@echo "  make clean      - Clean up generated files"

setup:
	@bash scripts/setup.sh

install:
	uv sync

run-main:
	uv run --directory apps/main streamlit run app.py --server.port 8501

run-sample:
	uv run --directory apps/sample streamlit run simple_app.py --server.port 8502

test:
	uv run pytest

format:
	uv run ruff format .

lint:
	uv run ruff check .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf .mypy_cache