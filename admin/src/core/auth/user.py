from datetime import datetime
from src.core.database import db
from sqlalchemy import asc, desc, inspect
from flask_sqlalchemy import SQLAlchemy
from src.core.service_requests.service_request import ServiceRequest



class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    activation_token = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
    roles = db.relationship("Usuario_tiene_rol", back_populates="usuario")
    #Mala Práctica: Esto no debe ir acá pero por cuestiones de tiempo
    #y porque los compañeros también utilizan este módulo lo dejo hasta la próxima entrega, en pos de no romper el sistema.
    def has_permission(self, permission_name):
        # devuelvo instancia de usuario con todos sus permisos y roles.
        if self.id is not None:
        # Recorre los roles del usuario
            for user_role in User.query.get(self.id).roles:
            # Recorre los permisos del rol
                for role_permission in user_role.rol.permisos:
                # Compara el nombre del permiso
                    if role_permission.permiso.nombre == permission_name:
                        return True
        return False

    service_requests = db.relationship("ServiceRequest", back_populates="user")

    
    def get_request_paginate(self, sort=None, order=None, page=1, per_page=10):
        # Crear una consulta 
        query = db.session.query(ServiceRequest).filter_by(user_id=self.id)
    
        # Validar que la columna de orden exista
        if sort and sort in ServiceRequest.__table__.columns.keys():
            # Hago una consulta que ordene por ese criterio
                    #Hago una consulta que ordene por ese criterio
                    if order =="asc":
                        query = query.order_by(asc(sort)) 
                    else:
                        query = query.order_by(desc(sort))
                    return  query.paginate(page=page, per_page=per_page, error_out=False) 
        #En este caso no se ingreso el sort entonces no tiene sentido el order, sólo pagino
        paginated_requests = query.paginate(page=page, per_page=per_page, error_out=False) 
        return paginated_requests

    def get_request_id(self, id):
        # Crear una consulta 
        return db.session.query(ServiceRequest).filter_by(user_id=self.id, id=id).first()
            


        
class Rol(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nombre = db.Column(db.String(255), nullable=False)
    
    usuarios = db.relationship("Usuario_tiene_rol", back_populates="rol")
    permisos = db.relationship("Rol_tiene_permiso", back_populates="rol")


class Permiso(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nombre = db.Column(db.String(255), nullable=False)
    
    roles = db.relationship("Rol_tiene_permiso", back_populates="permiso")


class Usuario_tiene_rol(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    rol_id = db.Column(db.Integer, db.ForeignKey("rol.id"))
    institucion_id = db.Column(db.Integer, db.ForeignKey("institutions.id"))
    
    usuario = db.relationship("User", back_populates="roles")
    rol = db.relationship("Rol", back_populates="usuarios")
    institucion = db.relationship("Institution")

    def has_permission(self, permission_name):
        if self.id is not None:
            for role_permission in self.rol.permisos:
                if role_permission.permiso.nombre == permission_name:
                    return True
        return False


class Rol_tiene_permiso(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    rol_id = db.Column(db.Integer, db.ForeignKey("rol.id"))
    permiso_id = db.Column(db.Integer, db.ForeignKey("permiso.id"))
    
    rol = db.relationship("Rol", back_populates="permisos")
    permiso = db.relationship("Permiso", back_populates="roles")
