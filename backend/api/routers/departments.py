from fastapi import APIRouter, Depends
import database, models, database
from sqlalchemy.orm import Session

router = APIRouter(tags=["Department"])

@router.get("/department")
async def get_departments_table(db: Session = Depends(database.get_db)):
	departments = db.query(models.Department).all()
	return departments