from wtforms_alchemy import ModelForm, DataRequired, Length
from wtforms import StringField, BooleanField, IntegerField


class ConfigurationUpdateForm(ModelForm):
    per_page = IntegerField('per_page', validators=[DataRequired(
        message='La cantidad de elementos por página es obligatorio.')])
    contact = StringField('contact', validators=[
                          DataRequired(message='La información de contacto es obligatoria.'), Length(min=1, max=255)])
    maintenance_message = StringField('maintenance_message', validators=[
                                      DataRequired(message='El mensaje de mantenimiento es obligatorio.'), Length(min=1, max=255)])
    enabled_site = BooleanField('enabled_site')
