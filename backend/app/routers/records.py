from datetime import date

from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import TypeAdapter
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.record import RecordCreate, RecordResponse
from app.services.record_service import create_record


router = APIRouter(
    prefix="/records",
    tags=["Records"],
)


record_adapter = TypeAdapter(RecordCreate)


@router.post("/", response_model=RecordResponse)
def create_record_endpoint(
    driver_id: int = Form(...),
    category: str = Form(...),
    date: date = Form(...),
    loading_location: str | None = Form(None),
    destination: str | None = Form(None),
    company: str | None = Form(None),
    remito_number: str | None = Form(None),
    liters: float | None = Form(None),
    amount: float | None = Form(None),
    photos: list[UploadFile] = File(...),
    db: Session = Depends(get_db),
):
    form_data = {
        "driver_id": driver_id,
        "category": category,
        "date": date,
        "loading_location": loading_location,
        "destination": destination,
        "company": company,
        "remito_number": remito_number,
        "liters": liters,
        "amount": amount,
    }

    form_data = {
        key: value
        for key, value in form_data.items()
        if value is not None
    }

    payload = record_adapter.validate_python(form_data)

    return create_record(db, payload, photos)