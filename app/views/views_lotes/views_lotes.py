"""
    Archivo que administra las vistas del
    apartado de lotes
"""

from flask import Blueprint, render_template, session, request, url_for, jsonify, flash, redirect
from ...controllers.controllers_notificaciones import NotificacionesController
from ...controllers.controllers_lotes import LotesController
from app.validadores import validar_formulario
from ...error_handlers import validar_respuesta
from markupsafe import Markup
import urllib.parse

# Registrar las vistas
bp = Blueprint('lotes', __name__)

###################
# Vistas de lotes #
###################

@bp.route("/estados_republica", methods=["GET", "POST"])
async def estados_republica():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error</strong>: No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener las notiificaciones y estados
        respuesta_notificaciones, total_notificaciones, codigo_estado = await NotificacionesController. \
            obtener_todas_notificaciones(token_acceso=token, notificaciones_no_leidas=True)
        respuesta_estados, codigo_estados = await LotesController.obtener_todos_estados(token_acceso=token)

        # Verificar respuestas
        respuesta_notificaciones = validar_respuesta(respuesta_notificaciones, codigo_estado, 'Notificaciones', mostrar_mensaje=False)
        respuesta_estados = validar_respuesta(respuesta_estados, codigo_estados, 'Estados')

        return render_template('vistas_lotes/estados.html', notificaciones = respuesta_notificaciones, estados = respuesta_estados, total_notificaciones=total_notificaciones)
    except Exception as error:
        print(f"Ocurrió un error al cargar la vista de estados: {error}")
        raise Exception("Ocurrió un error al mostrar la vista de resumen")

@bp.route("/municipios_estado/<string:identificador_estado>", methods=["GET", "POST"])
async def municipios_estado(identificador_estado):
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error</strong>: No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener las notificaciones y municipios
        respuesta_notificaciones, total_notificaciones, codigo_estado = await NotificacionesController. \
            obtener_todas_notificaciones(token_acceso=token, notificaciones_no_leidas=True)
        respuesta_municipios, codigo_municipio = await LotesController. \
            obtener_todos_municipios(identificador_estado=identificador_estado, token_acceso=token)

        # Verificar respuestas
        respuesta_notificaciones = validar_respuesta(respuesta_notificaciones, codigo_estado, 'Notificaciones', mostrar_mensaje=False)
        respuesta_municipios = validar_respuesta(respuesta_municipios, codigo_municipio, 'Municipios')

        return render_template('vistas_lotes/municipios.html', notificaciones = respuesta_notificaciones, municipios = respuesta_municipios, total_notificaciones = total_notificaciones)
    except Exception as error:
        print(f"Ocurrió un error al mostrar la vista de municipios: {error}")
        raise Exception("Ocurrió un error al mostrar la vista de municipios.")

@bp.route("/localidad_municipio/<string:identificador_municipio>", methods=["GET", "POST"])
async def localidad_municipio(identificador_municipio):
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error</strong>: No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener las notificaciones y las localides
        respuesta_notificaciones, total_notificaciones, codigo_estado = await NotificacionesController. \
            obtener_todas_notificaciones(token_acceso=token, notificaciones_no_leidas=True)
        respuesta_localidades, codigo_localidades = await LotesController. \
            obtener_todas_localidades(identificador_municipio=identificador_municipio, token_acceso=token)

        # Verificar respuesta de notificaciones
        respuesta_notificaciones = validar_respuesta(respuesta_notificaciones, codigo_estado, 'Notificaciones', mostrar_mensaje=False)
        respuesta_localidades = validar_respuesta(respuesta_localidades, codigo_localidades, 'Localidades')

        return render_template('vistas_lotes/localidad.html', notificaciones = respuesta_notificaciones, localidades = respuesta_localidades, total_notificaciones=total_notificaciones)
    except Exception as error:
        print(f"Ocurrió un error al mostrar la vista de localidad: {error}.")
        raise Exception("Ocurrió un error al mostrar la vista de localidad")

@bp.route("/complejo_residencial/<string:identificador_localidad>", methods=["GET", "POST"])
async def complejo_residencial(identificador_localidad):
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error</strong>: no tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener filtro por tipo de complejo
        tipo_complejo = request.args.get('tipoComplejo')

        # Verificar que el filtro sea válido
        if tipo_complejo and tipo_complejo not in ['Privada', 'Fraccionamiento', 'Residencial']:
            flash(Markup('<strong>Error</strong>: Filtro no válido, intente nuevamente'), category='error')
            return redirect(url_for('lotes.complejo_residencial', identificador_localidad=identificador_localidad))

        # Obtener las notificaciones y los complejos
        respuesta_notificaciones, total_notificaciones, codigo_estado = await NotificacionesController. \
            obtener_todas_notificaciones(token_acceso=token, notificaciones_no_leidas=True)
        respuesta_complejos, codigo_complejos = await LotesController. \
            obtener_todos_complejos(identificador_localidad=identificador_localidad, token_acceso=token, tipo_complejo=tipo_complejo)

        # Verificar respuesta
        respuesta_notificaciones = validar_respuesta(respuesta_notificaciones, codigo_estado, 'Notificaciones', mostrar_mensaje=False)
        respuesta_complejos = validar_respuesta(respuesta_complejos, codigo_complejos, 'Complejos')

        return render_template('vistas_lotes/complejo_residencial.html', notificaciones = respuesta_notificaciones, complejos =  respuesta_complejos, total_notificaciones=total_notificaciones)
    except Exception as error:
        print(f"Ocurrió un error al mostrar la vista de complejos: {error}.")
        raise Exception("Ocurrió un error al mostrar la vista de complejos.")

