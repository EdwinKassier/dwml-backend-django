# Cryptocurrency Portfolio API 🚀

[![CI/CD Pipeline](https://github.com/YOUR_USERNAME/crypto-backend-api/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/YOUR_USERNAME/crypto-backend-api/actions)
[![codecov](https://codecov.io/gh/YOUR_USERNAME/crypto-backend-api/branch/master/graph/badge.svg)](https://codecov.io/gh/YOUR_USERNAME/crypto-backend-api)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Django 4.1+](https://img.shields.io/badge/django-4.1+-green.svg)](https://www.djangoproject.com/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 🎯 Introduction

A production-ready Django REST API for cryptocurrency portfolio tracking and analysis with comprehensive CI/CD pipeline, code quality tools, and automated deployment.

## ✨ Features

- ✅ **Code Quality**: Black, Flake8, isort, Mypy
- ✅ **Testing**: Pytest with 80%+ coverage
- ✅ **Security**: Bandit security scanning, Safety dependency checks
- ✅ **Pre-commit Hooks**: Automated code quality checks
- ✅ **CI/CD Pipeline**: GitHub Actions with tag-based deployment
- ✅ **Type Checking**: Full mypy type annotations
- ✅ **API Documentation**: OpenAPI 3.0 specification
- ✅ **Monitoring**: Sentry error tracking, Prometheus metrics
- ✅ **Caching**: Redis for performance optimization

## 🛠 Requirements

* Python 3.10+
* pip or Pipenv
* Git
* Docker (optional, for containerized deployment)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd crypto-backend-api
```

### 2. Set Up Development Environment

```bash
# Install dependencies
make install-dev

# This will:
# - Install all Python dependencies
# - Set up pre-commit hooks
# - Configure development tools
```

### 3. Configure Environment

```bash
# Copy environment template
cp env.example .env

# Edit .env with your settings
nano .env
```

### 4. Run Migrations

```bash
make migrate
```

### 5. Run the Development Server

```bash
make runserver
```

The API will be available at `http://localhost:8000`

## 📦 Installation Options

### Option 1: Using Make (Recommended)

```bash
# Install production dependencies
make install

# Install development dependencies
make install-dev
```

### Option 2: Using pip directly

```bash
pip install -r requirements.txt
```

### Option 3: Using Docker Compose

```bash
# Start all services (database, redis, web)
docker-compose up -d

# View logs
docker-compose logs -f web
```

## 🧪 Testing

### Run All Tests

```bash
make test
```

### Run Specific Test Types

```bash
# Unit tests only
make test-unit

# Integration tests only
make test-integration

# With coverage report
make coverage
```

### Run Tests Directly with Pytest

```bash
cd Core
pytest -v
```

## 🎨 Code Quality

### Format Code

```bash
make format
```

This runs:
- Black (code formatting)
- isort (import sorting)

### Run Linting

```bash
make lint
```

This checks:
- Flake8 (code linting)
- Black (formatting)
- isort (import sorting)
- Mypy (type checking)

## 🔒 Security

### Run Security Scans

```bash
make security-check
```

This runs:
- **Bandit**: Finds common security issues in Python code
- **Safety**: Checks dependencies for known vulnerabilities

Reports are generated in:
- `bandit-report.json`
- `safety-report.json`

## 🔄 Pre-commit Hooks

Pre-commit hooks run automatically on every commit to ensure code quality.

### Install Hooks

```bash
pre-commit install
```

### Run Hooks Manually

```bash
pre-commit run --all-files
```

### Hooks Include:
- Trailing whitespace removal
- End-of-file fixer
- YAML/JSON validation
- Black formatting
- isort import sorting
- Flake8 linting
- Bandit security checks
- Django unit tests

## 🚀 CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment.

### Pipeline Stages

1. **Quality Checks** - Code formatting, linting, type checking, security scans
2. **Testing** - Unit tests, integration tests, coverage reporting
3. **Deployment** - Tag-based production deployment
4. **Verification** - Post-deployment health checks

### Triggers

- **Push** to main/master/develop branches
- **Pull requests** to main/master
- **Tags** matching `prod/v*` pattern

### Viewing Pipeline Status

Visit the [Actions tab](https://github.com/YOUR_USERNAME/dwml-backend-django/actions) in your GitHub repository.

## 📋 Available Make Commands

```bash
make help              # Show all available commands
make install           # Install production dependencies
make install-dev       # Install dev dependencies + pre-commit
make test              # Run all tests with coverage
make test-unit         # Run unit tests only
make test-integration  # Run integration tests only
make lint              # Run linting checks
make format            # Format code with black + isort
make security-check    # Run security scans
make coverage          # Generate coverage report
make pre-deploy        # Run all pre-deployment checks
make migrate           # Run Django migrations
make runserver         # Run Django development server
make clean             # Clean temporary files
```

## 🏷 Tag-Based Deployment

### Creating a Production Release

```bash
# Using the release script
./scripts/create-prod-release.sh 1.0.0

# Or manually
git tag -a prod/v1.0.0 -m "Release version 1.0.0"
git push origin prod/v1.0.0
```

### Version Format

Tags must follow the pattern: `prod/vMAJOR.MINOR.PATCH`

Examples:
- `prod/v1.0.0`
- `prod/v1.2.3`
- `prod/v2.0.0`

### Deployment Process

1. Developer creates a tag: `prod/vX.X.X`
2. GitHub Actions triggers deployment pipeline
3. All quality checks and tests run
4. If successful, deploys to production
5. Creates GitHub release
6. Runs post-deployment verification

## 📊 Coverage Reporting

Coverage reports are automatically generated and uploaded to Codecov on every CI run.

### View Coverage Locally

```bash
make coverage
open htmlcov/index.html  # Opens coverage report in browser
```

### Coverage Goals

- Overall: 80%+
- Critical modules: 90%+
- New code: 90%+

## 🔧 Configuration Files

- **`pyproject.toml`**: Project metadata, tool configuration
- **`setup.cfg`**: Flake8, MyPy, Coverage settings
- **`.pre-commit-config.yaml`**: Pre-commit hooks configuration
- **`Makefile`**: Development automation commands
- **`.github/workflows/push.yml`**: CI/CD pipeline
- **`requirements.txt`**: Python dependencies
- **`compose.yaml`**: Docker Compose configuration
- **`Dockerfile`**: Production container configuration

## 📝 API Documentation

API structure and endpoints are documented in `openapi.yaml` following OpenAPI 3.0 specification.

### Main Endpoint

```
GET /api/v1/calculations/?symbol=<SYMBOL>&investment=<AMOUNT>
```

Parameters:
- `symbol`: Cryptocurrency symbol (e.g., BTC, ETH)
- `investment`: Investment amount in USD

### API Documentation

- **Swagger UI**: `http://localhost:8000/api/docs/`
- **OpenAPI Schema**: `http://localhost:8000/api/schema/`
- **Health Check**: `http://localhost:8000/api/v1/health/`

## 🏗 Architecture

See `Architecture.png` for the enterprise-ready system architecture using GCP components.

### Build Pipeline

See `BuildPipeline.png` for the CI/CD pipeline visualization.

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Ensure all tests pass: `make test`
4. Ensure code quality: `make lint`
5. Run pre-deployment checks: `make pre-deploy`
6. Submit a pull request

### Code Standards

- Follow PEP 8 style guide
- Use Black for formatting (line length: 88)
- Add type hints to all functions
- Write tests for new features
- Maintain 80%+ code coverage

## 🐛 Troubleshooting

### Pre-commit Hooks Failing

```bash
# Update pre-commit hooks
pre-commit autoupdate

# Run manually to see errors
pre-commit run --all-files
```

### Tests Failing

```bash
# Run with verbose output
cd Core
pytest -vv --tb=long

# Run specific test
pytest tests/unit/test_models.py::TestResultsModel::test_create_result -v
```

### Import Errors

```bash
# Ensure you're in the virtual environment
python --version  # Should show 3.10+
pip list  # Check installed packages

# Reinstall dependencies
make clean
make install-dev
```

### Docker Issues

```bash
# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Check logs
docker-compose logs -f web
```

## 📄 License

[Add your license here]

## 👥 Authors

[Add your name/team here]

## 🙏 Acknowledgments

- Django REST Framework
- Pytest
- GitHub Actions
- All open-source contributors

---

**Made with ❤️ by the Development Team**

