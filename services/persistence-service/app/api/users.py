from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core import get_db
from app.models import User

router = APIRouter()


@router.get("/", response_model=List[dict])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return [
        {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "owns_boat": user.owns_boat,
        }
        for user in users
    ]


@router.get("/{user_id}", response_model=dict)
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "owns_boat": user.owns_boat,
        "schedule_preferences": user.schedule_preferences,
        "weather_preferences": user.weather_preferences,
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
                        "username": "hsimpson",
                        "email": "homer@example.com",
                        "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7t.6cLxHQW",
                        "preferred_lake_id": "00000000-0000-0000-0000-000000000000",
                        "owns_boat": True,
                        "schedule_preferences": {
                            "weekday": {"morning": False, "afternoon": False, "evening": True},
                            "weekend": {
                                "saturday": {"morning": False, "afternoon": False, "evening": True},
                                "sunday": {"morning": False, "afternoon": False, "evening": True}
                            }
                        },
                        "weather_preferences": {
                            "max_precipitation_probability": 30,
                            "max_wind_speed": 15,
                            "min_temperature": 65
                        },
                        "notification_preferences": {
                            "email_enabled": True,
                            "sms_enabled": False,
                            "weather_alerts": True,
                            "friend_notifications": False
                        }
                    }
                }
            }
        }
    }
)
def create_user(user_data: dict, db: Session = Depends(get_db)):
    user = User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": str(user.id), "username": user.username, "email": user.email}


@router.put("/{user_id}", response_model=dict)
def update_user(user_id: UUID, user_data: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return {"id": str(user.id), "username": user.username, "email": user.email}


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return None
