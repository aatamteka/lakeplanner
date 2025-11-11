from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.core import get_db
from app.models import BoatRamp

router = APIRouter()


@router.get("/", response_model=List[dict])
def list_boat_ramps(
    lake_id: Optional[UUID] = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(BoatRamp)

    if lake_id:
        query = query.filter(BoatRamp.lake_id == lake_id)

    ramps = query.offset(skip).limit(limit).all()
    return [
        {
            "id": str(ramp.id),
            "lake_id": str(ramp.lake_id),
            "name": ramp.name,
            "latitude": float(ramp.latitude),
            "longitude": float(ramp.longitude),
            "is_active": ramp.is_active,
        }
        for ramp in ramps
    ]


@router.get("/{ramp_id}", response_model=dict)
def get_boat_ramp(ramp_id: UUID, db: Session = Depends(get_db)):
    ramp = db.query(BoatRamp).filter(BoatRamp.id == ramp_id).first()
    if not ramp:
        raise HTTPException(status_code=404, detail="Boat ramp not found")
    return {
        "id": str(ramp.id),
        "lake_id": str(ramp.lake_id),
        "name": ramp.name,
        "latitude": float(ramp.latitude),
        "longitude": float(ramp.longitude),
        "hours_of_operation": ramp.hours_of_operation,
        "seasonal_availability": ramp.seasonal_availability,
        "is_active": ramp.is_active,
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
                        "name": "Boone Lake Main Ramp",
                        "latitude": 36.447359,
                        "longitude": -82.428104,
                        "hours_of_operation": {
                            "weekday": "6:00 AM - 10:00 PM",
                            "weekend": "5:00 AM - 11:00 PM"
                        },
                        "seasonal_availability": {
                            "open_season": "March - November"
                        },
                        "is_active": True
                    }
                }
            }
        }
    }
)
def create_boat_ramp(ramp_data: dict, db: Session = Depends(get_db)):
    ramp = BoatRamp(**ramp_data)
    db.add(ramp)
    db.commit()
    db.refresh(ramp)
    return {"id": str(ramp.id), "name": ramp.name}


@router.delete("/{ramp_id}", status_code=204)
def delete_boat_ramp(ramp_id: UUID, db: Session = Depends(get_db)):
    ramp = db.query(BoatRamp).filter(BoatRamp.id == ramp_id).first()
    if not ramp:
        raise HTTPException(status_code=404, detail="Boat ramp not found")

    db.delete(ramp)
    db.commit()
    return None
