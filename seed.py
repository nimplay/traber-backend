import json
import os
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from datetime import datetime

# Path to the data directory local to this backend
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))

def load_json(filename):
    with open(os.path.join(DATA_DIR, filename), 'r', encoding='utf-8') as f:
        return json.load(f)

def seed_db():
    # Create tables
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Load data
        users_data = load_json('users.json')
        portfolio_data = load_json('portfolio.json')
        reviews_data = load_json('reviews.json')
        badges_data = load_json('badges.json')
        user_badges_data = load_json('user_badges.json')
        services_data = load_json('services.json')

        # 1. Seed Services
        for s in services_data:
            service = models.Service(
                id=s['id'],
                name=s['name'],
                slug=s['slug'],
                icon=s['icon'],
                description=s.get('description')
            )
            db.add(service)
        db.commit()

        # 2. Seed Badges
        badge_objs = {}
        for b in badges_data:
            badge = models.Badge(id=b['id'], name=b['name'], icon=b['icon'])
            db.add(badge)
            badge_objs[b['id']] = badge
        db.commit()

        # 3. Seed Users
        user_objs = {}
        for u in users_data:
            createdAt = datetime.fromisoformat(u['createdAt'].replace('Z', '+00:00')) if 'createdAt' in u else datetime.utcnow()
            user = models.User(
                id=u['id'],
                name=u['name'],
                email=u['email'],
                password=u.get('password', '1234'), # Use actual password or mock
                role=u['role'],
                image=u.get('image'),
                createdAt=createdAt,
                type=u.get('type'),
                rating=u.get('rating', 0.0),
                jobs=u.get('jobs', 0),
                latitude=u.get('latitude'),
                longitude=u.get('longitude'),
                about=u.get('about'),
                hourly_rate=u.get('hourly_rate'),
                location_name=u.get('location_name'),
                phone=u.get('phone', '+58 424 0000000')
            )
            
            # Link badges
            ub_ids = [ub['badgeId'] for ub in user_badges_data if ub['userId'] == u['id']]
            for b_id in ub_ids:
                if b_id in badge_objs:
                    user.badges.append(badge_objs[b_id])
            
            db.add(user)
            user_objs[u['id']] = user
        db.commit()

        # 4. Seed Portfolio
        for p in portfolio_data:
            item = models.PortfolioItem(
                id=p['id'],
                providerId=p['providerId'],
                imageUrl=p['imageUrl'],
                title=p['title'],
                description=p.get('description', '')
            )
            db.add(item)
        
        # 5. Seed Reviews
        for r in reviews_data:
            review = models.Review(
                id=r['id'],
                providerId=r['providerId'],
                userId=r['userId'],
                userName=r['userName'],
                comment=r['comment'],
                rating=r['rating'],
                date=r['date']
            )
            db.add(review)
        
        db.commit()
        print("Database seeded successfully!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
