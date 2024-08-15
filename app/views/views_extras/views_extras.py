"""
    Archivo que administra las vistas de apartados
    extras
"""
from flask import Blueprint, render_template, session, request, url_for, flash, redirect, jsonify
from ...controllers.controllers_notificaciones import NotificacionesController
from ...error_handlers import validar_respuesta
from markupsafe import Markup
import urllib.parse

# Registrar las vistas
bp = Blueprint('extras', __name__)

#################
# Vistas extras #
#################

@bp.route("/ver_notificaciones", methods=["GET", "POST"])
async def ver_notificaciones():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa'), category='error')
            return redirect(url_for('generales.index'))

        pagina = int(request.args.get('pagina', 1))
        tamano= int(request.args.get('tamano', 10))
        estado_notificacion = request.args.get('estado_notificacion')
        fecha_notificacion = request.args.get('fecha_notificacion', 'desc')

        # Verificar filtro
        if (estado_notificacion and estado_notificacion not in ['sin_leer', 'leidas'] or
            fecha_notificacion and fecha_notificacion not in ['asc', 'desc']):
            flash(Markup('<strong>Precaución:</strong> Filtro no válido, intente nuevamente'), category='warning')
            return redirect(url_for('notificaciones.ver_notificaciones', tamano = tamano))

        # Asignar valor booleano
        estado = True if estado_notificacion == 'sin_leer' else False if estado_notificacion == 'leidas' else None

        # Obtener todas las ntificaciones
        respuesta_notificaciones, total_notificaciones, codigo_estado = await NotificacionesController. \
            obtener_todas_notificaciones(token_acceso=token, pagina=pagina, limite_notificaciones=tamano,
                                        notificaciones_no_leidas=estado, orden=fecha_notificacion)
        # Verificar respuesta
        respuesta_notificaciones = validar_respuesta(respuesta_notificaciones, codigo_estado, 'Notificaciones')
        return render_template('vistas_extras/ver_notificaciones.html', notificaciones = respuesta_notificaciones, \
                                total_notificaciones=total_notificaciones, pagina=pagina, tamano = tamano, total=total_notificaciones)
    except Exception as error:
        print(f"Ocurrió un error al cargar la vista de notificaciones: {error}")
        raise Exception("Ocurrió un error al cargar la vista de notificaciones")

@bp.route("/eliminar_una_notificacion", methods=["POST"])
async def eliminar_una_notificacion():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener el identificador del vendedor
        datos_eliminar = request.get_json()

        # Verificar envio de datos
        if not datos_eliminar:
            flash(Markup(f'<strong>Precaución</strong>: No se enviaron datos. Intente nuevamente'), category='warning')
            return redirect(url_for('notificaciones.ver_notificaciones'))

        # Obtener los datos correspondientes
        identificador_notificacion = datos_eliminar['identificador_notificacion']

        # Obtenemos la respuesta de la API
        respuesta_notificacion, codigo_estado = await NotificacionesController. \
            eliminar_una_notificacion(token_acceso=token, identificador_notificacion=identificador_notificacion)

        # Verificamos la respuesta de la API
        respuesta_notificacion = validar_respuesta(respuesta_notificacion, codigo_estado, 'Notificación')

        # Verificar que exista una respuesta
        if respuesta_notificacion:
            flash(Markup(f'<strong>Éxito</strong>: Se eliminó correctamente la notificación'), category='message')

        return jsonify({'success': True})
    except Exception as error:
        print(f"Ocurrió un error al intentar solicitar el eliminar una notificación: {error}")
        raise Exception("Ocurrió un error al intentar solicitar el eliminar una notificación")

