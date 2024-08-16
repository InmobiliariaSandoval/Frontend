# Descripción

Archivos que conforman el Frontend de la aplicación, en este caso y a diferencia del backend, solo se utiliza una versión para realizar la `build` del sistema

## Instalación local

Para trabajar con el sistema de manera local en tu dispositivo, realizar cambios y demás acciones se necesitan seguir los siguientes pasos:

1. Clona el repositorio en tu computadora, para ello asegurate de tener instalado `git` y utilizando el siguiente comando realiza el clonado del repositorio:

    ```
    git clone https://github.com/InmobiliariaSandoval/Frontend
    ```


2. Una vez que se haya clonado el respositorio, en la carpeta raíz encontrarás el archivo `requirements.txt`, el cuál contiene todas las dependencias que el sistema necesita para funcionar. Para instalar dichas dependencias ejecute el siguiente comando:

    ```
    pip install -r requirements.txt
    ```

3. Una vez tienes los recursos instalados, lo que necesitas hacer es crear un archivo llamado `.env` en donde deberás de agregar los siguientes valores:

    ```env
    SECRET_FLASK = '' # Valor para utilizar las sesiones en Flask

    URL_BACKEND = '' # URL del backend, cuando trabajas en local, debería de ser http://127.0.0.1:8000

    URL_FRONTEND = '' # URL del froentd, cuando trabajas en local, debería de ser http://127.0.0.1:8080
    ```
    Todos los valores serán proporcionados por parte de la inmobiliaria una vez que esté desplegado.

    * Si surje algún problema, intenta agregar la primer y tercer línea del ejemplo, en el archvio de inicio `run.py`, en caso de que no funcione, agrega donde se utilice las variables de entorno, es decir, en los archivos `config.py`, `utilidades.py` y `views_generales.py` y modifica la manera en que se obtiene las variables de entorno.

        Tome como referencia el siguiente código de ejemplo:

        ```python

        from dotenv import load_dotenv # Agregar al archivo run.py
        import os

        # Agregar al archvio run.py
        load_dotenv()  # Carga las variables desde el archivo .env

        # Manera de ejemplo
        secret_key = os.getenv("SECRET_KEY")
        database_url = os.getenv("DATABASE_URL")

        # Manera actual
        secret_key = os.environ['SECRET_KEY']
        database_url = os.environ['DATABASE_URL']

        print(f"Secret Key: {secret_key}")
        print(f"Database URL: {database_url}")

        ```

        Además, en el archivo `configuracion.js` necesita cambiar la URL proporcionada en esa constante a la correspondiente del backend.

4. Finalmente puedes ejecutar el siguiente comando para poner en función el sistema haciendo la siguiente modificación para tener un comando más sencillo.

   * En el archivo `run.py` agrega hasta el final del archivo las siguientes líneas

        ```python
        if __name__ == '__main__':
            app.run(port=8080)
        ```
    * En el archivo de `config.py` cambia el valor de la constante *DEBUG* a *True*:

        ```python
        DEBUG=True
        ```
    * Una vez realizadas estas configuraciones, ejecuta el siguiente comando desde la raíz:

    ```bash
    python run.py
    ```

En caso de volver a desplegar, lo único que necesitas hacer es comentar las líneas que acabas de añadir, así como cambiar el valor de la constante a su valor original. Evita que se envie el archivo .env con un archivo .gitignore:

```
.env
```

## Hostings

Este apartado debería de estar alojado en los siguientes hostings:

* [Zeabur](https://zeabur.com/)

La prueba y demostración del sistema se realizo en el hosting de [Heroku](https://www.heroku.com/)

Si desea replicar el mismo proceso, solamente necesitará añadir dos archivos extras en la raíz del proyecto, uno con el nombre de `Procfile` y otro con el nombre de `runtime.txt`

* `runtime.txt` es el archivo que almacena la versión de python necesaria para ejecutar y correr el programa, durante el desarrollo se utilizó `python 3.12.4`. En el archivo se debe de representar de la siguiente manera:

    ```
    python-3.12.4
    ```
* `Procfile` es un archivo indispensable el cuál indica la manera en que se ejecutará la aplicación dentro del hosting de [Heroku](https://devcenter.heroku.com/articles/procfile), para el hosting de [Zeabur](https://zeabur.com/docs/es-ES) no es necesario, si desea saber más de ambos, puede leer sus documentaciones respectivas, solo de click enncima de cualquiera de ellos de este parrafo. El archivo debe se debe de representar de la siguiente manera:

    ```
    web: gunicorn --bind 0.0.0.0:$PORT run:app
    ```

<hr>

Si tiene alguna duda, problema o detalle trabajando con el sistema intente contactando a los desarrolladores.