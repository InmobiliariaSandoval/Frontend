"""
    Archivo que administra los métodos de las operaciones
    realicionadas a las notificaciones
"""
# Importamos el módelo de notificaciones así como el servicio de API
from ..models.models_notificaciones import NotificacionesBase, ConfiguracionBase
from ..services.notificaciones_services import NotificacionesAPI

# Crear el objeto de NotificacionesAPI
NOTIFICACIONES = NotificacionesAPI()

# Clase con las operaciones referentes al apartado de Notificaicone
class NotificacionesController():

    @staticmethod
    async def obtener_todas_notificaciones(token_acceso: str, pagina: int = 1,
                                           limite_notificaciones: int = 5, notificaciones_no_leidas: bool = None, orden: str = None) -> list:
        """
        Función que se encarga de obtener todas las notificaciones
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para obtener todas las notificaciones
            notificaciones, total_notificaciones, codigo_estado = await NOTIFICACIONES. \
                obtener_todas_notificaciones(token=token_acceso, pagina=pagina, limite=limite_notificaciones,
                                             no_leidas=notificaciones_no_leidas, orden=orden)

            # Verificar el valor de notificaciones
            if notificaciones and codigo_estado == 200:

                # Iterar en cada elemento de la lismta
                # mapea el valor en base al módelo
                for notificacion in notificaciones:
                    respuesta.append(NotificacionesBase(**notificacion))
            elif notificaciones and codigo_estado != 200:
                respuesta.append(notificaciones)
            else:
                respuesta = notificaciones
            return respuesta, total_notificaciones, codigo_estado

        except Exception as error:
            print(f"Ocurrió un error al mapear las notificaciones: {error}")
            raise Exception("Ocurrió un error al mapear las notificaciones")

    @staticmethod
    async def eliminar_una_notificacion(token_acceso: str, identificador_notificacion: str) -> list:
        """
        Función que se encarga de obtener los datos para eliminar una notificación
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función que envía los datos
            notificacion, codigo_estado = await NOTIFICACIONES. \
                eliminar_una_notificacion(token=token_acceso, identificador=identificador_notificacion)

            # Verificar respuesta
            if notificacion:
                respuesta.append(notificacion)
            else:
                respuesta = notificacion

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener los datos para eliminar una notificacińo: {error}")
            raise Exception("Ocurrió un error al obtener los datos para eliminar una notificacińo")

    @staticmethod
    async def eliminar_notificaciones(token_acceso: str) -> list:
        """
        Función que se encarga de obtener los datos para eliminar todas las notificaciones
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función que envía los datos a la API
            notificacion, codigo_estado = await NOTIFICACIONES.eliminar_todas_notificaciones(token=token_acceso)

            # Verificar respuesta
            if notificacion:
                respuesta.append(notificacion)
            else:
                respuesta = notificacion

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al enviar los datos para eliminar todas las notificaciones: {error}")
            raise Exception("Ocurrió un error al enviar los datos para eliminar todas las notificaciones")

    @staticmethod
    async def marcar_leida_una_notificacion(token_acceso: str, identificador_notificacion: str) -> list:
        """
        Función que se encarga de obtener los datos para marcar cómo leída una notificación
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función que envía los datos
            notificacion, codigo_estado = await NOTIFICACIONES. \
                marcar_leida_una_notificacion(token=token_acceso, identificador=identificador_notificacion)

            # Verificar respuesta
            if notificacion:
                respuesta.append(notificacion)
            else:
                respuesta = notificacion

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener los datos para marcar como leída una notificacińo: {error}")
            raise Exception("Ocurrió un error al obtener los datos para marcar como leída una notificacińo")

    @staticmethod
    async def marcar_leida_todas_notificaciones(token_acceso: str) -> list:
        """
        Función que se encarga de obtener los datos para marcar cómo leída todas las notificaciones
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función que envía los datos a la API
            notificacion, codigo_estado = await NOTIFICACIONES.marcar_leida_todas_notificaciones(token=token_acceso)

            # Verificar respuesta
            if notificacion:
                respuesta.append(notificacion)
            else:
                respuesta = notificacion

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al enviar los datos para marcar como leída todas las notificaciones: {error}")
            raise Exception("Ocurrió un error al enviar los datos para marcar como leída todas las notificaciones")

    @staticmethod
    async def obtener_configuracion_especifica(identificador_configuracion: str, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener y mapear los datos de la configuración
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para obtener la información de la configuración
            respuesta_configuracion, codigo_estado = await NOTIFICACIONES. \
                obtener_configuracion_especifica(identificador=identificador_configuracion, token=token_acceso)

                        # Verificar el valor de la respuesta
            if respuesta_configuracion and codigo_estado == 200:

                # Iterar por vada valor de la lista
                # mapear el valo en base al módelo
                for dato in respuesta_configuracion:
                    respuesta.append(ConfiguracionBase(**dato))
            elif respuesta_configuracion and codigo_estado != 200:
                respuesta.append(respuesta_configuracion)
            else:
                respuesta = respuesta_configuracion

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener y mapear la configuración del estado: {error}")
            raise Exception("Ocurrió un error al obtener y mapear la configuración del estado")