"""
    Archivo que se encarga de administrar las operaciones
    relacionadas con el apartado de vendedores.
"""

import requests
from typing import Optional
from .utilidades import ENDPOINT_VENDEDORES, ENDPOINT_BASE, ENDPOINT_ANADIR_VENDEDOR, \
    ENDPOINT_ACTUALIZAR_VENDEDOR, EDNPOINT_SUSPENDER_VENDEDOR, ENDPOINT_ELIMINAR_VENDEDOR, \
    ENDPOINT_VENDEDORES_SIN_FILTR0

# Clase de las operaciones de la API
class VendedoresAPI():

    # Función para obtener todos los vendedores
    @staticmethod
    async def obtener_todos_vendedores(token: str, filtro: Optional[str] = None, estado: Optional[str] = None, pagina: int = 1, tamano: int = 10) -> tuple:
        """
        Función que se encarga de obtener todos los
        vendedores
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}'
            }

            # Verificar que exista el filtro de tipo de complejo
            URL_consulta = ENDPOINT_VENDEDORES
            params = {'pagina': pagina, 'tamano': tamano} if not filtro and not estado else {'pagina': pagina, 'tamano': tamano, 'orden': filtro, 'tipo': estado}

            # Realizar solicitud a la API
            respuesta_vendedores = requests.get(URL_consulta, headers=cabeceras, params=params)

            # Obtener código de estado de la respuesta
            codigo_estado = respuesta_vendedores.status_code

            # Intentar parserar la respuesta a JSON
            datos = respuesta_vendedores.json()

            total = 0

            # Verificar respuesta
            if respuesta_vendedores and codigo_estado == 200:
                total = datos['Total de vendedores']
                vendedores = datos['Vendedores']
            else:
                vendedores = 0

            return vendedores, total, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener los vendedores: {error}.")
            raise Exception("Ocurrió un error al obtener todos los vendedores")

    # Función para obtener todos los vendedores
    @staticmethod
    async def obtener_vendedor(identificador_vendedor: int, token: str) -> tuple:
        """
        Función que se encarga de obtener todos los
        vendedores
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}'
            }

            # Realizar solicitud a la API
            respuesta_vendedor = requests.get(f"{ENDPOINT_BASE}/{identificador_vendedor}/vendedor_especifico", headers=cabeceras)

            # Obtener código de estado de la respuesta
            codigo_estado = respuesta_vendedor.status_code

            # Intentar parserar la respuesta a JSON
            vendedor = respuesta_vendedor.json()

            return vendedor, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener los vendedores: {error}.")
            raise Exception("Ocurrió un error al obtener todos los vendedores")

    # Función que agregar un nuevo vendedor
    @staticmethod
    async def añadir_nuevo_vendedor(datos: dict, token: str) -> tuple:
        """
        Función que se encarga de enviar los datos obtenidos del formulario
        a la API
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            # Realizar solicitud a la API
            respuesta_vendedor = requests.post(ENDPOINT_ANADIR_VENDEDOR, json=datos, headers=cabeceras)

            # Obtener código de estado de la respuesta
            codigo_estado = respuesta_vendedor.status_code

            # Intentar pasear la respuesta a JSON
            vendedor = respuesta_vendedor.json()

            return vendedor, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error enviando los datos a al API: {error}")
            raise Exception("Ocurrió un error enviando los datos a al API")

    # Función para actualizar un vendedor
    @staticmethod
    async def actualizar_un_vendedor(datos: dict, identificador: str, token: str) -> tuple:
        """
        Función que se encarga de enviar los datos obtenidos del formulario
        para actualizar un vendedor
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            # Realizar la petición a la API
            respuesta_vendedor = requests.put(f"{ENDPOINT_ACTUALIZAR_VENDEDOR}/{identificador}", json=datos, headers=cabeceras)

            # Obtener código de estado de la respuesta
            codigo_estado = respuesta_vendedor.status_code

            # Intentar parsear la respuesta a JSON
            vendedor = respuesta_vendedor.json()

            return vendedor, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error enviando los datos para actualizar un vendedor: {error}")
            raise Exception("Ocurrió un error enviando los datos para actualizar un vendedor")

    # Función para suspender un vendedor
    @staticmethod
    async def suspender_un_vendedor(identificador: str, accion: str, token: str) -> tuple:
        """
        Función que se encarga de enviar el identificador de un vendedor
        para suspenderlo
        """
        try:
            # Cabeceras
            cabeceras = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            # Parametros de cambio
            parametros = {
                'estado': accion
            }

            # Realizar solicitud a la API
            respuesta_vendedor = requests.get(f"{EDNPOINT_SUSPENDER_VENDEDOR}/{identificador}", params=parametros, headers=cabeceras)

            # Obtener el código de estado de la respuesta
            codigo_estado = respuesta_vendedor.status_code

            # Intetar parsear la respuesta a JSON
            vendedor = respuesta_vendedor.json()

            return vendedor, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al enviar los datos para suspender un vendedor: {error}")
            raise Exception("Ocurrió un error al enviar los datos para suspender un vendedor")

    # Función para eliminar un vendedor
    @staticmethod
    async def eliminar_un_vendedor(identificador: str, token: str) -> tuple:
        """
        Función que se encarga de enviar el identificador de un vendedor
        para eliminarlo
        """
        try:
            # Cabeceras
            cabeceras = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            # Realizar solicitud a la API
            respuesta_vendedor = requests.delete(f"{ENDPOINT_ELIMINAR_VENDEDOR}/{identificador}", headers=cabeceras)

            # Obtener el código de respuesta
            codigo_estado = respuesta_vendedor.status_code

            # Intentar parsear la respuetsa a JSON
            vendedor = respuesta_vendedor.json()

            return vendedor, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al enviar los datos para eliminar un vendedor: {error}")
            raise Exception("Ocurrió un error al enviar los datos para eliminar un vendedor")

    # Función para obtener todos los vendedores sin filtros
    @staticmethod
    async def obtener_vendedores_sin_filtros(token: str) -> tuple:
        """
        Función que se encarga de obtener todos los vendedores
        sin necesidad del filtroobtener_vendedores
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}'
            }

            # Realizar la solicitud a la API
            respuesta_vendedores = requests.get(ENDPOINT_VENDEDORES_SIN_FILTR0, headers=cabeceras)

            # Obtener el código de estado
            codigo_estado = respuesta_vendedores.status_code

            # Intentar parser la respuesta a JSON
            vendedores = respuesta_vendedores.json()

            return vendedores, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener todos los vendedores: {error}")
            raise Exception("Ocurrió un error al obtener todos los vendedores")