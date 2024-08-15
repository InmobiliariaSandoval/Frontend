"""
    Archivo que se encarga de administrar
    las vistas del apartado de clientes
"""
from flask import Blueprint, render_template, session, request, url_for, flash, redirect
from ...controllers.controllers_notificaciones import NotificacionesController
from app.controllers.controllers_vendedores import VendedoresController
from ...controllers.controllers_cliente import ClienteController
from ...controllers.controllers_ventas import VentasController
from app.controllers.controllers_lotes import LotesController
from app.validadores import validar_formulario
from ...error_handlers import validar_respuesta
from markupsafe import Markup

# Registrar las vistas
bp = Blueprint('clientes', __name__)

######################
# Vistas de clientes #
######################

@bp.route("/ver_clientes", methods=["GET", "POST"])
async def ver_clientes():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener filtro de búsqueda
        tipo_filtro = request.args.get('ventas')
        pagina = int(request.args.get('pagina', 1))
        tamano = int(request.args.get('tamano', 10))

        # En caso de que el filtro sea todos, se elimina
        if tipo_filtro == 'Todos':
            tipo_filtro = None

        # Verificar que exista el tipo de filtro
        if tipo_filtro and tipo_filtro not in ['Cancelado', 'Proceso', 'Finalizado', 'Todos']:
            flash(Markup('<strong>Precaución:</strong> Filtro no válido, intente nuevamente'), category='warning')
            return redirect(url_for('clientes.ver_clientes', pagina=pagina, tamano = tamano))

        # Obtener las notificaciones y los vendedores
        respuesta_notificaciones, total_notificaciones, codigo_estado = await NotificacionesController. \
            obtener_todas_notificaciones(token_acceso=token, notificaciones_no_leidas=True)
        respuesta_clientes, total_clientes, codigo_estado_ventas = await VentasController. \
            obtener_todas_ventas(token_acceso=token, filtro_busqueda=tipo_filtro, numero_pagina=pagina, tamano_pagina=tamano)

        # Verificar respuestas
        respuesta_notificaciones = validar_respuesta(respuesta_notificaciones, codigo_estado, 'Notificaciones', mostrar_mensaje=False)
        respuesta_clientes = validar_respuesta(respuesta_clientes, codigo_estado_ventas, 'Clientes/Ventas')

        return render_template('vistas_clientes/ver_clientes.html', notificaciones = respuesta_notificaciones, ventas = respuesta_clientes, \
                               pagina = pagina, tamano = tamano, total = total_clientes, total_notificaciones=total_notificaciones)
    except Exception as error:
        print(f"Ocurrió un error al cargar la vista de clientes: {error}.")
        raise Exception("Ocurrió un error al cargar la vista de clientes.")

@bp.route("/cliente_especifico/<string:identificador_cliente>", methods=["GET", "POST"])
async def cliente_especifico(identificador_cliente):
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa, intenta iniciar sesión.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener las notificaciones y los vendedores
        respuesta_notificaciones, total_notificaciones, codigo_estado = await NotificacionesController. \
            obtener_todas_notificaciones(token_acceso=token, notificaciones_no_leidas=True)
        respuesta_clientes, codigo_estado_ventas = await ClienteController. \
            obtener_un_cliente(token_acceso=token, identificador_cliente=identificador_cliente)

        # Verificar respuesta de notificaciones
        respuesta_notificaciones = validar_respuesta(respuesta_notificaciones, codigo_estado, 'Notificaciones', mostrar_mensaje=False)
        respuesta_clientes = validar_respuesta(respuesta_clientes, codigo_estado_ventas, 'Clientes')

        return render_template('vistas_clientes/cliente_especifico.html', notificaciones = respuesta_notificaciones, clientes = respuesta_clientes, \
                                total_notificaciones = total_notificaciones)
    except Exception as error:
        print(f"Ocurrió un error al cargar la vista de cliente: {error}.")
        raise Exception("Ocurrió un error al cargar la vista de cliente")

