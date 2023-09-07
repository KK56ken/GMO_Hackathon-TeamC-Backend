from fastapi import APIRouter, Depends, status, HTTPException
import database, models, schemas
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import bcrypt
from datetime import timedelta
from tokens import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/signup")
async def signup(request: schemas.SignUp, db: Session = Depends(database.get_db)):
    hashedPassword = pwd_cxt.hash(request.password)
    new_user = models.User(email=request.email, password=hashedPassword, name=request.name, department_id=request.department_id, slack_id=request.slack_id, status=request.status)
    if db.query(models.User).filter(models.User.email == request.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Email already registered")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    if request.skill_set is not None:
        for skill in request.skill_set:
            new_userskill = models.UsersSkill(user_id=new_user.user_id, skill_id=skill)
            db.add(new_userskill)
            db.commit()
            db.refresh(new_userskill)
    return {"message": "User Created"}

@router.post("/auth")
async def auth(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    if not pwd_cxt.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect Password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": user.user_id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
