from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class GeneralExpense(Base):
    __tablename__ = "general_expenses"

    id: Mapped[int] = mapped_column(primary_key=True)

    load_id: Mapped[int] = mapped_column(
        ForeignKey("loads.id"),
        nullable=False
    )

    amount: Mapped[Numeric(12, 2)] = mapped_column(
        nullable=False
    )

    load = relationship("Load")
