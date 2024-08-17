"""
    Archivo que iniciar la aplicación de Flask
"""
# Importar función para crear el archivo
from app import crear_aplicacion
from dotenv import load_dotenv
import os

# Crear la aplicación en base a la función
app = crear_aplicacion()

# Cargar las variables de entorno
load_dotenv()

# Descomentar al utilizar local
if __name__ == '__main__':
    app.run(port=os.getenv("PORT", default=5000), host='0.0.0.0')
