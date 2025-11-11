from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.core import get_db
from app.models import Amenity

router = APIRouter()


@router.get("/", response_model=List[dict])
def list_amenities(
    lake_id: Optional[UUID] = Query(None),
    amenity_type: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(Amenity)

    if lake_id:
        query = query.filter(Amenity.lake_id == lake_id)
    if amenity_type:
        query = query.filter(Amenity.type == amenity_type)

    amenities = query.offset(skip).limit(limit).all()
    return [
        {
            "id": str(amenity.id),
            "lake_id": str(amenity.lake_id),
            "type": amenity.type,
            "name": amenity.name,
            "latitude": float(amenity.latitude),
            "longitude": float(amenity.longitude),
            "capacity_score": amenity.capacity_score,
        }
        for amenity in amenities
    ]


@router.get("/{amenity_id}", response_model=dict)
def get_amenity(amenity_id: UUID, db: Session = Depends(get_db)):
    amenity = db.query(Amenity).filter(Amenity.id == amenity_id).first()
    if not amenity:
        raise HTTPException(status_code=404, detail="Amenity not found")
    return {
        "id": str(amenity.id),
        "lake_id": str(amenity.lake_id),
        "type": amenity.type,
        "name": amenity.name,
        "latitude": float(amenity.latitude),
        "longitude": float(amenity.longitude),
        "capacity_score": amenity.capacity_score,
        "hours_of_operation": amenity.hours_of_operation,
    }


@router.post(
    "/",
    response_model=dict,
    status_code=201,
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "example": {
                        "lake_id": "00000000-0000-0000-0000-000000000000",
                        "type": "rope_swing",
                        "name": "Boone Lake Rope Swing",
                        "latitude": 36.433912,
                        "longitude": -82.397390,
                        "capacity_score": 15,
                        "hours_of_operation": {
                            "open": "sunrise",
                            "close": "sunset"
                        }
                    }
                }
            }
        }
    }
)
def create_amenity(amenity_data: dict, db: Session = Depends(get_db)):
    amenity = Amenity(**amenity_data)
    db.add(amenity)
    db.commit()
    db.refresh(amenity)
    return {"id": str(amenity.id), "type": amenity.type, "name": amenity.name}


@router.delete("/{amenity_id}", status_code=204)
def delete_amenity(amenity_id: UUID, db: Session = Depends(get_db)):
    amenity = db.query(Amenity).filter(Amenity.id == amenity_id).first()
    if not amenity:
        raise HTTPException(status_code=404, detail="Amenity not found")

    db.delete(amenity)
    db.commit()
    return None
