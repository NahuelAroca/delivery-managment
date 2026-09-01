from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class Receipt(Base):
    __tablename__ = "receipts"

    id: Mapped[int] = mapped_column(primary_key=True)

    load_id: Mapped[int] = mapped_column(
        ForeignKey("loads.id"),
        nullable=False
    )

    loading_location: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    destination: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    company: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    receipt_number: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    load = relationship("Load")
