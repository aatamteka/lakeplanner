from sqlalchemy import Column, String, Integer, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from .base import Base, UUIDMixin, TimestampMixin


class Amenity(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "amenities"

    lake_id = Column(UUID(as_uuid=True), ForeignKey("lakes.id", ondelete="CASCADE"), nullable=False, index=True)
    type = Column(String(50), nullable=False, index=True)
    name = Column(String(255), nullable=True)
    latitude = Column(Numeric(10, 8), nullable=False)
    longitude = Column(Numeric(11, 8), nullable=False)
    capacity_score = Column(Integer, default=10)
    hours_of_operation = Column(JSONB, nullable=True)
    seasonal_availability = Column(JSONB, nullable=True)

    lake = relationship("Lake", back_populates="amenities")
    contention_records = relationship("AmenityContention", back_populates="amenity", cascade="all, delete-orphan")
