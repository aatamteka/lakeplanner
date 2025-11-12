# Lake Planner Platform

A microservices-based platform for planning lake recreation activities with friends, featuring intelligent recommendations, weather integration, and amenity contention coordination.

## Project Structure

This project follows a microservices architecture with clear separation of concerns:

```
lakeplanner/
├── services/              # Microservices directory
│   ├── persistence-service/    # Data storage and REST APIs
│   ├── notification-service/   # Notification handling
│   └── [future-services]/      # Additional services as needed
├── infra/                # Infrastructure services (Docker Compose)
│   ├── docker-compose.yml      # PostgreSQL, RabbitMQ, Redis, etc.
│   ├── postgres/               # Database initialization
│   ├── prometheus/             # Metrics collection
│   └── grafana/                # Metrics visualization
├── docs/                 # Project documentation
│   ├── PRD.md                  # Product Requirements Document
│   ├── architecture.md        # Architecture documentation
│   ├── epics.md                # Epic and story breakdown
│   └── technical/              # Technical specifications
└── .bmad-ephemeral/      # Development tracking files
    ├── sprint-status.yaml      # Story tracking
    └── stories/                # Story markdown files
```

## Architecture

### Microservices Pattern

Each service in `services/` follows a consistent structure:

```
service-name/
├── app/                  # Application code
│   ├── api/              # REST API endpoints
│   ├── core/             # Core configuration and utilities
│   ├── models/           # Data models (SQLAlchemy)
│   └── main.py           # FastAPI application entry point
├── alembic/              # Database migrations (if applicable)
├── Dockerfile            # Service container definition
├── docker-compose.yml    # Service-specific compose config
├── requirements.txt      # Python dependencies
└── README.md             # Service-specific documentation
```

### Infrastructure Services

Infrastructure services (database, message bus, cache) are managed via `infra/docker-compose.yml`:

- **PostgreSQL with PostGIS**: Spatial data storage
- **RabbitMQ**: Message bus for event-driven communication
- **Redis**: Caching layer
- **Prometheus** (optional): Metrics collection
- **Grafana** (optional): Metrics visualization

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- Git

### Setup

1. **Start infrastructure services:**
   ```bash
   cd infra
   docker-compose up -d
   ```

2. **Start a service (example: persistence-service):**
   ```bash
   cd services/persistence-service
   cp .env.example .env  # If .env.example exists
   docker-compose up -d
   ```

3. **Verify services are running:**
   ```bash
   # Check infrastructure
   docker ps | grep lake-platform
   
   # Check service health
   curl http://localhost:8000/health
   ```

### Local Development

For local development without Docker:

1. **Set up Python environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install service dependencies:**
   ```bash
   cd services/persistence-service
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run the service:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Development Workflow

### Adding a New Service

1. **Create service directory:**
   ```bash
   mkdir -p services/new-service-name/app
   ```

2. **Copy templates:**
   - Use `Dockerfile.template` (if available) or reference existing service Dockerfile
   - Use `requirements.txt.template` (if available) or create from scratch
   - Reference `docker-compose.yml` from existing service

3. **Set up FastAPI application:**
   - Create `app/main.py` with FastAPI app
   - Create `app/core/config.py` for configuration
   - Add API routers in `app/api/`

4. **Configure service:**
   - Create `docker-compose.yml` referencing `lake-platform` network
   - Create `README.md` with service-specific documentation
   - Add `.env.example` if needed

5. **Test locally:**
   ```bash
   cd services/new-service-name
   docker-compose up -d
   ```

### Code Quality

- **Pre-commit hooks**: Run `pre-commit install` to set up git hooks
- **Linting**: Follow Python PEP 8 style guide
- **Type hints**: Use type hints for better code clarity
- **Testing**: Write unit and integration tests for new features

### Database Migrations

For services using Alembic:

```bash
cd services/service-name
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

## Environment Variables

Each service may require specific environment variables. See service-specific README files for details.

Common variables:
- `DATABASE_URL`: PostgreSQL connection string
- `RABBITMQ_URL`: RabbitMQ connection string
- `REDIS_URL`: Redis connection string
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

## API Documentation

Service APIs are documented via Swagger/OpenAPI:

- **Persistence Service**: http://localhost:8000/docs
- **Other Services**: Check service-specific README

## Testing

Run tests for a specific service:

```bash
cd services/service-name
pytest tests/
```

## Monitoring

- **Prometheus**: http://localhost:9090 (if enabled)
- **Grafana**: http://localhost:3000 (if enabled)
- **RabbitMQ Management**: http://localhost:15672

## Contributing

1. Create a feature branch
2. Make your changes
3. Write/update tests
4. Ensure all tests pass
5. Submit a pull request

## License

[Add license information]

## Support

For questions or issues, please refer to:
- Service-specific README files in `services/*/README.md`
- Architecture documentation in `docs/architecture.md`
- Product requirements in `docs/PRD.md`

