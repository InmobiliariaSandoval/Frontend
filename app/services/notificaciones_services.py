"""
    Archivo que almacena las solicitudes a la API
    de las notificaciones
"""
import requests
from .utilidades import ENDPOINT_NOTIFICACIONES, ENDPOINT_ELIMINAR_NOTIFICACION, ENDPOINT_ELIMINAR_TODAS_NOTIFICACIONES, \
    ENDPOINT_MARCAR_LEIDA_TODAS_NOTIFICACIONES, ENDPOINT_MARCAR_LEIDA_NOTIFICACION, ENDPOINT_CONFIGURACION

# Clase de las operaciones de la API
class NotificacionesAPI():

    # Métedo para obtener todas las notificaciones
    @staticmethod
    async def obtener_todas_notificaciones(token: str, pagina: int =1 , limite: int = 5, no_leidas: bool = None, orden: str = None):
        """
        Función que se encarga de obtener todas las notificaciones
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}'
            }

            # Parametros de búsqueda
            parametros = {
                'pagina': pagina,
                'limite':  limite,
                'no_leidas': no_leidas,
                'orden': orden
            }

            # Realizar solicitud a la API
            respuesta_notificaciones = requests.get(ENDPOINT_NOTIFICACIONES, headers=cabeceras, params=parametros)

            # Obtener estado de la respuesta
            codigo_estado = respuesta_notificaciones.status_code

            # Intentar parsear la respuesta JSON
            datos = respuesta_notificaciones.json()

            # Verificar código de estado de la respuesta
            if codigo_estado == 200:
                notificaciones = datos['Notificaciones']
                total_notificaciones = datos['Total de notificaciones']
            else:
                notificaciones, total_notificaciones = datos, 0

            return notificaciones, total_notificaciones, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener todas las notificaciones: {error}")
            raise Exception(f"No se logró obtener todas las notificaciones: {respuesta_notificaciones.status_code}")

    @staticmethod
    async def eliminar_una_notificacion(token: str, identificador: str) -> list:
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            # Realizar solicitud a la API
            respuesta_notificacion = requests.delete(f"{ENDPOINT_ELIMINAR_NOTIFICACION}/{identificador}", headers=cabeceras)

            # Obtener el código de estado de la solicitud
            codigo_estado = respuesta_notificacion.status_code

            # Intentar parsear la respuesta a JSON
            notificacion = respuesta_notificacion.json()

            return notificacion, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al enviar los datos para eliminar una notificación: {error}")
            raise Exception("Ocurrió un error al enviar los datos para eliminar una notificación")

    @staticmethod
    async def eliminar_todas_notificaciones(token: str) -> list:
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            # Realizar solicitud a la API
            respuesta_notificacion = requests.delete(ENDPOINT_ELIMINAR_TODAS_NOTIFICACIONES, headers=cabeceras)

            # Obtener el código de estado de la solicitud
            codigo_estado = respuesta_notificacion.status_code

            # Intentar parsear la respuesta a JSON
            notificacion = respuesta_notificacion.json()

            return notificacion, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al enviar los datos para eliminar todas las notificación: {error}")
            raise Exception("Ocurrió un error al enviar los datos para eliminar todas las notificación")

    @staticmethod
    async def marcar_leida_una_notificacion(token: str, identificador: str) -> list:
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            # Realizar solicitud a la API
            respuesta_notificacion = requests.get(f"{ENDPOINT_MARCAR_LEIDA_NOTIFICACION}/{identificador}", headers=cabeceras)

            # Obtener el código de estado de la solicitud
            codigo_estado = respuesta_notificacion.status_code

            # Intentar parsear la respuesta a JSON
            notificacion = respuesta_notificacion.json()

            return notificacion, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al enviar los datos para marcar como leída una notificación: {error}")
            raise Exception("Ocurrió un error al enviar los datos para marcar como leída una notificación")

    @staticmethod
    async def marcar_leida_todas_notificaciones(token: str) -> list:
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            # Realizar solicitud a la API
            respuesta_notificacion = requests.get(ENDPOINT_MARCAR_LEIDA_TODAS_NOTIFICACIONES, headers=cabeceras)

            # Obtener el código de estado de la solicitud
            codigo_estado = respuesta_notificacion.status_code

            # Intentar parsear la respuesta a JSON
            notificacion = respuesta_notificacion.json()

            return notificacion, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al enviar los datos para marcar como leídas todas las notificación: {error}")
            raise Exception("Ocurrió un error al enviar los datos para marcar como leídas todas las notificación")

    @staticmethod
    async def obtener_configuracion_especifica(identificador: str, token: str) -> tuple:
        """
        Función que se encarga de obtener la configuración de la cuenta
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}'
            }

            # Realizar solicitud a la API
            respuesta_configuracion = requests.get(f"{ENDPOINT_CONFIGURACION}/{identificador}", headers=cabeceras)

            # Obtener el código de estado de la solicitud
            codigo_estado = respuesta_configuracion.status_code

            # Intentar parsera la respuesta a JSON
            configuracion = respuesta_configuracion.json()

            return configuracion, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener la configuración: {error}")
            raise Exception("Ocurrió un error al obtener la configuración")