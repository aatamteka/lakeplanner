from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from .base import Base, UUIDMixin, TimestampMixin


class User(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "users"

    username = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    preferred_lake_id = Column(UUID(as_uuid=True), nullable=True)
    owns_boat = Column(Boolean, default=False)
    preferred_marina_id = Column(UUID(as_uuid=True), nullable=True)
    schedule_preferences = Column(JSONB, nullable=True)
    weather_preferences = Column(JSONB, nullable=True)
    notification_preferences = Column(JSONB, nullable=True)

    outings = relationship("Outing", back_populates="user", cascade="all, delete-orphan")
    friendships = relationship("Friendship", foreign_keys="Friendship.user_id", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user")
