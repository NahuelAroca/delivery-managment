from datetime import date

from fastapi import APIRouter, Depends, File, Form, UploadFile, Query, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import TypeAdapter
import os
from sqlalchemy.orm import Session
from supabase import create_client, Client

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)


from app.database.database import get_db
from app.schemas.record import RecordCreate, RecordResponse, RecordDetailResponse
from app.services.record_service import create_record, get_records, get_record


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


@router.get("/", response_model=list[RecordResponse])
def get_all_records(
    driver_id: int | None = Query(None),
    category: str | None = Query(None),
    start_date: str | None = Query(None),
    end_date: str | None = Query(None),
    db: Session = Depends(get_db)
):
    return get_records(db, driver_id, category, start_date, end_date)


@router.get("/{record_id}", response_model=RecordDetailResponse)
def get_single_record(
    record_id: int,
    db: Session = Depends(get_db)
):
    return get_record(db, record_id)


@router.get("/photos/{filename}")
def get_photo(filename: str):
    try:
        # Create a signed URL valid for 60 seconds (1 minute)
        response = supabase.storage.from_("photos").create_signed_url(filename, 60)
        signed_url = response.get("signedURL") or response.get("signedUrl")
        
        if not signed_url:
            raise HTTPException(status_code=404, detail="Photo not found")
            
        return RedirectResponse(url=signed_url, status_code=307)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error accessing photo: {str(e)}")