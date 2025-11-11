# Lake Platform Infrastructure

This directory contains the Docker Compose configuration for the lake recreation platform's infrastructure services.

## Services

- **PostgreSQL** (with PostGIS): Main database with spatial extensions
- **RabbitMQ**: Message broker for inter-service communication
- **Redis**: Caching layer for recommendations and weather data
- **Prometheus**: Metrics collection and storage
- **Grafana**: Metrics visualization and dashboarding

## Quick Start

1. Copy the sample environment file:
   ```bash
   cp .env.sample .env
   ```

2. Start all services:
   ```bash
   docker-compose up -d
   ```

3. Verify services are running:
   ```bash
   docker-compose ps
   ```

## Service Access

- **PostgreSQL**: `localhost:5432`
  - Database: `lakeplatform`
  - User: `lakeuser`
  - Password: `lakepass`

- **RabbitMQ Management**: http://localhost:15672
  - User: `admin`
  - Password: `admin`

- **RabbitMQ AMQP**: `localhost:5672`

- **Redis**: `localhost:6379`

- **Prometheus**: http://localhost:9090

- **Grafana**: http://localhost:3000
  - User: `admin`
  - Password: `admin`

## Database Management

The database schema is managed by the persistence service using Alembic migrations. The infrastructure only initializes the PostGIS extensions.

## Stopping Services

Stop all services:
```bash
docker-compose down
```

Stop and remove volumes (WARNING: deletes all data):
```bash
docker-compose down -v
```

## Logs

View logs for all services:
```bash
docker-compose logs -f
```

View logs for a specific service:
```bash
docker-compose logs -f postgres
```

## Troubleshooting

### PostgreSQL Connection Issues
- Ensure the container is running: `docker-compose ps`
- Check logs: `docker-compose logs postgres`
- Test connection: `docker-compose exec postgres psql -U lakeuser -d lakeplatform`

### RabbitMQ Connection Issues
- Check management UI is accessible
- Verify credentials in `.env`
- Check logs: `docker-compose logs rabbitmq`

### Port Conflicts
If ports are already in use, modify the port mappings in `.env` file.
