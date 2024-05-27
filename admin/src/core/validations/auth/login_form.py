from wtforms_alchemy import ModelForm, DataRequired, Length
from wtforms import StringField, PasswordField, validators


class LoginForm(ModelForm):
    email = StringField('email', [
        DataRequired(
            message='El correo electrónico es obligatorio.'),
        validators.Email(message='El correo electrónico no es válido.')
    ])
    password = PasswordField('password', [
        DataRequired(),
        Length(min=6, max=25),
    ])
