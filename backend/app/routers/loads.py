from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.load import LoadCreate
from app.services.load_service import create_load


router = APIRouter(
    prefix="/loads",
    tags=["Loads"],
)


@router.post("/")
def create_load_endpoint(
    payload: LoadCreate,
    db: Session = Depends(get_db),
):
    return create_load(db, payload)