@bp.route("/eliminar_todas_notificaciones", methods=["POST"])
async def eliminar_todas_notificaciones():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener el identificador del vendedor
        datos_eliminar = request.get_json()

        # Verificar envio de datos
        if not datos_eliminar:
            flash(Markup('<strong>Precaución</strong>: No se enviaron datos. Intente nuevamente'), category='warning')
            return redirect(url_for('notificaciones.ver_notificaciones'))

        # Obtenemos la respuesta de la API
        respuesta_notificacion, codigo_estado = await NotificacionesController. \
            eliminar_notificaciones(token_acceso=token)

        # Verificamos la respuesta de la API
        respuesta_notificacion = validar_respuesta(respuesta_notificacion, codigo_estado, 'Notificación')

        # Verificar que exista una respuesta
        if respuesta_notificacion:
            flash(Markup(f'<strong>Éxito</strong>: Se eliminó correctamente las notificaciones'), category='message')

        return jsonify({'success': True})
    except Exception as error:
        print(f"Ocurrió un error al intentar solicitar eliminar todas las notificaciones: {error}")
        raise Exception("Ocurrió un error al intentar solicitar el eliminar todas las notificaciones")

@bp.route("/marcar_una_leida", methods=["POST"])
async def marcar_una_leida():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener el identificador del vendedor
        datos_actualizar = request.get_json()

        # Verificar envio de datos
        if not datos_actualizar:
            flash(Markup('<strong>Precaución</strong>: No se enviaron datos. Intente nuevamente'), category='warning')
            return redirect(url_for('notificaciones.ver_notificaciones'))

        # Obtener los datos correspondientes
        identificador_notificacion = datos_actualizar['identificador_notificacion']

        # Obtenemos la respuesta de la API
        respuesta_notificacion, codigo_estado = await NotificacionesController. \
            marcar_leida_una_notificacion(token_acceso=token, identificador_notificacion=identificador_notificacion)

        # Verificamos la respuesta de la API
        respuesta_notificacion = validar_respuesta(respuesta_notificacion, codigo_estado, 'Notificación')

        return jsonify({'success': True})
    except Exception as error:
        print(f"Ocurrió un error al intentar solicitar marcar como leída una notificación: {error}")
        raise Exception("Ocurrió un error al intentar solicitar el marcar como leída una notificación")

@bp.route("/marcar_todas_notificaciones", methods=["POST"])
async def marcar_todas_notificaciones():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener el identificador del vendedor
        datos_eliminar = request.get_json()

        # Verificar envio de datos
        if not datos_eliminar:
            flash(Markup(f'<strong>Precaución</strong>: No se enviaron datos. Intente nuevamente'), category='warning')
            return redirect(url_for('notificaciones.ver_notificaciones'))

        # Obtenemos la respuesta de la API
        respuesta_notificacion, codigo_estado = await NotificacionesController. \
            marcar_leida_todas_notificaciones(token_acceso=token)

        # Verificamos la respuesta de la API
        respuesta_notificacion = validar_respuesta(respuesta_notificacion, codigo_estado, 'Notificación')

        # Verificar que exista una respuesta
        if respuesta_notificacion:
            flash(Markup(f'<strong>Éxito</strong>: Se cambió correctamente las notificaciones'), category='message')

        return jsonify({'success': True})
    except Exception as error:
        print(f"Ocurrió un error al intentar solicitar marcar como leídas todas las notificaciones: {error}")
        raise Exception("Ocurrió un error al intentar solicitar el marcar como leídas todas las notificaciones")

@bp.route("/configuracion", methods=["GET"])
async def ver_configuracion():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Validar que existe el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener el identificador de la configuración
        configuracion = urllib.parse.unquote(session.get('usuario'))

        # Obtener la configuración
        respuesta_notificaciones, total_notificaciones, codigo_estado = await NotificacionesController. \
            obtener_todas_notificaciones(token_acceso=token, notificaciones_no_leidas=True)
        respuesta_configuracion, codigo_estado_configuracion = await NotificacionesController. \
            obtener_configuracion_especifica(identificador_configuracion=configuracion, token_acceso=token)

        # Verificar respuesta de la configuración
        respuesta_notificaciones = validar_respuesta(respuesta_notificaciones, codigo_estado, 'Notificaciones', mostrar_mensaje=False)
        respuesta_configuracion = validar_respuesta(respuesta_configuracion, codigo_estado_configuracion, 'Configuración')

        return render_template('vistas_extras/configuracion.html', notificaciones = respuesta_notificaciones, total_notificaciones=total_notificaciones,
                                configuracion=respuesta_configuracion)
    except Exception as error:
        print(f"Ocurrió un error al cargar la vista de configuración: {error}")
        raise Exception("Ocurrió un error al cargar la vista de configuración")