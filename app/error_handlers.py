"""
    Archivo que se encarga de renderizar los
    errores
"""
from flask import render_template, session, flash, redirect, url_for
from markupsafe import Markup
from typing import List


def validar_respuesta(respuesta: list, codigo_estado: int, tipo_dato: str, mostrar_mensaje: bool = True) -> List:
    """
    Función que se encarga de validar la respuesta de la solicitud a la API y
    muestra un mensaje Flash dependiendo el código de estado

    Args:
        respuesta (list): La respuesta de la API en formato de lista.
        codigo_estado (int): El código de estado HTTP de la respuesta.
        tipo_dato (str): El tipo de dato al que corresponde la respuesta (usado en los mensajes flash).
        mostrar (bool): Opción para mostrar el mensaje en caso de que se requiera (usado en los mensajes flash)

    Returns:
        List: La respuesta validada. Devuelve una lista vacía si hay un error o advertencia.
    """
    if respuesta:
        # Eliminar valor del token
        if codigo_estado == 401:
            session.pop('token', None)
            session.pop('usuario', None)
            session.clear()

        if codigo_estado in [500, 401, 400, 422]:
            flash(Markup(f"<strong>Error en {tipo_dato}</strong>: {respuesta[0]['detail']}"), category="error")
            return []
        elif codigo_estado == 404:
            if mostrar_mensaje:
                flash(Markup(f"<strong>Precaución en {tipo_dato}</strong>: {respuesta[0]['detail']}"), category="warning")
            return []
    else:
        flash(Markup(f"<strong>Error:</strong> No se obtuvieron datos en {tipo_dato}"), category="error")
    return respuesta

# Función que se encarga de manejar los erroes
def register_error_handlers(app):

    # Manejar errors 404
    @app.errorhandler(404)
    def error_404(error):
        return render_template('404.html'), 404

    # Manejar errores 500
    @app.errorhandler(500)
    def error_500(error):
        return render_template('500.html', error=None), 500

    # Manejar errores generales
    @app.errorhandler(Exception)
    def handle_exception(error):
        return render_template('500.html', error=str(error)), 500
