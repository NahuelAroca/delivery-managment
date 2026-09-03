from datetime import date
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field


class LoadBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    driver_id: int
    date: date


class ReceiptLoadCreate(LoadBase):
    category: Literal["receipt"]

    loading_location: str
    destination: str
    company: str
    receipt_number: str


class FuelLoadCreate(LoadBase):
    category: Literal["fuel"]

    liters: float


class GeneralLoadCreate(LoadBase):
    category: Literal["general"]

    amount: float


LoadCreate = Annotated[
    ReceiptLoadCreate | FuelLoadCreate | GeneralLoadCreate,
    Field(discriminator="category"),
]
