from sqlalchemy import Column, String, Numeric
from sqlalchemy.orm import relationship
from .base import Base, UUIDMixin, TimestampMixin


class Lake(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "lakes"

    name = Column(String(255), nullable=False, index=True)
    latitude = Column(Numeric(10, 8), nullable=False)
    longitude = Column(Numeric(11, 8), nullable=False)

    amenities = relationship("Amenity", back_populates="lake", cascade="all, delete-orphan")
    boat_ramps = relationship("BoatRamp", back_populates="lake", cascade="all, delete-orphan")
    marinas = relationship("Marina", back_populates="lake", cascade="all, delete-orphan")
    outings = relationship("Outing", back_populates="lake", cascade="all, delete-orphan")
    weather_forecasts = relationship("WeatherForecast", back_populates="lake", cascade="all, delete-orphan")
