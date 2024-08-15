"""
    Archivo ques se encarga de administrar las
    operaciones del apartado cliente
"""
from .utilidades import ENDPOINT_BASE, ENDPOINT_CLIENTES, ENDPOINT_AGREGAR_CLIENTE, ENDPOINT_ACTUALIZAR_CLIENTE
import requests

# Clase de las operaciones de la API
class ClienteAPI():

    @staticmethod
    async def obtener_un_cliente(identificador_cliente: str, token: str) -> tuple:
        """
        Función que se encarga de obtener un cliente especifico
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}'
            }

            # Realizar solicitud a la API
            respuesta_cliente = requests.get(f"{ENDPOINT_BASE}/{identificador_cliente}/cliente_especifico", headers=cabeceras)

            # Obtener código de estado de la solicitud
            codigo_estado = respuesta_cliente.status_code

            # Intentar parsear la respuesta JSON
            cliente = respuesta_cliente.json()

            return cliente, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener el cliente: {error}")
            raise Exception("Ocurrió un error al obtener el cliente.")

    @staticmethod
    async def obtener_todos_clientes(token: str) -> tuple:
        try:
            # Cabeceras de acceso
            cabecearas = {
                'Authorization': f'Bearer {token}'
            }

            # Realizar solicitud a la API
            respuesta_cliente = requests.get(ENDPOINT_CLIENTES, headers=cabecearas)

            # Obtener código de estado de la solicitud
            codigo_estado = respuesta_cliente.status_code

            # Intentar parsear la respueta a JSON
            clientes = respuesta_cliente.json()

            return clientes, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener todos los clientes: {error}")
            raise Exception(f"Ocurrió un error al obtener todos los clientes")

    # Función que agregar un nuevo cliente
    @staticmethod
    async def agregar_nuevo_cliente(datos: dict, token: str) -> tuple:
        """
        Función que se encarga de enviar los datos obteneidos del formulario
        a la API
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            # Realizar solicitud a la API
            respuesta_cliente = requests.post(ENDPOINT_AGREGAR_CLIENTE, headers=cabeceras, json=datos)

            # Obtener código de estado de la soliitud
            codigo_estado = respuesta_cliente.status_code

            # Intentar parsear la respuesta a JSON
            cliente = respuesta_cliente.json()

            return cliente, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error enviando los datos a la API: {error}")
            raise Exception("Ocurrió un error enviando los datos a la API")

    # Función para actualizar un cliente
    @staticmethod
    async def actualizar_un_cliente(datos: dict, identificador: str, token: str) -> tuple:
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

            # Realizar solicitud a la API
            respuesta_cliente = requests.put(f"{ENDPOINT_ACTUALIZAR_CLIENTE}/{identificador}", headers=cabeceras, json=datos)

            # Obtener código de estado de la soliitud
            codigo_estado = respuesta_cliente.status_code

            # Intentar parsear la respuesta a JSON
            cliente = respuesta_cliente.json()

            return cliente, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error enviando los datos para actualizar un cliente: {error}")
            raise Exception("Ocurrió un error enviando los datos para actualizar un cliente")