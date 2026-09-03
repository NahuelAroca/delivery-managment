from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.driver import Driver
from app.schemas.driver import DriverResponse


router = APIRouter(
    prefix="/drivers",
    tags=["Drivers"],
)


@router.get("/", response_model=list[DriverResponse])
def get_drivers(db: Session = Depends(get_db)):
    return db.scalars(select(Driver)).all()