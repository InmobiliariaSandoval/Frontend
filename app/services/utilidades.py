"""
    Archivo que almacena los endpoints de solicitudes a la API
"""
import os

# Endpoint base
ENDPOINT_BASE = os.environ['URL_BACKEND']

# Endpoint para cerrar sesión
ENDPOINT_CERRAR_SESION = f'{ENDPOINT_BASE}/cerrar_sesion'
ENDPOINT_RECUPERAR_CONTRASENA = f'{ENDPOINT_BASE}/recuperar_contrasena'

# Endpoint para las notificaciones
ENDPOINT_NOTIFICACIONES = f'{ENDPOINT_BASE}/notificaciones'
ENDPOINT_ELIMINAR_NOTIFICACION = f'{ENDPOINT_BASE}/borrar_notificacion'
ENDPOINT_ELIMINAR_TODAS_NOTIFICACIONES = f'{ENDPOINT_BASE}/borrar_notificaciones'
ENDPOINT_MARCAR_LEIDA_NOTIFICACION = f'{ENDPOINT_BASE}/marcar_leida_notificacion'
ENDPOINT_MARCAR_LEIDA_TODAS_NOTIFICACIONES = f'{ENDPOINT_BASE}/marcar_leidas_todas'

# Endpoint para los estados
ENDPOINT_ESTADOS = f'{ENDPOINT_BASE}/estados_republica'
ENDPOINT_OBTENER_UBICACION = f'{ENDPOINT_BASE}/ubicacion_lote'
ENDPOINT_OBTENER_ESTADO = f'{ENDPOINT_BASE}/obtener_estado_especifico'
ENDPOINT_OBTENER_MUNICIPIO = f'{ENDPOINT_BASE}/obtener_municipio_especifico'
ENDPOINT_OBTENER_LOCALIDAD = f'{ENDPOINT_BASE}/obtener_localidad_especifica'
ENDPOINT_OBTENER_COMPLEJO = f'{ENDPOINT_BASE}/obtener_complejo_especifico'
ENDPOINT_OBTENER_LOTE = f'{ENDPOINT_BASE}/lote_informacion_extra'
ENDPOINT_OBTENER_LOTE_VENTA = f'{ENDPOINT_BASE}/informacion_venta_lote'

ENDPOINT_AGREGAR_ESTADO = f'{ENDPOINT_BASE}/agregar_estado'
ENDPOINT_AGREGAR_MUNICIPIO = f'{ENDPOINT_BASE}/agregar_municipio'
ENDPOINT_AGREGAR_LOCALIDAD = f'{ENDPOINT_BASE}/agregar_localidad'
ENDPOINT_AGREGAR_COMPLEJO = f'{ENDPOINT_BASE}/agregar_complejo_residencial'
ENDPOINT_AGREGAR_SECCION = f'{ENDPOINT_BASE}/agregar_seccion'
ENDPOINT_AGREGAR_LOTE = f'{ENDPOINT_BASE}/agregar_lote'

ENDPOINT_ELIMINAR_LOTE =f'{ENDPOINT_BASE}/eliminar_lote'
ENDPOINT_ELIMINAR_SECCOIN = f'{ENDPOINT_BASE}/eliminar_seccion'
ENDPOINT_ELIMINAR_COMPLEJO = f'{ENDPOINT_BASE}/eliminar_complejo'
ENDPOINT_ELIMINAR_LOCALIDAD= f'{ENDPOINT_BASE}/eliminar_localidad'
ENDPOINT_ELIMINAR_MUNICIPIO = f'{ENDPOINT_BASE}/eliminar_municipio'
ENDPOINT_ELIMINAR_ESTADO= f'{ENDPOINT_BASE}/eliminar_estado'

ENDPOINT_ACTUALIZAR_LOTE = f'{ENDPOINT_BASE}/actualizar_lote'
ENDPOINT_ACTUALIZAR_SECCION = f'{ENDPOINT_BASE}/actualizar_seccion'
ENDPOINT_ACTUALIZAR_COMPLEJO = f'{ENDPOINT_BASE}/actualizar_complejo'
ENDPOINT_ACTUALIZAR_LOCALIDAD = f'{ENDPOINT_BASE}/actualizar_localidad'
ENDPOINT_ACTUALIZAR_MUNICIPIO = f'{ENDPOINT_BASE}/actualizar_municipio'
ENDPOINT_ACTUALIZAR_ESTADO = f'{ENDPOINT_BASE}/actualizar_estado'

# Endpoint para los vendedores #
ENDPOINT_VENDEDORES = f'{ENDPOINT_BASE}/vendedores/'
ENDPOINT_VENDEDORES_SIN_FILTR0 = f'{ENDPOINT_BASE}/vendedores_sin_filtro'
ENDPOINT_ANADIR_VENDEDOR = f'{ENDPOINT_BASE}/añadir_vendedor'
ENDPOINT_ACTUALIZAR_VENDEDOR = f'{ENDPOINT_BASE}/actualizar_vendedor'
EDNPOINT_SUSPENDER_VENDEDOR = f'{ENDPOINT_BASE}/cambiar_estado_vendedor'
ENDPOINT_ELIMINAR_VENDEDOR = f'{ENDPOINT_BASE}/eliminar_vendedor'

# Endpoint para los clientes
ENDPOINT_CLIENTES = f'{ENDPOINT_BASE}/clientes'
ENDPOINT_AGREGAR_CLIENTE = f'{ENDPOINT_BASE}/agregar_cliente'
ENDPOINT_ACTUALIZAR_CLIENTE = f'{ENDPOINT_BASE}/actualizar_cliente'

# Endpoint para las ventas
ENDPOINT_VENTAS = f'{ENDPOINT_BASE}/ventas/'
ENDPOINT_AGREGAR_VENTA = f'{ENDPOINT_BASE}/agregar_venta'
ENDPOINT_OBTENER_UNA_VENTA = f'{ENDPOINT_BASE}/venta_especifica'
ENDPOINT_CAMBIAR_ESTADO_VENTA = f'{ENDPOINT_BASE}/cambiar_estado_venta'
ENDPOINT_TODOS_PLAZOS = f'{ENDPOINT_BASE}/plazo_compra'
ENDPOINT_AGREGAR_PLAZO = f'{ENDPOINT_BASE}/agregar_plazo_compra'
ENDPOINT_ELIMINAR_PLAZO = f'{ENDPOINT_BASE}/eliminar_plazo_compra'
ENDPOINT_ACTUALIZAR_PLAZO = f'{ENDPOINT_BASE}/actualizar_plazo_compra'
ENDPOINT_OBTENER_DETALLE = f'{ENDPOINT_BASE}/detalle_pago_plazo'
ENDPOINT_AGREGAR_DETALLE = f'{ENDPOINT_BASE}/agregar_detalle_pago'
ENDPOINT_ACTUALIZAR_DETALLE = f'{ENDPOINT_BASE}/actualizar_detalle_pago'
ENDPOINT_ELIMINAR_DETALLE = f'{ENDPOINT_BASE}/eliminar_detalle_pago'

# Endpoint para la configuración
ENDPOINT_CONFIGURACION =f'{ENDPOINT_BASE}/configuracion_especifica'