@bp.route("/lotes_complejo/<string:identificador_complejo>", methods=["GET", "POST"])
async def lotes_complejo(identificador_complejo):
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Validar que exista el token
        if not token:
            flash(Markup('<strong>Error</strong>: No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener los argumentos de búsqueda (filtros de la página)
        numero_seccion = request.args.get('tipoSeccion') or None
        tamano = request.args.get('tamaño') or None
        estado_vendido = request.args.get('estadoVendido') or None
        nombre_lote = request.args.get('nombre_lote') or None
        pagina = int(request.args.get('pagina', 1))
        tamano_pagina = int(request.args.get('tamano_pagina', 10))

        # Validar filtro de tamaño
        if tamano and tamano not in ['0-200', '200-400', '400-600', '600-800', '800-1000']:
            flash('Filtro no válido, intente nuevamente', category='error')
            return redirect(url_for('lotes.lotes_complejo', identificador_complejo=identificador_complejo))

        # Validar filtro de estado_vendido
        if estado_vendido and estado_vendido not in ['Proceso', 'Vendido', 'Disponible']:
            flash('Filtro no válido, intente nuevamente', category='error')
            return redirect(url_for('lotes.lotes_complejo', identificador_complejo=identificador_complejo))

        # Obtener las notificaciones, secciones y lotes
        respuesta_notificaciones, total_notificaciones,  codigo_estado = await NotificacionesController. \
            obtener_todas_notificaciones(token_acceso=token, notificaciones_no_leidas=True)
        respuesta_secciones, codigo_secciones = await LotesController. \
            obtener_secciones_filtro(identificador_complejo=identificador_complejo, token_acceso=token)
        respuesta_lotes, total, codigo_estado_lotes = await LotesController. \
            obtener_todos_lotes(identificador_complejo=identificador_complejo, token_acceso=token,
                                numero_seccion=numero_seccion, tamano=tamano, estado_vendido=estado_vendido,
                                pagina=pagina, tamano_pagina=tamano_pagina, nombre_lote=nombre_lote)

        # Verificar respuesta
        respuesta_notificaciones = validar_respuesta(respuesta_notificaciones, codigo_estado, 'Notificaciones', mostrar_mensaje=False)
        respuesta_secciones = validar_respuesta(respuesta_secciones, codigo_secciones, 'Secciones')
        respuesta_lotes = validar_respuesta(respuesta_lotes, codigo_estado_lotes, 'Lotes')

        return render_template('vistas_lotes/lotes.html', notificaciones = respuesta_notificaciones, lotes = respuesta_lotes, secciones = respuesta_secciones, \
                                pagina=pagina, tamano_pagina=tamano_pagina, total=total, identificador_complejo=identificador_complejo, \
                                total_notificaciones=total_notificaciones)
    except Exception as error:
        print(f"Ocurrió un error al cargar la vista de lotes. {error}.")
        raise Exception("Ocurrió un error al cargar la vista de lotes")

@bp.route("/lote_especifico/<string:identificador_lote>", methods=["GET", "POST"])
async def lote_especifico(identificador_lote):
    try:
        # Obtener token de sesión
        token = session.get('token')

        # Verificar que exista el token:
        if not token:
            flash(Markup('<strong>Error</strong>: No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener URL previa
        url_previa = session.get('previa_lote_especifico')

        # Verificar que exista
        if not url_previa:
            session['previa_lote_especifico'] = request.referrer
            url_previa = session.get('previa_lote_especifico')

        # Obtener las notificaciones y el lote
        respuesta_notificaciones, total_notificaciones,  codigo_estado = await NotificacionesController. \
            obtener_todas_notificaciones(token_acceso=token, notificaciones_no_leidas=True)
        respuesta_lote, codigo_estado_lote = await LotesController. \
            obtener_lote_especifico(identificador_lote=identificador_lote, token_acceso=token)
        respuesta_ubicacion, codigo_estado_ubicacion = await LotesController. \
            obtener_ubicacon_lote(identificador_lote=identificador_lote, token_acceso=token)

        # Verificar respuestas
        respuesta_notificaciones = validar_respuesta(respuesta_notificaciones, codigo_estado, 'Notificaciones', mostrar_mensaje=False)
        respuesta_lote = validar_respuesta(respuesta_lote, codigo_estado_lote, 'Lotes')
        respuesta_ubicacion = validar_respuesta(respuesta_ubicacion, codigo_estado_ubicacion, 'Ubicación')

        return render_template('vistas_lotes/lote_especifico.html', lotes=respuesta_lote, notificaciones = respuesta_notificaciones, \
                                url = url_previa, total_notificaciones=total_notificaciones, ubicacion=respuesta_ubicacion)
    except Exception as error:
        print(f"Ocurrió un error al cargar la vista de lote especifico. {error}.")
        raise Exception("Ocurrió un error al cargar la vista de lote especifico")

@bp.route("/lote_vendido/<string:identificador_lote>", methods=["GET", "POST"])
async def lote_vendido(identificador_lote):
    try:
        # Obtener token de sesión
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener URL previa
        url_previa = session.get('previa_lote_especifico')

        # Verificar que exista
        if not url_previa:
            session['previa_lote_especifico'] = request.referrer
            url_previa = session.get('previa_lote_especifico')

        # Obtener las notificaciones, el lote y su ubicación
        respuesta_notificaciones, total_notificaciones, codigo_estado = await NotificacionesController. \
            obtener_todas_notificaciones(token_acceso=token, notificaciones_no_leidas=True)
        respuesta_lote, codigo_estado_lote = await LotesController. \
            obtener_lote_especifico(identificador_lote=identificador_lote, token_acceso=token)
        respuesta_ubicacion, codigo_estado_ubicacion = await LotesController. \
            obtener_ubicacon_lote(identificador_lote=identificador_lote, token_acceso=token)
        respuesta_extra, codigo_estado_extra = await LotesController. \
            obtener_lote_venta(identificador_lote=identificador_lote, token_acceso=token)

        # Verificar respuestas
        respuesta_notificaciones = validar_respuesta(respuesta_notificaciones, codigo_estado, 'Notificaciones', mostrar_mensaje=False)
        respuesta_lote = validar_respuesta(respuesta_lote, codigo_estado_lote, 'Lote')
        respuesta_extra = validar_respuesta(respuesta_extra, codigo_estado_extra, 'Información Venta')
        respuesta_ubicacion = validar_respuesta(respuesta_ubicacion, codigo_estado_ubicacion, 'Ubicación')

        return render_template('vistas_lotes/lote_vendido.html', lotes=respuesta_lote, notificaciones = respuesta_notificaciones, \
                                url = url_previa, total_notificaciones=total_notificaciones, ubicacion=respuesta_ubicacion, \
                                venta = respuesta_extra)
    except Exception as error:
        print(f"Ocurrió un error al cargar la vista del lote vendido: {error}")
        raise Exception("Ocurrió un error al cargar la vista del lote vendido")

@bp.route("/agregar_estado_republica", methods=["GET"])
async def agregar_estado_republica():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token:
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa, intenta iniciando sesión'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener las notificaciones
        respuesta_notificaciones, total_notificaciones, codigo_estado = await NotificacionesController. \
            obtener_todas_notificaciones(token_acceso=token, notificaciones_no_leidas=True)

        # Verificar respuesta
        respuesta_notificaciones = validar_respuesta(respuesta_notificaciones, codigo_estado, 'Notificaciones', mostrar_mensaje=False)

        return render_template("agregar_nuevos_lotes/agregar_estado.html", notificaciones=respuesta_notificaciones, total_notificaciones=total_notificaciones)
    except Exception as error:
        print(f"Ocurrió un error al cargar la vista de agregar un estado: {error}")
        raise Exception("Ocurrió un error al cargar la vista de agregar un estado.")

@bp.route("/enviar_estado", methods=["POST"])
async def enviar_estado():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener el formulario enviado en diccionario
        formulario = request.form.to_dict()

        # Verificar formulario
        if not formulario:
            flash(Markup(f'<strong>Precaución</strong>: No se enviaron los datos.'), category='warning')
            return redirect(url_for('lotes.agregar_estado_republica'))

        errores = validar_formulario(formulario)

        # Verificar la existencia de un error
        if errores:
            flash(Markup(f'<strong>Precaución</strong>: {errores}'), category='warning')
            return redirect(url_for('lotes.agregar_estado_republica'))

        # Obtener respuesta al enviar los datos del vendedor
        respuesta_estado, codigo_estado = await LotesController. \
            agregar_estado(estado_agregar=formulario, token_acceso=token)

        # Verificar código de estado
        if codigo_estado == 201:
            flash(Markup('<strong>Éxito:</strong> Estado añadido con éxito'), category="message")
            return redirect(url_for('lotes.estados_republica'))
        else:
            # Validar respuesta
            respuesta_estado = validar_respuesta(respuesta_estado, codigo_estado, 'Estado')
            return redirect(url_for('lotes.agregar_estado_republica'))
    except Exception as error:
        print(f"Ocurrió un error al enviar la información del estado: {error}")
        raise Exception("Ocurrió un error al enviar la información del estado")

@bp.route("/enviar_estado_actualizado", methods=["POST"])
async def enviar_estado_actualizado():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener el formulario enviado en diccionario
        formulario = request.form.to_dict()

        # Verificar formulario
        if not formulario:
            flash(Markup(f'<strong>Precaución</strong>: No se enviaron los datos.'), category='warning')
            return redirect(url_for('lotes.estados_republica'))

        # Obtener los erros
        errores = validar_formulario(formulario)

        # Obtener el identificador del vendedor
        identificador_estado = formulario['identificador_estado']

        # Verificar la existencia de un error
        if errores:
            flash(Markup(f'<strong>Precaución</strong>: {errores}'), category='warning')
            return redirect(url_for('lotes.editar_estado', id_estado=identificador_estado))

        # Obtener respuesta al enviar el estado actualizado
        respuesta_estado, codigo_estado = await LotesController. \
            actualizar_un_estado(estado_actualizar=formulario, identificador_estado=identificador_estado, token_acceso=token)

        # Verificar código de estado
        if codigo_estado == 200:
            flash(Markup('<strong>Éxito:</strong> Estado actualizado con éxito'), category="message")
            return redirect(url_for('lotes.estados_republica'))
        else:
            # Validar respuesta
            respuesta_estado = validar_respuesta(respuesta_estado, codigo_estado, 'Estado')
            return redirect(url_for('lotes.editar_estado', id_estado=identificador_estado))
    except Exception as error:
        print(f"Ocurrió un error enviado los datos para actualizar: {error}")
        raise Exception("Ocurrió un error enviado los datos para actualizar")

@bp.route("/editar_estado/<string:id_estado>", methods=["GET"])
async def editar_estado(id_estado):
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup("<strong>Error:</strong> No tienes una sesión activa."), category="error")
            return redirect(url_for("generales.index"))

        # Obtener las notificaciones y el estado
        respuesta_notificaciones, total_notificaciones, codigo_estado = await NotificacionesController. \
            obtener_todas_notificaciones(token_acceso=token, notificaciones_no_leidas=True)

        respuesta_estado, codigo_estado_estado = await LotesController. \
            obtener_estado_especifico(identificador_estado=id_estado, token_acceso=token)

        # Validar respuesta
        respuesta_estado = validar_respuesta(respuesta_estado, codigo_estado_estado, 'Estado')
        respuesta_notificaciones = validar_respuesta(respuesta_notificaciones, codigo_estado, 'Notificaciones', mostrar_mensaje=False)

        return render_template("/editar_lotes/editar_estado.html", notificaciones = respuesta_notificaciones, estados = respuesta_estado,\
                                total_notificaciones=total_notificaciones)
    except Exception as error:
        print(f"Ocurrió un error al cargar la vista para editar un estado: {error}")
        raise Exception("Ocurrió un error al cargar la vista para editar un estado")

@bp.route("/eliminar_estado", methods=["POST"])
async def eliminar_estado():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener el identificador del vendedor
        datos_estado = request.get_json()

        # Verificar envio de datos
        if not datos_estado:
            flash(Markup(f'<strong>Precaución</strong>: No se enviaron datos. Intente nuevamente'), category='warning')
            return redirect(url_for('lotes.estados_republica'))

        # Obtener los datos correspondientes
        identificador_estado = datos_estado['identificador_estado']

        # Obtener respuesta al enviar el vendedor actualizado
        respuesta_estado, codigo_estado = await LotesController. \
            eliminar_un_estado(identificador_estado=identificador_estado, token_acceso=token)

        # Verificamos la respuesta de la API
        respuesta_estado = validar_respuesta(respuesta_estado, codigo_estado, 'Lote')

        # Verificar que exista una respuesta
        if respuesta_estado:
            flash(Markup(f'<strong>Éxito</strong>: Se eliminó correctamente el estado'), category='message')

        return jsonify({'success': True})
    except Exception as error:
        print(f"Ocurrió un error al enviar los datos para eliminar un estado: {error}")
        raise Exception("Ocurrió un error al enviar los datos para eliminar un estado")

@bp.route("/agregar_municipio", methods=["GET"])
async def agregar_municipio():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token:
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa, intenta iniciando sesión'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener las notificaciones
        respuesta_notificaciones, total_notificaciones, codigo_estado = await NotificacionesController. \
            obtener_todas_notificaciones(token_acceso=token, notificaciones_no_leidas=True)
        respuesta_estados, codigo_estados = await LotesController.obtener_todos_estados(token_acceso=token)

        # Verificar respuesta
        respuesta_notificaciones = validar_respuesta(respuesta_notificaciones, codigo_estado, 'Notificaciones',  mostrar_mensaje=False)
        respuesta_estados = validar_respuesta(respuesta_estados, codigo_estados, 'Estados')

        # Obtener URL previa
        url_previa = session.get('previa_municipio_ingresar')

        # Obtener url previa si no exista
        if not url_previa:
            session['previa_municipio_ingresar'] = request.referrer
            url_previa = session.get('previa_municipio_ingresar')

        estado = url_previa.split('/')[4]

        return render_template('agregar_nuevos_lotes/agregar_municipio.html', notificaciones = respuesta_notificaciones, \
                            total_notificaciones = total_notificaciones, estados=respuesta_estados, url_previa=url_previa, \
                            nombre=estado)
    except Exception as error:
        print(f"Ocurrió un error al cargar la vista de agregar municipio: {error}")
        raise Exception("Ocurrió un error al cargar la vista de agregar municipio")

@bp.route("/enviar_municipio", methods=["POST"])
async def enviar_municipio():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener el formulario enviado en diccionario
        formulario = request.form.to_dict()

        # Verificar formulario
        if not formulario:
            flash(Markup(f'<strong>Precaución</strong>: No se enviaron los datos.'), category='warning')
            return redirect(url_for('lotes.agregar_municipio'))

        errores = validar_formulario(formulario)

        # Verificar la existencia de un error
        if errores:
            flash(Markup(f'<strong>Precaución</strong>: {errores}'), category='warning')
            return redirect(url_for('lotes.agregar_municipio'))

        # Obtener respuesta al enviar los datos del vendedor
        respuesta_municipio, codigo_estado = await LotesController. \
            agregar_municipio(municipio_agregar=formulario, token_acceso=token)

        # Obtener estado
        url_previa = session.get('previa_municipio_ingresar')
        url_previa = url_previa.split('/')[4]

        # Verificar código de estado
        if codigo_estado == 201:
            session.pop('previa_municipio_ingresar', None)
            flash(Markup('<strong>Éxito:</strong> Municipio añadido con éxito'), category="message")
            return redirect(url_for('lotes.municipios_estado', identificador_estado = url_previa))
        else:
            # Validar respuesta
            respuesta_municipio = validar_respuesta(respuesta_municipio, codigo_estado, 'Municipio')
            return redirect(url_for('lotes.agregar_municipio'))
    except Exception as error:
        print(f"Ocurrió un error al enviar la información del municipio: {error}")
        raise Exception("Ocurrió un error al enviar la información del municipio")

@bp.route("/enviar_municipio_actualizado", methods=["POST"])
async def enviar_municipio_actualizado():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener el formulario enviado en diccionario
        formulario = request.form.to_dict()

        url_previa = session.get('previa_municipio_actualizar')

        # Verificar formulario
        if not formulario:
            flash(Markup(f'<strong>Precaución</strong>: No se enviaron los datos.'), category='warning')
            return redirect(url_previa)

        # Obtener los erros
        errores = validar_formulario(formulario)

        # Obtener el identificador del vendedor
        identificador_municipio = formulario['identificador_municipio']

        # Verificar la existencia de un error
        if errores:
            flash(Markup(f'<strong>Precaución</strong>: {errores}'), category='warning')
            return redirect(url_for('lotes.editar_municipio', id_municipio=identificador_municipio))

        # Obtener respuesta al enviar el municipio actualizado
        respuesta_municipio, codigo_estado = await LotesController. \
            actualizar_un_municipio(municipio_actualizar=formulario, identificador_municipio=identificador_municipio, token_acceso=token)

        # Obtener estado
        url_previa = url_previa.split('/')[4]

        # Verificar código de estado
        if codigo_estado == 200:
            session.pop('previa_municipio_actualizar', None)
            flash(Markup('<strong>Éxito:</strong> Municipio actualizado con éxito'), category="message")
            return redirect(url_for('lotes.municipios_estado', identificador_estado=url_previa))
        else:
            # Validar respuesta
            respuesta_municipio = validar_respuesta(respuesta_municipio, codigo_estado, 'Municipio')
            return redirect(url_for('lotes.editar_municipio', id_municipio=identificador_municipio))
    except Exception as error:
        print(f"Ocurrió un error enviado los datos para actualizar: {error}")
        raise Exception("Ocurrió un error enviado los datos para actualizar")

@bp.route("/editar_municipio/<string:id_municipio>", methods=["GET"])
async def editar_municipio(id_municipio):
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup("<strong>Error:</strong> No tienes una sesión activa."), category="error")
            return redirect(url_for("generales.index"))

        # Obtener las notificaciones y el estado
        respuesta_notificaciones, total_notificaciones, codigo_estado = await NotificacionesController. \
            obtener_todas_notificaciones(token_acceso=token, notificaciones_no_leidas=True)
        respuesta_estados, codigo_estados = await LotesController.obtener_todos_estados(token_acceso=token)
        respusta_municipio, codigo_estado_estado = await LotesController. \
            obtener_municipio_especifico(identificador_municipio=id_municipio, token_acceso=token)

        # Validar respuesta
        respuesta_estados = validar_respuesta(respuesta_estados, codigo_estados, 'Estados')
        respusta_municipio = validar_respuesta(respusta_municipio, codigo_estado_estado, 'Municipio')
        respuesta_notificaciones = validar_respuesta(respuesta_notificaciones, codigo_estado, 'Notificaciones', mostrar_mensaje=False)

        # Obtener url previa si no exista
        url_previa = session.get('previa_municipio_actualizar')

        if not url_previa:
            session['previa_municipio_actualizar'] = request.referrer
            url_previa = session.get('previa_municipio_actualizar')

        return render_template("/editar_lotes/editar_municipio.html", notificaciones = respuesta_notificaciones, municipios = respusta_municipio,\
                                total_notificaciones=total_notificaciones, estados=respuesta_estados, url_previa=url_previa)
    except Exception as error:
        print(f"Ocurrió un error al cargar la vista para editar un estado: {error}")
        raise Exception("Ocurrió un error al cargar la vista para editar un estado")

@bp.route("/eliminar_municipio", methods=["POST"])
async def eliminar_municipio():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener el identificador del vendedor
        datos_municipio = request.get_json()

        url_previa = request.referrer

        # Verificar envio de datos
        if not datos_municipio:
            flash(Markup(f'<strong>Precaución</strong>: No se enviaron datos. Intente nuevamente'), category='warning')
            return redirect(url_previa)

        # Obtener los datos correspondientes
        identificador_municipio = datos_municipio['identificador_municipio']

        # Obtener respuesta al enviar el vendedor actualizado
        respuesta_municipio, codigo_estado = await LotesController. \
            eliminar_un_municipio(identificador_municipio=identificador_municipio, token_acceso=token)

        # Verificamos la respuesta de la API
        respuesta_municipio = validar_respuesta(respuesta_municipio, codigo_estado, 'Municipio')

        # Verificar que exista una respuesta
        if respuesta_municipio:
            flash(Markup(f'<strong>Éxito</strong>: Se eliminó correctamente el municipio'), category='message')

        return jsonify({'success': True})
    except Exception as error:
        print(f"Ocurrió un error al enviar los datos para eliminar un estado: {error}")
        raise Exception("Ocurrió un error al enviar los datos para eliminar un estado")

@bp.route("/enviar_lote", methods=["POST"])
async def enviar_lote():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener el formulario enviado en diccionario
        formulario = request.form.to_dict()

        # Verificar formulario
        if not formulario:
            flash(Markup(f'<strong>Precaución</strong>: No se enviaron los datos.'), category='warning')
            return redirect(url_for('lotes.agregar_lote'))

        formulario['servicio_agua'] = False if 'servicio_agua' not in formulario else True
        formulario['servicio_electricidad'] = False if 'servicio_electricidad' not in formulario else True
        formulario['servicio_drenaje'] = False if 'servicio_drenaje' not in formulario else True
        formulario['estado_terreno'] = 'Disponible'

        errores = validar_formulario(formulario)

        # Verificar la existencia de un error
        if errores:
            flash(Markup(f'<strong>Precaución</strong>: {errores}'), category='warning')
            return redirect(url_for('lotes.agregar_lote'))

        # Obtener respuesta al enviar los datos del lote
        respuesta_lote, codigo_estado = await LotesController. \
            agregar_lote(lote_agregar=formulario, token_acceso=token)

        # Obtener complejo
        url_previa = session.get('previa_lotes_ingresar')

        url_previa = url_previa.split('/')[4]

        if '?' in url_previa:
            url_previa = url_previa.split('?')[0]

        complejo = urllib.parse.unquote(url_previa)

        # Verificar código de estado
        if codigo_estado == 201:
            session.pop('previa_lotes_ingresar', None)
            flash(Markup('<strong>Éxito</strong> Lote añadido con éxito'), category='message')
            return redirect(url_for('lotes.lotes_complejo', identificador_complejo=complejo))
        else:
            respuesta_lote = validar_respuesta(respuesta_lote, codigo_estado, 'Lote')
            return redirect(url_for('lotes.agregar_lote'))
    except Exception as error:
        print(f"Ocurrió un error al enviar la información del lote: {error}")
        raise Exception("Ocurrió un error al enviar la información del lote")

@bp.route("/agregar_lote", methods=["GET"])
async def agregar_lote():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token:
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa, intenta iniciando sesión'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener URL previa
        url_previa = session.get('previa_lotes_ingresar')

        # Verificar que exista
        if not url_previa:
            session['previa_lotes_ingresar'] = request.referrer
            url_previa = session.get('previa_lotes_ingresar')

        url_previa = url_previa.split('/')[4]
        if '?' in url_previa:
            url_previa = url_previa.split('?')[0]

        complejo = urllib.parse.unquote(url_previa)

        # Obtener los datos de la API
        respuesta_notificaciones, total_notificaciones, codigo_estado = await NotificacionesController. \
            obtener_todas_notificaciones(token_acceso=token, notificaciones_no_leidas=True)
        respuesta_secciones, codigo_estado_secciones = await LotesController. \
            obtener_secciones_filtro(identificador_complejo=complejo, token_acceso=token)
        respuesta_complejos, codigo_estados = await LotesController.obtener_todos_complejos_sin_localidad(token_acceso=token)

        # Verificar respuesta
        respuesta_notificaciones = validar_respuesta(respuesta_notificaciones, codigo_estado, 'Notificaciones', mostrar_mensaje=False)
        respuesta_secciones = validar_respuesta(respuesta_secciones, codigo_estado_secciones, 'Secciones')
        respuesta_complejos = validar_respuesta(respuesta_complejos, codigo_estados, 'Complejos')

        return render_template('agregar_nuevos_lotes/agregar_lote.html', notificaciones = respuesta_notificaciones, \
                            total_notificaciones = total_notificaciones, complejos=respuesta_complejos, url_previa=url_previa, \
                            secciones=respuesta_secciones)
    except Exception as error:
        print(f"Ocurrió un error al cargar la vista de agregar lotes: {error}")
        raise Exception("Ocurrió un error al cargar la vista de agregar lotes")

@bp.route("/editar_lote/<string:id_lote>", methods=["GET"])
async def editar_lote(id_lote):
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup("<strong>Error:</strong> No tienes una sesión activa."), category="error")
            return redirect(url_for("generales.index"))

        # Obtener las notificaciones y el estado
        respuesta_notificaciones, total_notificaciones, codigo_estado = await NotificacionesController. \
            obtener_todas_notificaciones(token_acceso=token, notificaciones_no_leidas=True)
        respuesta_secciones, codigo_estado_municipio = await LotesController. \
            obtener_secciones_filtro(identificador_complejo='Fraccionamiento la Loma', token_acceso=token)
        respuesta_lote, codigo_estado_estado = await LotesController. \
            obtener_lote_especifico(identificador_lote=id_lote, token_acceso=token)

        # Validar respuesta
        respuesta_secciones = validar_respuesta(respuesta_secciones, codigo_estado_municipio, 'Secciones')
        respuesta_lote = validar_respuesta(respuesta_lote, codigo_estado_estado, 'Lote')
        respuesta_notificaciones = validar_respuesta(respuesta_notificaciones, codigo_estado, 'Notificaciones', mostrar_mensaje=False)

        # Obtener URL previa
        url_previa = session.get('previa_lote_acciones')

        # Verificar que exista la url_previa
        if not url_previa:
            session['previa_lote_acciones'] = request.referrer
            url_previa = session.get('previa_lote_acciones')

        return render_template("/editar_lotes/editar_lote.html", notificaciones = respuesta_notificaciones, lotes = respuesta_lote,\
                                total_notificaciones=total_notificaciones, secciones=respuesta_secciones, url_previa=url_previa)
    except Exception as error:
        print(f"Ocurrió un error al cargar la vista para editar un estado: {error}")
        raise Exception("Ocurrió un error al cargar la vista para editar un estado")

@bp.route("/enviar_lote_actualizado", methods=["POST"])
async def enviar_lote_actualizado():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener el formulario enviado en diccionario
        formulario = request.form.to_dict()

        url_previa = session.get('previa_lote_acciones')

        # Verificar formulario
        if not formulario:
            flash(Markup(f'<strong>Precaución</strong>: No se enviaron los datos.'), category='warning')
            return redirect(url_previa)

        # Obtener los erros
        errores = validar_formulario(formulario)

        # Obtener el identificador del vendedor
        identificador_lote = formulario['identificador_lote']
        formulario['servicio_agua'] = False if 'servicio_agua' not in formulario else True
        formulario['servicio_electricidad'] = False if 'servicio_electricidad' not in formulario else True
        formulario['servicio_drenaje'] = False if 'servicio_drenaje' not in formulario else True

        # Verificar la existencia de un error
        if errores:
            flash(Markup(f'<strong>Precaución</strong>: {errores}'), category='warning')
            return redirect(url_for('lotes.editar_lote', id_lote=identificador_lote))

        # Obtener respuesta al enviar el complejo actualizado
        respuesta_complejo, codigo_estado = await LotesController. \
            actualizar_un_lote(lote_actualizar=formulario, identificador_lote=identificador_lote, token_acceso=token)

        # Obtener el lote previo
        url_previa = url_previa.split('/')[4]

        # Verificar código de estado
        if codigo_estado == 200:
            session.pop('previa_lote_acciones',None)
            flash(Markup('<strong>Éxito:</strong> Lote actualizado con éxito'), category="message")
            return redirect(url_for('lotes.lote_especifico', identificador_lote=url_previa))
        else:
            # Validar respuesta
            respuesta_complejo = validar_respuesta(respuesta_complejo, codigo_estado, 'Lote')
            return redirect(url_for('lotes.editar_lote', id_lote=url_previa))
    except Exception as error:
        print(f"Ocurrió un error enviado los datos para actualizar: {error}")
        raise Exception("Ocurrió un error enviado los datos para actualizar")

@bp.route("/eliminar_lote", methods=["POST"])
async def eliminar_lote():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener el identificador del vendedor
        datos_lote = request.get_json()

        url_previa = request.referrer

        # Verificar envio de datos
        if not datos_lote:
            flash(Markup(f'<strong>Precaución</strong>: No se enviaron datos. Intente nuevamente'), category='warning')
            return redirect(url_previa)

        # Obtener los datos correspondientes
        identificador_lote = datos_lote['identificador_lote']

        # Obtener respuesta al enviar el vendedor actualizado
        respuesta_lote, codigo_estado = await LotesController. \
            eliminar_un_lote(identificador_lote=identificador_lote, token_acceso=token)

        # Verificamos la respuesta de la API
        respuesta_lote = validar_respuesta(respuesta_lote, codigo_estado, 'Lote')

        # Verificar que exista una respuesta
        if respuesta_lote:
            flash(Markup(f'<strong>Éxito</strong>: Se eliminó correctamente el lote'), category='message')

        return jsonify({'success': True})
    except Exception as error:
        print(f"Ocurrió un error al enviar los datos para eliminar un estado: {error}")
        raise Exception("Ocurrió un error al enviar los datos para eliminar un estado")

@bp.route("/enviar_complejo_residencial", methods=["POST"])
async def enviar_complejo_residencial():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener el formulario enviado en diccionario
        formulario = request.form.to_dict()

        # Verificar formulario
        if not formulario:
            flash(Markup(f'<strong>Precaución</strong>: No se enviaron los datos.'), category='warning')
            return redirect(url_for('lotes.agregar_complejo_residencial'))

        errores = validar_formulario(formulario)

        # Verificar la existencia de un error
        if errores:
            flash(Markup(f'<strong>Precaución</strong>: {errores}'), category='warning')
            return redirect(url_for('lotes.agregar_complejo_residencial'))

        # Obtener respuesta al enviar los datos del complejo
        respuesta_complejo, codigo_estado = await LotesController. \
            agregar_complejo(complejo_agregar=formulario, token_acceso=token)

        # Obtener localidad
        url_previa = session.get('previa_complejo_ingresar')

        url_previa = url_previa.split('/')[4]

        if '?' in url_previa:
            url_previa = url_previa.split('?')[0]

        localidad = urllib.parse.unquote(url_previa)

        # Verificar código de estado
        if codigo_estado == 201:
            session.pop('previa_complejo_ingresar', None)
            flash(Markup('<strong>Éxito:</strong> Complejo residencial añadido con éxito'), category="message")
            return redirect(url_for('lotes.complejo_residencial', identificador_localidad=localidad ))
        else:
            # Validar respuesta
            respuesta_complejo = validar_respuesta(respuesta_complejo, codigo_estado, 'Complejo')
            return redirect(url_for('lotes.agregar_complejo_residencial'))
    except Exception as error:
        print(f"Ocurrió un error al enviar la información del estado: {error}")
        raise Exception("Ocurrió un error al enviar la información del estado")

@bp.route("/eliminar_complejo", methods=["POST"])
async def eliminar_complejo():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener el identificador del vendedor
        datos_complejo = request.get_json()

        url_previa = request.referrer

        # Verificar envio de datos
        if not datos_complejo:
            flash(Markup(f'<strong>Precaución</strong>: No se enviaron datos. Intente nuevamente'), category='warning')
            return redirect(url_previa)

        # Obtener los datos correspondientes
        identificador_complejo = datos_complejo['identificador_complejo']

        # Obtener respuesta al enviar el vendedor actualizado
        respuesta_complejo, codigo_estado = await LotesController. \
            eliminar_un_complejo(identificador_complejo=identificador_complejo, token_acceso=token)

        # Verificamos la respuesta de la API
        respuesta_complejo = validar_respuesta(respuesta_complejo, codigo_estado, 'Complejo')

        # Verificar que exista una respuesta
        if respuesta_complejo:
            flash(Markup(f'<strong>Éxito</strong>: Se eliminó correctamente el complejo residencial'), category='message')

        return jsonify({'success': True})
    except Exception as error:
        print(f"Ocurrió un error al enviar los datos para eliminar un complejo: {error}")
        raise Exception("Ocurrió un error al enviar los datos para eliminar un complejo")

@bp.route("/enviar_complejo_actualizado", methods=["POST"])
async def enviar_complejo_actualizado():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener el formulario enviado en diccionario
        formulario = request.form.to_dict()

        url_previa = session.get('previa_complejo_actualizar')

        # Verificar formulario
        if not formulario:
            flash(Markup(f'<strong>Precaución</strong>: No se enviaron los datos.'), category='warning')
            return redirect(url_previa)

        # Obtener los erros
        errores = validar_formulario(formulario)

        # Obtener el identificador del vendedor
        identificador_complejo = formulario['identificador_complejo']

        # Verificar la existencia de un error
        if errores:
            flash(Markup(f'<strong>Precaución</strong>: {errores}'), category='warning')
            return redirect(url_for('lotes.editar_complejo', id_complejo=identificador_complejo))

        # Obtener respuesta al enviar el complejo actualizado
        respuesta_complejo, codigo_estado = await LotesController. \
            actualizar_un_complejo(complejo_actualizar=formulario, identificador_complejo=identificador_complejo, token_acceso=token)

        # Obtener localidad
        url_previa = url_previa.split('/')[4]

        if '?' in url_previa:
            url_previa = url_previa.split('?')[0]

        localidad = urllib.parse.unquote(url_previa)

        # Verificar código de estado
        if codigo_estado == 200:
            session.pop('previa_complejo_actualizar', None)
            flash(Markup('<strong>Éxito:</strong> Complejo actualizado con éxito'), category="message")
            return redirect(url_for('lotes.complejo_residencial', identificador_localidad=localidad))
        else:
            # Validar respuesta
            respuesta_complejo = validar_respuesta(respuesta_complejo, codigo_estado, 'Complejo')
            return redirect(url_for('lotes.editar_complejo', id_complejo=identificador_complejo))
    except Exception as error:
        print(f"Ocurrió un error enviado los datos para actualizar: {error}")
        raise Exception("Ocurrió un error enviado los datos para actualizar")

@bp.route("/editar_complejo/<string:id_complejo>", methods=["GET"])
async def editar_complejo(id_complejo):
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup("<strong>Error:</strong> No tienes una sesión activa."), category="error")
            return redirect(url_for("generales.index"))

        # Obtener las notificaciones y el estado
        respuesta_notificaciones, total_notificaciones, codigo_estado = await NotificacionesController. \
            obtener_todas_notificaciones(token_acceso=token, notificaciones_no_leidas=True)
        respuesta_localidades, codigo_estado_municipio = await LotesController.obtener_todas_localidades_sin_municipio(token_acceso=token)
        respuesta_complejo, codigo_estado_estado = await LotesController. \
            obtener_complejo_especifico(identificador_complejo=id_complejo, token_acceso=token)

        # Validar respuesta
        respuesta_localidades = validar_respuesta(respuesta_localidades, codigo_estado_municipio, 'Localidades')
        respuesta_complejo = validar_respuesta(respuesta_complejo, codigo_estado_estado, 'Complejo')
        respuesta_notificaciones = validar_respuesta(respuesta_notificaciones, codigo_estado, 'Notificaciones', mostrar_mensaje=False)

        # Obtener URL previa
        url_previa = session.get('previa_complejo_actualizar')

        # Obtener URL previa si no existe
        if not url_previa:
            session['previa_complejo_actualizar'] = request.referrer
            url_previa = session.get('previa_complejo_actualizar')

            url_previa = url_previa.split('/')[4]
            if '?' in url_previa:
                url_previa = url_previa.split('?')[0]

        localidad = urllib.parse.unquote(url_previa)

        return render_template("/editar_lotes/editar_complejo_residencial.html", notificaciones = respuesta_notificaciones, complejos = respuesta_complejo,\
                                total_notificaciones=total_notificaciones, localidades=respuesta_localidades, url_previa=localidad)
    except Exception as error:
        print(f"Ocurrió un error al cargar la vista para editar un estado: {error}")
        raise Exception("Ocurrió un error al cargar la vista para editar un estado")

