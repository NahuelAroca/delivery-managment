from sqlalchemy import select

from app.database.database import SessionLocal
from app.models.driver import Driver


drivers = [
    "Driver 1",
    "Driver 2",
    "Driver 3",
    "Driver 4",
]


def seed_drivers():
    with SessionLocal() as session:
        for name in drivers:
            existing_driver = session.scalar(
                select(Driver).where(Driver.name == name)
            )

            if existing_driver is None:
                session.add(Driver(name=name))

        session.commit()


if __name__ == "__main__":
    seed_drivers()