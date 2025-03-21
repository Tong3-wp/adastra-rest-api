from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.user import schemas
from typing import List, Optional
from app import models


router = APIRouter(prefix="/user", tags=["user"])


@router.get("/", response_model=List[schemas.User], summary="Get User")
def read_users(
    db: Session = Depends(get_db),
    offset: int = Query(0, description="Offset for pagination"),
    limit: int = Query(100, description="Limit for pagination"),
    role_filter: Optional[str] = Query("user", description="Filter by role"),
    search: Optional[str] = Query(None, description="Search by username or email"),
):
    query = db.query(models.User)

    if role_filter:
        query = query.filter(models.User.role == role_filter)
    if search:
        query = query.filter(
            models.User.username.like(f"%{search}%")
            | models.User.email.like(f"%{search}%")
        )

    users = query.offset(offset).limit(limit).all()
    if users:
        return users
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.get("/{user_id}", response_model=schemas.User, summary="Get User By ID")
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{user_id}", response_model=schemas.User, summary="Update User By ID")
def update_user(user_id: int, user: schemas.UserBase, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    existing_user = (
        db.query(models.User).filter(models.User.username == user.username).first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )
    existing_email = (
        db.query(models.User).filter(models.User.email == user.email).first()
    )
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )
    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/{user_id}", response_model=schemas.User, summary="Delete User By ID")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user