@bp.route("/agregar_complejo_residencial", methods=["GET"])
async def agregar_complejo_residencial():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token:
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa, intenta iniciando sesión'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener las notificaciones
        respuesta_notificaciones, total_notificaciones, codigo_estado = await NotificacionesController. \
            obtener_todas_notificaciones(token_acceso=token, notificaciones_no_leidas=True)
        respuesta_localidades, codigo_estados = await LotesController.obtener_todas_localidades_sin_municipio(token_acceso=token)

        # Verificar respuesta
        respuesta_notificaciones = validar_respuesta(respuesta_notificaciones, codigo_estado, 'Notificaciones', mostrar_mensaje=False)
        respuesta_localidades = validar_respuesta(respuesta_localidades, codigo_estados, 'Localidades')

        # Obtener URL previa
        url_previa = session.get('previa_complejo_ingresar')

        # Obtener URL previa si no existe
        if not url_previa:
            session['previa_complejo_ingresar'] = request.referrer
            url_previa = session.get('previa_complejo_ingresar')

            url_previa = url_previa.split('/')[4]
            if '?' in url_previa:
                url_previa = url_previa.split('?')[0]

        localidad = urllib.parse.unquote(url_previa)

        return render_template('agregar_nuevos_lotes/agregar_complejo_residencial.html', notificaciones = respuesta_notificaciones, \
                            total_notificaciones = total_notificaciones, localidades=respuesta_localidades, url_previa=url_previa, \
                            nombre=localidad)
    except Exception as error:
        print(f"Ocurrió un error al cargar la vista de agregar nuevo complejo: {error}")
        raise Exception("Ocurrió un error al cargar la vista de agregar nuevo complejo")

