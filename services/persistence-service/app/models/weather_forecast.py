from sqlalchemy import Column, String, Date, Integer, Numeric, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base, UUIDMixin


class WeatherForecast(Base, UUIDMixin):
    __tablename__ = "weather_forecasts"
    __table_args__ = (UniqueConstraint('lake_id', 'forecast_date', name='uq_lake_forecast_date'),)

    lake_id = Column(UUID(as_uuid=True), ForeignKey("lakes.id", ondelete="CASCADE"), nullable=False, index=True)
    forecast_date = Column(Date, nullable=False, index=True)
    temperature_high = Column(Numeric(5, 2), nullable=True)
    temperature_low = Column(Numeric(5, 2), nullable=True)
    precipitation_probability = Column(Integer, nullable=True)
    wind_speed = Column(Numeric(5, 2), nullable=True)
    conditions = Column(String(255), nullable=True)
    raw_data = Column(JSONB, nullable=True)
    fetched_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    lake = relationship("Lake", back_populates="weather_forecasts")
