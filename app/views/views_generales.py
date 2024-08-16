"""
    Archivo que administra las vistas generales
    de la aplicación
"""
from flask import Blueprint, render_template, session, request, url_for, jsonify, flash, redirect
from app.controllers.controllers_vendedores import VendedoresController
from app.controllers.controllers_ventas import VentasController
from app.validadores import validar_formulario
from ..controllers.controllers_notificaciones import NotificacionesController
from app.services.utilidades import ENDPOINT_CERRAR_SESION, ENDPOINT_RECUPERAR_CONTRASENA
from ..error_handlers import validar_respuesta
from markupsafe import Markup
import requests
import os

# Registrar las vistas
bp = Blueprint('generales', __name__)

##############################
# Rutas de manejo de sesión  #
##############################

@bp.route("/", methods=["GET", "POST"])
def index():
    try:
        # Verificar que exista el token
        token = session.get('token')

        if token:
            flash(Markup('<strong>Precaución:</strong> Ya cuentas con una sesión'), category="warning")
            return redirect(url_for('generales.resumen'))

        # Verificar que el método sea POST
        if request.method == 'POST':

            # Obtener el token desde el cliente
            token = request.json.get('token')
            usuario = request.json.get('usuario')

            # Verificar que exista el token
            if not token or token == '':
                flash(Markup("<strong>Error:</strong> No se logró guardar el token de acceso"), category="error")
                return jsonify({'success': False})

            # Guardar token en sessions
            session['token'] = token
            session['usuario'] = usuario

            flash(f'Bienvenido {usuario}', category="message")
            return jsonify({'success': True})

        return render_template('inicio_sesion.html')
    except Exception as error:
        print(f"Ocurrió un error al cargar la vista de cambiar inicial: {error}")
        raise Exception(f"Ocurri un error al mostrar la vista de inicial.")

@bp.route("/cerrar_sesion", methods=["POST"])
async def cerrar_sesion():
    try:
        # Veriicar que el método sea POST
        if request.method == 'POST':

            # Verificar que exista una sesión que cerrar
            token = session['token']

            if not token:
                flash(Markup('<strong>Error:</strong> No se puede cerrar sesión, no tienes una cuenta activa'), category="error")
                return jsonify({'success': False})

            cabeceras = {
                'Authorization': f'Bearer {token}'
            }

            # Cambiar estado de la cuenta
            cambiar_estado = requests.get(ENDPOINT_CERRAR_SESION, headers=cabeceras)

            if cambiar_estado.status_code != 200:
                return jsonify({'success': False})

            session.pop('token', None)
            session.pop('usuario', None)
            session.clear()
            flash(Markup('<strong>Éxito:</strong> Sesión cerrada correctamente'), category="message")
            return jsonify({'success': True})
    except Exception as error:
        print(f"Ocurrió un error al cerrar sesión: {error}")
        raise Exception(f"Ocurrio un error cerrar sesión")

@bp.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    try:
        return render_template('reset_password.html')
    except Exception as error:
        print(f"Ocurrió un error al cargar la vista de cambiar contraseña: {error}")
        raise Exception(f"Ocurri un error al mostrar la vista de cambiar contraseña.")

@bp.route("/resumen", methods=["GET", "POST"])
async def resumen():
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
        respuesta_clientes, _, codigo_estado_ventas = await VentasController. \
            obtener_todas_ventas(token_acceso=token, filtro_busqueda=None, numero_pagina=1, tamano_pagina=5)
        respuesta_vendedor, _, codigo_estado_vendedor = await VendedoresController.\
            obtener_todos_vendedores(token_acceso=token, tipo_filtro='mas', tipo_estado=None, numero_pagina=1,tamano_pagina=5)

        # Verificar respuesta
        respuesta_notificaciones = validar_respuesta(respuesta_notificaciones, codigo_estado, 'Notificaciones', mostrar_mensaje=False)
        respuesta_clientes = validar_respuesta(respuesta_clientes, codigo_estado_ventas, 'Ventas')
        respuesta_vendedor = validar_respuesta(respuesta_vendedor, codigo_estado_vendedor, 'Vendedores')

        return render_template('index.html', notificaciones = respuesta_notificaciones, total_notificaciones = total_notificaciones, \
                               clientes=respuesta_clientes, vendedores=respuesta_vendedor)
    except Exception as error:
        print(f"Ocurrió un error al cargar la vista de resumen: {error}")
        raise Exception("Ocurrió un error al mostrar la vista de resumen.")

