"""
    Archivo que administra las vistas del
    apartado de pagos
"""

from flask import Blueprint, render_template, session, request, url_for, jsonify, flash, redirect
from ...controllers.controllers_notificaciones import NotificacionesController
from ...controllers.controllers_vendedores import VendedoresController
from ...controllers.controllers_cliente import ClienteController
from ...controllers.controllers_ventas import VentasController
from ...controllers.controllers_lotes import LotesController
from app.error_handlers import validar_respuesta
from app.validadores import validar_formulario
from markupsafe import Markup
from datetime import datetime

# Registrar las vistas
bp = Blueprint('pagos', __name__)

###################
# Vistas de pagos #
###################

@bp.route("/informacion_venta/<string:identificador_lote>", methods=["GET", "POST"])
async def informacion_venta(identificador_lote):
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token:
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa, intenta inciando sesión'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener las notificaciones
        respuesta_notificaciones, total_notificaciones, codigo_estado = await NotificacionesController. \
            obtener_todas_notificaciones(token_acceso=token, notificaciones_no_leidas=True)

        # Obtener todos los clientes
        # Obtener todos los vendedores
        respuesta_clientes, codigo_estado_clientes = await ClienteController.obtener_todos_cliente(token_acceso=token)
        respuesta_vendedores, codigo_estado_vendedores = await VendedoresController.obtener_vendedores_sin_filtros(token_acceso=token)
        respuesta_lote, codigo_estado_lote = await LotesController.obtener_lote_extra(identificador_lote=identificador_lote, token_acceso=token)

        # Verificar respuesta
        respuesta_notificaciones = validar_respuesta(respuesta_notificaciones, codigo_estado, 'Notificaciones', mostrar_mensaje=False)
        respuesta_clientes = validar_respuesta(respuesta_clientes, codigo_estado_clientes, 'Clientes')
        respuesta_vendedores = validar_respuesta(respuesta_vendedores, codigo_estado_vendedores, 'Vendedores')
        respuesta_lote = validar_respuesta(respuesta_lote, codigo_estado_lote, 'Lote')

        # Obtener URL previa
        url_previa = session.get('previa_venta_lote')

        # Verificar URL
        if not url_previa:
            session['previa_venta_lote'] = request.referrer
            url_previa = session.get('previa_venta_lote')

        return render_template('vistas_pagos/informacion_pago_venta.html', notificaciones = respuesta_notificaciones, \
                               total_notificaciones = total_notificaciones, clientes=respuesta_clientes, url_previa = url_previa, \
                               vendedores = respuesta_vendedores, identificador_lote=identificador_lote, lote=respuesta_lote)
    except Exception as error:
        print(f"Ocurrió un error al cargar la vista de la información de la venta: {error}")
        raise Exception("Ocurrió un error al cargar la vista de la información de la venta")

@bp.route("/enviar_informacion_venta", methods=["POST"])
async def enviar_informacion_venta():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener el formulario enviado en diccionario
        formulario = request.form.to_dict()

        url_previa = session.get('previa_venta_lote')

        # Verificar formulario
        if not formulario:
            flash(Markup(f'<strong>Precaución:</strong> No se enviaron los datos.'), category='warning')
            return redirect(url_previa)

        # Validar formulario
        errores = validar_formulario(formulario)

        # Obtener el identificador del lote
        identificador_lote = formulario['id_lote']

        # Verificar la existencia de un error
        if errores:
            flash(Markup(f'<strong>Precaución:</strong>: {errores}'), category='warning')
            return redirect(url_for('pagos.informacion_venta', identificador_lote=identificador_lote))

        # Guardar el formulario en la sesión
        session['formulario_enviar_venta'] = formulario

        # Verificar formulario
        verificar = session.get('formulario_enviar_venta')

        if verificar:
            return redirect(url_for('pagos.resumen_venta'))
        else:
            flash(Markup(f'<strong>Error:</strong> No se logró guardar la información. Vuelva a intentarlo'), category='error')
            return redirect(url_for('pagos.informacion_venta', identificador_lote=identificador_lote))
    except Exception as error:
        print(f"Ocurrió un error al enviar la información de la venta: {error}")
        raise Exception("Ocurrió un error al enviar la información de la venta")

