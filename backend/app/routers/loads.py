from datetime import date

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.load_service import create_load
from app.schemas.load import LoadCreate, LoadResponse


router = APIRouter(
    prefix="/loads",
    tags=["Loads"],
)


@router.post("/")
def create_load_endpoint(
    driver_id: int = Form(...),
    category: str = Form(...),
    date: date = Form(...),
    photos: list[UploadFile] = File(...),
    db: Session = Depends(get_db),
):
    if len(photos) < 1 or len(photos) > 2:
        raise ValueError("A load must have between 1 and 2 photos")

    # We will build LoadCreate here in the next step.

    return {
        "driver_id": driver_id,
        "category": category,
        "date": date,
        "photos": [photo.filename for photo in photos],
    }