# Flask
from flask import Blueprint
from flask import render_template, redirect, url_for
from flask import request
from src.core import auth
from src.core import insts
from src.web.helpers.auth import login_required
from src.web.helpers.auth import permission_required
from flask import flash
from src.core.auth import Rol
from flask import session
from flask import flash
from flask import session
# Helpers (Decoradores)
from src.web.helpers.auth import login_required
from src.web.helpers.auth import permission_required
from src.web.helpers.maintenance import is_in_maintenance_mode
from src.web.helpers.activated import is_activated
# Validaciones
from src.core.validations.users.user_store import UserStoreForm
from src.core.validations.users.user_update import UserUpdateForm
from sqlalchemy.exc import IntegrityError
from src.core.auth import Usuario_tiene_rol
from src.core.insts import Institution
from src.core import insts
# Modulo de consultas
from src.core import auth
from src.core import configuration
# Modelos
from src.core.auth import Rol
from src.core.insts import Institution
from src.core.auth import User


user_bp = Blueprint("users", __name__, url_prefix="/usuarios")


@user_bp.get("/result")
@login_required
@permission_required('user_index')
@is_activated
@is_in_maintenance_mode
@permission_required('user_index')
def search_result():
    email = request.args.get('email')
    active = request.args.get('active')
    per_page = configuration.get_configuration().per_page

    users = auth.users_filtered_by_email_or_active(
        email, active, page=1, per_page=per_page)

    url_host = request.url.split('/usuarios')[0]
    return render_template("users/index.html", url_host=url_host, users=users)


@user_bp.get("/page=<int:page>")
@login_required
@is_activated
@is_in_maintenance_mode
@permission_required('user_index')
def index(page=1):
    per_page = configuration.get_configuration().per_page
    users = auth.list_users(page, per_page)
    url_host = request.url.split('/usuarios')[0]
    return render_template("users/index.html", url_host=url_host, users=users)


@user_bp.get("/create")
@login_required
@is_activated
@is_in_maintenance_mode
@permission_required('user_new')
def create():
    url_host = request.url.split('/usuarios')[0]
    form = UserStoreForm()
    return render_template("users/create.html", url_host=url_host, form=form)


@user_bp.post("/store")
@login_required
@permission_required('user_new')
@is_activated
@is_in_maintenance_mode
@permission_required('user_new')
def store():
    form = UserStoreForm(request.form)
    if form.validate():
        auth.create_user(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            active=True,
        )

        flash("Usuario creado correctamente", "success")

        return redirect(url_for("users.index", page=1))
    else:
        url_host = request.url.split('/usuarios')[0]
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error en el campo {field}: {error}', 'danger')

        form.populate_obj(request.form)
        return render_template("users/create.html", url_host=url_host, form=form)


@user_bp.get("/edit/<int:id>")
@login_required
@permission_required('user_update')
@is_activated
@is_in_maintenance_mode
@permission_required('user_update')
def edit(id):
    user = auth.find_user_by_id(id)
    if user is None:
        return redirect(url_for("users.index", page=1))

    url_host = request.url.split('/usuarios')[0]
    form = UserUpdateForm(obj=user)
    return render_template("users/edit.html", url_host=url_host, user=user, form=form)


@user_bp.post("/update/<int:id>")
@login_required
@permission_required('user_update')
@is_activated
@is_in_maintenance_mode
@permission_required('user_update')
def update(id):
    url_host = request.url.split('/usuarios')[0]
    user = auth.find_user_by_id(id)
    if user is None:
        return redirect(url_for("users.index", page=1))

    # form = UserUpdateForm(obj=user)
    form = UserUpdateForm(request.form)

    if form.validate():
        try:
            # Check if password is the same
            if form.password.data == "":
                password = user.password
            else:
                password = form.password.data

            auth.update_user(user,
                             first_name=form.first_name.data,
                             last_name=form.last_name.data,
                             username=form.username.data,
                             email=form.email.data,
                             password=password,
                             active=form.active.data
                             )

            flash("Usuario actualizado correctamente", "success")

            return redirect(url_for("users.index", page=1))
        except IntegrityError:
            auth.rollback()
            flash("Error: El email y/o username ya están en uso.", "danger")
            return render_template("users/edit.html", url_host=url_host, user=user, form=form)
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error en el campo {field}: {error}', 'danger')

        form.populate_obj(request.form)
        return render_template("users/edit.html", url_host=url_host, user=user, form=form)


@user_bp.post("/delete/<int:id>")
@login_required
@permission_required('user_destroy')
@is_activated
@is_in_maintenance_mode
@permission_required('user_destroy')
def delete(id):
    user = auth.find_user_by_id(id)
    if user is None:
        return redirect(url_for("users.index", page=1))

    auth.delete_user(user)

    flash("Usuario eliminado correctamente", "success")

    return redirect(url_for("users.index", page=1))



@login_required
@is_activated
@is_in_maintenance_mode
@user_bp.route("/add_user_institution/<int:id>", methods=["GET", "POST"])
def asignar_usuario_rol(id):

    url_host = request.url.split('/instituciones')[0]
    
    current_user = session.get("user")
    
    if current_user is None:
        # El usuario no inició sesión
        flash("Debes iniciar sesión para acceder a esta función", "danger")
        return redirect("/login")
    
    # Viendo que el usuario tenga el rol "Dueño" en la institución especificada
    es_dueno = insts.es_dueño(current_user, id)
    
    if not es_dueno:
        flash("No tienes permisos para acceder a esta institución", "danger")
        return redirect("/login")

    if request.method == "POST":
        # Obtén los datos del formulario
        user_email = request.form.get("user_email")
        rol_id = request.form.get("rol")

        # Verifica si los datos son válidos
        if not user_email or not rol_id:
            flash("Faltan parámetros", "danger")
        else:
            # Consulta la base de datos para obtener el usuario por correo electrónico
            user = auth.find_user_by_email(user_email)
            rol = auth.find_rol_by_id(rol_id)
            
            if user and rol:
                if user.id != current_user.id:
                    # Asigna el rol al usuario en la institución
                    auth.add_rol_to_user_for_institution(user, rol, id)
                    flash("Rol asignado correctamente", "success")
                else:
                    flash("No puedes asignarte un rol a vos mismo", "danger")
            else:
                flash("Usuario no válido o rol no válido", "danger")

    roles = auth.get_roles()
    institucion = insts.find_inst_by_id(id)
    
    return render_template("users/add_user_institution.html", roles=roles, url_host=url_host, institucion=institucion)

