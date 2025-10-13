<div align="center">

<img src="https://www.edwinkassier.com/Assets/Monogram.png" alt="Ashes Project Monogram" width="80" height="80">

# Ashes Project Django REST API Boilerplate

**A production-ready Django REST API with simplified domain-driven design**

> **Note:** Replace badge placeholders with your repository details

[![codecov](https://codecov.io/gh/YOUR_USERNAME/YOUR_REPO_NAME/branch/master/graph/badge.svg)](https://codecov.io/gh/YOUR_USERNAME/YOUR_REPO_NAME)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Django 5.2+](https://img.shields.io/badge/django-5.2+-green.svg)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/docker-supported-blue.svg)](https://www.docker.com/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## What Is This?

A Django REST API boilerplate designed for rapid development of production-ready web APIs. This template provides:

- ✅ **Simplified Architecture**: 2-app structure (domain + shared) following Django best practices
- ✅ **Complete CI/CD Pipeline**: GitHub Actions with automated testing and deployment
- ✅ **Code Quality Tools**: Black, Flake8, isort, Mypy, pre-commit hooks
- ✅ **Testing Framework**: Pytest with 80%+ coverage target
- ✅ **Security Scanning**: Bandit and Safety integration
- ✅ **Background Tasks**: Celery with Redis for async processing and scheduled jobs
- ✅ **Docker Ready**: Multi-stage builds and compose configuration with Redis, Celery, Beat, Flower
- ✅ **API Documentation**: Auto-generated OpenAPI/Swagger docs
- ✅ **Example Implementation**: Cryptocurrency portfolio app demonstrating the architecture

### Important Note

**This boilerplate includes a complete example application** (cryptocurrency portfolio calculator) to demonstrate the architecture in action. **You should replace this example with your own domain logic** - see [Customizing This Boilerplate](#customizing-this-boilerplate).

---

## Quick Start

Get up and running in 5 minutes.

### Prerequisites

- Python 3.10+
- pip or Pipenv
- Git

### Setup

```bash
# 1. Clone repository
git clone <repository-url>
cd dwml-backend-django

# 2. Install dependencies and setup development environment
make install-dev

# 3. Configure environment
cp env.example .env
# Edit .env and set your SECRET_KEY (generate with: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')

# 4. Run migrations
make migrate

# 5. Start development server
make runserver
```

The API will be available at:
- **Main API**: http://localhost:8000/api/
- **API Docs**: http://localhost:8000/api/docs/
- **Health Check**: http://localhost:8000/api/health/

### Test the Example App

```bash
# Test health endpoint
curl http://localhost:8000/api/health/

# Test example endpoint (cryptocurrency portfolio - replace with your own)
curl "http://localhost:8000/api/process_request/?symbol=BTC&investment=1000"
```

---

## Customizing This Boilerplate

The included cryptocurrency portfolio app is just an example. Here's how to replace it with your own domain logic:

### Step 1: Define Your Domain Models

```bash
# Open backend/domain/models.py
# Replace these example models:
# - PortfolioResult
# - PortfolioLog  
# - OpeningAverage
# - MarketPrice
# - Prediction
# - AnalysisReport

# With your own models, for example:
# - Task
# - Project
# - User
# - etc.
```

After updating models:
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

### Step 2: Update Business Logic (Services)

```bash
# Open backend/domain/services.py
# Replace example services:
# - PortfolioService
# - MarketDataService
# - CalculatorService
# - AnalyticsService
# - CovidAnalyzerService

# With your own business logic services
```

### Step 3: Update Background Tasks

```bash
# Open backend/domain/tasks.py
# Replace example tasks with your own:
# - process_portfolio_async → your_async_task
# - fetch_market_prices_task → your_scheduled_task
# - cleanup_old_data_task → your_maintenance_task

# Remember: Tasks should wrap services, not duplicate business logic
# Example pattern:
#   @shared_task(name='domain.my_task')
#   def my_task(params):
#       service = MyService()
#       return service.do_something(params)
```

### Step 4: Create Your API Endpoints

```bash
# Open backend/domain/views.py
# Replace example endpoints:
# - process_request (cryptocurrency calculator)
# - result_list, result_detail
# - current_price, opening_average, price_history
# - covid_prediction, analytics_report

# With your own API views

# Keep the generic endpoints:
# - health_check (useful for load balancers)
```

### Step 5: Update Serializers

```bash
# Open backend/domain/serializers.py
# Create serializers for your models
# Replace the example serializers:
# - PortfolioResultSerializer
# - CalculationRequestSerializer
# - etc.
```

### Step 6: Update URL Routing

```bash
# Open backend/domain/urls.py
# Update URL patterns to match your new endpoints
```

### Step 7: Rename Project References

```bash
# Search and replace throughout the project:
# - "dwml-backend" → "your-project-name"
# - Update backend/domain/views.py health_check endpoint
# - Update any project-specific references
```

### Step 8: Update Tests

```bash
# Delete example tests:
# - tests/unit/test_models.py (crypto-specific)
# - tests/unit/test_serializers.py (crypto-specific)
# - tests/integration/test_api_endpoints.py (crypto-specific)

# Write new tests for your domain logic
# Keep the test structure and pytest configuration
```

### Step 9: Update Documentation

```bash
# Update this README.md with your project details
# Update openapi.yaml with your API specification
# Remove or update docs/Django_Tutorial.md
```

---

## Project Structure

### Simplified Codebase Architecture

```
dwml-backend-django/
├── backend/
│   ├── domain/                 # YOUR BUSINESS LOGIC GOES HERE
│   │   ├── models.py           # Database models
│   │   ├── services.py         # Business logic layer (sync)
│   │   ├── tasks.py            # Background tasks (async)
│   │   ├── views.py            # API endpoints
│   │   ├── serializers.py      # Request/response serialization
│   │   ├── urls.py             # URL routing
│   │   └── migrations/         # Database migrations
│   ├── shared/                 # Shared utilities (keep these)
│   │   ├── exceptions/         # Custom exceptions
│   │   └── middleware.py       # Exception handling middleware
│   └── config/                 # Django configuration
│       ├── settings.py         # Django settings
│       ├── celery.py           # Celery configuration
│       ├── urls.py             # Root URL configuration
│       └── wsgi.py / asgi.py   # Server entry points
├── tests/
│   ├── unit/                   # Unit tests
│   └── integration/            # Integration tests
├── Dockerfile                  # Container configuration
├── compose.yaml                # Docker Compose (Django, Redis, Celery, Beat, Flower)
├── Makefile                    # Development commands
└── requirements.txt            # Python dependencies
```

### Architecture Design

**Why Simplified 2-App Structure?**

- ✅ **Django-Idiomatic**: Follows Django conventions, not over-engineered
- ✅ **Easy to Understand**: All business logic in one place
- ✅ **Fast Development**: Less boilerplate, more productivity
- ✅ **Still Scalable**: Add more apps when truly needed

**What Goes Where?**

- **`domain/` app**: All your business-specific code
  - `models.py` - Domain entities with behavior
  - `services.py` - Business logic (synchronous)
  - `tasks.py` - Background tasks (asynchronous wrappers around services)
  - `views.py` - API endpoints
  - `serializers.py` - Request/response handling
- **`shared/` app**: Cross-cutting concerns used across domains (exceptions, middleware, utilities)
- **`config/` folder**: Infrastructure configuration (Django settings, Celery config, server entry points)

---

## Development

### Available Commands

| Command | Purpose |
|:--------|:--------|
| `make install` | Install production dependencies |
| `make install-dev` | Install dev dependencies and setup pre-commit hooks |
| `make test` | Run all tests with coverage |
| `make test-unit` | Run unit tests only |
| `make test-integration` | Run integration tests only |
| `make coverage` | Generate detailed coverage report |
| `make lint` | Run all linting checks (Flake8, Black, isort, Mypy) |
| `make format` | Auto-format code with Black and isort |
| `make security-check` | Run security scans (Bandit, Safety) |
| `make migrate` | Run Django database migrations |
| `make runserver` | Start Django development server |
| `make pre-deploy` | Run all checks before deployment |
| `make clean` | Clean temporary files and caches |
| `make help` | Show all available commands |

### Code Quality Tools

This boilerplate includes pre-configured code quality tools:

- **Black**: Code formatting (line length: 88)
- **isort**: Import sorting
- **Flake8**: Linting and style checking
- **Mypy**: Static type checking
- **Pre-commit hooks**: Automatic checks before each commit

Install pre-commit hooks:
```bash
make install-dev  # Installs hooks automatically
```

Run checks manually:
```bash
make format  # Format code
make lint    # Check code quality
```

### Testing

Run tests with coverage:
```bash
make test              # All tests with coverage
make test-unit         # Unit tests only
make test-integration  # Integration tests only
make coverage          # Generate HTML coverage report
```

**Coverage Goals:**
- Overall: 80%+
- Critical modules: 90%+
- New code: 90%+

### Security

Run security scans:
```bash
make security-check
```

This runs:
- **Bandit**: Security vulnerability scanning
- **Safety**: Dependency vulnerability checking

### Background Tasks (Celery)

This boilerplate includes **Celery** for background task processing with Redis as the message broker.

**Use Cases:**
- Asynchronous API operations (long-running calculations)
- Scheduled tasks (data cleanup, report generation)
- Periodic data fetching (market prices, external APIs)
- Batch processing operations

**Quick Start with Docker:**
```bash
# Start all services (Django, Redis, Celery, Beat, Flower)
make docker-up

# View Celery worker logs
docker-compose logs -f celery

# Access Flower monitoring UI
open http://localhost:5555
```

**Create a Background Task:**

Tasks are placed in `backend/domain/tasks.py` and should wrap domain services:

```python
from celery import shared_task
from .services import PortfolioService

@shared_task(name='domain.my_task')
def my_task(symbol: str, investment: float):
    """Background task wrapping domain service."""
    service = PortfolioService()
    result = service.process_request(symbol, investment)
    return result.id
```

**Call Task from View:**

```python
from .tasks import my_task

@api_view(['POST'])
def my_view(request):
    # Execute asynchronously
    task = my_task.delay(
        symbol=request.data['symbol'],
        investment=request.data['investment']
    )
    return Response({'task_id': task.task_id})
```

**Schedule Periodic Tasks:**

1. Run migrations: `docker-compose exec web python manage.py migrate`
2. Access admin: http://localhost:8080/admin/
3. Go to **Periodic Tasks** → **Add**
4. Configure task name, schedule, and enable

**Available Services:**
- **Redis** (port 6379): Message broker and result backend
- **Celery Worker**: Processes background tasks
- **Celery Beat**: Schedules periodic tasks
- **Flower** (port 5555): Web-based monitoring and management

**Local Development (without Docker):**

```bash
# Terminal 1: Start Redis
brew install redis && brew services start redis

# Terminal 2: Start Django
make runserver

# Terminal 3: Start Celery worker
make celery-worker

# Terminal 4: Start Celery beat (optional)
make celery-beat

# Terminal 5: Start Flower (optional)
make celery-flower
```

**Useful Commands:**
- `make celery-worker` - Start worker locally
- `make celery-beat` - Start scheduler locally
- `make celery-flower` - Start monitoring UI locally
- `make celery-purge` - Clear all pending tasks
- `make redis-cli` - Access Redis CLI

See `CELERY_QUICKSTART.md` for detailed documentation.

---

## Docker

### Using Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f web

# Stop services
docker-compose down

# Rebuild after changes
docker-compose build --no-cache
docker-compose up -d
```

### Building Docker Image

```bash
# Build image
docker build -t your-project-name .

# Run container
docker run -p 8000:8000 your-project-name
```

---

## CI/CD Pipeline

### Automated Pipeline

The boilerplate includes a complete GitHub Actions CI/CD pipeline:

**On Every Push/PR:**
1. ✅ Code quality checks (Black, Flake8, isort, Mypy)
2. ✅ Security scanning (Bandit, Safety)
3. ✅ Test suite with coverage reporting
4. ✅ Coverage upload to Codecov

**On Production Tag (`prod/v*`):**
1. ✅ All quality checks
2. ✅ Docker image build
3. ✅ Push to container registry
4. ✅ Deploy to cloud (configure for your platform)
5. ✅ Health check verification

### Deployment

To deploy to production:

```bash
# Using the release script
./scripts/create-prod-release.sh 1.0.0

# Or manually
git tag -a prod/v1.0.0 -m "Release v1.0.0"
git push origin prod/v1.0.0
```

**Tag Format:** `prod/vMAJOR.MINOR.PATCH` (e.g., `prod/v1.0.0`, `prod/v2.1.3`)

### Configuring Deployment

Update `.github/workflows/` files to configure deployment for your cloud provider:
- Google Cloud Run
- AWS ECS
- Azure Container Instances
- Heroku
- Your own infrastructure

---

## API Documentation

### Interactive Documentation

Once running, visit:

- **Swagger UI**: http://localhost:8000/api/docs/ - Interactive API testing
- **OpenAPI Schema**: http://localhost:8000/api/schema/ - Machine-readable spec

### Example API Endpoints (Replace These)

The included example app provides these endpoints:

| Endpoint | Method | Purpose | Status |
|:---------|:-------|:--------|:-------|
| `/api/process_request/` | GET, POST | Portfolio calculation | **Example - Replace** |
| `/api/results/` | GET | List portfolio results | **Example - Replace** |
| `/api/results/<id>/` | GET | Get specific result | **Example - Replace** |
| `/api/logs/` | GET | Audit logs | **Example - Replace** |
| `/api/price/current/` | GET | Current crypto price | **Example - Replace** |
| `/api/analytics/covid/` | GET | COVID impact analysis | **Example - Replace** |

### Generic Endpoints (Keep These)

| Endpoint | Method | Purpose |
|:---------|:-------|:--------|
| `/api/health/` | GET | Health check for load balancers |
| `/api/docs/` | GET | Interactive API documentation |
| `/api/schema/` | GET | OpenAPI schema |
| `/metrics/` | GET | Prometheus metrics (if configured) |

---

## Environment Configuration

### Required Environment Variables

Copy `env.example` to `.env` and configure:

| Variable | Purpose | Example |
|:---------|:--------|:--------|
| `SECRET_KEY` | Django secret key | Generate: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` |
| `DEBUG` | Debug mode | `True` (development) / `False` (production) |
| `ALLOWED_HOSTS` | Allowed hostnames | `localhost,127.0.0.1` (dev) / `yourdomain.com` (prod) |
| `DATABASE_URL` | Database connection | `sqlite:///db.sqlite3` (dev) / `postgresql://...` (prod) |

See `env.example` for all available configuration options.

---

## Troubleshooting

### Common Issues

**Pre-commit hooks failing:**
```bash
# Update hooks
pre-commit autoupdate

# Run manually to see errors
pre-commit run --all-files

# Skip hooks temporarily (not recommended)
git commit --no-verify -m "message"
```

**Tests failing:**
```bash
# Run with verbose output
cd backend
pytest -vv --tb=long

# Run specific test
pytest tests/unit/test_models.py::TestClass::test_method -v
```

**Docker issues:**
```bash
# Rebuild from scratch
docker-compose down -v
docker system prune -a
docker-compose build --no-cache
docker-compose up -d
```

**Import errors:**
```bash
# Check Python version
python --version  # Should be 3.10+

# Reinstall dependencies
make clean
make install-dev
```

**Database issues:**
```bash
# Reset database (WARNING: deletes all data)
rm backend/db.sqlite3
make migrate
```

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Run quality checks (`make format && make lint && make test`)
5. Commit your changes (`git commit -m "Add feature"`)
6. Push to your fork (`git push origin feature/your-feature`)
7. Create a Pull Request

### Code Standards

- Follow PEP 8 style guide
- Use type hints for all functions
- Write tests for new features (80%+ coverage)
- Format with Black (line length: 88)
- Add docstrings to public functions
- Update documentation as needed

---

## Additional Resources

### Documentation

- `docs/Django_Tutorial.md` - Django development guide
- `docs/Architecture.png` - Architecture diagram
- `docs/BuildPipeline.png` - CI/CD pipeline diagram

### Related Projects

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Twelve-Factor App](https://12factor.net/)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