@bp.route("/resumen_venta", methods=["GET", "POST"])
async def resumen_venta():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener formulario
        datos_formulario = session.get('formulario_enviar_venta')

        # Obtener las notificaciones
        respuesta_notificaciones, total_notificaciones, codigo_estado = await NotificacionesController. \
            obtener_todas_notificaciones(token_acceso=token, notificaciones_no_leidas=True)
        respuesta_cliente, codigo_estado_cliente = await ClienteController. \
            obtener_un_cliente(identificador_cliente=datos_formulario['CURP_cliente'], token_acceso=token)
        respuesta_vendededor, codigo_estado_vendedor = await VendedoresController. \
            obtener_vendedor(identificador_vendedor=datos_formulario['id_vendedor'], token_acceso=token)
        respuesta_lotes, codigo_estado_lote = await LotesController. \
            obtener_lote_extra(identificador_lote=datos_formulario['id_lote'], token_acceso=token)
        respuesta_ubicacion, codigo_estado_ubicacion = await LotesController. \
            obtener_ubicacon_lote(identificador_lote=datos_formulario['id_lote'], token_acceso=token)

        # Verificar respuesta
        respuesta_notificaciones = validar_respuesta(respuesta_notificaciones, codigo_estado, 'Notificaciones', mostrar_mensaje=False)
        respuesta_cliente = validar_respuesta(respuesta_cliente, codigo_estado_cliente, 'Cliente')
        respuesta_vendededor = validar_respuesta(respuesta_vendededor, codigo_estado_vendedor, 'Vendedor')
        respuesta_lotes = validar_respuesta(respuesta_lotes, codigo_estado_lote, 'Lotes')
        respuesta_ubicacion = validar_respuesta(respuesta_ubicacion, codigo_estado_ubicacion, 'Ubicación')

        # Obtener URL previa
        url_previa = session.get('previa_venta_resumen')

        # Verificar URL
        if not url_previa:
            session['previa_venta_resumen'] = request.referrer
            url_previa = session.get('previa_venta_resumen')

        return render_template('vistas_pagos/resumen_venta.html', notificaciones = respuesta_notificaciones,
                               total_notificaciones=total_notificaciones, datos_formulario=datos_formulario,
                               url_previa = url_previa, cliente=respuesta_cliente, vendedor=respuesta_vendededor,
                               lote=respuesta_lotes, ubicacion=respuesta_ubicacion)
    except Exception as error:
        print(f"Ocurrió un error al cargar la vista de resumen de la venta: {error}")
        raise Exception("Ocurrió un error al cargar la vista de resumen de la venta")

@bp.route("/enviar_venta_final", methods=["POST"])
async def enviar_venta_final():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token:
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa, intenta iniciando sesión'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener venta
        venta = session.get('formulario_enviar_venta')
        venta['fecha_compra'] = datetime.now().strftime('%Y-%m-%d')

        # Obtener respustsa al enviar los datos de la venta
        respuesta_venta, codigo_estado = await VentasController.agregar_venta_lote(venta_enviar=venta, token_acceso=token)
        # Obtener URL_previa
        url_previa_error = session.get('previa_venta_resumen')
        url_previa_exito = session.get('previa_venta_lote')

        if codigo_estado == 201:
            session.pop('previa_venta_lote', None)
            session.pop('formulario_enviar_venta',None)
            session.pop('previa_venta_resumen', None)
            flash(Markup('<strong>Éxito:</strong> Venta añadida con éxito'), category="message")
            return redirect(url_previa_exito)
        else:
            respuesta_venta = validar_respuesta(respuesta_venta, codigo_estado, 'Venta')
            return redirect(url_previa_error)

    except Exception as error:
        print(f"Ocurrió un error enviando la información de la venta: {error}")
        raise Exception("Ocurrió un error enviando la información de la venta")

@bp.route("/cancelar_formulario_venta", methods=["POST"])
async def cancelar_formulario_venta():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Verificar que exista una sesión que cerrar
        formulario = session.get('formulario_enviar_venta')

        if formulario:
            session.pop('formulario_enviar_venta', None)

        return jsonify({'success': True})

    except Exception as error:
        print(f"Ocurrió un error al cancelar formulario: {error}")
        raise Exception(f"Ocurrio un error al cancelar formulario")

