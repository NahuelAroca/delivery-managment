import os
import uuid
from datetime import date, datetime
from zoneinfo import ZoneInfo
from fastapi import HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session
from supabase import create_client, Client

from app.models.driver import Driver
from app.models.record import Record
from app.models.remito import Remito
from app.models.fuel_record import FuelRecord
from app.models.general_expense import GeneralExpense
from app.models.photo import Photo
from app.schemas.record import RecordCreate

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

def create_record(
    db: Session,
    payload: RecordCreate,
    photos: list[UploadFile],
):
    if len(photos) < 1 or len(photos) > 2:
        raise HTTPException(
            status_code=400,
            detail="A record must have between 1 and 2 photos",
        )

    driver = db.scalar(
        select(Driver).where(Driver.id == payload.driver_id)
    )

    if driver is None:
        raise HTTPException(
            status_code=404,
            detail="Driver not found",
        )

    record = Record(
        driver_id=payload.driver_id,
        category=payload.category,
        date=payload.date,
    )

    db.add(record)
    db.flush()

    if payload.category == "remito":
        remito = Remito(
            record_id=record.id,
            loading_location=payload.loading_location,
            destination=payload.destination,
            company=payload.company,
            remito_number=payload.remito_number,
        )
        db.add(remito)

    elif payload.category == "fuel":
        fuel_record = FuelRecord(
            record_id=record.id,
            liters=payload.liters,
        )
        db.add(fuel_record)

    elif payload.category == "general":
        general_expense = GeneralExpense(
            record_id=record.id,
            amount=payload.amount,
        )
        db.add(general_expense)

    for photo in photos:
        ext = os.path.splitext(photo.filename)[1]
        if not ext:
            ext = ".jpg" # fallback
        unique_filename = f"{uuid.uuid4()}{ext}"
        
        file_bytes = photo.file.read()
        
        # Upload to Supabase Storage
        supabase.storage.from_("photos").upload(
            path=unique_filename,
            file=file_bytes,
            file_options={"content-type": photo.content_type}
        )

        db.add(
            Photo(
                record_id=record.id,
                file_path=unique_filename,
            )
        )

    db.commit()
    db.refresh(record)

    return record

def get_records(
    db: Session,
    driver_id: int | None = None,
    category: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None
):
    query = select(Record)
    if driver_id:
        query = query.where(Record.driver_id == driver_id)
    if category:
        query = query.where(Record.category == category)
    tz = ZoneInfo("America/Argentina/Buenos_Aires")
    
    if start_date:
        dt_start = datetime.combine(start_date, datetime.min.time(), tzinfo=tz)
        utc_start = dt_start.astimezone(ZoneInfo("UTC")).replace(tzinfo=None)
        query = query.where(Record.created_at >= utc_start)
    if end_date:
        dt_end = datetime.combine(end_date, datetime.max.time(), tzinfo=tz)
        utc_end = dt_end.astimezone(ZoneInfo("UTC")).replace(tzinfo=None)
        query = query.where(Record.created_at <= utc_end)
        
    query = query.order_by(Record.date.desc(), Record.id.desc())
    return db.scalars(query).all()

def get_record(db: Session, record_id: int):
    record = db.scalar(select(Record).where(Record.id == record_id))
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
        
    photos = db.scalars(select(Photo).where(Photo.record_id == record_id)).all()
    
    detail_data = {
        "id": record.id,
        "driver_id": record.driver_id,
        "category": record.category,
        "date": record.date,
        "created_at": record.created_at,
        "photos": photos
    }
    
    if record.category == "remito":
        remito = db.scalar(select(Remito).where(Remito.record_id == record_id))
        if remito:
            detail_data.update({
                "loading_location": remito.loading_location,
                "destination": remito.destination,
                "company": remito.company,
                "remito_number": remito.remito_number
            })
    elif record.category == "fuel":
        fuel = db.scalar(select(FuelRecord).where(FuelRecord.record_id == record_id))
        if fuel:
            detail_data["liters"] = fuel.liters
    elif record.category == "general":
        general = db.scalar(select(GeneralExpense).where(GeneralExpense.record_id == record_id))
        if general:
            detail_data["amount"] = general.amount
            
    return detail_data