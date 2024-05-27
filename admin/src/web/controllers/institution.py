# Flask
from flask import Blueprint, render_template, request, redirect, url_for, flash
# Helpers (Decoradores)
from src.web.helpers.auth import login_required
from src.web.helpers.activated import is_activated
from src.web.helpers.maintenance import is_in_maintenance_mode
# Modulo de consultas
from src.core import insts
from src.core import auth
from src.web.helpers.auth import permission_required
from src.core.insts import Institution
from flask import session
from src.core.auth import Usuario_tiene_rol
from src.core.database import db
from src.core.auth import User
from sqlalchemy import and_
from sqlalchemy.orm import contains_eager
from src.core import configuration
from src.core.validations.intitutions.institution_store import InstitutionStoreForm


institution_bp = Blueprint("institutions", __name__,
                           url_prefix="/instituciones")


@institution_bp.get("/page=<int:page>")
@login_required
@is_activated
@is_in_maintenance_mode
@permission_required("institution_index")
def index(page=1):
    per_page = configuration.get_configuration().per_page
    institutions = insts.list_institutions(page, per_page)
    url_host = request.url.split('/instituciones')[0]
    return render_template("institutions/index.html", url_host=url_host, institutions=institutions)


@institution_bp.get("/create")
@permission_required("institution_new")
@login_required
@is_activated
@is_in_maintenance_mode
def create():
    url_host = request.url.split('/instituciones')[0]
    form = InstitutionStoreForm()
    return render_template("institutions/create.html", url_host=url_host, form=form)


@institution_bp.post("/store")
@permission_required("institution_new")
@login_required
@is_activated
@is_in_maintenance_mode
def store():
    form = InstitutionStoreForm(request.form)
    if form.validate():
        insts.create_inst(
            name=form.name.data,
            info=form.info.data,
            direccion=form.direccion.data,
            localizacion=form.localizacion.data,
            web=form.web.data,
            palabras_clave=form.palabras_clave.data,
            dias_horarios=form.dias_horarios.data,
            contacto=form.contacto.data,
            habilitado=True,
        )
        flash("Institución creada correctamente", "success")
        return redirect(url_for("institutions.index", page=1))
    else:
        url_host = request.url.split('/instituciones')[0]
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error en el campo {field}: {error}', 'danger')
        return render_template("institutions/create.html", url_host=url_host, form=form)


@institution_bp.get("/edit/<int:id>")
@permission_required("institution_update")
@login_required
@is_activated
@is_in_maintenance_mode
def edit(id):
    institution = Institution.query.get(id)

    if institution is None:
        flash("Institución no encontrada", "danger")
        return redirect(url_for("institutions.index", page=1))

    current_user = session.get("user")

    # Verifica si el usuario es el dueño de la institución
    es_dueno = insts.es_dueño(current_user, id)

    if es_dueno:
        url_host = request.url.split('/instituciones')[0]
        form = InstitutionStoreForm(obj=institution)
        return render_template("institutions/edit.html", url_host=url_host, institution=institution, form=form)
    else:
        flash("No tienes permisos para editar esta institución", "danger")
        return redirect(url_for("institutions.index", page=1))


@institution_bp.post("/update/<int:id>")
@permission_required("institution_update")
@login_required
@is_activated
@is_in_maintenance_mode
def update(id):
    institution = insts.find_inst_by_id(id)
    if institution is None:
        flash("Institución no encontrada", "danger")
        return redirect(url_for("institutions.index", page=1))

    form = InstitutionStoreForm(request.form)
    if form.validate():
        insts.update_inst(institution,
                          name=form.name.data,
                          info=form.info.data,
                          direccion=form.direccion.data,
                          localizacion=form.localizacion.data,
                          web=form.web.data,
                          palabras_clave=form.palabras_clave.data,
                          dias_horarios=form.dias_horarios.data,
                          contacto=form.contacto.data,
                          habilitado=True,
                          )
        flash("Institución actualizada correctamente", "success")
        return redirect(url_for("institutions.index", page=1))
    else:
        url_host = request.url.split('/instituciones')[0]
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error en el campo {field}: {error}', 'danger')
        return render_template("institutions/edit.html", url_host=url_host, institution=institution, form=form)


@institution_bp.post("/delete/<int:id>")
@permission_required("institution_destroy")
@login_required
@is_activated
@is_in_maintenance_mode
def delete(id):
    institution = insts.find_inst_by_id(id)
    if institution is None:
        return redirect(url_for("institutions.index", page=1))

    current_user = session.get("user")

    # Verifica si el usuario es el dueño de la institución que desea eliminar
    es_dueno = insts.es_dueño(current_user, id)

    if es_dueno:
        # Obtener todas las relaciones relacionadas con la institución
        relaciones = auth.obtener_relaciones(institution.id)

        auth.eliminar_inst_y_relaciones(relaciones, institution)

        flash("Institución eliminada correctamente", "success")
        return redirect(url_for("institutions.index", page=1))
    else:
        flash("No tienes permisos para eliminar esta institución", "danger")
        return redirect(url_for("institutions.index", page=1))


@institution_bp.get("/show/<int:id>")
@permission_required("institution_show")
@login_required
@is_activated
@is_in_maintenance_mode
def show(id):
    institution = insts.find_inst_by_id(id)
    if institution is None:
        return redirect(url_for("institutions.index", page=1))

    url_host = request.url.split('/instituciones')[0]

    return render_template("institutions/show.html", url_host=url_host, institution=institution)