@bp.route("/enviar_localidad", methods=["POST"])
async def enviar_localidad():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener el formulario enviado en diccionario
        formulario = request.form.to_dict()

        # Verificar formulario
        if not formulario:
            flash(Markup(f'<strong>Precaución</strong>: No se enviaron los datos.'), category='warning')
            return redirect(url_for('lotes.agregar_localidad'))

        errores = validar_formulario(formulario)

        # Verificar la existencia de un error
        if errores:
            flash(Markup(f'<strong>Precaución</strong>: {errores}'), category='warning')
            return redirect(url_for('lotes.agregar_localidad'))

        # Obtener respuesta al enviar los datos del vendedor
        respuesta_localidad, codigo_estado = await LotesController. \
            agregar_localidad(localidad_agregar=formulario, token_acceso=token)

        # Obtener municipio
        url_previa = session.get('previa_localidad_ingresar')
        url_previa = urllib.parse.unquote(url_previa.split('/')[4])

        # Verificar código de estado
        if codigo_estado == 201:
            session.pop('previa_localidad_ingresar', None)
            flash(Markup('<strong>Éxito:</strong> Localidad añadida con éxito'), category="message")
            return redirect(url_for('lotes.localidad_municipio', identificador_municipio = url_previa))
        else:
            # Validar respuesta
            respuesta_localidad = validar_respuesta(respuesta_localidad, codigo_estado, 'Localidad')
            return redirect(url_for('lotes.agregar_localidad'))
    except Exception as error:
        print(f"Ocurrió un error al enviar la información del estado: {error}")
        raise Exception("Ocurrió un error al enviar la información del estado")

