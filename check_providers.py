from database import SessionLocal
import models
import schemas

db = SessionLocal()
try:
    providers = db.query(models.User).filter(models.User.role == "provider").all()
    print(f"Num providers: {len(providers)}")
    for p in providers:
        # Check if they have coordinates
        print(f"Provider: {p.name}, Lat: {p.latitude}, Lng: {p.longitude}")
except Exception as e:
    print(f"Error: {e}")
finally:
    db.close()
