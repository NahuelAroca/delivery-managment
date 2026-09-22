import sys
import os
sys.path.append(os.getcwd())

from app.database.database import SessionLocal
from app.services.record_service import get_records

db = SessionLocal()
try:
    print("ALL RECORDS:")
    all_recs = get_records(db)
    for r in all_recs:
        print(r.id, r.date)

    print("\nFILTERED 16 to 23:")
    filtered = get_records(db, start_date="2026-09-16", end_date="2026-09-23")
    for r in filtered:
        print(r.id, r.date)
finally:
    db.close()
