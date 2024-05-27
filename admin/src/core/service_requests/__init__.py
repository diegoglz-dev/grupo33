from src.core.database import db
from src.core.service_requests.service_request import ServiceRequest, StateRequest, EventRequest, NoteRequest
from collections import defaultdict


def create_service_request(**kwargs):
    serv = ServiceRequest(**kwargs)
    db.session.add(serv)
    db.session.commit()
    return serv


def create_state_request(**kwargs):
    state = StateRequest(**kwargs)
    db.session.add(state)
    db.session.commit()
    return state


def update_service_request(serv, **kwargs):
    serv.close_date = kwargs['close_date']
    db.session.commit()
    return serv


def create_note_request(**kwargs):
    note = NoteRequest(**kwargs)
    db.session.add(note)
    db.session.commit()
    return note


def create_event_service_request(**kwargs):
    event = EventRequest(**kwargs)
    db.session.add(event)
    db.session.commit()
    return event


def delete_service_request(reque):
    db.session.delete(reque)
    db.session.commit()


# esta funcion la voy a borrar...... no la uso
def list_service_requests(id_serv, page, per_page):
    return ServiceRequest.query.filter_by(service_id_id=id_serv).paginate(page=page, per_page=per_page, error_out=False)


def find_service_request_by_id(id):
    return ServiceRequest.query.filter_by(id=id).first()


def find_event_request_by_id(id):
    return EventRequest.query.filter_by(id=id).first()


def find_state_request_by_id(id):
    return StateRequest.query.filter_by(id=id).first()


def solicitudes_por_estado():
    # Obtén todas las solicitudes con sus estados
    solicitudes = ServiceRequest.query.all()

    # Inicializa un diccionario para contar las solicitudes por estado
    solicitudes_por_estado = defaultdict(int)

    # Contabiliza las solicitudes por estado
    for solicitud in solicitudes:
        estado = solicitud.last_state
        if estado:
            solicitudes_por_estado[estado.name] += 1

    return dict(solicitudes_por_estado)