@bp.route('/enviar_datos', methods=["POST"])
async def enviar_datos():
    try:
        # Verificar que exista el formulario
        formulario = request.form.to_dict()

        # Verificar formulario
        if not formulario:
            flash(Markup(f'<strong>Precaución</strong>: No se enviaron los datos.'), category='warning')
            return redirect(url_for('generales.reset_password'))

        errores = validar_formulario(formulario)

        # Verificar la existencia de un error
        if errores:
            flash(Markup(f'<strong>Precaución</strong>: {errores}'), category='warning')
            return redirect(url_for('generales.reset_password'))

        # Cabeceras de acceso
        cabeceras = {
            'Content-Type': 'application/json'
        }

        # Obtener respuesta a enviar los datos de la sección
        respuesta = requests.post(ENDPOINT_RECUPERAR_CONTRASENA, json=formulario, headers=cabeceras)

        # Obtener el código de estado
        codigo_estado = respuesta.status_code

        # Obtener los valores
        respuesta_json = respuesta.json()

        # Verificar estado de la respuesta
        if codigo_estado == 200 and respuesta_json['success']:
            flash(Markup('<strong>Éxito:</strong> Se envió el correo con la contraseña'), category="success")
            return redirect('/')
        else:
            error = respuesta_json['detail']
            print(error)
            flash(Markup(f'<strong>Error:</strong> {error}'), category="error")
            return redirect('/reset_password')
    except Exception as error:
        print(f"Ocurrió un error al enviar los datos: {error}")
        raise Exception("Ocurrió un error al enviar los datos")


# Función para manejar las redirecciones
def manejar_redireccion(ruta: str, parametros: str = None):

    # Endpoint base del sistema
    ENDPOINT_BASE = os.getenv('URL_FRONTEND')

    # Paginación básica
    paginacion = "pagina=1&tamano=10"

    # Ruta final
    ruta_final = f"{ENDPOINT_BASE}/{ruta}" if not parametros else f"{ENDPOINT_BASE}/{ruta}?{paginacion}{parametros}"

    return redirect(ruta_final)

@bp.route("/buscar_opciones", methods=["POST"])
def buscar_opciones():
    try:
        # Verificar que se esté pasando un parámetro
        parametro_busqueda = request.form["buscar"]

        # Obtener la URL de donde se solicita
        url_anterior = request.referrer

        parametro_acciones = {
            'Estados': lambda: manejar_redireccion(ruta="estados_republica"),
            'Agregar estado de la república': lambda: manejar_redireccion(ruta="agregar_estado_republica"),
            'Agregar nuevo vendedor': lambda: manejar_redireccion(ruta="agregar_vendedor"),
            'Vendedores': lambda: manejar_redireccion(ruta="ver_vendedores"),
            'Vendedores con más ventas': lambda: manejar_redireccion(ruta="ver_vendedores", parametros="&tipo_estado=&vendedores=mas"),
            'Vendedores con menos ventas': lambda: manejar_redireccion(ruta="ver_vendedores", parametros="&tipo_estado=&vendedores=menos"),
            'Vendedores activos': lambda: manejar_redireccion(ruta="ver_vendedores", parametros="&tipo_estado=Activos"),
            'Vendedores inactivos': lambda: manejar_redireccion(ruta="ver_vendedores", parametros="&tipo_estado=Suspendidos"),
            'Compras': lambda: manejar_redireccion(ruta="ver_clientes"),
            'Compras terminadas': lambda: manejar_redireccion(ruta="ver_clientes", parametros="&ventas=Finalizado"),
            'Compras en proceso': lambda: manejar_redireccion(ruta="ver_clientes", parametros="&ventas=Proceso"),
            'Compras canceladas': lambda: manejar_redireccion(ruta="ver_clientes", parametros="&ventas=Cancelado"),
            'Agregar nuevo cliente': lambda: manejar_redireccion(ruta="agregar_cliente"),
            'Notificaciones': lambda: manejar_redireccion(ruta="ver_notificaciones"),
            'Notificaciones no leídas': lambda: manejar_redireccion(ruta="ver_notificaciones", parametros="&estado_notificacion=sin_leer"),
            'Notificaciones leídas': lambda: manejar_redireccion(ruta="ver_notificaciones", parametros="&estado_notificacion=leidas"),
            'Notificaciones más antigüas': lambda: manejar_redireccion(ruta="ver_notificaciones", parametros="&orden=asc"),
            'Notificaciones más recientes': lambda: manejar_redireccion(ruta="ver_notificaciones", parametros="&orden=desc"),
            'Recuperar contraseña': lambda: manejar_redireccion(ruta="reset_password"),
            'Configuración': lambda: manejar_redireccion(ruta="configuracion"),
        }

        # Obtener la acción
        accion = parametro_acciones.get(parametro_busqueda)

        # Verifica si exista
        if accion:
            return accion()
        else:
            flash(Markup('<strong>Error:</strong> No se encontró la opción seleccionada'), category='error')
            return redirect(url_anterior)

    except Exception as error:
        print(f"Ocurrió un error al intentar redireccionar a la búsqueda seleccionada: {error}")
        raise Exception("Ocurrió un error al intentar redireccionar a la búsqueda seleccionada.")