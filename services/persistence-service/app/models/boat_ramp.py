from sqlalchemy import Column, String, Boolean, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from .base import Base, UUIDMixin, TimestampMixin


class BoatRamp(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "boat_ramps"

    lake_id = Column(UUID(as_uuid=True), ForeignKey("lakes.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    latitude = Column(Numeric(10, 8), nullable=False)
    longitude = Column(Numeric(11, 8), nullable=False)
    hours_of_operation = Column(JSONB, nullable=True)
    seasonal_availability = Column(JSONB, nullable=True)
    is_active = Column(Boolean, default=True)

    lake = relationship("Lake", back_populates="boat_ramps")
