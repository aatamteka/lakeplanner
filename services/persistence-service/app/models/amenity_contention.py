from sqlalchemy import Column, String, Date, Integer, Numeric, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base, UUIDMixin


class AmenityContention(Base, UUIDMixin):
    __tablename__ = "amenity_contention"
    __table_args__ = (UniqueConstraint('amenity_id', 'date', 'time_slot', name='uq_amenity_date_time'),)

    amenity_id = Column(UUID(as_uuid=True), ForeignKey("amenities.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    time_slot = Column(String(20), nullable=False)
    planned_groups_count = Column(Integer, default=0)
    contention_score = Column(Numeric(5, 2), default=0.0, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    amenity = relationship("Amenity", back_populates="contention_records")
