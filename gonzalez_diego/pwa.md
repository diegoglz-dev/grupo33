# Pasos para crear una Progressive Web App (PWA)

1. Crear el archivo `manifest.json`, en mi caso lo cree en la carpeta public.
2. Configurar el contenido del archivo `manifest.json` esté es un breve ejemplo:

-   **name:** El nombre de tu PWA.
-   **short_name:** Un nombre corto para tu PWA.
-   **description:** Una descripción de tu PWA.
-   **start_url:** La URL desde la cual se cargará tu PWA cuando se inicie.
-   **display:** Define cómo se mostrará tu PWA (puede ser "fullscreen", "standalone", "minimal-ui" o "browser").
-   **background_color:** El color de fondo de tu PWA.
-   **theme_color:** El color de tema de tu PWA.
-   **icons:** Una lista de íconos en diferentes tamaños para tu PWA.

Para ver la configuración especifica dirijase al archivo ubicado en [portal/public/manifest.json](https://gitlab.catedras.linti.unlp.edu.ar/proyecto2023/proyectos/grupo33/-/blob/main/portal/public/manifest.json?ref_type=heads)

3. Se deben colocar los iconos en la carpeta correcta, en mi caso los ubique en la carpeta `portal/public/img/`.
4. Se debe referenciar al archivo `manifest.json` en el `index.html` de la aplicación. Para hacer esto, se agrega una etiqueta `<link>`en la sección de `<head>` del archivo `index.html`.

Por ejemplo: `<link rel="manifest" href="/manifest.json">`

Para comprobar que fue instalado correctamente, abrimos el navegador con el proyecto, abrimos la herramientas de desarrollador y nos dirigimos a `Application` y vamos a notar un apartado que nos indica el Manifest.

## Instalar Service Worker

Un service worker es un script que se ejecuta en segundo plano y permite que la PWA funcione sin conexión a internet. En mi caso, hago uso de la librería workbox, para instalarla hice lo siguiente, ejecute el comando `npm install workbox-cli --global`.

Luego instalarlo, se ejecuta en la carpeta raíz del proyecto el comando `workbox wizard` que es un asistente el cual nos ayudará a crear el script de configuración, siguiendo los pasos que nos va indicando. Se generará un archivo llamado `workbox-config.js` a partir de este, vamos a generar el service worker `sw.js` con el siguiente comando `workbox generateSW workbox-config.js`. En mi caso me lo genero en la carpeta `public`. Luego este archivo `sw.js` lo tendremos que ingresar en un script dentro de nuestro archivo [index.html](https://gitlab.catedras.linti.unlp.edu.ar/proyecto2023/proyectos/grupo33/-/blob/main/portal/index.html?ref_type=heads)

Finalmente, cuando iniciemos nuestro navegador con el proyecto, en la barra de direcciones vamos a notar un icono de instalación, que al presionarlo nos va a preguntar si deseamos instalar la aplicación.
