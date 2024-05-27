from flask import Blueprint
from flask import render_template, redirect, url_for
from flask import request
from src.core import configuration
from flask import flash
from src.core.validations.configuration.configuration_update import ConfigurationUpdateForm
from src.web.helpers.auth import login_required
from src.web.helpers.auth import permission_required
from src.web.helpers.maintenance import is_in_maintenance_mode

configuration_bp = Blueprint(
    "configuration", __name__, url_prefix="/configuracion")


@configuration_bp.get("/show")
@login_required
@is_in_maintenance_mode
@permission_required('configuration_show')
def show():
    url_host = request.url.split('/configuracion')[0]
    config = configuration.get_configuration()
    form = ConfigurationUpdateForm(obj=config)
    return render_template("configuration/show.html", url_host=url_host, form=form)


@configuration_bp.post("/update")
@login_required
@is_in_maintenance_mode
@permission_required('configuration_update')
def update():
    url_host = request.url.split('/configuracion')[0]
    form = ConfigurationUpdateForm(request.form)
    if form.validate():
        configuration.update_configuration(
            per_page=form.per_page.data,
            contact=form.contact.data,
            enabled_site=form.enabled_site.data,
            maintenance_message=form.maintenance_message.data,
        )

        flash("Configuración actualizada correctamente", "success")

        return redirect(url_for("configuration.show"))
    else:
        form.populate_obj(request.form)
        return render_template("configuration/show.html", url_host=url_host, form=form)