@bp.route("/agregar_localidad", methods=["GET"])
async def agregar_localidad():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token:
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa, intenta iniciando sesión'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener las notificaciones
        respuesta_notificaciones, total_notificaciones, codigo_estado = await NotificacionesController. \
            obtener_todas_notificaciones(token_acceso=token, notificaciones_no_leidas=True)
        respuesta_municipios, codigo_estados = await LotesController.obtener_todos_municipios_sin_estado(token_acceso=token)

        # Verificar respuesta
        respuesta_notificaciones = validar_respuesta(respuesta_notificaciones, codigo_estado, 'Notificaciones', mostrar_mensaje=False)
        respuesta_municipios = validar_respuesta(respuesta_municipios, codigo_estados, 'Municipio')

        # Obtener URL previa
        url_previa = session.get('previa_localidad_ingresar')

        # Obtener URL previa si no exista
        if not url_previa:
            session['previa_localidad_ingresar'] = request.referrer
            url_previa = session.get('previa_localidad_ingresar')

        municipio = urllib.parse.unquote(url_previa.split('/')[4])

        return render_template('agregar_nuevos_lotes/agregar_localidad.html', notificaciones = respuesta_notificaciones, \
                            total_notificaciones = total_notificaciones, municipios=respuesta_municipios, url_previa=url_previa, \
                            nombre=municipio)
    except Exception as error:
        print(f"Ocurrió un error al cargar la vista de agregar localidad: {error}")
        raise Exception("Ocurrió un error al cargar la vista de agregar localidad")