@bp.route("/editar_cliente/<string:id_cliente>", methods=["GET"])
async def editar_cliente(id_cliente):
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
        respuesta_cliente, codigo_estado_cliente = await ClienteController. \
            obtener_un_cliente(identificador_cliente=id_cliente, token_acceso=token)

        # Validar respuesta
        respuesta_notificaciones = validar_respuesta(respuesta_notificaciones, codigo_estado, 'Notificaciones', mostrar_mensaje=False)
        respuesta_cliente = validar_respuesta(respuesta_cliente, codigo_estado_cliente, 'Cliente')

        # Obtener URL previa
        url_previa = session.get('previa_cliente_editar')

        # Verificar que exista la URL_previa
        if not url_previa:
            session['previa_cliente_editar'] = request.referrer
            url_previa = session.get('previa_cliente_editar')

        return render_template('vistas_clientes/editar_cliente.html', notificaciones = respuesta_notificaciones, 
                               total_notificaciones = total_notificaciones, clientes = respuesta_cliente)
    except Exception as error:
        print(f"Ocurrió un error al cargar la vista de editar clientes: {error}")
        raise Exception("Ocurrió un error al cargar la vista de editar clientes.")

@bp.route("/enviar_cliente_actualizado", methods=["POST"])
async def enviar_cliente_actualizado():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener el formulario enviado en diccionario
        formulario = request.form.to_dict()

        url_previa = session.get('previa_cliente_editar')

        # Verificar formulario
        if not formulario:
            flash(Markup(f'<strong>Precaución</strong>: No se enviaron los datos.'), category='warning')
            return redirect(url_previa)

                # Obtener los erros
        errores = validar_formulario(formulario)

        identificador_cliente = formulario['CURP_cliente_previo']

        formulario['entrega_credencial_elector'] = True if 'entrega_credencial_elector' in formulario else False
        formulario['entrega_curp'] =  True if 'entrega_curp' in formulario else False
        formulario['entrega_comprobante_domicilio'] =  True if 'entrega_comprobante_domicilio' in formulario else False

        # Verificar la existencia de un error
        if errores:
            flash(Markup(f'<strong>Precaución</strong>: {errores}'), category='warning')
            return redirect(url_for('clientes.editar_cliente', id_cliente=identificador_cliente))

        # Obtener respuesta al enviar el cliente acutalizado
        respuesta_cliente, codigo_estado = await ClienteController. \
            actualizar_un_cliente(datos_actualizar=formulario, identificador_cliente=identificador_cliente, token_acceso=token)

        # Verificar código de estado
        if codigo_estado == 200:
            session.pop('previa_cliente_editar', None)
            flash(Markup('<strong>Éxito:</strong> Cliente actualizado con éxito'), category="message")
            return redirect(url_for('clientes.cliente_especifico', identificador_cliente=identificador_cliente))
        else:
            # Validar respuesta
            respuesta_cliente = validar_respuesta(respuesta_cliente, codigo_estado, 'Cliente')
            return redirect(url_for('clientes.editar_cliente', id_cliente=identificador_cliente))
    except Exception as error:
        print(f"Ocurrió un error al enviar el cliente actulizado: {error}")
        raise Exception("Ocurrió un error al enviar el cliente actulizado")

@bp.route("/agregar_cliente", methods=["GET"])
async def agregar_cliente():
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa, intenta iniciando sesión'), category='error')
            return redirect(url_for('generales.index'))

        # Obtener las notificaciones
        respuesta_notificaciones, total_notificaciones, codigo_estado = await NotificacionesController. \
            obtener_todas_notificaciones(token_acceso=token, notificaciones_no_leidas=True)

        # Verificar respuesta
        respuesta_notificaciones = validar_respuesta(respuesta_notificaciones, codigo_estado, 'Notificaciones', mostrar_mensaje=False)

        # Obtener URL previa
        url_previa = session.get('previa_cliente_ingresar')

        # Verificar que exista
        if not url_previa:
            session['previa_cliente_ingresar'] = request.referrer
            url_previa = session.get('previa_cliente_ingresar')

        return render_template('vistas_clientes/agregar_cliente.html', notificaciones = respuesta_notificaciones, \
                               total_notificaciones = total_notificaciones)
    except Exception as error:
        print(f"Ocurrió un error al cargar la vista de agregar cliente: {error}")
        raise Exception("Ocurrió un error al cargar la vista de agregar cliente")

