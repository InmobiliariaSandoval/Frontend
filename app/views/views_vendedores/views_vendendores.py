"""
    Archivo que administra las vistas del
    apartado de vendedores
"""

from flask import Blueprint, render_template, session, request, url_for, jsonify, flash, redirect
from ...controllers.controllers_notificaciones import NotificacionesController
from ...controllers.controllers_vendedores import VendedoresController
from ...error_handlers import validar_respuesta
from ...validadores import validar_formulario
from markupsafe import Markup

# Registrar las vistas
bp = Blueprint('vendedores', __name__)

#######################
# Vista de vendedores #
#######################

@bp.route("/ver_vendedores", methods=["GET", "POST"])
async def ver_vendedores():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener filtro de búsqueda
        tipo_filtro = request.args.get('vendedores')
        pagina = int(request.args.get('pagina', 1))
        tamano = int(request.args.get('tamano', 10))
        tipo_estado = request.args.get('tipo_estado')

        # Cambiar el valor
        if tipo_filtro and tipo_filtro == 'todos':
            tipo_filtro = None

        # Verificar filtro
        if (tipo_filtro and tipo_filtro not in ['mas', 'todos', 'menos']
            or tipo_estado and tipo_estado not in ['Activos', 'Suspendidos']):
            flash(Markup('<strong>Precaución:</strong> Filtro no válido, intente nuevamente'), category='warning')
            return redirect(url_for('vendedores.ver_vendedores', pagina = pagina, tamano = tamano))

        # Obtener las notificaciones y los vendedores
        respuesta_notificaciones, total_notificaciones, codigo_estado = await NotificacionesController. \
            obtener_todas_notificaciones(token_acceso=token, notificaciones_no_leidas=True)

        respuesta_vendedor, total, codigo_estado_vendedor = await VendedoresController.\
            obtener_todos_vendedores(token_acceso=token, tipo_filtro=tipo_filtro, tipo_estado=tipo_estado, numero_pagina=pagina,tamano_pagina=tamano)

        # Validar respuestas
        respuesta_vendedor = validar_respuesta(respuesta_vendedor, codigo_estado_vendedor, 'Vendedor')
        respuesta_notificaciones = validar_respuesta(respuesta_notificaciones, codigo_estado, 'Notificaciones', mostrar_mensaje=False)

        return render_template('vistas_vendedores/ver_vendedores.html', notificaciones = respuesta_notificaciones, vendedores = respuesta_vendedor, \
                               pagina=pagina, tamano=tamano, total=total, total_notificaciones=total_notificaciones)
    except Exception as error:
        print(f"Ocurrrió un error al cargar la vista de vendedores: {error}.")
        raise Exception("Ocurrrió un error al cargar la vista de vendedores.")

@bp.route("/vendedor_especifico/<string:identificador_vendedor>", methods=["GET", "POST"])
async def vendedor_especifico(identificador_vendedor):
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener las notificaciones y el vendedor
        respuesta_notificaciones, total_notificaciones, codigo_estado = await NotificacionesController. \
            obtener_todas_notificaciones(token_acceso=token, notificaciones_no_leidas=True)

        respuesta_vendedor, codigo_estado_vendedor = await VendedoresController. \
            obtener_vendedor(identificador_vendedor, token)

        # Validar respuestas
        respuesta_vendedor = validar_respuesta(respuesta_vendedor, codigo_estado_vendedor, 'Vendedor')
        respuesta_notificaciones = validar_respuesta(respuesta_notificaciones, codigo_estado, 'Notificaciones', mostrar_mensaje=False)

        return render_template('vistas_vendedores/vendedor_especifico.html', notificaciones = respuesta_notificaciones, vendedores = respuesta_vendedor,\
                                total_notificaciones=total_notificaciones)
    except Exception as error:
        print(f"Ocurrió un error al cargar la vista de vendedor: {error}.")
        raise Exception("Ocurrió un error al cargar la vista de vendedor.")

