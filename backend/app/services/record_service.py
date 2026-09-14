import os
import shutil
import uuid
from fastapi import HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.driver import Driver
from app.models.record import Record
from app.models.remito import Remito
from app.models.fuel_record import FuelRecord
from app.models.general_expense import GeneralExpense
from app.models.photo import Photo
from app.schemas.record import RecordCreate


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

    storage_dir = os.path.join(os.getcwd(), "storage", "photos")
    os.makedirs(storage_dir, exist_ok=True)

    for photo in photos:
        ext = os.path.splitext(photo.filename)[1]
        if not ext:
            ext = ".jpg" # fallback
        unique_filename = f"{uuid.uuid4()}{ext}"
        file_path = os.path.join(storage_dir, unique_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)

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
    start_date: str | None = None,
    end_date: str | None = None
):
    query = select(Record)
    if driver_id:
        query = query.where(Record.driver_id == driver_id)
    if category:
        query = query.where(Record.category == category)
    if start_date:
        query = query.where(Record.date >= start_date)
    if end_date:
        query = query.where(Record.date <= end_date)
        
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