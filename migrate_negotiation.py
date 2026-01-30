from database import SessionLocal, engine
from sqlalchemy import text

# Add columns manually to SQLite
with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TABLE job_requests ADD COLUMN milestones JSON DEFAULT '[]'"))
        print("Added milestones column")
    except Exception as e:
        print(f"milestones might exist: {e}")

    try:
        conn.execute(text("ALTER TABLE job_requests ADD COLUMN proposal_status VARCHAR DEFAULT 'none'"))
        print("Added proposal_status column")
    except Exception as e:
        print(f"proposal_status might exist: {e}")

    try:
        conn.execute(text("ALTER TABLE job_requests ADD COLUMN budget_final FLOAT"))
        print("Added budget_final column")
    except Exception as e:
        print(f"budget_final might exist: {e}")

    conn.commit()