@bp.route("/enviar_nuevo_plazo", methods=["POST"])
async def enviar_nuevo_plazo():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener el formulario enviado en diccionario
        formulario = request.form.to_dict()

        url_previa = request.referrer

        # Verificar formulario
        if not formulario:
            flash(Markup(f'<strong>Precaución:</strong> No se enviaron los datos.'), category='warning')
            return redirect(url_previa)

        # Validar formulario
        errores = validar_formulario(formulario)

        # Obtener el identificador de la compra
        identificador_compra = formulario['id_compra']
        formulario['comprobante'] = False
        formulario['restante'] = formulario['cantidad_esperada']

        # Verificar la existencia de un error
        if errores:
            flash(Markup(f'<strong>Precaución:</strong>: {errores}'), category='warning')
            return redirect(url_for('clientes.resumen_compra', id_compra=identificador_compra))

        # Obtener respuesta al enviar los datos del plazo
        respuesta_plazo, codigo_estado = await VentasController.\
            agregar_nuevo_plazo(datos_plazo=formulario, token_acceso=token)

        # Validar resultados
        if codigo_estado == 201:
            flash(Markup('<strong>Éxito:</strong> Plazo añadido con éxito'), category="message")
            return redirect(url_for('clientes.resumen_compra', id_compra = identificador_compra))
        else:
            respuesta_plazo = validar_respuesta(respuesta_plazo, codigo_estado, 'Plazo')
            return redirect(url_for('clientes.resumen_compra', id_compra = identificador_compra))

    except Exception as error:
        print(f"Ocurrió un error al enviar los datos del nuevo plazo: {error}")
        raise Exception("Ocurrió un error al enviar los datos del nuevo plazo")

@bp.route("/eliminar_plazo", methods=["POST"])
async def eliminar_plazo():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener los datos de la solicitud
        datos_plazo = request.get_json()

        url_previa = request.referrer

        # Verificar envio de datos
        if not datos_plazo:
            flash(Markup(f'<strong>Precaución</strong>: No se enviaron datos. Intente nuevamente'), category='warning')
            return redirect(url_previa)

        # Obtener identificaodr del plazo
        identificador_plazo = datos_plazo['identificador_plazo']

        # Obtener respuesta el eliminar el plazo
        respuesta_plazo, codigo_estado = await VentasController.\
            eliminar_un_plazo(identificador_plazo=identificador_plazo, token_acceso=token)

        # Verificar respuesta de la API
        respuesta_plazo = validar_respuesta(respuesta_plazo, codigo_estado, 'Plazo')

        if respuesta_plazo:
            flash(Markup(f'<strong>Éxito</strong>: Se eliminó correctamente el plazo'), category='message')

        return jsonify({'success': True})
    except Exception as error:
        print(f"Ocurrió un error enviando la información para eliminar el plazo: {error }")
        raise Exception("Ocurrió un error enviando la información para eliminar el plazo")

@bp.route("/enviar_plazo_actualizado", methods=["POST"])
async def enviar_plazo_actualizado():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener el formulario enviado en diccionario
        formulario = request.form.to_dict()

        url_previa = request.referrer

        # Verificar formulario
        if not formulario:
            flash(Markup(f'<strong>Precaución</strong>: No se enviaron los datos.'), category='warning')
            return redirect(url_previa)

        # Obtener los erros
        errores = validar_formulario(formulario)

        # Obtener identificador de la compra
        identificador_compra = formulario['id_compra']
        identificador_plazo = formulario['id_plazo']
        formulario['comprobante'] = False
        formulario['restante'] = formulario['cantidad_esperada']

        # Verificar la exista
        if errores:
            flash(Markup(f'<strong>Precaución</strong>: {errores}'), category='warning')
            return redirect(url_for('clientes.resumen_compra', id_compra=identificador_compra))

        # Obteenr respuesta al enviar el plazo actualizado
        respuesta_plazo, codigo_estado = await VentasController.\
            actualizar_un_plazo(identificador_plazo=identificador_plazo, plazo_actualizado=formulario, token_acceso=token)

        # Verificar código de estado
        if codigo_estado == 200:
            flash(Markup('<strong>Éxito:</strong> Plazo actualizado con éxito'), category="message")
            return redirect(url_for('clientes.resumen_compra', id_compra=identificador_compra))
        else:
            # Validar respuesta
            respuesta_plazo = validar_respuesta(respuesta_plazo, codigo_estado, 'Lote')
            return redirect(url_for('clientes.resumen_compra', id_compra=identificador_compra))
    except Exception as error:
        print(f"Ocurrió un erro al enviar los datos de plazo actualizado: {error}")
        raise Exception("Ocurrió un erro al enviar los datos de plazo actualizado")

