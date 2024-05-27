from src.core.database import db
from datetime import datetime
from enum import Enum


class ServiceType(Enum):
    ANALYSIS = 'Análisis'
    CONSULTING = 'Consultoría'
    DEVELOPMENT = 'Desarrollo'

class Service(db.Model):
    __tablename__ = "services"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    keywords = db.Column(db.String(255), nullable=False)
    type_of_service = db.Column(db.Enum(ServiceType, 
                                        values_callable=lambda x: [str(type.value) for type in ServiceType]), 
                                        nullable=False)
    institution_id = db.Column(db.Integer, db.ForeignKey("institutions.id"))
    institution = db.relationship("Institution", back_populates="services")

    requests = db.relationship("ServiceRequest", back_populates="service")
    
    enabled = db.Column(db.Boolean, nullable=False, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )