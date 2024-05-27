from wtforms_alchemy import ModelForm, DataRequired, Length
from wtforms import StringField, validators
from wtforms import TextAreaField
from src.core.auth import Institution


class InstitutionStoreForm(ModelForm):
    name = StringField('name', [DataRequired(), Length(min=1, max=255)])
    info = TextAreaField('info', [DataRequired()])
    direccion = StringField(
        'direccion', [DataRequired(), Length(min=1, max=255)])
    localizacion = StringField(
        'localizacion', [DataRequired(), Length(min=1, max=255)])
    web = StringField('web', [DataRequired(), Length(min=1, max=255)])
    palabras_clave = StringField(
        'palabras_clave', [DataRequired(), Length(min=1, max=255)])
    dias_horarios = StringField(
        'dias_horarios', [DataRequired(), Length(min=1, max=255)])
    contacto = StringField(
        'contacto', [DataRequired(), Length(min=1, max=255)])
