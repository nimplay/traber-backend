from database import SessionLocal
import models

db = SessionLocal()
try:
    # Find the job request
    job = db.query(models.JobRequest).first()
    if job:
        print(f"Updating job {job.id} status from {job.status} to pending")
        job.status = 'pending'
        db.commit()
        print("Status updated successfully.")
    else:
        print("No job request found.")

except Exception as e:
    print(f"Error: {e}")
finally:
    db.close()
