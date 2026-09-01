from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class FuelRecord(Base):
    __tablename__ = "fuel_records"

    id: Mapped[int] = mapped_column(primary_key=True)

    load_id: Mapped[int] = mapped_column(
        ForeignKey("loads.id"),
        nullable=False
    )

    liters: Mapped[float] = mapped_column(
        nullable=False
    )

    load = relationship("Load")
