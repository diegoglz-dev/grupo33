# Grupo 33

# Instalaciones necesarias

-   Poetry
-   Python 3.8.10

# Dependencias instaladas

-   Flask 2.3.3
-   Jinja2 3.1.2
-   Pytest 7.4.1
-   Psycopg2-binary (2.9.7)
-   Flask-sqlalchemy (3.1.1)
-   Python-dotenv (1.0.0)
-   Flask-shell-ipython (0.5.1)
-   Flask-session (0.5.0)
-   Flask-bcrypt (1.0.1)
-   Flask-mail (0.9.1)
-   Pyjwt (2.8.0)
-   Flask-jwt-extended (4.5.3)
-   Flask-cors (4.0.0)
-   Authlib (1.2.1)
-   Requests (2.31.0)
-   Pyopenssl (23.3.0)

# Como levantar el proyecto

1. Una vez clonado el proyecto. Posicionarse en la carpeta `/admin`, una vez dentro de ella, ejecutar el comando `poetry install`
2. Ejecutar en la terminal el siguiente comando: `poetry shell`
3. Y para no tener que levantar el servidor cada vez que se modifican funcionalidades del proyecto, el comando es: `flask --debug run`
4. Para detener el servidor en la terminal presionar las teclas `ctrl + c`

# ¿Como ingresar al sistema?

Para ingresar a la app privada ingresar como cualquiera de estos usuarios después de correr los seeds con el comando `flask refreshdb`:

1. Superadministrador: usuario: `superadmin` - email: `superadmin@gmail.com` - contraseña: `password`
2. Administrador: usuario: `admin` - email: `admin@gmail.com` - contraseña: `password`
3. Dueño: usuario: `duenio` - email: `duenio@gmail.com` - contraseña: `password`
4. Operador: usuario: `operador` - email: `operador@gmail.com` - contraseña: `password`
