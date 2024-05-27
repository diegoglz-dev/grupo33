# Flask
from flask import Blueprint, render_template, request, redirect, url_for
from flask import session
from flask import flash
from flask import abort
# Helpers
from src.web.helpers.auth import login_required
from src.web.helpers.permission import permission_required
from src.web.helpers.maintenance import is_in_maintenance_mode
from src.web.helpers.activated import is_activated
# Validaciones
from src.core.validations.services.service import ServiceForm
# Modulo consultas
from src.core import services
from src.core import auth, insts
from src.core import configuration
from src.core.services.service import ServiceType


services_bp = Blueprint("services", __name__, url_prefix="/servicios")


@services_bp.get("/<int:id_inst>/page=<int:page>")
@permission_required("service_index")
@login_required
@is_activated
@is_in_maintenance_mode
def index(id_inst, page=1):
    per_page = configuration.get_configuration().per_page

    institution = insts.find_inst_by_id(id_inst)

    servs = services.list_services(id_inst, page, per_page)

    url_host = request.url.split('/servicios')[0]
    return render_template("services/index.html", url_host=url_host, servs=servs, inst=id_inst)


@services_bp.get("/create/<int:id_inst>")
@permission_required("service_new")
@login_required
@is_activated
@is_in_maintenance_mode
def create(id_inst):
    institution = insts.find_inst_by_id(id_inst)
    form = ServiceForm()
    url_host = request.url.split('/servicios')[0]
    return render_template("services/create.html", url_host=url_host, inst=id_inst, form=form)


@services_bp.post("/store/<int:id_inst>")
@permission_required("service_new")
@login_required
@is_activated
@is_in_maintenance_mode
def store(id_inst):
    institution = insts.find_inst_by_id(id_inst)

    form = ServiceForm(request.form)
    url_host = request.url.split('/servicios')[0]

    if form.validate():
        services.create_service(
            name=form.name.data,
            description=form.description.data,
            keywords=form.keywords.data,
            type_of_service=ServiceType(form.type_of_service.data),
            institution_id=id_inst,
            enabled=form.enabled.data,
        )

        flash("El servicio se ha creado correctamente", "success")
        redirect(url_for("services.index", id_inst=id_inst, page=1))
    else:
        url_host = request.url.split('/servicios')[0]
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error en el campo {field}: {error}', 'danger')

        form.populate_obj(request.form)
        return render_template("services/create.html", url_host=url_host, inst=id_inst, form=form)

    return redirect(url_for("services.index", id_inst=id_inst, page=1))


@services_bp.get("/edit/<int:id_inst>/<int:id_serv>")
@permission_required("service_update")
@login_required
@is_activated
@is_in_maintenance_mode
def edit(id_inst, id_serv):
    serv = services.find_service_by_id(id_serv)
    if serv is None:
        return redirect(url_for("services.index", id_inst=id_inst, page=1))

    form = ServiceForm(obj=serv)
    url_host = request.url.split('/servicios')[0]
    return render_template("services/edit.html", url_host=url_host, serv=serv, inst=id_inst, form=form)


@services_bp.post("/update/<int:id_inst>/<int:id_serv>")
@permission_required("service_update")
@login_required
@is_activated
@is_in_maintenance_mode
def update(id_inst, id_serv):
    serv = services.find_service_by_id(id_serv)
    if serv is None:
        return redirect(url_for("services.index", id_inst=id_inst, page=1))

    form = ServiceForm(request.form)

    url_host = request.url.split('/servicios')[0]

    if form.validate():
        services.update_service(serv,
                                name=form.name.data,
                                description=form.description.data,
                                keywords=form.keywords.data,
                                type_of_service=ServiceType(
                                    form.type_of_service.data),
                                institution_id=id_inst,
                                enabled=form.enabled.data,
                                )

        flash("El servicio se ha creado correctamente", "success")

    return redirect(url_for("services.index", id_inst=id_inst, page=1, url_host=url_host))



@services_bp.post("/delete/<int:id_inst>/<int:id_serv>")
@permission_required("service_destroy")
@login_required
@is_activated
@is_in_maintenance_mode
def delete(id_inst, id_serv):
    serv = services.find_service_by_id(id_serv)
    if serv is None:
        return redirect(url_for("services.index", id_inst=id_inst))

    services.delete_service(serv)
    flash("El servicio se ha eliminado correctamente", "success")
    return redirect(url_for("services.index", id_inst=id_inst, page=1))


@services_bp.get("/show/<int:id_inst>/<int:id_serv>")
@permission_required("service_show")
@login_required
@is_activated
@is_in_maintenance_mode
def show(id_inst, id_serv):
    serv = services.find_service_by_id(id_serv)
    if serv is None:
        return redirect(url_for("services.index", id_inst=id_inst, page=1))

    url_host = request.url.split('/servicios')[0]

    return render_template("services/show.html", url_host=url_host, serv=serv, inst=id_inst)
