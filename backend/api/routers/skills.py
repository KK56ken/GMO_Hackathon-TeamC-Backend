from fastapi import APIRouter, Depends
import database, models, database
from sqlalchemy.orm import Session

router = APIRouter(tags=["Skill"])

@router.get("/skill")
async def get_skills_table(db: Session = Depends(database.get_db)):
	skills = db.query(models.Skill).all()
	return skills