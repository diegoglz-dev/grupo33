# Flask
from flask import Blueprint
from flask import render_template
from flask import request
# Helpers (Decoradores)
from src.web.helpers.auth import login_required
from src.web.helpers.activated import is_activated
from src.web.helpers.maintenance import is_in_maintenance_mode

dashboard_bp = Blueprint("dash", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/")
@login_required
@is_activated
@is_in_maintenance_mode
def dashboard():
    url_host = request.url.split('/dashboard')[0]
    return render_template("dashboard.html", url_host=url_host)