@institution_bp.get("/search")
@login_required
@is_activated
@is_in_maintenance_mode
def search():
    params = request.args
    institutions = insts.search_insts(params["q"])
    url_host = request.url.split('/instituciones')[0]
    return render_template("institutions/index.html", url_host=url_host, institutions=institutions)


@institution_bp.post("/activate/<int:id>")
@permission_required("institution_activate")
@login_required
@is_activated
@is_in_maintenance_mode
def activate(id):
    institution = insts.find_inst_by_id(id)
    if institution is None:
        return redirect(url_for("institutions.index", page=1))

    insts.activate_inst(id)

    flash("Institución activada correctamente", "success")

    return redirect(url_for("institutions.index", page=1))


@institution_bp.post("/deactivate/<int:id>")
@permission_required("institution_deactivate")
@login_required
@is_activated
@is_in_maintenance_mode
def deactivate(id):
    institution = insts.find_inst_by_id(id)
    if institution is None:
        return redirect(url_for("institutions.index", page=1))

    insts.deactivate_inst(id)

    flash("Institución desactivada correctamente", "success")

    return redirect(url_for("institutions.index", page=1))


@institution_bp.route("/my_institutions/page=<int:page>", methods=["GET"])
@login_required
@is_activated
@is_in_maintenance_mode
@permission_required("user_index_dueño")
def my_institutions(page=1):
    current_user = session.get("user")
    per_page = configuration.get_configuration().per_page
    # Obtengo todas las instituciones del usuario
    institutions = insts.mis_instituciones_como_dueño(
        current_user, page, per_page)

    url_host = request.url.split('/instituciones')[0]
    return render_template("institutions/my_institutions.html", url_host=url_host, my_institutions=institutions)


@institution_bp.route("/users_my_institution/<int:id>/page=<int:page>", methods=["GET"])
@permission_required("user_index_dueño")
@login_required
@is_activated
@is_in_maintenance_mode
def users_my_institution(id, page=1):
    url_host = request.url.split('/instituciones')[0]
    per_page = configuration.get_configuration().per_page
    # Obtengo todos los usuarios y sus roles en la institución
    users_with_roles = auth.users_and_roles(id, page, per_page=per_page)

    # Obtengo el usuario actual (dueño) para no mostrarlo en la lista
    current_user = session.get("user")

    # Filtra y excluye al dueño
    users_to_display = [
        user for user in users_with_roles if user.id != current_user.id]

    return render_template("institutions/users_my_institution.html", users_with_roles=users_with_roles, url_host=url_host, id=id)


@institution_bp.route("/delete_user/<int:id>/<int:institution_id>", methods=["POST"])
@permission_required("user_destroy_dueño")
@login_required
@is_activated
@is_in_maintenance_mode
def delete_user_my_inst(id, institution_id):
    user_to_delete = auth.find_user_by_id(id)
    institution = insts.find_inst_by_id(institution_id)
    current_user = session.get("user")

    if not user_to_delete or not institution:
        flash("Usuario o institución no encontrados.", "error")
    elif current_user == user_to_delete:
        flash("No puedes eliminarte a ti mismo de la institución.", "error")
    elif not insts.es_dueño(current_user, institution_id):
        flash("No tienes permiso para eliminar a este usuario de la institución.", "error")
    else:
        insts.remove_user_from_inst(user_to_delete, institution)
        flash(
            f"Usuario {user_to_delete.first_name} eliminado de la institución.", "success")

    return redirect(url_for("institutions.users_my_institution", id=institution_id))


@institution_bp.route("/edit_user_role/<int:id>/<int:user_id>", methods=["GET", "POST"])
@permission_required("user_update_dueño")
@login_required
@is_activated
@is_in_maintenance_mode
def edit_user_rol(id, user_id):
    url_host = request.url.split('/instituciones')[0]
    # Recupera la institución y el usuario correspondientes
    institution = insts.find_inst_by_id(id)
    user = auth.find_user_by_id(user_id)

    if request.method == "POST":
        # Obtén el nuevo rol del formulario
        new_role_id = request.form.get("new_role")

        # Actualiza el rol del usuario en la institución
        success, message = auth.update_user_rol_in_institution(
            user, institution, new_role_id)

        if success:
            flash(message, "success")
        else:
            flash(message, "danger")

    roles = auth.get_roles()
    return render_template("institutions/edit_user_rol.html", institution=institution, url_host=url_host, user=user, roles=roles)


@institution_bp.route("/create_assignment", methods=["GET", "POST"])
@permission_required("user_assign_rol")
@login_required
@is_activated
@is_in_maintenance_mode
def create_assignment():
    url_host = request.url.split('/instituciones')[0]

    if request.method == "POST":
        user_id = request.form.get("user")
        institution_id = request.form.get("institution")
        role_id = request.form.get("role")

        # Obtener los objetos de modelo reales a partir de los IDs
        user = auth.find_user_by_id(user_id)
        institution = insts.find_inst_by_id(institution_id)
        role = auth.find_rol_by_id(role_id)

        # Realiza la asignación
        success, message = auth.add_rol_to_user_for_institution2(
            user.id, role.id, institution.id)

        if success:
            flash(message, "success")
        else:
            flash(message, "danger")

    users = auth.get_users()
    institutions = insts.list_insts()
    roles = auth.get_roles()

    return render_template("institutions/create_assignment.html", url_host=url_host, users=users, institutions=institutions, roles=roles)
