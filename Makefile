.PHONY: dev test test-cov lint format clean build release help

# Default target
.DEFAULT_GOAL := help

help:  ## Show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

dev:  ## Build and install in development mode
	maturin develop

dev-release:  ## Build and install in development mode with optimizations
	maturin develop --release

test:  ## Run tests
	pytest tests/ -v

test-cov:  ## Run tests with coverage report
	pytest tests/ -v --cov=blart-py --cov-report=term-missing --cov-report=html

test-watch:  ## Run tests in watch mode (requires pytest-watch)
	ptw tests/ -- -v

lint:  ## Run all linters
	@echo "Running Rust linters..."
	cargo clippy --all-targets --all-features -- -D warnings
	@echo "Running Python linters..."
	ruff check python/ tests/ examples/
	mypy python/ --ignore-missing-imports

format:  ## Format all code
	@echo "Formatting Rust code..."
	cargo fmt --all
	@echo "Formatting Python code..."
	black python/ tests/ examples/

format-check:  ## Check code formatting without making changes
	@echo "Checking Rust formatting..."
	cargo fmt --all -- --check
	@echo "Checking Python formatting..."
	black --check python/ tests/ examples/

clean:  ## Clean build artifacts
	cargo clean
	rm -rf target/
	rm -rf dist/
	rm -rf python/blart/__pycache__/
	rm -rf tests/__pycache__/
	rm -rf examples/__pycache__/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +

build:  ## Build release wheels
	maturin build --release

build-all:  ## Build wheels for all interpreters
	maturin build --release --find-interpreter

release:  ## Build release wheels and test installation
	maturin build --release
	@echo "Testing wheel installation..."
	pip install --force-reinstall target/wheels/*.whl
	python -c "import blart; print('Import successful!')"

benchmark:  ## Run performance benchmarks
	pytest tests/test_performance.py -v

install:  ## Install from local wheel
	pip install --force-reinstall target/wheels/*.whl

check: lint test  ## Run linters and tests

ci: format-check lint test-cov  ## Run all CI checks locally

examples:  ## Run all example scripts
	@echo "Running basic usage example..."
	python examples/basic_usage.py
	@echo "\nRunning prefix queries example..."
	python examples/prefix_queries.py
	@echo "\nRunning fuzzy matching example..."
	python examples/fuzzy_matching.py

setup:  ## Set up development environment
	pip install -U pip maturin
	pip install pytest pytest-cov black ruff mypy
	pip install pytest-watch  # optional, for test-watch
