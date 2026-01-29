from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON, Boolean, Table
from sqlalchemy.orm import relationship
from database import Base
import datetime

# Association table for User-Badge relationship
user_badges = Table(
    'user_badges',
    Base.metadata,
    Column('user_id', String, ForeignKey('users.id')),
    Column('badge_id', String, ForeignKey('badges.id'))
)

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String) # 'client', 'provider', 'admin'
    image = Column(String, nullable=True)
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Provider specific fields
    type = Column(String, nullable=True) # 'electric', 'plumbing', etc.
    rating = Column(Float, default=0.0)
    jobs = Column(Integer, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    about = Column(String, nullable=True)
    hourly_rate = Column(JSON, nullable=True) # {"min": 10, "max": 20}
    location_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)

    # Relationships
    portfolio = relationship("PortfolioItem", back_populates="provider")
    reviews = relationship("Review", back_populates="provider", foreign_keys="Review.providerId")
    badges = relationship("Badge", secondary=user_badges, back_populates="users")

class PortfolioItem(Base):
    __tablename__ = "portfolio"

    id = Column(String, primary_key=True, index=True)
    providerId = Column(String, ForeignKey('users.id'))
    imageUrl = Column(String)
    title = Column(String)
    description = Column(String, nullable=True)

    provider = relationship("User", back_populates="portfolio")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(String, primary_key=True, index=True)
    providerId = Column(String, ForeignKey('users.id'))
    userId = Column(String) # The client who wrote it
    userName = Column(String)
    comment = Column(String)
    rating = Column(Float)
    date = Column(String)

    provider = relationship("User", back_populates="reviews", foreign_keys=[providerId])

class Badge(Base):
    __tablename__ = "badges"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    icon = Column(String)

    users = relationship("User", secondary=user_badges, back_populates="badges")

class JobRequest(Base):
    __tablename__ = "job_requests"

    id = Column(String, primary_key=True, index=True)
    clientId = Column(String, ForeignKey('users.id'))
    providerId = Column(String, ForeignKey('users.id'), nullable=True) # For direct requests
    title = Column(String)
    description = Column(String)
    type = Column(String)  # 'electric', 'plumbing', etc.
    budget_min = Column(Float)
    budget_max = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
    request_type = Column(String, default="open") # 'open' (map) or 'direct' (private)
    status = Column(String, default="pending")  # 'pending', 'accepted', 'rejected', 'in_process', 'completed', 'cancelled'
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)

    client = relationship("User", foreign_keys=[clientId])
    provider = relationship("User", foreign_keys=[providerId])