@bp.route("/editar_localidad/<string:id_localidad>", methods=["GET"])
async def editar_localidad(id_localidad):
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup("<strong>Error:</strong> No tienes una sesión activa."), category="error")
            return redirect(url_for("generales.index"))

        # Obtener las notificaciones y el estado
        respuesta_notificaciones, total_notificaciones, codigo_estado = await NotificacionesController. \
            obtener_todas_notificaciones(token_acceso=token, notificaciones_no_leidas=True)
        respuesta_municipios, codigo_estado_municipio = await LotesController.obtener_todos_municipios_sin_estado(token_acceso=token)
        respuesta_localidad, codigo_estado_estado = await LotesController. \
            obtener_localidad_especifica(identificador_localidad=id_localidad, token_acceso=token)

        # Validar respuesta
        respuesta_municipios = validar_respuesta(respuesta_municipios, codigo_estado_municipio, 'Municipios')
        respuesta_localidad = validar_respuesta(respuesta_localidad, codigo_estado_estado, 'Localidad')
        respuesta_notificaciones = validar_respuesta(respuesta_notificaciones, codigo_estado, 'Notificaciones', mostrar_mensaje=False)

        # Obtener url previa
        url_previa = session.get('previa_localidad_actualizar')

        # Verificar que exista la url
        if not url_previa:
            session['previa_localidad_actualizar'] = request.referrer
            url_previa = session.get('previa_localidad_actualizar')

        return render_template("/editar_lotes/editar_localidad.html", notificaciones = respuesta_notificaciones, localidades = respuesta_localidad,\
                                total_notificaciones=total_notificaciones, municipios=respuesta_municipios, url_previa=url_previa)
    except Exception as error:
        print(f"Ocurrió un error al cargar la vista para editar un estado: {error}")
        raise Exception("Ocurrió un error al cargar la vista para editar un estado")

