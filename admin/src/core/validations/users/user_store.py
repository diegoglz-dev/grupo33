from wtforms_alchemy import ModelForm, DataRequired, Length, Unique
from wtforms import StringField, PasswordField, validators
from src.core.auth import User


class UserStoreForm(ModelForm):
    first_name = StringField(
        'first_name', [DataRequired(), Length(min=1, max=50)])
    last_name = StringField(
        'last_name', [DataRequired(), Length(min=1, max=50)])
    username = StringField(
        'username', [DataRequired(), Length(min=4, max=25), Unique(User.username)])
    email = StringField('email', [
        DataRequired(
            message='El correo electrónico es obligatorio.'),
        validators.Email(message='El correo electrónico no es válido.'),
        Unique(User.email)
    ])
    password = PasswordField('password', [
        DataRequired(),
        Length(min=8, max=25),
        validators.EqualTo('password_confirmation',
                           message='Las contraseñas deben coincidir')
    ])
    password_confirmation = PasswordField('password_confirmation')
