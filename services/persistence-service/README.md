# Persistence Service

The persistence service manages all data storage and retrieval for the lake recreation platform. It provides both REST APIs and RabbitMQ message handling for data operations.

## Features

- **SQLAlchemy ORM**: Type-safe database models with relationships
- **Alembic Migrations**: Version-controlled schema management
- **FastAPI REST APIs**: High-performance async HTTP endpoints
- **RabbitMQ Integration**: Event-driven architecture for audit logging and inter-service communication
- **PostGIS Support**: Spatial queries for lake boundaries, amenities, and locations
- **Health Checks**: Service status monitoring
- **Metrics Endpoint**: Prometheus-compatible metrics (placeholder)

## Architecture

### Data Models

- **User**: User accounts, preferences, and authentication
- **Lake**: Lake metadata and GIS boundaries
- **Amenity**: Lake amenities (rope swings, picnic areas, fishing spots)
- **BoatRamp**: Boat launch locations
- **Marina**: Marina locations and rental inventory
- **Outing**: User-planned lake outings
- **AmenityContention**: Tracks crowding at amenities
- **Friendship**: User friend networks
- **WeatherForecast**: Cached weather data
- **AuditLog**: Event audit trail

### REST API Endpoints

All endpoints are prefixed with `/api/v1`:

- `GET /users/` - List users
- `GET /users/{user_id}` - Get user details
- `POST /users/` - Create user
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user

- `GET /lakes/` - List lakes
- `GET /lakes/{lake_id}` - Get lake details
- `POST /lakes/` - Create lake
- `PUT /lakes/{lake_id}` - Update lake
- `DELETE /lakes/{lake_id}` - Delete lake

- `GET /amenities/?lake_id=&type=` - List amenities (filterable)
- `GET /amenities/{amenity_id}` - Get amenity details
- `POST /amenities/` - Create amenity
- `DELETE /amenities/{amenity_id}` - Delete amenity

- `GET /outings/?user_id=&lake_id=&start_date=` - List outings (filterable)
- `GET /outings/{outing_id}` - Get outing details
- `POST /outings/` - Create outing
- `DELETE /outings/{outing_id}` - Delete outing

### RabbitMQ Message Handlers

The service subscribes to the following topics:

- `audit.*` - Audit events logged to database
- `outing.created` - Triggers amenity contention recalculation
- `weather.alert` - Weather alerts for planned outings

## Setup

### Prerequisites

**Option 1: Docker (Recommended)**
- Docker and Docker Compose
- Infrastructure services running (see `../../infra/README.md`)

**Option 2: Local Development**
- Python 3.11+
- PostgreSQL with PostGIS extension
- RabbitMQ
- Virtual environment (recommended)

### Installation

#### Docker Deployment (Recommended)

1. **Start infrastructure services first:**
   ```bash
   cd ../../infra
   docker-compose up -d
   ```

2. **Configure environment:**
   ```bash
   cd ../services/persistence-service
   cp .env.sample .env
   # Edit .env if needed (default values work with infrastructure)
   ```

3. **Build and start the service:**
   ```bash
   docker-compose up -d
   ```

4. **Run database migrations:**
   ```bash
   # Enter the container
   docker-compose exec persistence-service bash

   # Generate and apply migrations
   alembic revision --autogenerate -m "Initial schema"
   alembic upgrade head
   exit
   ```

5. **Verify service is running:**
   ```bash
   curl http://localhost:8000/health
   ```

#### Local Development

1. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment:
   ```bash
   cp .env.sample .env
   # Edit .env with your database and RabbitMQ credentials
   ```

4. Initialize database with Alembic:
   ```bash
   # Create initial migration
   alembic revision --autogenerate -m "Initial schema"

   # Apply migrations
   alembic upgrade head
   ```

### Running the Service

**With Docker:**
```bash
docker-compose up -d
```

**Development mode (local):**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Production mode (local):**
```bash
python -m app.main
```

## Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migration:
```bash
alembic downgrade -1
```

View migration history:
```bash
alembic history
```

## Testing

Run tests (when implemented):
```bash
pytest tests/
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Health Check

```bash
curl http://localhost:8000/health
```

## Development

### Adding New Models

1. Create model in `app/models/`
2. Import in `app/models/__init__.py`
3. Generate migration: `alembic revision --autogenerate -m "Add model"`
4. Apply migration: `alembic upgrade head`

### Adding New Endpoints

1. Create router in `app/api/`
2. Register in `app/api/__init__.py`
3. Test with `/docs` interactive API

### Adding Message Handlers

1. Create handler in `app/messaging/handlers.py`
2. Subscribe in `app/main.py` lifespan function

## RabbitMQ Command Line Testing

### Publishing Audit Events from Command Line

Install RabbitMQ tools:
```bash
pip install pika
```

Publish a sample audit event using Python:
```bash
python3 << 'EOF'
import pika
import json

connection = pika.BlockingConnection(pika.URLParameters('amqp://admin:admin@localhost:5672/'))
channel = connection.channel()

user_id = "e2164d9b-389c-48c5-9d3f-05a72301fef7"
audit_event = {
    "event_type": "user.created",
    "user_id": user_id,
    "entity_type": "user",
    "entity_id": user_id,
    "payload": {"username": "hsimpson", "email": "homer@example.com","ip": "10.0.0.1"}
}

channel.basic_publish(
    exchange='lake_platform_events',
    routing_key='audit.user',
    body=json.dumps(audit_event)
)

print(f"Published audit event: {audit_event}")
connection.close()
EOF
```

### Consuming Messages from Command Line

Consume messages from the audit queue:
```bash
python3 << 'EOF'
import pika

def callback(ch, method, properties, body):
    print(f"Received: {body.decode()}")

connection = pika.BlockingConnection(pika.URLParameters('amqp://admin:admin@localhost:5672/'))
channel = connection.channel()

channel.queue_declare(queue='audit.user')
channel.basic_consume(queue='audit.user', on_message_callback=callback, auto_ack=True)

print('Waiting for messages. Press CTRL+C to exit.')
channel.start_consuming()
EOF
```

### Sample Audit Event Formats

**User Creation:**
```json
{
  "event_type": "user.created",
  "user_id": 123,
  "entity_type": "user",
  "entity_id": 123,
  "payload": {"username": "john_doe", "email": "john@example.com"}
}
```

**Lake Update:**
```json
{
  "event_type": "lake.updated",
  "user_id": 456,
  "entity_type": "lake",
  "entity_id": 789,
  "payload": {"name": "Lake Tahoe", "state": "CA"}
}
```

**Outing Deleted:**
```json
{
  "event_type": "outing.deleted",
  "user_id": 123,
  "entity_type": "outing",
  "entity_id": 456,
  "payload": {"lake_id": 789, "date": "2024-07-15"}
}
```

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- Verify PostGIS extensions installed

### RabbitMQ Connection Issues
- Ensure RabbitMQ is running
- Check RABBITMQ_URL in .env
- Verify credentials match RabbitMQ config

### Migration Issues
- Check alembic.ini database URL matches .env
- Ensure all models imported in models/__init__.py
- Review migration file before applying
