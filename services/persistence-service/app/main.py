import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.core.config import settings
from app.messaging.rabbitmq import rabbitmq_client
from app.messaging.handlers import handle_audit_event, handle_outing_created, handle_weather_alert

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting persistence service...")
    try:
        await rabbitmq_client.connect()
        await rabbitmq_client.subscribe("audit.*", "persistence_audit_queue", handle_audit_event)
        await rabbitmq_client.subscribe("outing.created", "persistence_outing_queue", handle_outing_created)
        await rabbitmq_client.subscribe("weather.alert", "persistence_weather_queue", handle_weather_alert)
        logger.info("Persistence service started successfully")
    except Exception as e:
        logger.error(f"Failed to start persistence service: {e}")

    yield

    logger.info("Shutting down persistence service...")
    await rabbitmq_client.close()


app = FastAPI(
    title="Lake Platform Persistence Service",
    description="Data persistence and management service for the lake recreation platform",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    openapi_tags=[
        {"name": "users", "description": "User management operations"},
        {"name": "lakes", "description": "Lake data operations"},
        {"name": "amenities", "description": "Lake amenity operations"},
        {"name": "boat-ramps", "description": "Boat ramp operations"},
        {"name": "outings", "description": "Outing planning operations"},
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "persistence"}


@app.get("/metrics")
def metrics():
    return {"message": "Metrics endpoint placeholder"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)
