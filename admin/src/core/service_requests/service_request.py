from src.core.database import db
from datetime import datetime


class StateRequest(db.Model):
        __tablename__ = "state_requests"
        id = db.Column(db.Integer, primary_key=True, unique=True)
    
        name = db.Column(db.String(255), nullable=False)
        
        events = db.relationship("EventRequest", back_populates="state_request")

        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(
            db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
         

class EventRequest(db.Model):
        """
        Esta clase representa los eventuales estados por los que puede 
        pasar la solicitud. Cada evento está relacionada con una solicitud de 
        servicio y un estado de solicitud específicos.
    
        """
        __tablename__ = "event_requests"
        id = db.Column(db.Integer, primary_key=True, unique=True)
        observation = db.Column(db.String(255), nullable=False)
        #date = db.Column(db.DateTime, default=datetime.utcnow)
       

        service_request_id = db.Column(db.Integer, db.ForeignKey("service_requests.id"))
        service_request = db.relationship("ServiceRequest", back_populates="events")

        state_request_id = db.Column(db.Integer, db.ForeignKey("state_requests.id"))
        state_request = db.relationship("StateRequest", back_populates="events")


        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(
            db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class NoteRequest(db.Model):
        __tablename__ = "note_requests"
        id = db.Column(db.Integer, primary_key=True, unique=True)
        note = db.Column(db.String(255), nullable=False)
        
        service_request_id = db.Column(db.Integer, db.ForeignKey("service_requests.id"))
        service_request = db.relationship("ServiceRequest", back_populates="notes")
  
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(
            db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
            

class ServiceRequest(db.Model):
    """
    Esta clase representa las solicitudes a servicio.

    Atributos:
    - notes: Relación con las notas hechas a esta solicitud.
    - service: Relación con el servicio al que pertenece esta solicitud.
    
    """

    __tablename__ = "service_requests"
    id = db.Column(db.Integer, primary_key=True, unique=True)   
    
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    close_date =  db.Column(db.DateTime)

    notes = db.relationship("NoteRequest", back_populates="service_request")

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="service_requests")

    service_id = db.Column(db.Integer, db.ForeignKey("services.id"))
    service = db.relationship("Service", back_populates="requests")

    events = db.relationship("EventRequest", back_populates="service_request")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @property
    def last_state(self):
        # Obtener el último EventRequest asociado a esta ServiceRequest ordenando por created_at en orden descendente
        last_event = (
            EventRequest.query.filter_by(service_request_id=self.id)
            .order_by(EventRequest.created_at.desc())
            .first()
        )
        
        # Retornar el estado asociado al último EventRequest
        return last_event.state_request if last_event else None
    
    def get_notes_as_json(self):
        notes_list = [
            {"note": note.note, "creation_date": note.created_at.strftime("%Y-%m-%d %H:%M:%S")}
            for note in self.notes
        ]
        return {"service_request_id": self.id, "notes": notes_list}