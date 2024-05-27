from datetime import datetime
from src.core.database import db


class Configuration(db.Model):
    __tablename__ = "configurations"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    per_page = db.Column(db.Integer, nullable=False)
    contact = db.Column(db.String(255), nullable=False)
    maintenance_message = db.Column(db.String(255), nullable=False)
    enabled_site = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
