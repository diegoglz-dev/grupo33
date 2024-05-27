from flask import Blueprint
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import session
from src.core import auth
from src.core.validations.auth.login_form import LoginForm
from src.core.validations.users.user_store import UserStoreForm
from src.web.oauth_config import oauth

from src.web.mail import send_activation_email

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.get("/login")
def login():
    if not session.get("user"):
        form = LoginForm()
        return render_template("auth/login.html", form=form)
    else:
        return redirect(url_for("dash.dashboard"))


@auth_bp.post("/authenticate")
def authenticate():
    form = LoginForm(request.form)
    user = auth.check_user(
        form.data["email"], form.data["password"])
    if not user:
        flash("Usuario, correo o contraseña incorrecta.", "danger")
        return redirect(url_for("auth.login", form=form))

    session['name'] = user.first_name
    session['last_name'] = user.last_name
    session["user"] = user
    session["email"] = user.email
    flash("La sesión se inició correctamente.", "success")
    return redirect(url_for("dash.dashboard"))


@auth_bp.get("/logout")
def logout():
    if session.get("user"):
        del session["user"]
        session.clear()
        flash("La sesión se cerró correctamente.", "info")
    else:
        flash("No hay sesión iniciada.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.get("/register")
def register():
    if not session.get("user"):
        form = UserStoreForm()
        return render_template("auth/register.html", form=form)
    else:
        return redirect(url_for("dash.dashboard"))


@auth_bp.post("/registration")
def registration():
    form = UserStoreForm(request.form)
    if form.validate():
        user = auth.create_user(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            active=False,
        )
        # Enviar email de activación
        try:
            send_activation_email(user)
            flash(
                "Bienvenido, por favor verifique su email para comenzar a operar", "success")
            return redirect(url_for("auth.login"))
        except Exception as e:
            flash("Ocurrió un error al enviar el email de activación", "danger")
            return redirect(url_for("auth.register"))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error en el campo {field}: {error}', 'danger')

        form.populate_obj(request.form)
        return render_template("auth/register.html", form=form)


@auth_bp.get('/activate/<token>')
def activate_account(token):
    # Busca el usuario con el token proporcionado
    user = auth.find_user_by_token(token)

    if user:
        # Marca al usuario como activado
        auth.user_activate(user)
        flash("Tu cuenta ha sido activada. Inicia sesión, para comenzar", "success")
        return redirect(url_for('auth.login'))
    else:
        flash("Token de activación inválido o expirado. Comunicate con el administrador.", "danger")
        return redirect(url_for('auth.login'))


@auth_bp.get('/login-google')
def login_google():
    redirect_uri = url_for('auth.auth_google', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@auth_bp.get('/login-google/callback')
def auth_google():
    token = oauth.google.authorize_access_token()
    email_google = token['userinfo']['email']
    user = auth.find_user_by_email(email_google)
    if user is None:
        # Separar el nombre completo en nombre y apellido
        full_name = token['userinfo']['name']
        if full_name:
            first_name, *last_name_parts = full_name.split()
            last_name = ' '.join(last_name_parts)

        user = auth.create_user(
            first_name=first_name,
            last_name=last_name,
            username=auth.generate_unique_username(first_name, last_name),
            email=email_google,
            password="password",
            active=True,
        )

    session['name'] = user.first_name
    session['last_name'] = user.last_name
    session["user"] = user
    session["email"] = user.email
    flash("La sesión se inició correctamente.", "success")
    return redirect(url_for("dash.dashboard"))
