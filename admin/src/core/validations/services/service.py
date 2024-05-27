from wtforms_alchemy import ModelForm, Length
from wtforms import StringField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired
from src.core.services import Service, ServiceType


class ServiceForm(ModelForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(min=1, max=50)])
    description = TextAreaField('Descripcion', validators=[DataRequired(), Length(min=1, max=200)])
    keywords = StringField('Palabras clave', validators=[DataRequired(), Length(min=1, max=150)])
    type_of_service = SelectField('Tipo de servicio', 
                                  choices=[(str(type.value), type.value) for type in ServiceType], 
                                  validators=[DataRequired()])
    enabled = BooleanField('Habilitado', default=True)



