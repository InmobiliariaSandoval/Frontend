"""
    Archivo que administra los métodos de las operaciones
    relacionadas con las ventas
"""
# Importamos el módelo de estados así como el de servicio
from ..models.models_ventas import VentasMostrar, Ventas
from ..models.models_ventas import Plazos, DetallesPlazo
from ..services.ventas_services import VentasAPI

# Crear objeto de VentasAPI
VENTAS = VentasAPI()

# Clase con las operaciones referentes a las ventas
class VentasController():

    @staticmethod
    async def obtener_todas_ventas(token_acceso: str, filtro_busqueda: str = None, numero_pagina: int = 1, tamano_pagina: int = 10) -> tuple:
        """
        Función que se encarga de obtener y mapear
        todas las ventas
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Obtener las ventas
            ventas, total, codigo_estado = await VENTAS.obtener_todas_ventas(token=token_acceso,filtro=filtro_busqueda, pagina=numero_pagina, tamano=tamano_pagina)

            # Verificar el valor de la respuesta
            if ventas and codigo_estado == 200:

                # Iterar por cada elemento de la lista
                # mapear cada valor en base al módelo
                for venta in ventas:
                    respuesta.append(VentasMostrar(**venta))
            elif ventas and codigo_estado != 200:
                respuesta.append(ventas)
            else:
                respuesta = ventas

            return respuesta, total, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al mapear las ventas: {error}.")
            raise Exception("Ocurrió un error al mapear las ventas.")

    @staticmethod
    async def agregar_venta_lote(venta_enviar: dict, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener los datos de la venta y enviarlos
        a la función que maneja la comunicación con la API
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para enviar los datos a la API
            venta, codigo_estado = await VENTAS.agregar_nueva_venta(datos=venta_enviar, token=token_acceso)

            # Verificar el valor
            if venta:
                respuesta.append(venta)
            else:
                respuesta = venta

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener y enviar los valores de la venta: {error}")
            raise Exception("Ocurrió un error al obtener y enviar los valores de la venta")

    # Función que se encarga de obtener y mapear la compra
    @staticmethod
    async def obtener_compra_especifica(identificador_compra: str, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener y mapear los datos de una
        compra en especifico
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función que realiza la solicitud a la API
            compra, codigo_estado = await VENTAS.obtener_compra_especifica(identificador_compra, token_acceso)

            # Verificar el valor del compra y su código de estado
            if compra and codigo_estado == 200:

                # Iterar por cada elemento de la lista
                # mapear el valor en base al módelo
                for valor in compra:
                    respuesta.append(Ventas(**valor))
            else:
                respuesta.append(compra)

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al mapear la información de la compra: {error}")
            raise Exception("Ocurrió un error al mapear la información de la compra")

    # Función que se encarga de obtener y mapear los plazos
    @staticmethod
    async def obtener_plazos_compra(identificador_compra: str, token_acceso: int, pagina: int = 1, tamano: int = 10) -> tuple:
        """
        Función que se encarga de obtener y mapear los datos
        de todos los plazos
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función que obtiene los datos de la API
            plazos, total, codigo_estado = await VENTAS. \
                obtener_plazos_compra(identificador_compra=identificador_compra, token=token_acceso, pagina=pagina, tamano=tamano)

            # Verificar el valor de la respuesta
            if plazos and codigo_estado == 200:

                # Iterar en cada elemento de la lista
                # mapear el valor en base al módelo
                for plazo in plazos:
                    respuesta.append(Plazos(**plazo))
            elif plazos and codigo_estado != 200:
                respuesta.append(plazos)
            else:
                respuesta = plazos

            return plazos, total, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al mapear todos los plazos de una compra: {error}")
            raise Exception("Ocurrió un error al mapear todos los plazos de una compra")

    # Función que obtiene los valores para agregar un nuevo plazo
    @staticmethod
    async def agregar_nuevo_plazo(datos_plazo: dict, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener los valores para agregar
        un nuevo plazo
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para enviar los datos a la API
            plazo, codigo_estado = await VENTAS.agregar_nuevo_plazo(datos=datos_plazo, token=token_acceso)

            # Verificar el valore de la respuesta
            if plazo:
                respuesta.append(plazo)
            else:
                respuesta = plazo

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener y enviar los datos de un nuevo plazo: {error}")
            raise Exception("Ocurrió un error al obtener y enviar los datos de un nuevo plazo")

    # Función que se encarga de eliminar un plazo
    @staticmethod
    async def eliminar_un_plazo(identificador_plazo: str, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener y enviar la información para eliminar
        un plazo
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a al función para enviar los datos a la API
            respuesta_plazo, codigo_estado = await VENTAS.\
                eliminar_un_plazo(identificador_plazo=identificador_plazo, token=token_acceso)

            # Verificar respuesta
            if respuesta_plazo:
                respuesta.append(respuesta_plazo)
            else:
                respuesta = respuesta_plazo

            return respuesta,codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener la información para eliminar un plazo: {error}")
            raise Exception("Ocurrió un error al obtener la información para eliminar un plazo")


    # Función que se encarga de actualizar un plazo
    @staticmethod
    async def actualizar_un_plazo(identificador_plazo: int, plazo_actualizado: dict, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener los datos del plazo
        actualizado para enviarlos a la API
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función que envia los datos a la API
            plazo, codigo_estado = await VENTAS. \
                editar_un_plazo(identificador=identificador_plazo, datos=plazo_actualizado, token=token_acceso)

            # Verificar la respuesta
            if plazo:
                respuesta.append(plazo)
            else:
                respuesta = plazo

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener y enviar los datos actualizados del plazo: {error}")
            raise Exception("Ocurrió un error al obtener y enviar los datos actualizados del plazo")

    # Función que se encarga de obtener y enviar los datos para cambiar el estado de una venta
    @staticmethod
    async def cambiar_estado_una_compra(identificador_venta: str, estado_venta: str, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener y enviar los datos para cambiar el estado
        de una venta
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función que envia los datos a la API
            venta, codigo_estado = await VENTAS. \
                cambiar_estado_una_compra(identificador=identificador_venta, estado=estado_venta, token=token_acceso)

            # Verificar respuesta de la API
            if venta:
                respuesta.append(venta)
            else:
                respuesta = venta

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener los datos para cambiar el estado de una venta: {error}")
            raise Exception("Ocurrió un error al obtener los datos para cambiar el estado de una venta")

    # Función que se encarga de obtener y mapear los datos de un detalle
    @staticmethod
    async def obtener_un_detalle(identificador_plazo: str, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener un detalle y mapear sus datos a la
        estructura pedida
        """
        try:
            # Variablde de respuesta
            respuesta = []

            # Llamar a la función que realiza la solicitud a la API
            detalle, codigo_estado = await VENTAS. \
                obtener_un_detalle(identificador=identificador_plazo, token=token_acceso)

            # Verificar el valor del detalle y su código de estado
            if detalle and codigo_estado == 200:

                # Iterar por cada elemento de la lista
                # mapear el valor en base al módelo
                for valor in detalle:
                    respuesta.append(DetallesPlazo(**valor))
            else:
                respuesta.append(detalle)

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al mapear los datos del detalle de plazo: {error}")
            raise Exception("Ocurrió un error al mapear los datos del detalle de plazo")

    @staticmethod
    async def agregar_un_detalle(identificador_plazo: str, detalle_enviar: dict, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener los datos del detalle de plazo y enviarlos
        a la función que maneja la comunicación con la API
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para enviar los datos a la API
            detalle, codigo_estado = await VENTAS. \
                agregar_un_detalle(identificador=identificador_plazo, datos=detalle_enviar, token=token_acceso)

            # Verificar el valor
            if detalle:
                respuesta.append(detalle)
            else:
                respuesta = detalle

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener y enviar los valores de la detalle: {error}")
            raise Exception("Ocurrió un error al obtener y enviar los valores de la detalle")

    # Función que se encarga de eliminar un plazo
    @staticmethod
    async def eliminar_un_detalle(identificador_detalle: str, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener y enviar la información para eliminar
        un detalle de plazo
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a al función para enviar los datos a la API
            detalle, codigo_estado = await VENTAS.\
                eliminar_un_detalle(identificador=identificador_detalle, token=token_acceso)

            # Verificar respuesta
            if detalle:
                respuesta.append(detalle)
            else:
                respuesta = detalle

            return respuesta,codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener la información para eliminar un detalle de plazo: {error}")
            raise Exception("Ocurrió un error al obtener la información para eliminar un detalle de plazo")

    @staticmethod
    async def actualizar_un_detalle(identificador_plazo: int, detalle_actualizado: dict, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener los datos del detalle de plazo
        actualizado para enviarlos a la API
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función que envia los datos a la API
            detalle, codigo_estado = await VENTAS. \
                actualizar_un_detalle(identificador=identificador_plazo, datos=detalle_actualizado, token=token_acceso)

            # Verificar la respuesta
            if detalle:
                respuesta.append(detalle)
            else:
                respuesta = detalle

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener y enviar los datos actualizados del detalle: {error}")
            raise Exception("Ocurrió un error al obtener y enviar los datos actualizados del detalle")