from database import SessionLocal
import models

db = SessionLocal()
try:
    users = db.query(models.User).all()
    print(f"Total users in DB: {len(users)}")
    for u in users:
        print(f"ID: {u.id}, Name: {u.name}, Role: {u.role}")
    
    portfolio = db.query(models.PortfolioItem).all()
    print(f"Total portfolio items: {len(portfolio)}")
except Exception as e:
    print(f"Error: {e}")
finally:
    db.close()
