from src.core.database import db
from sqlalchemy import and_
from src.core.service_requests.service_request import ServiceRequest
from src.core.services.service import Service
from src.core.auth.user import User
from datetime import datetime


class Institution(db.Model):
    __tablename__ = "institutions"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255), nullable=False)
    info = db.Column(db.Text, nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    localizacion = db.Column(db.String(255), nullable=False)
    web = db.Column(db.String(255), nullable=False)
    palabras_clave = db.Column(db.String(255), nullable=False)
    dias_horarios = db.Column(db.String(255), nullable=False)
    contacto = db.Column(db.String(255), nullable=False)
    habilitado = db.Column(db.Boolean, nullable=False, default=True)
    services= db.relationship("Service", back_populates="institution")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def get_service_requests(self):
        """
        Retorna todas las solicitudes de los servicios que ofrece la institución.
        """
        # Inicializo una lista para almacenar todas las solicitudes de servicios
        service_requests = []

        # Itero sobre los servicios para obtener las solicitudes asociadas
        for service in self.services:
            service_requests.extend(service.requests)

        return service_requests
    
    
    def get_service_requests_paginate(self, page, per_page):
        """
        Retorna todas las solicitudes de los servicios que ofrece la institución paginados.
        """
        # Utilizo la consulta SQLAlchemy para obtener las solicitudes paginadas
        paginated_service_requests = (
            ServiceRequest.query
            .join(Service)
            .filter(Service.institution == self)
            .order_by(ServiceRequest.created_at.desc())
            .paginate(page=page, per_page=per_page, error_out=False) # Si no pongo page=page, per_page=per_page me da error!!!!
        )

        # Devuelvo las solicitudes y el objeto de paginación
        return paginated_service_requests
    
    def get_service_requests_filter_paginate(self, email=None, start_date=None, end_date=None, type_of_service=None, page=1, per_page=10):
        """
        Retorna las solicitudes de servicios filtradas por tipo de servicio, email y rango de fechas (opcionales).
        """
        print("...................................................")
        print(email)
        print(type_of_service)
        print(start_date)
        print(end_date)
        # Construir la base de la consulta
        query = db.session.query(ServiceRequest).join(Service).filter(Service.institution == self)

        # Aplicar filtros adicionales si se proporcionan
        if email:
            query = query.filter(ServiceRequest.user.has(User.email.like(f"%{email}%")))


        if start_date and end_date:
            query = query.filter(and_(ServiceRequest.created_at >= start_date, ServiceRequest.created_at <= end_date))
        elif start_date:
            query = query.filter(ServiceRequest.created_at >= start_date)
        elif end_date:
            query = query.filter(ServiceRequest.created_at <= end_date)

        if type_of_service and type_of_service != 'todos':
            query = query.filter(Service.type_of_service == type_of_service)

        # Ordenar por fecha de creación descendente
        query = query.order_by(ServiceRequest.created_at.desc())

        # Paginar los resultados
        paginated_service_requests = query.paginate(page=page, per_page=per_page, error_out=False) 

        return paginated_service_requests