"""
    Archivo que administra los métodos de las operaciones
    relacionadas con los clientes
"""
# Importamos el módelo de estados así como el de servicio
from ..models.models_cliente import ClienteBase
from ..services.cliente_services import ClienteAPI

# Crear objeto de ClienteAPI
CLIENTE = ClienteAPI()

# Clase con las operaciones referentes al apartado de clientes
class ClienteController():

    @staticmethod
    async def obtener_un_cliente(identificador_cliente: str, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener y mapear la información del cliente
        especifico
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para obtener la información de cliente
            cliente, codigo_estado = await CLIENTE.obtener_un_cliente(identificador_cliente=identificador_cliente, token=token_acceso)

            # Verificar el valor de la respuesta
            if cliente and codigo_estado == 200:

                # Iterar en cada elemento de la lista
                # mapear el valor en base al módelo
                for valor in cliente:
                    respuesta.append(ClienteBase(**valor))
            else:
                respuesta.append(cliente)

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al mapear el cliente: {error}")
            raise Exception("Ocurrió un error al mapear el cliente")

    @staticmethod
    async def obtener_todos_cliente(token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener y mapear todos los clientes
        de la base de datos
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para obtener todos los clientes
            clientes, codigo_estado = await CLIENTE.obtener_todos_clientes(token=token_acceso)

            # Verificar el valor de la respuesta
            if clientes and codigo_estado == 200:

                # Iterar en cada elemento de la lista
                # mapear el valor en base al modelo
                for cliente in clientes:
                    respuesta.append(ClienteBase(**cliente))
            else:
                respuesta.append(clientes)

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurró un error al mapear la información de los clientes: {error}")
            raise Exception("Ocurró un error al mapear la información de los clientes")

    @staticmethod
    async def agregar_nuevo_cliente(datos_enviar: dict, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener todos los datos para añadir
        un nuevo cliente
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función que envia los datos a la API
            cliente, codigo_estado = await CLIENTE.agregar_nuevo_cliente(datos=datos_enviar, token=token_acceso)

            # Verificar la respuesta
            if cliente:
                respuesta.append(cliente)
            else:
                respuesta = cliente

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener los datos del cliente: {error}")
            raise Exception("Ocurrió un error al obtener los datos del cliente")

    @staticmethod
    async def actualizar_un_cliente(datos_actualizar: dict, identificador_cliente: str, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener los datos para actualizar
        un cliente existente
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función que envia los datos a la API
            cliente, codigo_estado = await CLIENTE. \
                actualizar_un_cliente(datos=datos_actualizar, identificador=identificador_cliente, token=token_acceso)

            # Verificar la respuesta
            if cliente:
                respuesta.append(cliente)
            else:
                respuesta = cliente

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener los datos para actualizar un cliente: {error}")
            raise Exception("Ocurrió un error al obtener los datos para actualizar un cliente")