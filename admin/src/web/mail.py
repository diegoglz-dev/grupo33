from flask_mail import Mail, Message
from flask import render_template, url_for
from src.core.auth import set_user_activation_token
import secrets

mail = Mail()


def init_app(app):
    # CONFIG EMAIL
    mail.init_app(app)


def generate_activation_token():
    token = secrets.token_hex(16)
    return token


def send_activation_email(user):
    token = generate_activation_token()
    set_user_activation_token(user, token)
    activation_link = url_for('auth.activate_account',
                              token=token, _external=True)

    msg = Message('[CIDEPINT] Activa tu cuenta',
                  sender='info@cidepint.com', recipients=[user.email])
    msg.html = render_template(
        'mail/activation_email.html', activation_link=activation_link)

    mail.send(msg)
