from sqlalchemy import Column, String, Date, ForeignKey, Text, ARRAY
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from .base import Base, UUIDMixin, TimestampMixin


class Outing(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "outings"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    lake_id = Column(UUID(as_uuid=True), ForeignKey("lakes.id", ondelete="CASCADE"), nullable=False, index=True)
    planned_date = Column(Date, nullable=False, index=True)
    time_slot = Column(String(20), nullable=False, index=True)
    target_amenities = Column(ARRAY(UUID(as_uuid=True)), nullable=True)
    invited_friends = Column(ARRAY(UUID(as_uuid=True)), nullable=True)
    rsvp_status = Column(JSONB, nullable=True)
    notes = Column(Text, nullable=True)

    user = relationship("User", back_populates="outings")
    lake = relationship("Lake", back_populates="outings")
