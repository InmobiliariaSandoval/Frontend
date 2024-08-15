"""
    Archivo ques se encarga de administrar las
    operaciones del apartado de ventas / compras
"""
from .utilidades import ENDPOINT_ACTUALIZAR_DETALLE, ENDPOINT_VENTAS, ENDPOINT_AGREGAR_VENTA, ENDPOINT_OBTENER_UNA_VENTA, \
                        ENDPOINT_TODOS_PLAZOS, ENDPOINT_AGREGAR_PLAZO, ENDPOINT_ELIMINAR_PLAZO, \
                        ENDPOINT_ACTUALIZAR_PLAZO, ENDPOINT_CAMBIAR_ESTADO_VENTA, ENDPOINT_OBTENER_DETALLE, \
                        ENDPOINT_AGREGAR_DETALLE, ENDPOINT_ELIMINAR_DETALLE
import requests

# Clase de las operaciones de la API
class VentasAPI():

    # Función para obtener todas la ventas
    @staticmethod
    async def obtener_todas_ventas(token: str, filtro: str = None, pagina: int = 1, tamano: int = 10) -> list:
        """
        Función que se encarga de obtener todas las ventas
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}'
            }

            # Parametros de búsqueda
            parametros = {
                'filtro': filtro,
                'pagina': pagina,
                'tamano': tamano
            }

            # Realizar consulta a la API
            respuesta_ventas = requests.get(ENDPOINT_VENTAS, headers=cabeceras, params=parametros)

            # Obtener código de estado de la consulta
            codigo_estado = respuesta_ventas.status_code

            # Intentar parsear a JSON la respuesta
            datos = respuesta_ventas.json()

            # Verificar datos
            if codigo_estado == 200:
                ventas = datos['Ventas']
                total = datos['Total de ventas']
            else:
                ventas, total = datos, 0

            return ventas, total, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener todas las ventas: {error}.")
            raise Exception("Ocurrió un error al obtener todas las ventas.")

    @staticmethod
    async def agregar_nueva_venta(datos: dict, token: str) -> tuple:
        """
        Función que se encarga de enviar los datos de una nueva venta
        para ser agregada
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            #Eliminar valores innecesarios
            if 'compra_completa' in datos:
                del datos['compra_completa']

            del datos['pago_plazo']
            del datos['precio_inicial']

            # Realizar solicitud a la API
            respuesta_venta = requests.post(ENDPOINT_AGREGAR_VENTA, json=datos, headers=cabeceras)

            # Obtener el código de estado de la solicitud
            codigo_estado = respuesta_venta.status_code

            # Intentar parsear la respusta a JSON
            venta = respuesta_venta.json()

            return venta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al enviar los datos para agregar una venta: {error}")
            raise Exception("Ocurrió un error al enviar los datos para agregar una venta")

    # Función para obtener una compra en especifico
    @staticmethod
    async def obtener_compra_especifica(identificador: str, token: str) -> tuple:
        """
        Función que se encarga de obtener una compra
        en especifico
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}'
            }

            # Realizar la solicitud a la API
            respuesta_compra = requests.get(f'{ENDPOINT_OBTENER_UNA_VENTA}/{identificador}', headers=cabeceras)

            # Obtener el código de estado de la solicitud
            codigo_estado = respuesta_compra.status_code

            # Intentar parsear la respuesta a JSON
            compra = respuesta_compra.json()

            return compra, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener la compra: {error}")
            raise Exception("Ocurrió un error al obtener la compra")


    # Función que obtiene todos los plazos de una compra
    @staticmethod
    async def obtener_plazos_compra(identificador_compra: str, token: str, pagina: int = 1, tamano: int = 10) -> tuple:
        """
        Función que obtiene todos los plazos de una compra
        de la base de datos
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}'
            }

            # Parametros de búsqueda
            params = {'pagina': pagina, 'tamano': tamano}

            # Realizar solicitud a la API
            respuesta_plazos = requests.get(f'{ENDPOINT_TODOS_PLAZOS}/{identificador_compra}', headers=cabeceras, params=params)

            # Obtener el código de estado de la solicitud
            codigo_estado = respuesta_plazos.status_code

            # Intentar parsear la respuesta a JSON
            datos = respuesta_plazos.json()

            total = 0

            if datos and codigo_estado == 200:
                total = datos['Total de plazos']
                plazos = datos['Plazos']
            else:
                plazos = 0

            return plazos, total, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener todos los plazos de una compra: {error}")
            raise Exception("Ocurrió un error al obtener todos los plasos de una compra")

    # Función que agrega un nuevo plazo a la venta
    @staticmethod
    async def agregar_nuevo_plazo(datos: dict, token: str) -> tuple:
        """
        Función que se encarga de enviar los datos para agregar un nuevo
        plazo
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}'
            }

            # Realizar la solicitud a la API
            respuesta_plazo = requests.post(ENDPOINT_AGREGAR_PLAZO, json=datos, headers=cabeceras)

            # Obtener el código de estado de la respuesta
            codigo_estado = respuesta_plazo.status_code

            # Intentar parsear la respuesta a JSON
            plazo = respuesta_plazo.json()

            return plazo, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al enviar los datos del plazo: {error}")
            raise Exception("Ocurrió un error al enviar los datos del plazo")

    # Función que elimina un plazo
    @staticmethod
    async def eliminar_un_plazo(identificador_plazo: str, token: str) -> tuple:
        """
        Función que se encarga de enviar los datos a la API para eliminar
        un plazo
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}'
            }

            # Realizar la solicitud a la API
            respuesta_plazo = requests.delete(f"{ENDPOINT_ELIMINAR_PLAZO}/{identificador_plazo}", headers=cabeceras)

            # Obtener código de estado de la solicitud
            codigo_estado = respuesta_plazo.status_code

            # Intentar parsear la respuesta a JSON
            plazo = respuesta_plazo.json()

            return plazo, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al enviar los datos para eliminar el plazo: {error}")
            raise Exception("Ocurrió un error al enviar los datos para eliminar el plazo")

    # Función que se encarga de editar un plazo
    @staticmethod
    async def editar_un_plazo(identificador: str, datos: dict, token: str) -> tuple:
        """
        Función que se encarga de enviar los datos para editar
        un plazo en especifico
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            # Realizar solicitud a la API
            respuesta_plazo = requests.put(f"{ENDPOINT_ACTUALIZAR_PLAZO}/{identificador}", json=datos, headers=cabeceras)

            # Obtener el código de estado de la solicitud
            codigo_estado = respuesta_plazo.status_code

            # Intentar parsera la respuesta a JSON
            plazo = respuesta_plazo.json()

            return plazo, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al enviar los datos del plazo actualizado: {error}")
            raise Exception("Ocurrió un error al enviar los datos del plazo actualizado")

    # Función que se encarga de cambiar el estado de una compra
    @staticmethod
    async def cambiar_estado_una_compra(identificador: str, estado: str, token: str) -> tuple:
        """
        Función que se encarga de enviar los datos para cambiar
        el estadod de una compra
        """
        try:
            # Cabecears de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}'
            }

            # Parametros
            parametros = {
                'estado': estado
            }

            # Realizar la solicitud a la API
            respuesta_compra = requests.get(f'{ENDPOINT_CAMBIAR_ESTADO_VENTA}/{identificador}', params=parametros, headers=cabeceras)

            # Obtener el código de esatdo de la compra
            codigo_estado = respuesta_compra.status_code

            # Intentar parsear la respuesta a JSON
            compra = respuesta_compra.json()

            return compra, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al enviar los datos para cambiar el estado de la venta: {error}")
            raise Exception("Ocurrió un error al enviar los datos para cambiar el estado de la venta")

    @staticmethod
    async def obtener_un_detalle(identificador: str, token: str) -> tuple:
        """
        Función que se encarga de obtener los datos de un detalle
        de pago en especifico
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}'
            }

            # Realizar solicitud a la API
            respuesta_detalle = requests.get(f'{ENDPOINT_OBTENER_DETALLE}/{identificador}', headers=cabeceras)

            # Obtener código de estado de la solicitud
            codigo_estado = respuesta_detalle.status_code

            # Intentar parsear la respuesta a JSON
            detalle = respuesta_detalle.json()

            return detalle, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener los datos del detalle de plazo: {error}")
            raise Exception("Ocurrió un error al obtener los datos del detalle de plazo")

    @staticmethod
    async def agregar_un_detalle(identificador: str, datos: dict, token: str) -> tuple:
        """
        Función que se encarga de enviar los datos para agregar un
        nuevo detalle
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            # Realizar solicitud a la API
            respuesta_detalle = requests.post(f'{ENDPOINT_AGREGAR_DETALLE}/{identificador}', json=datos, headers=cabeceras)

            # Obtener código de estado de la solicitud
            codigo_estado = respuesta_detalle.status_code

            # Intentar parsear la respuesta a JSON
            detalle = respuesta_detalle.json()

            return detalle, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al enviar los datos para agregar un detalle: {error}")
            raise Exception("Ocurrió un error al enviar los datos para agregar un detalle")

    @staticmethod
    async def actualizar_un_detalle(identificador: str, datos: dict, token: str) -> tuple:
        """
        Función que se encarga de enviar los datos actualizados de
        un detalle de pago
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            print(datos)

            if datos['cantidad_dada'] and datos['cantidad_anterior']:
                datos['cantidad_dada'] = float(datos['cantidad_dada']) + float(datos['cantidad_anterior'])
            else:
                datos['cantidad_dada'] = datos['cantidad_anterior']
            del datos['total_plazo']
            del datos['restante']
            del datos['restante_viejo']

            # Realizar solicitud a la API
            respuesta_detalle = requests.put(f'{ENDPOINT_ACTUALIZAR_DETALLE}/{identificador}', json=datos, headers=cabeceras)

            # Obtener código de estado de la solicitud
            codigo_estado = respuesta_detalle.status_code

            # Intentar parsear la respuesta a json
            detalle = respuesta_detalle.json()

            return detalle, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al enviar los datos del detalle actualizado: {error}")
            raise Exception(f"Ocurrió un error al enviar los datos del detalle actualizado")

    @staticmethod
    async def eliminar_un_detalle(identificador: str, token: str) -> tuple:
        """
        Función que se encarga de enviar los datos para eliminar
        un detalle en especifico
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}'
            }

            # Realizar solicitud a la API
            respuesta_detalle = requests.delete(f'{ENDPOINT_ELIMINAR_DETALLE}/{identificador}', headers=cabeceras)

            # Obtener código de estado de la solicitud
            codigo_estado = respuesta_detalle.status_code

            # Intentar parsear la respuesta a JSON
            detalle = respuesta_detalle.json()

            return detalle, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al enviar los datos para eliminar un detalle: {error}")
            raise Exception("Ocurrió un error al enviar los datos para eliminar un detalle")