@bp.route("/cancelar_formulario", methods=["POST"])
async def cancelar_formulario():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Verificar que exista una sesión que cerrar
        formulario = session.get('form_data')

        if formulario:
            session.pop('form_data', None)

        return jsonify({'success': True})

    except Exception as error:
        print(f"Ocurrió un error al cancelar formulario: {error}")
        raise Exception(f"Ocurrio un error al cancelar formulario")

@bp.route("/enviar_vendedor", methods=["POST"])
async def enviar_vendedor():
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
            return redirect(url_for('vendedores.agregar_vendedor'))

        session['form_data'] = formulario  # Guardar los datos del formulario en la sesión

        # Obtener los erros
        errores = validar_formulario(formulario)

        # Verificar la existencia de un error
        if errores:
            flash(Markup(f'<strong>Precaución</strong>: {errores}'), category='warning')
            return redirect(url_for('vendedores.agregar_vendedor'))

        # Obtener respuesta al enviar los datos del vendedor
        respuesta_vendedor, codigo_estado = await VendedoresController. \
            añadir_nuevo_vendedor(datos_enviar=formulario, token_acceso=token)

        # Verificar código de estado
        if codigo_estado == 201:
            session.pop('form_data', None)
            flash(Markup('<strong>Éxito:</strong> Vendedor añadido con éxito'), category="message")
            return redirect(url_for('vendedores.vendedor_especifico', identificador_vendedor=respuesta_vendedor[0]['id_vendedor']))
        else:
            # Validar respuesta
            respuesta_vendedor = validar_respuesta(respuesta_vendedor, codigo_estado, 'Vendedor')
            return redirect(url_for('vendedores.agregar_vendedor'))

    except Exception as error:
        print(f"Ocurrió un error enviando los datos del vendedor: {error}")
        raise Exception("Ocurrió un error enviando los datos del vendedor")

@bp.route("/agregar_vendedor", methods=["GET"])
async def agregar_vendedor():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener las notificaciones
        respuesta_notificaciones, total_notificaciones, codigo_estado = await NotificacionesController. \
            obtener_todas_notificaciones(token_acceso=token, notificaciones_no_leidas=True)

        respuesta_notificaciones = validar_respuesta(respuesta_notificaciones, codigo_estado, 'Notificaciones', mostrar_mensaje=False)

        return render_template('vistas_vendedores/agregar_vendedor.html', respuesta_notificaciones=respuesta_notificaciones, total_notificaciones = total_notificaciones)
    except Exception as error:
        print(f"Ocurrió un error al cargar la vista de agregar vendedores: {error}")
        raise Exception("Ocurrió un error al cargar la vista de agregar vendedores.")

@bp.route("/enviar_vendedor_actualizado", methods=["POST"])
async def enviar_vendedor_actualizado():
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
            return redirect(url_for('vendedores.ver_vendedores'))

        # Obtener los erros
        errores = validar_formulario(formulario)

        # Obtener el identificador del vendedor
        identificador_vendedor = formulario['identificador_vendedor']

        # Verificar la existencia de un error
        if errores:
            flash(Markup(f'<strong>Precaución</strong>: {errores}'), category='warning')
            return redirect(url_for('vendedores.vendedor_especifico', identificador_vendedor=identificador_vendedor))

        # Obtener respuesta al enviar el vendedor actualizado
        respuesta_vendedor, codigo_estado = await VendedoresController. \
            actualizar_un_vendedor(datos_actualizar=formulario, identificador_vendedor=identificador_vendedor, token_acceso=token)

        # Verificar código de estado
        if codigo_estado == 200:
            flash(Markup('<strong>Éxito:</strong>Vendedor actualizado con éxito'), category="message")
            return redirect(url_for('vendedores.vendedor_especifico', identificador_vendedor=respuesta_vendedor[0]['id_vendedor']))
        else:
            # Validar respuesta
            respuesta_vendedor = validar_respuesta(respuesta_vendedor, codigo_estado, 'Vendedor')
            return redirect(url_for('vendedores.editar_vendedor', identificador_vendedor=identificador_vendedor))
    except Exception as error:
        print(f"Ocurrió un error enviado los datos para actualizar: {error}")
        raise Exception("Ocurrió un error enviado los datos para actualizar")

