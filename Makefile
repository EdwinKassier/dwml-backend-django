.PHONY: install install-dev test test-unit test-integration lint format clean pre-deploy security-check coverage help migrate runserver
.PHONY: docker-up docker-down docker-logs docker-ps docker-rebuild docker-shell
.PHONY: celery-worker celery-beat celery-flower celery-purge redis-cli redis-flush

# Variables
PYTHON := python3
PIP := $(PYTHON) -m pip
PYTEST := $(PYTHON) -m pytest
BLACK := $(PYTHON) -m black
FLAKE8 := $(PYTHON) -m flake8
MYPY := $(PYTHON) -m mypy
BANDIT := $(PYTHON) -m bandit
ISORT := $(PYTHON) -m isort
COVERAGE := $(PYTHON) -m coverage

# Default target
help:
	@echo "Available commands:"
	@echo ""
	@echo "Development:"
	@echo "  make install          - Install production dependencies"
	@echo "  make install-dev      - Install dev dependencies and pre-commit"
	@echo "  make migrate          - Run Django migrations"
	@echo "  make runserver        - Run Django development server"
	@echo "  make clean            - Clean temporary files and caches"
	@echo ""
	@echo "Testing:"
	@echo "  make test             - Run all tests with coverage"
	@echo "  make test-unit        - Run unit tests only"
	@echo "  make test-integration - Run integration tests only"
	@echo "  make coverage         - Generate coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint             - Run linting checks"
	@echo "  make format           - Format code with black and isort"
	@echo "  make security-check   - Run security scans (bandit + safety)"
	@echo "  make pre-deploy       - Run all pre-deployment checks"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-up        - Start all Docker services"
	@echo "  make docker-down      - Stop all Docker services"
	@echo "  make docker-logs      - View Docker logs (follow mode)"
	@echo "  make docker-ps        - Show Docker service status"
	@echo "  make docker-rebuild   - Rebuild and restart all services"
	@echo "  make docker-shell     - Open shell in web container"
	@echo ""
	@echo "Celery:"
	@echo "  make celery-worker    - Start Celery worker (local)"
	@echo "  make celery-beat      - Start Celery beat scheduler (local)"
	@echo "  make celery-flower    - Start Flower monitoring UI (local)"
	@echo "  make celery-purge     - Purge all Celery tasks"
	@echo ""
	@echo "Redis:"
	@echo "  make redis-cli        - Open Redis CLI"
	@echo "  make redis-flush      - Flush all Redis data"

# Install production dependencies
install:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# Install development dependencies and setup pre-commit
install-dev: install
	$(PIP) install pytest pytest-django pytest-cov black flake8 mypy bandit safety pre-commit isort coverage django-stubs djangorestframework-stubs
	pre-commit install
	@echo "✅ Development environment setup complete!"

# Run all tests with coverage
test:
	cd backend && $(PYTEST) -v --cov=. --cov-report=term-missing --cov-report=xml --cov-report=html --tb=short
	@echo "✅ All tests passed!"

# Run unit tests only
test-unit:
	cd backend && $(PYTEST) -v -m unit --tb=short
	@echo "✅ Unit tests passed!"

# Run integration tests only
test-integration:
	cd backend && $(PYTEST) -v -m integration --tb=short
	@echo "✅ Integration tests passed!"

# Run all linting checks
lint:
	@echo "Running flake8..."
	$(FLAKE8) backend/ --max-line-length=88 --extend-ignore=E203,W503,E501,F401,F841,F403,F405,E711,E712 --exclude=migrations,__pycache__
	@echo "Running black check..."
	$(BLACK) --check backend/ --line-length=88 --exclude="migrations/"
	@echo "Running isort check..."
	$(ISORT) --check-only backend/ --profile=black --skip=migrations
	@echo "Running mypy..."
	$(MYPY) backend/ --ignore-missing-imports --exclude="migrations/" || true
	@echo "✅ All linting checks passed!"

# Format code with black and isort
format:
	@echo "Formatting with black..."
	$(BLACK) backend/ --line-length=88 --exclude="migrations/"
	@echo "Sorting imports with isort..."
	$(ISORT) backend/ --profile=black --skip=migrations
	@echo "✅ Code formatted successfully!"

# Run security checks
security-check:
	@echo "Running bandit security scan..."
	$(BANDIT) -r backend/ -f json -o bandit-report.json --exclude "*/tests/*,*/migrations/*" || true
	@echo "Running safety dependency scan..."
	$(PIP) list --format=freeze | safety check --stdin --json --output safety-report.json || true
	@echo "✅ Security scans complete! Check reports: bandit-report.json, safety-report.json"

# Generate coverage report
coverage:
	cd backend && $(COVERAGE) run --source='.' -m pytest
	$(COVERAGE) report -m
	$(COVERAGE) html
	@echo "✅ Coverage report generated in htmlcov/"

# Pre-deployment checks (runs everything)
pre-deploy: clean format lint test security-check
	@echo "✅✅✅ All pre-deployment checks passed! Ready to deploy! ✅✅✅"

# Django specific commands
migrate:
	cd backend && $(PYTHON) manage.py migrate

runserver:
	cd backend && $(PYTHON) manage.py runserver

# Clean temporary files
clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name '.pytest_cache' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name '.mypy_cache' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name 'htmlcov' -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '.coverage' -delete 2>/dev/null || true
	find . -type f -name 'coverage.xml' -delete 2>/dev/null || true
	find . -type f -name '*-report.json' -delete 2>/dev/null || true
	@echo "✅ Cleaned temporary files!"

# Docker Commands
docker-up:
	docker-compose up -d
	@echo "✅ Docker services started!"
	@echo "   Web: http://localhost:8080"
	@echo "   Flower: http://localhost:5555"

docker-down:
	docker-compose down
	@echo "✅ Docker services stopped!"

docker-logs:
	docker-compose logs -f

docker-ps:
	docker-compose ps

docker-rebuild:
	docker-compose down
	docker-compose build --no-cache
	docker-compose up -d
	@echo "✅ Docker services rebuilt and restarted!"

docker-shell:
	docker-compose exec web /bin/bash

# Celery Commands (for local development without Docker)
celery-worker:
	cd backend && celery -A config worker --loglevel=info --concurrency=2
	@echo "✅ Celery worker started!"

celery-beat:
	cd backend && celery -A config beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
	@echo "✅ Celery beat started!"

celery-flower:
	cd backend && celery -A config flower --port=5555
	@echo "✅ Flower monitoring UI started at http://localhost:5555"

celery-purge:
	cd backend && celery -A config purge -f
	@echo "✅ All Celery tasks purged!"

# Redis Commands
redis-cli:
	docker-compose exec redis redis-cli

redis-flush:
	docker-compose exec redis redis-cli FLUSHALL
	@echo "⚠️  All Redis data flushed!"
