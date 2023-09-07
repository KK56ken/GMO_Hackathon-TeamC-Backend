from fastapi import APIRouter, Depends, status, HTTPException
import database, models, schemas
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import bcrypt


router = APIRouter(tags=['Authentication'])

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/signup")
async def signup(request: schemas.User, db: Session = Depends(database.get_db)):
    hashedPassword = pwd_cxt.hash(request.password)
    new_user = models.User(email=request.email, password=hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return 