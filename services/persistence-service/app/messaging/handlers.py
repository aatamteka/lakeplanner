import logging
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import AuditLog
from app.core.database import SessionLocal

logger = logging.getLogger(__name__)


async def handle_audit_event(data: dict):
    db: Session = SessionLocal()
    try:
        audit_log = AuditLog(
            event_type=data.get("event_type"),
            user_id=data.get("user_id"),
            entity_type=data.get("entity_type"),
            entity_id=data.get("entity_id"),
            payload=data.get("payload"),
        )
        db.add(audit_log)
        db.commit()
        logger.info(f"Logged audit event: {data.get('event_type')}")
    except Exception as e:
        logger.error(f"Failed to log audit event: {e}")
        db.rollback()
    finally:
        db.close()


async def handle_outing_created(data: dict):
    logger.info(f"Outing created event received: {data}")


async def handle_weather_alert(data: dict):
    logger.info(f"Weather alert received: {data}")
