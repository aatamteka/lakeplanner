from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import date

from app.core import get_db
from app.models import Outing

router = APIRouter()


@router.get("/", response_model=List[dict])
def list_outings(
    user_id: Optional[UUID] = Query(None),
    lake_id: Optional[UUID] = Query(None),
    start_date: Optional[date] = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(Outing)

    if user_id:
        query = query.filter(Outing.user_id == user_id)
    if lake_id:
        query = query.filter(Outing.lake_id == lake_id)
    if start_date:
        query = query.filter(Outing.planned_date >= start_date)

    outings = query.offset(skip).limit(limit).all()
    return [
        {
            "id": str(outing.id),
            "user_id": str(outing.user_id),
            "lake_id": str(outing.lake_id),
            "planned_date": outing.planned_date.isoformat(),
            "time_slot": outing.time_slot,
            "target_amenities": [str(a) for a in outing.target_amenities] if outing.target_amenities else [],
        }
        for outing in outings
    ]


@router.get("/{outing_id}", response_model=dict)
def get_outing(outing_id: UUID, db: Session = Depends(get_db)):
    outing = db.query(Outing).filter(Outing.id == outing_id).first()
    if not outing:
        raise HTTPException(status_code=404, detail="Outing not found")
    return {
        "id": str(outing.id),
        "user_id": str(outing.user_id),
        "lake_id": str(outing.lake_id),
        "planned_date": outing.planned_date.isoformat(),
        "time_slot": outing.time_slot,
        "target_amenities": [str(a) for a in outing.target_amenities] if outing.target_amenities else [],
        "invited_friends": [str(f) for f in outing.invited_friends] if outing.invited_friends else [],
        "rsvp_status": outing.rsvp_status,
        "notes": outing.notes,
    }


@router.post("/", response_model=dict, status_code=201)
def create_outing(outing_data: dict, db: Session = Depends(get_db)):
    outing = Outing(**outing_data)
    db.add(outing)
    db.commit()
    db.refresh(outing)
    return {"id": str(outing.id), "planned_date": outing.planned_date.isoformat()}


@router.delete("/{outing_id}", status_code=204)
def delete_outing(outing_id: UUID, db: Session = Depends(get_db)):
    outing = db.query(Outing).filter(Outing.id == outing_id).first()
    if not outing:
        raise HTTPException(status_code=404, detail="Outing not found")

    db.delete(outing)
    db.commit()
    return None
