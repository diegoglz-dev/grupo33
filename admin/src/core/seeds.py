from src.core import auth
from src.core import insts
from src.core import configuration
from src.core import services
from src.core import service_requests


def run():
    superadmin = auth.create_user(
        first_name="Super",
        last_name="Admin",
        username="superadmin",
        email="superadmin@gmail.com",
        password="password",
        active=True,
    )

    administrador = auth.create_user(
        first_name="Admin",
        last_name="Admin",
        username="admin",
        email="admin@gmail.com",
        password="password",
        active=True,
    )

    duenio = auth.create_user(
        first_name="Dueño",
        last_name="Dueño",
        username="duenio",
        email="duenio@gmail.com",
        password="password",
        active=True,
    )

    operador = auth.create_user(
        first_name="Operador",
        last_name="Operador",
        username="operador",
        email="operador@gmail.com",
        password="password",
        active=True,
    )

    institucion = insts.create_inst(
        name="Institucion 1",
        info="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Facilisi cras fermentum odio eu feugiat. Tortor dignissim convallis aenean et tortor. Volutpat ac tincidunt vitae semper quis. Odio euismod lacinia at quis risus sed vulputate odio ut. Condimentum id venenatis a condimentum. Pulvinar sapien et ligula ullamcorper malesuada proin libero. At varius vel pharetra vel turpis. Ut ornare lectus sit amet est placerat.",
        direccion="Av. 7 1172",
        localizacion="-34.91810188094189, -57.94509778446659",
        web="www.institucion1.com",
        palabras_clave="totor, dignissim, convallis, aenean, et, tortor",
        dias_horarios="Lun. a Vie. de 8:00 a 18:00 hs",
        contacto="+54 9 11 1234-9876",
        habilitado=True,
    )

    institucion2 = insts.create_inst(
        name="Institucion 2",
        info="Sollicitudin ac orci phasellus egestas tellus rutrum. Gravida quis blandit turpis cursus in hac habitasse. Leo integer malesuada nunc vel risus commodo viverra maecenas accumsan. Lectus arcu bibendum at varius vel pharetra.<br>Bibendum arcu vitae elementum curabitur vitae nunc. In nulla posuere sollicitudin aliquam ultrices sagittis orci a. Risus sed vulputate odio ut enim. Diam ut venenatis tellus in metus vulputate eu. Pretium nibh ipsum consequat nisl vel pretium lectus quam. Sit amet luctus venenatis lectus. Convallis a cras semper auctor neque vitae tempus quam.",
        direccion="Av. 66 161",
        localizacion="-34.917034972898584, -57.926188276543186",
        web="www.institucion2.com",
        palabras_clave="sit, amet, luctus, venenatis, lectus",
        dias_horarios="Lun. a Vie. de 8:00 a 18:00 hs y Sab. de 8:00 a 12:00 hs.",
        contacto="+54 9 11 1234-5678",
        habilitado=True,
    )

    config = configuration.create_configuration(
        per_page=10,
        contact="contact@cidepint.com.ar",
        enabled_site=True,
        maintenance_message="Regresaremos pronto. Gracias por su paciencia.",
    )

    en_proceso = service_requests.create_state_request(
        name="EN PROCESO",
    )

    aceptada = service_requests.create_state_request(
        name="ACEPTADA",
    )

    rechazada = service_requests.create_state_request(
        name="RECHAZADA",
    )

    finalizada = service_requests.create_state_request(
        name="FINALIZADA",
    )

    cancelada = service_requests.create_state_request(
        name="CANCELADA",
    )

    # Creación de Roles
    rol_superAdmin = auth.create_rol(nombre="Super-Administrador")
    rol_admin = auth.create_rol(nombre="Administrador")
    rol_dueño = auth.create_rol(nombre="Dueño")
    rol_operador = auth.create_rol(nombre="Operador")

    # Permisos para administrar usuarios
    user_index = auth.create_permiso(nombre="user_index")
    user_new = auth.create_permiso(nombre="user_new")
    user_destroy = auth.create_permiso(nombre="user_destroy")
    user_update = auth.create_permiso(nombre="user_update")
    user_show = auth.create_permiso(nombre="user_show")
    user_assign_rol = auth.create_permiso(nombre="user_assign_rol")

    # Permisos para administrar instituciones
    institution_index = auth.create_permiso(nombre="institution_index")
    institution_new = auth.create_permiso(nombre="institution_new")
    institution_destroy = auth.create_permiso(nombre="institution_destroy")
    institution_update = auth.create_permiso(nombre="institution_update")
    institution_show = auth.create_permiso(nombre="institution_show")
    institution_activate = auth.create_permiso(nombre="institution_activate")
    institution_deactivate = auth.create_permiso(
        nombre="institution_deactivate")

    # Permisos para administrar usuarios como dueño
    user_index_dueño = auth.create_permiso(nombre="user_index_dueño")
    user_new_dueño = auth.create_permiso(nombre="user_new_dueño")
    user_destroy_dueño = auth.create_permiso(nombre="user_destroy_dueño")
    user_update_dueño = auth.create_permiso(nombre="user_update_dueño")

    # Permisos para administrar servicios
    service_index = auth.create_permiso(nombre="service_index")
    service_new = auth.create_permiso(nombre="service_new")
    service_destroy = auth.create_permiso(nombre="service_destroy")
    service_update = auth.create_permiso(nombre="service_update")
    service_show = auth.create_permiso(nombre="service_show")

    # Permisos para administrar solicitudes
    service_request_index = auth.create_permiso(nombre="service_request_index")
    service_request_show = auth.create_permiso(nombre="service_request_show")
    service_request_update = auth.create_permiso(
        nombre="service_request_update")
    service_request_destroy = auth.create_permiso(
        nombre="service_request_destroy")

    # Permisos para administrar configuraciones
    configuration_show = auth.create_permiso(nombre="configuration_show")
    configuration_index = auth.create_permiso(nombre="configuration_update")

    # Agrega de permisos a rol Super-Administrador
    auth.add_permiso_rol(rol_superAdmin, user_index)
    auth.add_permiso_rol(rol_superAdmin, user_new)
    auth.add_permiso_rol(rol_superAdmin, user_destroy)
    auth.add_permiso_rol(rol_superAdmin, user_update)
    auth.add_permiso_rol(rol_superAdmin, user_show)
    auth.add_permiso_rol(rol_superAdmin, institution_index)
    auth.add_permiso_rol(rol_superAdmin, institution_new)
    auth.add_permiso_rol(rol_superAdmin, institution_destroy)
    auth.add_permiso_rol(rol_superAdmin, institution_update)
    auth.add_permiso_rol(rol_superAdmin, institution_show)
    auth.add_permiso_rol(rol_superAdmin, institution_activate)
    auth.add_permiso_rol(rol_superAdmin, institution_deactivate)
    auth.add_permiso_rol(rol_superAdmin, configuration_show)
    auth.add_permiso_rol(rol_superAdmin, configuration_index)
    auth.add_permiso_rol(rol_superAdmin, user_assign_rol)
    auth.add_permiso_rol(rol_superAdmin, service_request_index)
    auth.add_permiso_rol(rol_superAdmin, service_request_show)
    auth.add_permiso_rol(rol_superAdmin, service_request_update)
    auth.add_permiso_rol(rol_superAdmin, service_request_destroy)

    # Agrega de permisos a rol Dueño
    auth.add_permiso_rol(rol_dueño, institution_index)
    auth.add_permiso_rol(rol_dueño, institution_new)
    auth.add_permiso_rol(rol_dueño, institution_destroy)
    auth.add_permiso_rol(rol_dueño, institution_update)
    # Permisos para administrar usuarios como dueño
    auth.add_permiso_rol(rol_dueño, user_index_dueño)
    auth.add_permiso_rol(rol_dueño, user_new_dueño)
    auth.add_permiso_rol(rol_dueño, user_destroy_dueño)
    auth.add_permiso_rol(rol_dueño, user_update_dueño)
    auth.add_permiso_rol(rol_dueño, user_assign_rol)

    auth.add_permiso_rol(rol_dueño, service_index)
    auth.add_permiso_rol(rol_dueño, service_new)
    auth.add_permiso_rol(rol_dueño, service_update)
    auth.add_permiso_rol(rol_dueño, service_show)
    auth.add_permiso_rol(rol_dueño, service_destroy)

    auth.add_permiso_rol(rol_dueño, service_request_index)
    auth.add_permiso_rol(rol_dueño, service_request_show)
    auth.add_permiso_rol(rol_dueño, service_request_update)
    auth.add_permiso_rol(rol_dueño, service_request_destroy)

    auth.add_permiso_rol(rol_dueño, service_index)
    auth.add_permiso_rol(rol_dueño, service_new)
    auth.add_permiso_rol(rol_dueño, service_update)
    auth.add_permiso_rol(rol_dueño, service_show)
    auth.add_permiso_rol(rol_dueño, service_destroy)

    auth.add_permiso_rol(rol_dueño, service_request_index)
    auth.add_permiso_rol(rol_dueño, service_request_show)
    auth.add_permiso_rol(rol_dueño, service_request_update)
    auth.add_permiso_rol(rol_dueño, service_request_destroy)

    # Agrega de permisos a rol admin
    auth.add_permiso_rol(rol_admin, service_index)
    auth.add_permiso_rol(rol_admin, service_new)
    auth.add_permiso_rol(rol_admin, service_update)
    auth.add_permiso_rol(rol_admin, service_show)
    auth.add_permiso_rol(rol_dueño, service_destroy)

    auth.add_permiso_rol(rol_admin, service_request_index)
    auth.add_permiso_rol(rol_admin, service_request_show)
    auth.add_permiso_rol(rol_admin, service_request_update)
    auth.add_permiso_rol(rol_admin, service_request_destroy)

    # Agrega de permisos a rol Operador
    auth.add_permiso_rol(rol_operador, service_index)
    auth.add_permiso_rol(rol_operador, service_new)
    auth.add_permiso_rol(rol_operador, service_update)
    auth.add_permiso_rol(rol_operador, service_show)

    auth.add_permiso_rol(rol_operador, service_request_index)
    auth.add_permiso_rol(rol_operador, service_request_show)
    auth.add_permiso_rol(rol_operador, service_request_update)

    # Agrega rol a los usuarios
    # Solo los super-administradores
    auth.add_rol_to_user(superadmin, rol_superAdmin)
    # Asigna rol usuario a una institución
    auth.add_rol_to_user_for_institution(duenio, rol_dueño, institucion2.id)
    auth.add_rol_to_user_for_institution(
        administrador, rol_dueño, institucion2.id)
    auth.add_rol_to_user_for_institution(operador, rol_dueño, institucion.id)

    services.create_service(
        name="Servicio de Desarrollo",
        description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Sapien pellentesque habitant morbi tristique senectus.",
        keywords="Lorem, ipsum, dolor, sit, amet",
        type_of_service="Desarrollo",
        institution_id=institucion.id,
        enabled=True,
    )

    services.create_service(
        name="Servicio de Análisis",
        description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Sapien pellentesque habitant morbi tristique senectus.",
        keywords="habitant, morbi, tristique, senectus",
        type_of_service="Análisis",
        institution_id=institucion2.id,
        enabled=True,
    )
