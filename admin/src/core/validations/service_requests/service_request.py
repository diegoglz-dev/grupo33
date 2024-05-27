from wtforms_alchemy import ModelForm, Length
from wtforms import StringField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, Email, Optional
from src.core.service_requests import StateRequest
from src.core.services import Service, ServiceType


class EventRequestForm(ModelForm):
    observation = TextAreaField('Observaciones', validators=[DataRequired(), Length(min=1, max=200)])
    state_request_id = SelectField("Estado", choices=[], validators=[DataRequired()])
   
    def __init__(self, **kwargs):
    
        super(EventRequestForm, self).__init__(**kwargs)

        choices = []
        dtypes = StateRequest.query.all()
        for t in dtypes:
            item = (t.id, t.name)
            choices.append(item)

        self.state_request_id.choices = choices


class NoteRequestForm(ModelForm):
    observation = TextAreaField('Note', validators=[DataRequired(), Length(min=1, max=200)])


class FilterRequestForm(ModelForm):
    email = StringField('Email del Usuario', [Optional()])  
    type_of_service_choices = [(str(type.value), type.value) for type in ServiceType]
    type_of_service_choices.insert(0, ('todos', 'Todos'))  # Agregamos la opción 'Todos' al principio

    type_of_service = SelectField('Tipo de servicio', 
                                  choices=type_of_service_choices, 
                                  validators=[Optional()])
    # Puedes personalizar los mensajes de error si lo deseas
    start_date = DateField('Fecha Desde', format='%Y-%m-%d', validators=[Optional()])
    end_date = DateField('Fecha Hasta', format='%Y-%m-%d', validators=[Optional()])
    
   

    
