from typing import Annotated, Literal
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class RecordBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    driver_id: int
    date: date


class RemitoRecordCreate(RecordBase):
    category: Literal["remito"]

    loading_location: str
    destination: str
    company: str
    remito_number: str


class FuelRecordCreate(RecordBase):
    category: Literal["fuel"]

    liters: float


class GeneralRecordCreate(RecordBase):
    category: Literal["general"]

    amount: float


RecordCreate = Annotated[
    RemitoRecordCreate | FuelRecordCreate | GeneralRecordCreate,
    Field(discriminator="category"),
]

class RecordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    driver_id: int
    category: str
    date: date
    created_at: datetime

class PhotoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    file_path: str

class RecordDetailResponse(RecordResponse):
    loading_location: str | None = None
    destination: str | None = None
    company: str | None = None
    remito_number: str | None = None
    liters: float | None = None
    amount: float | None = None
    
    photos: list[PhotoResponse] = []