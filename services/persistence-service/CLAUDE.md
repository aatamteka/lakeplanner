# Persistence Service - Claude Code Context

## Service Overview
FastAPI-based persistence layer for lake recreation platform. Manages data storage with REST APIs and RabbitMQ message handling.

## Tech Stack
- **Framework**: FastAPI 0.109.0
- **ORM**: SQLAlchemy 2.0.25
- **Migrations**: Alembic 1.13.1
- **Database**: PostgreSQL with PostGIS
- **Messaging**: RabbitMQ (aio-pika)
- **Server**: Uvicorn 0.27.0

## Project Structure
```
persistence-service/
├── app/
│   ├── api/              # REST endpoint routers
│   ├── models/           # SQLAlchemy models
│   ├── messaging/        # RabbitMQ handlers
│   └── main.py          # FastAPI app entry point
├── alembic/             # Database migrations
├── scripts/             # Utility scripts
└── tests/               # Test suite
```

## Key Commands

### Development
```bash
# Start service (Docker - recommended)
docker-compose up -d

# Local development with hot reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
python -m app.main
```

### Database Migrations
```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1

# View history
alembic history
```

### Testing
```bash
# Run tests
pytest tests/

# Integration tests
python scripts/test_integration.py
```

### Health & Monitoring
```bash
# Health check
curl http://localhost:8000/health

# API documentation
# Swagger: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

## Data Models
- **User**: Accounts and preferences
- **Lake**: Metadata and GIS boundaries
- **Amenity**: Lake amenities (rope swings, fishing spots, etc.)
- **BoatRamp**: Boat launch locations
- **Marina**: Marina locations and rentals
- **Outing**: User-planned outings
- **AmenityContention**: Crowding tracking
- **Friendship**: User networks
- **WeatherForecast**: Cached weather
- **AuditLog**: Event audit trail

## API Endpoints
Base path: `/api/v1`

- **Users**: GET, POST `/users/`, GET, PUT, DELETE `/users/{id}`
- **Lakes**: GET, POST `/lakes/`, GET, PUT, DELETE `/lakes/{id}`
- **Amenities**: GET (filterable), POST `/amenities/`, GET, DELETE `/amenities/{id}`
- **Outings**: GET (filterable), POST `/outings/`, GET, DELETE `/outings/{id}`

## RabbitMQ Topics
- `audit.*` - Audit event logging
- `outing.created` - Contention recalculation
- `weather.alert` - Weather alerts for outings

## Development Workflow

### Adding Models
1. Create in `app/models/`
2. Import in `app/models/__init__.py`
3. Generate migration: `alembic revision --autogenerate -m "Add model"`
4. Apply: `alembic upgrade head`

### Adding Endpoints
1. Create router in `app/api/`
2. Register in `app/api/__init__.py`
3. Test at `/docs`

### Adding Message Handlers
1. Create handler in `app/messaging/handlers.py`
2. Subscribe in `app/main.py` lifespan

## Environment Configuration
Copy `.env.sample` to `.env`. Default values work with infrastructure services.

## Dependencies
Infrastructure services required (see `../../infra/README.md`):
- PostgreSQL with PostGIS
- RabbitMQ

## Code Style
- Follow existing patterns in codebase
- Use SQLAlchemy ORM for database operations
- Async/await for all API endpoints
- Type hints with Pydantic models
