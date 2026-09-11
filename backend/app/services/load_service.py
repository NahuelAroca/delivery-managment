from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.driver import Driver
from app.models.load import Load
from app.models.receipt import Receipt
from app.models.fuel_record import FuelRecord
from app.models.general_expense import GeneralExpense
from app.schemas.load import LoadCreate


def create_load(db: Session, payload: LoadCreate):
    driver = db.scalar(
        select(Driver).where(Driver.id == payload.driver_id)
    )

    if driver is None:
        raise HTTPException(
            status_code=404,
            detail="Driver not found",
        )

    load = Load(
        driver_id=payload.driver_id,
        category=payload.category,
        date=payload.date,
    )

    db.add(load)
    db.flush()

    if payload.category == "receipt":
        receipt = Receipt(
            load_id=load.id,
            loading_location=payload.loading_location,
            destination=payload.destination,
            company=payload.company,
            receipt_number=payload.receipt_number,
        )

        db.add(receipt)

    elif payload.category == "fuel":
        fuel_record = FuelRecord(
            load_id=load.id,
            liters=payload.liters,
        )

        db.add(fuel_record)

    elif payload.category == "general":
        general_expense = GeneralExpense(
            load_id=load.id,
            amount=payload.amount,
        )

        db.add(general_expense)

    db.commit()
    db.refresh(load)

    return load