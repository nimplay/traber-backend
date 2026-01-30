from database import SessionLocal
import models

db = SessionLocal()
try:
    print("--- Users ---")
    users = db.query(models.User).all()
    print(f"Total users: {len(users)}")
    
    print("\n--- Job Requests ---")
    requests = db.query(models.JobRequest).all()
    print(f"Total requests: {len(requests)}")
    for r in requests:
        print(f"ID: {r.id}")
        print(f"  Title: {r.title}")
        print(f"  Type: {r.type}")
        print(f"  Status: {r.status}")
        print(f"  Request Type: {r.request_type}")
        print(f"  Client: {r.clientId}")
        print(f"  Provider: {r.providerId}")
        print(f"  Lat/Lng: {r.latitude}, {r.longitude}")
        print("-" * 20)

except Exception as e:
    print(f"Error: {e}")
finally:
    db.close()
