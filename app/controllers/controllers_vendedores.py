"""
    Archivo que administra los métodos de las operaciones
    relacionadas con los vendedores
"""
# Importamos el módelo de estados así como el de servicio
from ..models.modes_vendedores import VendedoresBase
from ..services.vendedores_services import VendedoresAPI
from typing import Optional

# Crear objeto de VendedoresAPI
VENDEDORES = VendedoresAPI()

# Clase con las operaciones referentes al apartado de lotes
class VendedoresController():

    @staticmethod
    async def obtener_todos_vendedores(token_acceso: str, tipo_filtro: Optional[str] = None, tipo_estado: Optional[str] = None, numero_pagina: int = 1, tamano_pagina: int = 10) -> tuple:
        """
        Función que se encarga de obtener y mapear todos los
        vendedores
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para obtener todos los vendedores
            vendedores, total, codigo_estado = await VENDEDORES. \
                obtener_todos_vendedores(token=token_acceso, filtro=tipo_filtro, estado=tipo_estado, pagina=numero_pagina, tamano=tamano_pagina)

            # Verificar el valor de la respuesta
            if vendedores and codigo_estado == 200:

                # Iterar en cada elemento de la lista
                # mapear el valor en base al módelo
                for vendedor in vendedores:
                    respuesta.append(VendedoresBase(**vendedor))
            elif vendedores and codigo_estado != 200:
                respuesta.append(vendedores)
            else:
                respuesta = vendedores

            return respuesta, total, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al mapear todos los vendedosres: {error}")
            raise Exception("Ocurrió un error al mapear todos los vendedosres")

    @staticmethod
    async def obtener_vendedor(identificador_vendedor: int, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener y mapear la información de un
        vendedor
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para obtener la información del vendedor
            vendedor, codigo_estado = await VENDEDORES.obtener_vendedor(identificador_vendedor, token_acceso)

            # Verificar el valor de la respuesta
            if vendedor and codigo_estado == 200:

                # Iterar por vada valor de la lista
                # mapear el valo en base al módelo
                for dato in vendedor:
                    respuesta.append(VendedoresBase(**dato))
            elif vendedor and codigo_estado != 200:
                respuesta.append(vendedor)
            else:
                respuesta = vendedor

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al mapear el vendedor: {error}.")
            raise Exception("Ocurrió un error al mapear el vendedor.")

    @staticmethod
    async def añadir_nuevo_vendedor(datos_enviar: dict, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener los datos para añadir
        un nuevo vendedor
        """
        try:
            # Respuesta del vendedor
            respuesta = []

            # Llamar a la función para enviar los datos a la API
            vendedor, codigo_estado = await VENDEDORES.añadir_nuevo_vendedor(datos=datos_enviar, token=token_acceso)

            # Verificar el valor
            if vendedor:
                respuesta.append(vendedor)
            else:
                respuesta = vendedor

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener los datos del vendedor: {error}")
            raise Exception("Ocurrió un error al obtener los datos del vendedor")

    @staticmethod
    async def actualizar_un_vendedor(datos_actualizar: dict, identificador_vendedor: str, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener los datos para actualizar
        un vendedor existente
        """
        try:
            # Respuesta vendedor
            respuesta = []

            # Llamara a la función que envia los datos a la API
            vendedor, codigo_estado = await VENDEDORES.actualizar_un_vendedor(datos=datos_actualizar, identificador=identificador_vendedor, token=token_acceso)

            # Verificar la respuesta
            if vendedor:
                respuesta.append(vendedor)
            else:
                respuesta = vendedor

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener los datos al actualizar un vendedor: {error}")
            raise Exception("Ocurrió un error al obtener los datos al actualizar un vendedor")

    @staticmethod
    async def suspender_un_vendedor(identificador_vendedor: str, accion_solicitada: str, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener y enviar los datos necesarios
        para suspender a n vendedor
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función que envia los datos a la API
            vendedor, codigo_estado = await VENDEDORES. \
                suspender_un_vendedor(identificador=identificador_vendedor, accion=accion_solicitada, token=token_acceso)

            # Verificar respuesta de la API
            if vendedor:
                respuesta.append(vendedor)
            else:
                respuesta = vendedor

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener los datos para suspender un vendedor: {error}")
            raise Exception("Ocurrió un error al obtener los datos para suspender un vendedor")

    @staticmethod
    async def eliminar_un_vendedor(identificador_vendedor: str, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener y enviar los datos para eliminar un vendedor
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la unficón que envia los datos a la API
            vendedor, codigo_estado = await VENDEDORES.eliminar_un_vendedor(identificador=identificador_vendedor, token=token_acceso)

            # Verificar respuesta de la API
            if vendedor:
                respuesta.append(vendedor)
            else:
                respuesta = vendedor

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener los datos para eliminar un vendedor: {error}")
            raise Exception("Ocurrió un error al obtener los datos para eliminar un vendedor")

    @staticmethod
    async def obtener_vendedores_sin_filtros(token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener y mapear todos los vendedores
        sin filtros
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función que obtiene los datos de la API
            vendedores, codigo_estado = await VENDEDORES.obtener_vendedores_sin_filtros(token = token_acceso)

            # Verificar la respuesta de la PIA
            if vendedores and codigo_estado == 201:
                # Iterar en cada elemento de la lista
                # mapear el valor en base al módelo
                for vendedor in vendedores:
                    respuesta.append(VendedoresBase(**vendedor))
            elif vendedores and codigo_estado != 200:
                respuesta.append(vendedores)
            else:
                respuesta = vendedores

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener y mapear los datos de los vendedores: {error}")
            raise Exception(f"Ocurrió un error al obtener y mapear los datos de los vendedores: {error}")