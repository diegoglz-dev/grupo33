from src.core.database import db
from src.core.insts.institution import Institution
from src.core.auth import Usuario_tiene_rol
from datetime import timedelta


def list_insts():
    return Institution.query.all()


def list_institutions(page, per_page):
    return Institution.query.paginate(
        page=page, per_page=per_page, error_out=False)


def list_insts_paginate(page, per_page):
    return Institution.query.paginate(
        page=page, per_page=per_page, error_out=False)


def create_inst(**kwargs):
    inst = Institution(**kwargs)
    db.session.add(inst)
    db.session.commit()

    return inst


def find_inst_by_id(id):
    return Institution.query.filter_by(id=id).first()


def find_inst_by_name(name):
    return Institution.query.filter_by(name=name).first()


def check_inst(name):
    inst = find_inst_by_name(name)

    if inst:
        return inst
    else:
        return None


def update_inst(inst, **kwargs):
    inst.name = kwargs['name']
    inst.info = kwargs['info']
    inst.direccion = kwargs['direccion']
    inst.localizacion = kwargs['localizacion']
    inst.web = kwargs['web']
    inst.palabras_clave = kwargs['palabras_clave']
    inst.dias_horarios = kwargs['dias_horarios']
    inst.contacto = kwargs['contacto']
    inst.habilitado = kwargs['habilitado']
    db.session.commit()

    return inst


def delete_inst(inst):
    db.session.delete(inst)
    db.session.commit()


def activate_inst(inst):
    inst = Institution.query.get(inst)
    if inst:
        inst.habilitado = True
        db.session.commit()

    return inst


def deactivate_inst(inst):
    inst = Institution.query.get(inst)
    if inst:
        inst.habilitado = False
        db.session.commit()

    return inst


def es_dueño(current_user, institution_id):
    # Verifica si el usuario es el dueño de la institución
    es_dueno = Usuario_tiene_rol.query.filter_by(
        usuario_id=current_user.id,
        rol_id=3,  # Rol Dueño
        institucion_id=institution_id
    ).first()

    return es_dueno


def mis_instituciones_como_dueño(current_user, page, per_page):
    # Obtener todas las instituciones del usuario
    institutions = Usuario_tiene_rol.query.filter_by(
        usuario_id=current_user.id,
        rol_id=3  # Rol Dueño
    ).paginate(
        page=page, per_page=per_page, error_out=False)

    return institutions


def remove_user_from_inst(user, institution):
    # Elimina un usuario de una institución
    user = Usuario_tiene_rol.query.filter_by(
        usuario_id=user.id,
        institucion_id=institution.id
    ).first()

    if user:
        db.session.delete(user)
        db.session.commit()

    return user


def find_inst_by_service(id):
    # Obtiene el detalle de una institución específica pasandole por parámetro el id del servicio.
    inst = Institution.query.join(Institution.services).filter_by(id=id).first()

    return inst


def average_resolution_time(institution):
    """
    Calcula el tiempo promedio de resolución para una institución.

    Args:
        - institution: La institución para la cual se calculará el tiempo promedio de resolución.

    Returns:
        - dict: Un diccionario que contiene el tiempo promedio de resolución en días, o None si no hay solicitudes finalizadas.
    """
    # Obtener todas las solicitudes de la institución
    service_requests = institution.get_service_requests()

    # Filtrar las solicitudes que han sido finalizadas
    completed_requests = [request for request in service_requests if request.last_state.name == 'FINALIZADA']
    
    # Verificar si hay solicitudes finalizadas
    if not completed_requests:
        return None

    # Calcular el tiempo promedio de resolución en días
    total_time = sum([request.close_date - request.creation_date for request in completed_requests], timedelta())
    average_time = total_time / len(completed_requests)

    # Obtener el tiempo promedio en días
    average_time_days = average_time.days + average_time.seconds / (24 * 3600)

    return {"average_resolution_time_days": average_time_days}
