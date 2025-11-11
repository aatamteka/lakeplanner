# Notification Service - Claude Code Context

## Service Overview
JMS-based messaging service for the lake recreation platform. Integrates with Twilio and SMTP to send messages to members.

## Tech Stack
- **Messaging**: RabbitMQ (aio-pika)
- **Server**: Uvicorn 0.27.0

## Project Structure
```
notification-service/
├── app/
│   ├── models/           # SQLAlchemy models
│   ├── messaging/        # RabbitMQ handlers
│   └── main.py          # App entry point
├── scripts/             # Utility scripts
└── tests/               # Test suite
```

## Key Commands

### Development
```bash
# Start service (Docker - recommended)
docker-compose up -d

# Local development with hot reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

# Production mode
python -m app.main
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
curl http://localhost:8001/health

# API documentation
# Swagger: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

## RabbitMQ Topics
- `audit.*` - Audit event logging
- `outing.created` - Contention recalculation
- `weather.alert` - Weather alerts for outings

## Environment Configuration
Copy `.env.sample` to `.env`. Default values work with infrastructure services.

## Dependencies
Infrastructure services required (see `../../infra/README.md`):
- PostgreSQL with PostGIS
- RabbitMQ

## Code Style
- Follow existing patterns in codebase
- Type hints with Pydantic models
