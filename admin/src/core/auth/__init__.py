from src.core.database import db
from src.core.bcrypt import bcrypt
from src.core.auth.user import User
from src.core.auth.user import Rol
from src.core.auth.user import Permiso
from src.core.auth.user import Usuario_tiene_rol
from src.core.auth.user import Rol_tiene_permiso
from src.core.insts import Institution
from sqlalchemy import and_
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import contains_eager
from src.core import insts

import uuid


def all_users():
    return User.query.all()


def list_users(page, per_page):
    return User.query.paginate(
        page=page, per_page=per_page, error_out=False)


def users_filtered_by_email_or_active(email, active, page, per_page):
    # Filtrar usuarios en base a los parámetros
    query = User.query

    if email:
        query = query.filter(User.email.like(f"%{email}%"))

    if active is not None and active != "":
        # Convierte el valor a entero
        active = int(active)
        query = query.filter(User.active == bool(active))

    filtered_users = query.paginate(
        page=page, per_page=per_page, error_out=False)
    return filtered_users


def user_rol_inst(id_user, id_inst):
    rol = Usuario_tiene_rol.query.filter_by(
        usuario_id=id_user, institucion_id=id_inst).first()
    return rol


def create_user(**kwargs):
    hash = bcrypt.generate_password_hash(kwargs["password"].encode("utf-8"))
    kwargs.update(password=hash.decode("utf-8"))
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()

    return user


def find_user_by_email(email):
    return User.query.filter_by(email=email).first()


def find_user_by_username(username):
    return User.query.filter_by(username=username).first()


def find_user_by_id(id):
    return User.query.filter_by(id=id).first()


def find_user_by_token(token):
    return User.query.filter_by(activation_token=token).first()


def user_activate(user):
    user.active = True
    # Borra el token de activación
    user.activation_token = None
    db.session.commit()

    return user


def check_user(email, password):
    user = find_user_by_email(email)

    if not user:
        user = find_user_by_username(email)

    if user and bcrypt.check_password_hash(user.password, password.encode("utf-8")):
        return user
    else:
        return None


def update_user(user, **kwargs):
    if user.password != kwargs['password']:
        hash = bcrypt.generate_password_hash(
            kwargs["password"].encode("utf-8"))
        kwargs.update(password=hash.decode("utf-8"))

    user.first_name = kwargs['first_name']
    user.last_name = kwargs['last_name']
    user.username = kwargs['username']
    user.email = kwargs['email']
    user.password = kwargs['password']
    user.active = kwargs['active']
    db.session.commit()

    return user


def set_user_activation_token(user, token):
    user.activation_token = token
    db.session.commit()

    return user


def delete_user(user):
    db.session.delete(user)
    db.session.commit()


def create_rol(nombre):
    rol = Rol(nombre=nombre)
    db.session.add(rol)
    db.session.commit()
    return rol


def create_permiso(nombre):
    permiso = Permiso(nombre=nombre)
    db.session.add(permiso)
    db.session.commit()
    return permiso


def add_rol_to_user(user, rol):
    # Para el caso del SuperAdmin, no se le asigna institucion
    usuario_tiene_rol = Usuario_tiene_rol(usuario=user, rol=rol)
    db.session.add(usuario_tiene_rol)
    db.session.commit()
    return usuario_tiene_rol


def add_rol_to_user_for_institution(user, rol, institucion):

    usuario_tiene_rol = Usuario_tiene_rol(
        usuario=user, rol=rol, institucion_id=institucion)
    db.session.add(usuario_tiene_rol)
    db.session.commit()
    return usuario_tiene_rol


def add_rol_to_user_for_institution2(user_id, role_id, institution_id):
    user = find_user_by_id(user_id)
    role = find_rol_by_id(role_id)
    institution = insts.find_inst_by_id(institution_id)

    if user and role and institution:
        new_assignment = Usuario_tiene_rol(
            usuario=user, rol=role, institucion=institution)
        db.session.add(new_assignment)
        db.session.commit()
        return True, "Asignación exitosa"
    else:
        return False, "No se encontró el usuario, rol o institución correspondiente"


def add_permiso_rol(rol, permiso):
    rol_tiene_permiso = Rol_tiene_permiso(rol=rol, permiso=permiso)
    db.session.add(rol_tiene_permiso)
    db.session.commit()
    return rol_tiene_permiso


def user_has_role(user, rol):
    for user_rol in user.roles:
        if user_rol.rol.nombre == rol:
            return True
    return False


def rollback():
    db.session.rollback()


def get_rol_by_name(name):
    return Rol.query.filter_by(nombre=name).first()


def get_roles():
    # Filtra los roles excluyendo el rol "Super-Administrador"
    return Rol.query.filter(Rol.nombre != "Super-Administrador").all()


def find_rol_by_id(id):
    return Rol.query.filter_by(id=id).first()


def es_dueño_de_institucion(user, institucion):
    return Usuario_tiene_rol.query.filter_by(usuario=user, rol_id=3, institucion_id=institucion).first()


def obtener_instituciones_de_dueño(user_id):
    return Usuario_tiene_rol.query.filter(
        and_(Usuario_tiene_rol.usuario_id ==
             user_id, Usuario_tiene_rol.rol_id == 3)
    ).options(joinedload(Usuario_tiene_rol.institucion)).all()


def update_user_rol_in_institution(user, institution, new_role_id):
    if user is not None and institution is not None:
        user_role = Usuario_tiene_rol.query.filter_by(
            usuario_id=user.id,
            institucion_id=institution.id
        ).first()

        if user_role:
            # Actualizar el ID del rol en la relación
            user_role.rol_id = new_role_id

            # Guardar los cambios en la base de datos
            db.session.commit()

            return True, "Rol actualizado correctamente"
        else:
            return False, "No se encontró la relación Usuario_tiene_rol"
    else:
        return False, "Usuario o institución no válidos"


def users_and_roles(id, page, per_page):
    # Acá consultamos la base de datos para obtener los usuarios y sus roles en la institución
    users_with_roles = User.query.join(Usuario_tiene_rol, (User.id == Usuario_tiene_rol.usuario_id)).filter(
        and_(Usuario_tiene_rol.institucion_id == id)
    ).options(contains_eager(User.roles)).paginate(page=page, per_page=per_page, error_out=False)

    return users_with_roles


def obtener_relaciones(institution_id):
    return Usuario_tiene_rol.query.filter_by(institucion_id=institution_id).all()


def eliminar_inst_y_relaciones(relaciones, institution):
    # Eliminar las relaciones encontradas
    for relacion in relaciones:
        db.session.delete(relacion)

    # Eliminar la institución
    insts.delete_inst(institution)


def get_users():
    return User.query.all()


def generate_unique_username(first_name, last_name):
    """ Genera un nombre de usuario único, combinando nombre y apellido
    y añadiendo un sufijo único (por ejemplo, un UUID) """
    base_username = f"{first_name.lower()}_{last_name.lower()}"
    unique_suffix = str(uuid.uuid4().hex[:6])
    username = f"{base_username}_{unique_suffix}"
    return username