@bp.route("/enviar_informacion_cliente", methods=["POST"])
async def enviar_informacion_cliente():
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
            return redirect(url_for('lotes.agregar_cliente'))

        formulario['entrega_credencial_elector'] = True if 'entrega_credencial_elector' in formulario else False
        formulario['entrega_curp'] =  True if 'entrega_curp' in formulario else False
        formulario['entrega_comprobante_domicilio'] =  True if 'entrega_comprobante_domicilio' in formulario else False

        # Obtener los errores
        errores = validar_formulario(formulario=formulario)

        # Verificar la existencia de un error
        if errores:
            flash(Markup(f'<strong>Precaución</strong>: {errores}'), category='warning')
            return redirect(url_for('lotes.agregar_cliente'))

        # Obtener respuesta al enviar los datos del cliente
        respuesta_cliente, codigo_estado = await ClienteController. \
            agregar_nuevo_cliente(datos_enviar=formulario, token_acceso=token)

        # Verificar código de estado
        if codigo_estado == 201:
            session.pop('previa_cliente_ingresar', None)
            flash(Markup('<strong>Éxito</strong> Cliente añadido con éxito'), category='message')
            return redirect(url_for('clientes.ver_clientes'))
        else:
            respuesta_cliente = validar_respuesta(respuesta_cliente, codigo_estado, 'Cliente')
            return redirect(url_for('clientes.agregar_cliente'))
    except Exception as error:
        print(f"Ocurrió un error al enviar el cliente: {error}")
        raise Exception("Ocurrió un error al enviar el cliente")


@bp.route("/resumen_compra/<string:id_compra>", methods=["GET"])
async def resumen_compra(id_compra):
    try:
        # Obtener token de acceso
        token = session.get('token')

        # Verificar que exista el token
        if not token:
            flash(Markup('<strong>Error:</strong> No tienes una sesión activa.'), category='error')
            return redirect(url_for('generales.index'))

        pagina = int(request.args.get('pagina', 1))
        tamano = int(request.args.get('tamano', 10))

        # Obtener datos importantes
        respuesta_notificaciones, total_notificaciones, codigo_estado = await NotificacionesController. \
            obtener_todas_notificaciones(token_acceso=token, notificaciones_no_leidas=True)
        respuesta_compra, codigo_estado_compra = await VentasController.\
            obtener_compra_especifica(identificador_compra=id_compra, token_acceso=token)

        # Validar respuestas
        respuesta_notificaciones = validar_respuesta(respuesta_notificaciones, codigo_estado, 'Notificaciones', mostrar_mensaje=False)
        respuesta_compra = validar_respuesta(respuesta_compra, codigo_estado_compra, 'Compra')

        if respuesta_compra:
            id_compra = respuesta_compra[0].id_compra
            cliente = respuesta_compra[0].CURP_cliente
            vendedor = respuesta_compra[0].id_vendedor
            lote = respuesta_compra[0].id_lote
            respuesta_plazo, total_plazo, codigo_estado_plazo = await VentasController. \
                obtener_plazos_compra(identificador_compra=id_compra, token_acceso=token, pagina=pagina, tamano=tamano)

            respuesta_cliente, codigo_estado_cliente = await ClienteController. \
                obtener_un_cliente(identificador_cliente=cliente, token_acceso=token)

            respuesta_vendedor, codigo_estado_vendedor = await VendedoresController. \
                obtener_vendedor(identificador_vendedor=vendedor, token_acceso=token)

            respuesta_lote, codigo_estado_lote = await LotesController. \
                obtener_lote_extra(identificador_lote=lote, token_acceso=token)
            respuesta_ubicacion_lote, codigo_estado_ubicacion = await LotesController. \
                obtener_ubicacon_lote(identificador_lote=lote, token_acceso=token)

            if respuesta_compra[0].estado_compra != 'Finalizado':
                respuesta_plazo = validar_respuesta(respuesta_plazo, codigo_estado_plazo, 'Plazos')
            respuesta_cliente = validar_respuesta(respuesta_cliente, codigo_estado_cliente, 'Cliente')
            respuesta_vendedor = validar_respuesta(respuesta_vendedor, codigo_estado_vendedor, 'Vendedor')
            respuesta_lote = validar_respuesta(respuesta_lote, codigo_estado_lote, 'Lote')
            respuesta_ubicacion_lote = validar_respuesta(respuesta_ubicacion_lote, codigo_estado_ubicacion, 'Ubicación de lote')

        return render_template('vistas_clientes/resumen_compra.html', notificaciones=respuesta_notificaciones,
                               total_notificaciones=total_notificaciones, compra = respuesta_compra, plazos = respuesta_plazo,
                               total = total_plazo, ubicacion = respuesta_ubicacion_lote, cliente = respuesta_cliente,
                               vendedor = respuesta_vendedor, lote = respuesta_lote, id_compra =id_compra, pagina=pagina,
                                tamano_pagina=tamano, precio_total = respuesta_compra[0].precio_total)
    except Exception as error:
        print(f"Ocurrió un error al cargar la vista de resumen de compra: {error}.")
        raise Exception("Ocurrió un error al cargar la vista de resumen de compra.")

