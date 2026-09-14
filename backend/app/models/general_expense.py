from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class GeneralExpense(Base):
    __tablename__ = "general_expenses"

    id: Mapped[int] = mapped_column(primary_key=True)

    record_id: Mapped[int] = mapped_column(
        ForeignKey("records.id"),
        nullable=False
    )

    amount: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    record = relationship("Record")