@bp.route("/cambiar_estado_compra", methods=["POST"])
async def cambiar_estado_compra():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener el identificador de la compra
        datos_compra = request.get_json()

        url_previa = request.referrer

        # Verificar envio de datos
        if not datos_compra:
            flash(Markup(f'<strong>Precaución</strong>: No se enviaron datos. Intente nuevamente'), category='warning')
            return redirect(url_previa)

        # Obtener los datos corresponientes
        identificador_compra = datos_compra['identificador_compra']
        estado_compra = datos_compra['estado_compra']

        # Realizar la solicitud
        respuesta_compra, codigo_estado = await VentasController. \
            cambiar_estado_una_compra(identificador_venta=identificador_compra, estado_venta=estado_compra, token_acceso=token)

        # Verificamos la respuesta de la API
        respuesta_compra = validar_respuesta(respuesta_compra, codigo_estado, 'Venta')

        # Verificar que exista una respuesta
        if respuesta_compra:
            flash(Markup(f'<strong>Éxito</strong>: Se cambió el estado de la venta'), category='message')

        return jsonify({'success': True})
    except Exception as error:
        print(f"Ocurrió un error al solicitar cambiar el estado de la compra: {error}")
        raise Exception("Ocurrió un error al solicitar cambiar el estado de la compra")

@bp.route("/enviar_nuevo_detalle", methods=["POST"])
async def enviar_nuevo_detalle():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token:
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa, intenta inciando sesión'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener el formulario enviado en diccionario
        formulario = request.form.to_dict()

        url_previa = request.referrer

        # Verificar formulario
        if not formulario:
            flash(Markup(f'<strong>Precaución:</strong> No se enviaron los datos.'), category='warning')
            return redirect(url_previa)

        # Obtener el identificador de la compra
        identificador_compra = formulario['id_compra']
        identificador_plazo = formulario['id_plazo']

        # Validar formualio
        errores = validar_formulario(formulario)

        # Verificar la existencia de un error
        if errores:
            flash(Markup(f'<strong>Precaución:</strong>: {errores}'), category='warning')
            return redirect(url_for('clientes.resumen_compra', id_compra=identificador_compra))

        # Obtener respuesta al enviar los datos del detalle
        respuesta_detalle, codigo_estado = await VentasController. \
            agregar_un_detalle(identificador_plazo=identificador_plazo, detalle_enviar=formulario, token_acceso=token)

        # Validar resultados
        if codigo_estado == 201:
            flash(Markup('<strong>Éxito:</strong> Detalle de plazo añadido con éxito'), category="message")
            return redirect(url_for('clientes.resumen_compra', id_compra = identificador_compra))
        else:
            respuesta_detalle = validar_respuesta(respuesta_detalle, codigo_estado, 'Detalle')
            return redirect(url_for('clientes.resumen_compra', id_compra = identificador_compra))

    except Exception as error:
        print(f"Ocurrió un error al enviar los datos del nuevo detalle: {error}")
        raise Exception(f"Ocurrió un error al enviar los datos del nuevo detalle: {error}")