@bp.route("/enviar_localidad_actualizada", methods=["POST"])
async def enviar_localidad_actualizada():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener el formulario enviado en diccionario
        formulario = request.form.to_dict()

        url_previa = session.get('previa_localidad_actualizar')

        # Verificar formulario
        if not formulario:
            flash(Markup(f'<strong>Precaución</strong>: No se enviaron los datos.'), category='warning')
            return redirect(url_previa)

        # Obtener los erros
        errores = validar_formulario(formulario)

        # Obtener el identificador del vendedor
        identificador_localidad = formulario['identificador_localidad']

        # Verificar la existencia de un error
        if errores:
            flash(Markup(f'<strong>Precaución</strong>: {errores}'), category='warning')
            return redirect(url_for('lotes.editar_localidad', id_localidad=identificador_localidad))

        # Obtener respuesta al enviar el Haciendalocalida d actualizado
        respuesta_localidad, codigo_estado = await LotesController. \
            actualizar_una_localidad(localidad_actualizar=formulario, identificador_localidad=identificador_localidad, token_acceso=token)

        # Obyener estado
        url_previa = urllib.parse.unquote(url_previa.split('/')[4])

        # Verificar código de estado
        if codigo_estado == 200:
            session.pop('previa_localidad_actualizar', None)
            flash(Markup('<strong>Éxito:</strong> Localidad actualizada con éxito'), category="message")
            return redirect(url_for('lotes.localidad_municipio', identificador_municipio=url_previa))
        else:
            # Validar respuesta
            respuesta_localidad = validar_respuesta(respuesta_localidad, codigo_estado, 'Localidad')
            return redirect(url_for('lotes.editar_localidad', id_localidad=identificador_localidad))
    except Exception as error:
        print(f"Ocurrió un error enviado los datos para actualizar: {error}")
        raise Exception("Ocurrió un error enviado los datos para actualizar")

@bp.route("/eliminar_localidad", methods=["POST"])
async def eliminar_localidad():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener el identificador del vendedor
        datos_localidad = request.get_json()

        url_previa = request.referrer

        # Verificar envio de datos
        if not datos_localidad:
            flash(Markup(f'<strong>Precaución</strong>: No se enviaron datos. Intente nuevamente'), category='warning')
            return redirect(url_previa)

        # Obtener los datos correspondientes
        identificador_localidad = datos_localidad['identificador_localidad']

        # Obtener respuesta al enviar el vendedor actualizado
        respuesta_localidad, codigo_estado = await LotesController. \
            eliminar_una_localidad(identificador_localidad=identificador_localidad, token_acceso=token)

        # Verificamos la respuesta de la API
        respuesta_localidad = validar_respuesta(respuesta_localidad, codigo_estado, 'Localidad')

        # Verificar que exista una respuesta
        if respuesta_localidad:
            flash(Markup(f'<strong>Éxito</strong>: Se eliminó correctamente la localidad'), category='message')

        return jsonify({'success': True})
    except Exception as error:
        print(f"Ocurrió un error al enviar los datos para eliminar una localidad: {error}")
        raise Exception("Ocurrió un error al enviar los datos para eliminar una localidad")

@bp.route("/enviar_seccion", methods=["POST"])
async def enviar_seccion():
    try:
        # Obtener token de acceso
        token =session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa, intenta iniciando sesión'), category="error")
            return redirect(url_for('generales.index'))

        # Obtener el formulario enviado en diccionario
        formulario = request.form.to_dict()

        # Verficar formulario
        if not formulario:
            flash(Markup(f'<strong>Precaución</strong>: No se enviaron los datos.'), category='warning')
            return redirect(url_for('lotes.agregar_seccion'))

        errores = validar_formulario(formulario)

        # Verificar la existencia de un error
        if errores:
            flash(Markup(f'<strong>Precaución</strong>: {errores}'), category='warning')
            return redirect(url_for('lotes.agregar_seccion'))

        # Obtener respuesta al enviar los datos de la sección
        respuesta_seccion, codigo_estado = await LotesController. \
            agregar_seccion(seccion_agregar=formulario, token_acceso=token)

        # Obtener complejo
        url_previa = session.get('previa_lotes_ingresar')

        url_previa = url_previa.split('/')[4]

        if '?' in url_previa:
            url_previa = url_previa.split('?')[0]

        complejo = urllib.parse.unquote(url_previa)

        # Verificar código de estado
        if codigo_estado == 201:
            session.pop('previa_lotes_ingresar', None)
            flash(Markup('<strong>Éxito: </strong> Sección añadida con éxito'), category="message")
            return redirect(url_for('lotes.lotes_complejo', identificador_complejo=complejo))
        else:
            # Validar respuesta
            respuesta_seccion = validar_respuesta(respuesta_seccion, codigo_estado, 'Sección')
            return redirect(url_for('lotes.agregar_seccion'))

    except Exception as error:
        print(f"Ocurrió un error al enviar los datos para añadir una nueva sección: {error}")
        raise Exception("Ocurrió un error al enviar los datos para añadir una nueva sección")

