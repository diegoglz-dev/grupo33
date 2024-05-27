from sqlalchemy import func
from sqlalchemy import or_
from src.core.database import db
from src.core.services.service import Service, ServiceType
from src.core.service_requests import ServiceRequest



def list_service_by_name_type1(name, type, page, per_page):
    if type:
        return Service.query.filter_by(name=name).filter_by(type_of_service=type).paginate(page=page, per_page=per_page, error_out=False)
    else:
        return Service.query.filter_by(name=name).paginate(page=page, per_page=per_page, error_out=False)
    
    


def list_service_by_name_type(name, type, page, per_page):
    query = Service.query

    if name:
        name_filter = func.lower(Service.name).like(func.lower(f"%{name}%"))
        description_filter = func.lower(Service.description).like(func.lower(f"%{name}%"))
        keywords_filter = func.lower(Service.keywords).like(func.lower(f"%{name}%"))

        query = query.filter(or_(name_filter, description_filter, keywords_filter))
        
    if type: 
        query = query.filter(Service.type_of_service == type)

    filtered_services = query.paginate(
        page=page, per_page=per_page, error_out=False)
    
    return filtered_services



def list_services(id_inst, page, per_page):
    return Service.query.filter_by(institution_id=id_inst).paginate(page=page, per_page=per_page, error_out=False)

def list_types_of_services():
    types_services= [str(type.value) for type in ServiceType]
    return types_services

def create_service(**kwargs):
    serv = Service(**kwargs)
    db.session.add(serv)
    db.session.commit()
    return serv

def find_service_by_name_and_institution(name_service, id_inst):
    return Service.query.filter_by(institution_id=id_inst, name=name_service).first()

def find_service_by_id(id):
    return Service.query.filter_by(id=id).first()

def find_service_by_name(name):
    return Service.query.filter_by(name=name).first()


def check_service(name):
    serv = find_service_by_name(name)

    if serv:
        return serv
    else:
        return None
    
def update_service(serv, **kwargs):
    serv.name = kwargs['name']
    serv.description = kwargs['description']
    serv.keywords = kwargs['keywords']
    #serv.authorized_centers = kwargs['authorized_centers']
    serv.type_of_service = kwargs['type_of_service']
    serv.enabled = kwargs['enabled']
    db.session.commit()
    return serv

def delete_service(serv):
    db.session.delete(serv)
    db.session.commit()


def services_most_requested():
    servicios_solicitados = (
        db.session.query(
            Service.name,
            Service.type_of_service,
            func.count(ServiceRequest.id).label('total_requests')
        )
        .join(ServiceRequest, Service.id == ServiceRequest.service_id)
        .group_by(Service.id, Service.name, Service.type_of_service)  
        .order_by(func.count(ServiceRequest.id).desc())
        .limit(3)
        .all()
    )

    # Convertir las tuplas a un formato más manejable
    service_data = [
        {
            "name": service[0],
            "type_of_service": service[1],
            "total_requests": service[2]
        }
        for service in servicios_solicitados
    ]

    return service_data




