# Flask
from flask import Blueprint, render_template, request, redirect, url_for
from flask import session
from flask import abort, flash
from datetime import datetime
# Helpers
from src.web.helpers.auth import login_required
from src.web.helpers.permission import permission_required
from src.web.helpers.maintenance import is_in_maintenance_mode
from src.web.helpers.activated import is_activated
# Validaciones
from src.core.validations.service_requests.service_request import EventRequestForm, NoteRequestForm, FilterRequestForm
from src.core.services.service import ServiceType
# Modulo consultas
from src.core import service_requests, services, insts
from src.core import configuration


service_requests_bp = Blueprint(
    "service_requests", __name__, url_prefix="/solicitudes")


@service_requests_bp.get("/result/<int:id_inst>/page=<int:page>")
@permission_required("service_request_index")
@login_required
@is_activated
@is_in_maintenance_mode
def search_result(id_inst, page):
    per_page = configuration.get_configuration().per_page

    form = FilterRequestForm()

    institution = insts.find_inst_by_id(id_inst)
    print(request.args.get('email'))
    print(request.args.get('type_of_service'))
    print(request.args.get('start_date'))
    print(request.args.get('end_date'))

    # Por cada servicio que tenga la institutucion necesito quedarme con las solicitudes de ese servicio
    reques = institution.get_service_requests_filter_paginate(
        email=request.args.get('email'),
        start_date=request.args.get('start_date'),
        end_date=request.args.get('end_date'),
        type_of_service=request.args.get('type_of_service'),
        page=page,
        per_page=per_page)

    url_host = request.url.split('/usuarios')[0]
    return render_template("service_requests/index.html", url_host=url_host,  reques=reques, inst=id_inst, institution=institution, form=form)


@service_requests_bp.get("/<int:id_inst>/page=<int:page>")
@permission_required("service_request_index")
@login_required
@is_activated
@is_in_maintenance_mode
def index(id_inst, page=1):
    per_page = configuration.get_configuration().per_page

    institution = insts.find_inst_by_id(id_inst)

    # Por cada servicio que tenga la institutucion necesito quedarme con las solicitudes de ese servicio
    # reques = institution.get_service_requests()
    reques = institution.get_service_requests_paginate(page, per_page)

    form = FilterRequestForm()

    url_host = request.url.split('/solicitudes')[0]
    return render_template("service_requests/index.html", url_host=url_host, reques=reques, inst=id_inst, institution=institution, form=form)


@service_requests_bp.get("/show_notes/<int:id_inst>/<int:id_reque>")
@permission_required("service_request_index")
@login_required
@is_activated
@is_in_maintenance_mode
def show_notes(id_inst, id_reque):

    institution = insts.find_inst_by_id(id_inst)
    reque = service_requests.find_service_request_by_id(id_reque)

    if reque is None:
        return redirect(url_for("service_requests.index", id_inst=id_inst, page=1))
    else:
        reque.notes.sort(key=lambda x: x.created_at, reverse=True)

    form = NoteRequestForm()
    url_host = request.url.split('/solicitudes')[0]
    return render_template("service_requests/show_notes.html", url_host=url_host, reque=reque, form=form, id_inst=id_inst, institution=institution)


@service_requests_bp.post("/create_note/<int:id_inst>/<int:id_reque>")
@permission_required("service_request_update")
@login_required
@is_activated
@is_in_maintenance_mode
def create_note(id_inst, id_reque):
    reque = service_requests.find_service_request_by_id(id_reque)
    if reque is None:
        return redirect(url_for("service_requests.index", id_inst=id_inst, page=1))

    form = NoteRequestForm(formdata=request.form)

    url_host = request.url.split('/solicitudes')[0]

    if form.validate():
        # GUARDO UNA NOTA
        service_requests.create_note_request(
            service_request_id=reque.id,
            note=form.observation.data,
        )

        flash("Se ha creado una nota", "success")
        return redirect(url_for("service_requests.show_notes", id_inst=id_inst, id_reque=id_reque, url_host=url_host))
    else:
        return redirect(url_for("service_requests.index", id_inst=id_inst, page=1, url_host=url_host))


@service_requests_bp.get("/edit/<int:id_inst>/<int:id_reque>")
@permission_required("service_request_update")
@login_required
@is_activated
@is_in_maintenance_mode
def edit(id_inst, id_reque):

    reque = service_requests.find_service_request_by_id(id_reque)
    if reque is None:
        return redirect(url_for("service_requests.index", id_inst=id_inst, page=1))

    form = EventRequestForm()
    url_host = request.url.split('/solicitudes')[0]
    return render_template("service_requests/edit.html", url_host=url_host, id_inst=id_inst, id_reque=id_reque, form=form)


@service_requests_bp.post("/update/<int:id_inst>/<int:id_reque>")
@permission_required("service_request_update")
@login_required
@is_activated
@is_in_maintenance_mode
def update(id_inst, id_reque):
    """
    Se modificara el estado de la solicitud sólo si esta en el estado de "EN PROCESO"
    """
    reque = service_requests.find_service_request_by_id(id_reque)
    if reque is None or reque.last_state.name in ["FINALIZADA", "CANCELADA", "RECHAZADA"]:
        flash("La solicitud esta cerrada, no es posible modificar el estado!")
        return redirect(url_for("service_requests.index", id_inst=id_inst, page=1))

    form = EventRequestForm(formdata=request.form)

    url_host = request.url.split('/solicitudes')[0]

    if form.validate():
        # ME QUEDO CON EL ESTADO
        state = service_requests.find_state_request_by_id(
            form.state_request_id.data)
        if state:
           # CREO UN NUEVO EVENT REQUESTS PARA LA SOLICITUD
            service_requests.create_event_service_request(
                state_request_id=form.state_request_id.data,
                service_request_id=id_reque,
                observation=form.observation.data,
            )
        if state.name in ["FINALIZADA", "CANCELADA", "RECHAZADA"]:
            # EN ESTE CASO ACTUALIZO LA FECHA DE CIERRE DE LA SOLiCITUD
            service_requests.update_service_request(reque,
                                                    close_date=datetime.utcnow())

        flash("Se ha modificado el estado de la solicitud", "success")

    return redirect(url_for("service_requests.index", id_inst=id_inst, page=1, url_host=url_host))


@service_requests_bp.post("/delete/<int:id_inst>/<int:id_reque>")
@permission_required("service_request_destroy")
@login_required
@is_activated
@is_in_maintenance_mode
def delete(id_inst, id_reque):

    reque = service_requests.find_service_request_by_id(id_reque)

    if reque is None:
        return redirect(url_for("service_requests.index", id_inst=id_inst, page=1))

    service_requests.delete_service_request(reque)

    return redirect(url_for("service_requests.index", id_inst=id_inst, page=1))


@service_requests_bp.get("/show/<int:id_inst>/<int:id_reque>")
@permission_required("service_request_show")
@login_required
@is_activated
@is_in_maintenance_mode
def show(id_inst, id_reque):
    reque = service_requests.find_service_request_by_id(id_reque)

    if reque is None:
        return redirect(url_for("service_requests.index", id_inst=id_inst, page=1))
    else:
        reque.events.sort(key=lambda x: x.created_at, reverse=True)

    url_host = request.url.split('/solicitudes')[0]

    return render_template("service_requests/show.html", url_host=url_host, reque=reque, id_inst=id_inst)