@bp.route("/editar_vendedor/<string:identificador_vendedor>", methods=["GET", "POST"])
async def editar_vendedor(identificador_vendedor):
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener las notificaciones y el vendedor
        respuesta_notificaciones, total_notificaciones, codigo_estado = await NotificacionesController. \
            obtener_todas_notificaciones(token_acceso=token, notificaciones_no_leidas=True)

        respuesta_vendedor, codigo_estado_vendedor = await VendedoresController. \
            obtener_vendedor(identificador_vendedor, token)

        # Validar respuestas
        respuesta_vendedor = validar_respuesta(respuesta_vendedor, codigo_estado_vendedor, 'Vendedor')
        respuesta_notificaciones = validar_respuesta(respuesta_notificaciones, codigo_estado, 'Notificaciones', mostrar_mensaje=False)

        return render_template('vistas_vendedores/editar_vendedor.html', notificaciones = respuesta_notificaciones, vendedores = respuesta_vendedor,\
                                total_notificaciones=total_notificaciones)
    except Exception as error:
        print(f"Ocurrió un error al cargar la vista de editar vendedores: {error}")
        raise Exception("Ocurrió un error al cargar la vista de editar vendedores.")

@bp.route("/suspender_vendedor", methods=["POST"])
async def suspender_vendedor():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener el identificador del vendedor
        datos_vendedor = request.get_json()

        # Verificar envio de datos
        if not datos_vendedor:
            flash(Markup(f'<strong>Precaución</strong>: No se enviaron datos. Intente nuevamente'), category='warning')
            return redirect(url_for('vendedores.ver_vendedores'))

        # Obtener los datos corresponientes
        identificador_vendedor = datos_vendedor['identificador_vendedor']
        estado_vendedor = datos_vendedor['estado_vendedor']

        # Obtener respuesta al enviar el vendedor actualizado
        respuesta_vendedor, codigo_estado = await VendedoresController. \
            suspender_un_vendedor(identificador_vendedor=identificador_vendedor, accion_solicitada=estado_vendedor, token_acceso=token)

        # Verificamos la respuesta de la API
        respuesta_vendedor = validar_respuesta(respuesta_vendedor, codigo_estado, 'Vendedor')

        # Verificar que exista una respuesta
        if respuesta_vendedor:
            flash(Markup(f'<strong>Éxito</strong>: Se cambió el estado del vendedor'), category='message')

        return jsonify({'success': True})

    except Exception as error:
        print(f"Ocurrió un error al solicitar suspender un vendedor: {error}")
        raise Exception("Ocurrió un error al solicitar suspender a un vendedor")

@bp.route("/eliminar_vendedor", methods=["POST"])
async def eliminar_vendedor():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener el identificador del vendedor
        datos_vendedor = request.get_json()

        # Verificar envio de datos
        if not datos_vendedor:
            flash(Markup(f'<strong>Precaución</strong>: No se enviaron datos. Intente nuevamente'), category='warning')
            return redirect(url_for('vendedores.ver_vendedores'))

        # Obtener los datos correspondientes
        identificador_vendedor = datos_vendedor['identificador_vendedor']

        # Obtener respuesta al enviar el vendedor actualizado
        respuesta_vendedor, codigo_estado = await VendedoresController. \
            eliminar_un_vendedor(identificador_vendedor=identificador_vendedor, token_acceso=token)

        # Verificamos la respuesta de la API
        respuesta_vendedor = validar_respuesta(respuesta_vendedor, codigo_estado, 'Vendedor')

        # Verificar que exista una respuesta
        if respuesta_vendedor:
            flash(Markup(f'<strong>Éxito</strong>: Se eliminó correctamente al vendedor'), category='message')

        return jsonify({'success': True})
    except Exception as error:
        print(f"Ocurrió un error al enviar los datos para eliminar un vendedor: {error}")
        raise Exception("Ocurrió un error al enviar los datos para eliminar un vendedor")