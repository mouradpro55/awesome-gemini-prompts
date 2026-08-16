import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Text, Enum, ForeignKey, JSON, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from app.db.database import Base
import enum

class RoleEnum(str, enum.Enum):
    merchant = "merchant"
    creator = "creator"
    admin = "admin"

class CampaignStatusEnum(str, enum.Enum):
    active = "active"
    completed = "completed"
    cancelled = "cancelled"

class ApplicationStatusEnum(str, enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
    completed = "completed"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    merchant = relationship("Merchant", back_populates="user", uselist=False)
    creator = relationship("Creator", back_populates="user", uselist=False)


class Merchant(Base):
    __tablename__ = "merchants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    store_name = Column(String, nullable=False)
    category = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    location = Column(Geometry(geometry_type='POINT', srid=4326))
    address_text = Column(String)
    social_links = Column(JSON)

    user = relationship("User", back_populates="merchant")
    campaigns = relationship("Campaign", back_populates="merchant")


class Creator(Base):
    __tablename__ = "creators"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    bio = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    location = Column(Geometry(geometry_type='POINT', srid=4326))
    platforms = Column(JSON)
    engagement_rate = Column(Float)

    user = relationship("User", back_populates="creator")
    applications = relationship("Application", back_populates="creator")


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    merchant_id = Column(UUID(as_uuid=True), ForeignKey("merchants.id"))
    title = Column(String, nullable=False)
    description = Column(Text)
    content_type = Column(String)
    reward_type = Column(String)
    reward_value = Column(String)
    status = Column(Enum(CampaignStatusEnum), default=CampaignStatusEnum.active)
    created_at = Column(DateTime, default=datetime.utcnow)

    merchant = relationship("Merchant", back_populates="campaigns")
    applications = relationship("Application", back_populates="campaign")


class Application(Base):
    __tablename__ = "applications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("campaigns.id"))
    creator_id = Column(UUID(as_uuid=True), ForeignKey("creators.id"))
    status = Column(Enum(ApplicationStatusEnum), default=ApplicationStatusEnum.pending)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    campaign = relationship("Campaign", back_populates="applications")
    creator = relationship("Creator", back_populates="applications")