@bp.route("/detalle_pago_especifico/<string:identificador_plazo>", methods=["GET"])
async def detalle_pago_especifico(identificador_plazo):
    try:
        # Obtener token de accesoi
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa, intenta inciando sesión'), category='error')
            return redirect(url_for('generales.index'))

        id_plazo, cantidad_compra, restante = identificador_plazo.split('-')

        # Obtener las notificaciones
        respuesta_notificaciones, total_notificaciones, codigo_estado = await NotificacionesController. \
            obtener_todas_notificaciones(token_acceso=token, notificaciones_no_leidas=True)
        respuesta_detalle, codigo_estado_datalle = await VentasController.\
            obtener_un_detalle(identificador_plazo=id_plazo, token_acceso=token)

        respuesta_notificaciones = validar_respuesta(respuesta_notificaciones, codigo_estado, 'Notificaciones', mostrar_mensaje=False)
        respuesta_detalle = validar_respuesta(respuesta_detalle, codigo_estado_datalle, 'Detalle de plazo')

        # Obtener URL previa
        url_previa = session.get('previa_detalle_modificar')

        # Verificar url
        if not url_previa:
            session['previa_detalle_modificar'] = request.referrer
            url_previa = session.get('previa_detalle_modificar')

        return render_template('vistas_pagos/ver_detalle_pago.html', notificaciones = respuesta_notificaciones,
                               total_notificaciones = total_notificaciones, url_previa = url_previa, detalle = respuesta_detalle,
                               cantidad_compra = cantidad_compra, restante = restante)
    except Exception as error:
        print(f"Ocurrió un error al cargar la vista de ver un detalle de pago: {error}")
        raise Exception("Ocurrió un error al cargar la vista de ver un detalle de pago")

@bp.route("/enviar_detalle_actualizado", methods=["POST"])
async def enviar_detalle_actualizado():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificaf que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        url_previa = session.get('previa_detalle_modificar')

        # Obtener el formulario enviado en diccionario
        formulario = request.form.to_dict()

        # Verificar formulario
        if not formulario:
            flash(Markup(f'<strong>Precaución</strong>: No se enviaron los datos.'), category='warning')
            return redirect(url_previa)

        # Obtener los errores
        errores = validar_formulario(formulario)

        # Obtener el identificador del detalle
        identificador_detalle = formulario['id_detalle_pago']

        # Verificar la existencia de un error
        if errores:
            flash(Markup(f'<strong>Precaución</strong>: {errores}'), category='warning')
            return redirect(url_previa)

        # Obtener respuesta al enviar el detalle actualizado
        respuesta_detalle, codigo_estado = await VentasController.\
            actualizar_un_detalle(identificador_plazo=identificador_detalle, detalle_actualizado=formulario, token_acceso=token)

        # Verificar código de estado
        if codigo_estado == 200:
            session.pop('previa_detalle_modificar', None)
            flash(Markup('<strong>Éxito:</strong> Localidad actualizada con éxito'), category="message")
            return redirect(url_previa)
        else:
            # Validar respuesta
            respuesta_detalle = validar_respuesta(respuesta_detalle, codigo_estado, 'Detalle de pago')
            return redirect(url_previa)
    except Exception as error:
        print(f"Ocurrió un error al enviar los datos del detalle actualizado: {error}")
        raise Exception("Ocurrió un error al enviar los datos del detalle actualizado")

@bp.route("/eliminar_detalle_pago", methods=["POST"])
async def eliminar_detalle_pago():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener el identificador del detalle de pago
        datos_detalle = request.get_json()

        url_previa = request.referrer

        # Verificar envio de datos
        if not datos_detalle:
            flash(Markup(f'<strong>Precaución</strong>: No se enviaron datos. Intente nuevamente'), category='warning')
            return redirect(url_previa)

        # Obtener los datos correspondientes
        identificador_detalle = datos_detalle['identificador_detalle']

        # Obtener respuesta al enviar los datos
        respuesta_detalle, codigo_estado = await VentasController.\
            eliminar_un_detalle(identificador_detalle=identificador_detalle, token_acceso=token)

        # Verificair la respuesta de la API
        respuesta_detalle = validar_respuesta(respuesta_detalle, codigo_estado, 'Detalle de pago')

        # Verificar que exista un respuesta
        if respuesta_detalle:
            flash(Markup(f'<strong>Éxito</strong>: Se eliminó correctamente el detalle de pago'), category='message')

        return {'success': True}
    except Exception as error:
        print(f"Ocurrió un error al enviar los datos para eliminar un detalle: {error}")
        raise Exception("Ocurrió un error al enviar los datos para eliminar un detalle")