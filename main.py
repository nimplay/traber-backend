from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import models, schemas, database, uuid
from database import engine, get_db

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Truber API")

# Enable CORS for the mobile app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Truber API"}

@app.post("/auth/login", response_model=schemas.UserProfile)
def login(user_auth: schemas.UserAuth, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_auth.email).first()
    if not user or user.password != user_auth.password: # Plain text for demo, use hashing in prod
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

from sqlalchemy.orm import joinedload

@app.get("/providers", response_model=List[schemas.UserProfile])
def get_providers(db: Session = Depends(get_db)):
    return db.query(models.User).options(
        joinedload(models.User.portfolio),
        joinedload(models.User.badges)
    ).filter(models.User.role == "provider").all()

@app.get("/providers/{provider_id}", response_model=schemas.UserProfile)
def get_provider(provider_id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).options(
        joinedload(models.User.portfolio),
        joinedload(models.User.badges)
    ).filter(models.User.id == provider_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Provider not found")
    return user

@app.put("/users/{user_id}/profile", response_model=schemas.UserProfile)
def update_profile(user_id: str, updates: schemas.ProviderUpdate, db: Session = Depends(get_db)):
    print(f"Updating profile for user: {user_id}")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user

@app.put("/users/{user_id}/portfolio")
def update_portfolio(user_id: str, portfolio: List[schemas.PortfolioBase], db: Session = Depends(get_db)):
    print(f"Updating portfolio for user: {user_id}")
    print(f"Items received: {len(portfolio)}")
    # Delete existing portfolio items
    db.query(models.PortfolioItem).filter(models.PortfolioItem.providerId == user_id).delete()
    
    # Add new ones
    for item in portfolio:
        item_id = item.id if item.id else str(uuid.uuid4())
        new_item = models.PortfolioItem(
            id=item_id,
            providerId=user_id,
            imageUrl=item.imageUrl,
            title=item.title,
            description=item.description
        )
        db.add(new_item)
    
    db.commit()
    return {"message": "Portfolio updated successfully"}

@app.get("/badges", response_model=List[schemas.BadgeBase])
def get_badges(db: Session = Depends(get_db)):
    return db.query(models.Badge).all()

@app.post("/job-requests", response_model=schemas.JobRequestResponse)
def create_job_request(request: schemas.JobRequestCreate, userId: str, db: Session = Depends(get_db)):
    # Check if direct request has providerId
    if request.request_type == 'direct' and not request.providerId:
        raise HTTPException(status_code=400, detail="Direct request must have a providerId")
        
    new_job = models.JobRequest(
        id=str(uuid.uuid4()),
        clientId=userId,
        **request.dict()
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

@app.get("/job-requests", response_model=List[schemas.JobRequestResponse])
def get_job_requests(type: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.JobRequest).options(
        joinedload(models.JobRequest.client),
        joinedload(models.JobRequest.provider)
    )
    
    # Only show 'open' requests on the map
    query = query.filter(models.JobRequest.request_type == "open")
    
    if type and type != 'all':
        query = query.filter(models.JobRequest.type == type)
    return query.filter(models.JobRequest.status == "pending").all()

@app.get("/users/{user_id}/requests", response_model=List[schemas.JobRequestResponse])
def get_user_requests(user_id: str, db: Session = Depends(get_db)):
    # Return requests where user is client OR provider
    return db.query(models.JobRequest).options(
        joinedload(models.JobRequest.client),
        joinedload(models.JobRequest.provider)
    ).filter(
        (models.JobRequest.clientId == user_id) | (models.JobRequest.providerId == user_id)
    ).order_by(models.JobRequest.createdAt.desc()).all()

@app.get("/job-requests/{job_id}", response_model=schemas.JobRequestResponse)
def get_job_request(job_id: str, db: Session = Depends(get_db)):
    job = db.query(models.JobRequest).options(
        joinedload(models.JobRequest.client),
        joinedload(models.JobRequest.provider)
    ).filter(models.JobRequest.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.put("/job-requests/{job_id}/status")
def update_job_status(job_id: str, status: str, db: Session = Depends(get_db)):
    job = db.query(models.JobRequest).filter(models.JobRequest.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job.status = status
    db.commit()
    return {"message": f"Job status updated to {status}"}

@app.put("/job-requests/{job_id}/accept")
def accept_job(job_id: str, provider_id: str, db: Session = Depends(get_db)):
    job = db.query(models.JobRequest).filter(models.JobRequest.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.providerId and job.providerId != provider_id:
        raise HTTPException(status_code=400, detail="Job already taken by another provider")
        
    job.providerId = provider_id
    job.status = "accepted"
    db.commit()
    return {"message": "Job accepted successfully"}
