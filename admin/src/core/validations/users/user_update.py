from wtforms_alchemy import ModelForm, DataRequired, Length
from wtforms import StringField, PasswordField, BooleanField, validators
from src.core.auth import User

# Cuando se actualiza mail o username (y lo ingresado se encuentra en la base de datos)
# se captura el error desde el controlador y se muestra un mensaje de error al usuario.


class UserUpdateForm(ModelForm):
    first_name = StringField(
        'first_name', [DataRequired(), Length(min=1, max=50)])
    last_name = StringField(
        'last_name', [DataRequired(), Length(min=1, max=50)])
    username = StringField(
        'username', [DataRequired(), Length(min=4, max=25)])
    email = StringField('email', [
        DataRequired(
            message='El correo electrónico es obligatorio.'),
        validators.Email(message='El correo electrónico no es válido.')
    ])
    password = PasswordField('password', [
        validators.EqualTo('password_confirmation',
                           message='Las contraseñas deben coincidir'),
        validators.Optional(), validators.Length(min=8, max=25)
    ])
    password_confirmation = PasswordField('Confirmar Contraseña')
    active = BooleanField('active')
