"""
    Archivo que inicializa la aplicación Flask y sus
    configuracoines
"""
from flask import Flask
import logging

# Función que crea y configura la aplicación
def crear_aplicacion():
    # Crear el objeto de la aplicación
    app = Flask(__name__)

    # Cargar la configuración de un objeto
    app.config.from_object('config')

    # Configuración del logger
    #logging.basicConfig(level=logging.ERROR)
    #logger = logging.getLogger(__name__)

    # Mensaje de registro inicial
    #logger.info("Inicializando la aplicación")

    # Registrar las vistas de la aplicaicón
    from .views import views_generales
    from .views.views_lotes import views_lotes
    from .views.views_vendedores import views_vendendores
    from .views.views_pagos import views_pagos
    from .views.views_clientes import views_clientes
    from .views.views_extras import views_extras

    app.register_blueprint(views_generales.bp)
    app.register_blueprint(views_lotes.bp)
    app.register_blueprint(views_vendendores.bp)
    app.register_blueprint(views_pagos.bp)
    app.register_blueprint(views_clientes.bp)
    app.register_blueprint(views_extras.bp)

    # Importar y registrar los controladores de errores
    from .error_handlers import register_error_handlers
    register_error_handlers(app)

    return app