@bp.route("/agregar_seccion", methods=["GET"])
async def agregar_seccion():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa, intenta iniciando sesión'), category="error")
            return redirect(url_for('generales.index'))

        # Obtener las notificaciones
        respuesta_notificaciones,total_notificaciones, codigo_estado = await NotificacionesController. \
            obtener_todas_notificaciones(token_acceso=token, notificaciones_no_leidas=True)
        respuesta_complejos, codigo_estados = await LotesController.obtener_todos_complejos_sin_localidad(token_acceso=token)

        # Verificar respuesta
        respuesta_notificaciones = validar_respuesta(respuesta_notificaciones, codigo_estado, 'Notificaciones',  mostrar_mensaje=False)
        respuesta_complejos = validar_respuesta(respuesta_complejos, codigo_estados, 'Complejos')

        # Obtener URL previa
        url_previa = session.get('previa_lotes_ingresar')

        # Verificar que exista
        if not url_previa:
            session['previa_lotes_ingresar'] = request.referrer
            url_previa = session.get('previa_lotes_ingresar')

        url_previa = url_previa.split('/')[4]
        if '?' in url_previa:
            url_previa = url_previa.split('?')[0]

        complejo = urllib.parse.unquote(url_previa)

        return render_template('agregar_nuevos_lotes/agregar_seccion.html', notificaciones = respuesta_notificaciones, \
                            total_notificaciones = total_notificaciones, complejos=respuesta_complejos, url_previa=url_previa, \
                            nombre=complejo)
    except Exception as error:
        print(f"Ocurrió un error al cargar la vista de agregar sección: {error}")
        raise Exception("Ocurrió un error al cargar la vista de agregar sección")

@bp.route("/obtener_token_lote", methods=["GET"])
async def obtener_token_lote():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup("<strong>Error:</strong> No tienes una sesión activa."), category="error")
            return redirect(url_for("generales.index"))

        return jsonify({'success': True, 'token': token})
    except Exception as error:
        print(f"Ocurrió un error al enviar el token: {error}")
        raise Exception("Ocurrió un error al enviar el token")

@bp.route("/editar_seccion/", methods=["GET"])
async def editar_seccion():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup("<strong>Error:</strong> No tienes una sesión activa."), category="error")
            return redirect(url_for("generales.index"))

        # Obtener URL previa
        url_previa = session.get('previa_lotes_ingresar')

        # Verificar que exista
        if not url_previa:
            session['previa_lotes_ingresar'] = request.referrer
            url_previa = session.get('previa_lotes_ingresar')

        url_previa = url_previa.split('/')[4]
        if '?' in url_previa:
            url_previa = url_previa.split('?')[0]

        seccion = urllib.parse.unquote(url_previa)

        # Obtener las notificaciones y el estado
        respuesta_notificaciones, total_notificaciones, codigo_estado = await NotificacionesController. \
            obtener_todas_notificaciones(token_acceso=token, notificaciones_no_leidas=True)
        respuesta_seccion, codigo_estado_estado = await LotesController. \
            obtener_secciones_filtro(identificador_complejo=seccion, token_acceso=token)

        # Validar respuesta
        respuesta_seccion = validar_respuesta(respuesta_seccion, codigo_estado_estado, 'Seccion')
        respuesta_notificaciones = validar_respuesta(respuesta_notificaciones, codigo_estado, 'Notificaciones', mostrar_mensaje=False)

        return render_template("/editar_lotes/editar_seccion.html", notificaciones = respuesta_notificaciones, secciones = respuesta_seccion,\
                                total_notificaciones=total_notificaciones)
    except Exception as error:
        print(f"Ocurrió un error al cargar la vista para editar una sección: {error}")
        raise Exception("Ocurrió un error al cargar la vista para editar una sección")

@bp.route("/enviar_seccion_actualizada", methods=["POST"])
async def enviar_seccion_actualizada():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener el formulario enviado en diccionario
        formulario = request.form.to_dict()

        url_previa = session.get('previa_lotes_ingresar')

        # Verificar formulario
        if not formulario:
            flash(Markup(f'<strong>Precaución</strong>: No se enviaron los datos.'), category='warning')
            return redirect(url_previa)

        # Obtener los erros
        errores = validar_formulario(formulario)

        # Obtener el identificador del vendedor
        identificador_seccion = formulario['identificador_seccion']

        # Verificar la existencia de un error
        if errores:
            flash(Markup(f'<strong>Precaución</strong>: {errores}'), category='warning')
            return redirect(url_for('lotes.editar_seccion'))

        # Obtener respuesta al enviar el Haciendalocalida d actualizado
        respuesta_seccion, codigo_estado = await LotesController. \
            actualizar_una_seccion(seccion_actualizar=formulario, identificador_seccion=identificador_seccion, token_acceso=token)

        # Obtener complejo
        url_previa = url_previa.split('/')[4]

        if '?' in url_previa:
            url_previa = url_previa.split('?')[0]

        complejo = urllib.parse.unquote(url_previa)

        # Verificar código de estado
        if codigo_estado == 200:
            session.pop('previa_lotes_ingresar', None)
            flash(Markup('<strong>Éxito:</strong> Localidad actualizada con éxito'), category="message")
            return redirect(url_for('lotes.lotes_complejo', identificador_complejo=complejo))
        else:
            # Validar respuesta
            respuesta_seccion = validar_respuesta(respuesta_seccion, codigo_estado, 'Seccion')
            return redirect(url_for('lotes.editar_seccion'))
    except Exception as error:
        print(f"Ocurrió un error enviado los datos para actualizar: {error}")
        raise Exception("Ocurrió un error enviado los datos para actualizar")

@bp.route("/eliminar_seccion", methods=["POST"])
async def eliminar_seccion():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener el identificador del vendedor
        datos_seccion = request.get_json()

        url_previa = request.referrer

        # Verificar envio de datos
        if not datos_seccion:
            flash(Markup(f'<strong>Precaución</strong>: No se enviaron datos. Intente nuevamente'), category='warning')
            return redirect(url_previa)

        # Obtener los datos correspondientes
        identificador_seccion = datos_seccion['identificador_seccion']

        # Obtener respuesta al enviar el vendedor actualizado
        respuesta_complejo, codigo_estado = await LotesController. \
            eliminar_una_seccion(identificador_seccion=identificador_seccion, token_acceso=token)

        # Verificamos la respuesta de la API
        respuesta_complejo = validar_respuesta(respuesta_complejo, codigo_estado, 'Sección')

        # Verificar que exista una respuesta
        if respuesta_complejo:
            flash(Markup(f'<strong>Éxito</strong>: Se eliminó correctamente la sección'), category='message')

        return jsonify({'success': True})
    except Exception as error:
        print(f"Ocurrió un error al enviar los datos para eliminar un complejo: {error}")
        raise Exception("Ocurrió un error al enviar los datos para eliminar un complejo")

@bp.route("/eliminar_url_previa", methods=["POST"])
async def eliminar_url_previa():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener el identificador del vendedor
        datos_url = request.get_json()

        regresar = request.referrer

        # Verificar envio de datos
        if not datos_url:
            flash(Markup(f'<strong>Precaución</strong>: No se enviaron datos. Intente nuevamente'), category='warning')
            return redirect(regresar)

        # Obtener la URL a eliminar
        url_eliminar = datos_url['objetivo_url']

        # Guardarla para redireccionarla
        url_previa = session.get(url_eliminar)

        print(url_previa)

        # Eliminarla
        session.pop(url_eliminar, None)

        return jsonify({'success': True, 'url_previa': url_previa})
    except Exception as error:
        print(f"Ocurrió un error al enviar los datos para eliminar un complejo: {error}")
        raise Exception("Ocurrió un error al enviar los datos para eliminar un complejo")