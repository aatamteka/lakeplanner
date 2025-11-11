from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core import get_db
from app.models import Lake

router = APIRouter()


@router.get("/", response_model=List[dict])
def list_lakes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    lakes = db.query(Lake).offset(skip).limit(limit).all()
    return [
        {
            "id": str(lake.id),
            "name": lake.name,
            "latitude": float(lake.latitude),
            "longitude": float(lake.longitude),
        }
        for lake in lakes
    ]


@router.get("/{lake_id}", response_model=dict)
def get_lake(lake_id: UUID, db: Session = Depends(get_db)):
    lake = db.query(Lake).filter(Lake.id == lake_id).first()
    if not lake:
        raise HTTPException(status_code=404, detail="Lake not found")
    return {
        "id": str(lake.id),
        "name": lake.name,
        "latitude": float(lake.latitude),
        "longitude": float(lake.longitude),
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
                        "name": "Boone Lake",
                        "latitude": 36.4667,
                        "longitude": -82.4167
                    }
                }
            }
        }
    }
)
def create_lake(lake_data: dict, db: Session = Depends(get_db)):
    lake = Lake(**lake_data)
    db.add(lake)
    db.commit()
    db.refresh(lake)
    return {
        "id": str(lake.id),
        "name": lake.name,
        "latitude": float(lake.latitude),
        "longitude": float(lake.longitude),
    }


@router.put("/{lake_id}", response_model=dict)
def update_lake(lake_id: UUID, lake_data: dict, db: Session = Depends(get_db)):
    lake = db.query(Lake).filter(Lake.id == lake_id).first()
    if not lake:
        raise HTTPException(status_code=404, detail="Lake not found")

    for key, value in lake_data.items():
        setattr(lake, key, value)

    db.commit()
    db.refresh(lake)
    return {
        "id": str(lake.id),
        "name": lake.name,
        "latitude": float(lake.latitude),
        "longitude": float(lake.longitude),
    }


@router.delete("/{lake_id}", status_code=204)
def delete_lake(lake_id: UUID, db: Session = Depends(get_db)):
    lake = db.query(Lake).filter(Lake.id == lake_id).first()
    if not lake:
        raise HTTPException(status_code=404, detail="Lake not found")

    db.delete(lake)
    db.commit()
    return None
