"""
    Archivo que se encarga de administrar las operaciones
    realicionadas con el apartado de lotes
"""
import requests
from urllib.parse import urlencode, urljoin
from .utilidades import *
from typing import Optional

# Clase de las operaciones de la API
class LotesAPI():

    # Método para obtener todos los estados
    @staticmethod
    async def obtener_todos_estados(token: str) -> tuple:
        """
        Función que se encarga de obtener todos los estados
        """
        try:
            # Cabeceras de acceso:
            cabeceras = {
                'Authorization': f'Bearer {token}'
            }

            # Realizar solicitud a la API
            respuesta_estados = requests.get(ENDPOINT_ESTADOS, headers=cabeceras)

            # Obtener el código de estado de la respuesta
            codigo_estado = respuesta_estados.status_code

            # Intentar parsear la respuesta JSON
            estados = respuesta_estados.json()

            return estados, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al consultar todos los estados: {error}")
            raise Exception("Ocurrió un error al consultar todos los estados")

    # Método para obtener todos los municipios sin necesidad de su estado
    @staticmethod
    async def obtener_todos_municipios_sin_estado(token: str) -> tuple:
        """
        Función que se encarga de obtener todos los municipios
        sin necesidad de su estado
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}'
            }

            # Realizar solicitud a la API
            respuesta_municipios = requests.get(f"{ENDPOINT_BASE}/obtener_todos_municipios", headers=cabeceras)

            # Obtener el código de estado de la respuesta
            codigo_estado = respuesta_municipios.status_code

            # Intentar parsear la respuesta JSON
            municipios = respuesta_municipios.json()

            return municipios, codigo_estado
        except Exception as error:
            print(f"Ocurrió un erro al consultar todos los municipios sin estado: {error}")
            raise Exception(f"Ocurrió un erro al consultar todos los municipios sin estado.")

    # Método para obtener todos los municipios
    @staticmethod
    async def obtener_todos_municipios(identificador_estado: str, token: str) -> tuple:
        """
        Función que se encarga de obtener todos los municipios de
        un estado
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}'
            }

            # Realizar solicitud a la API
            respuesta_municipios = requests.get(f"{ENDPOINT_BASE}/{identificador_estado}/municipios", headers=cabeceras)

            # Obtener el código de estado de la respuesta
            codigo_estado = respuesta_municipios.status_code

            # Intentar parsear la respuesta JSON
            municipios = respuesta_municipios.json()

            return municipios, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al solicitar los municipios: {error}")
            raise Exception("Ocurrió un error al solicitar los municipios.")

    # Método para obtener todas las localidades sin necesidad de su municipio
    @staticmethod
    async def obtener_todas_localidades_sin_municipio(token: str) -> tuple:
        """
        Función que se encarga de obtener todas las localidades
        sin necesidad de su municipio
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}'
            }

            # Realizar solicitud a la API
            respuesta_localidades = requests.get(f"{ENDPOINT_BASE}/obtener_todas_localidades", headers=cabeceras)

            # Obtener el código de estado de la respuesta
            codigo_estado = respuesta_localidades.status_code

            # Intentar parsear la respuesta JSON
            localidades = respuesta_localidades.json()

            return localidades, codigo_estado
        except Exception as error:
            print(f"Ocurrió un erro al consultar todos las localidades sin municipio: {error}")
            raise Exception(f"Ocurrió un erro al consultar las localidades sin municipio.")

    # Método para obtener todas las localidades
    @staticmethod
    async def obtener_todas_localidades(identificador_municipio: str, token: str) -> tuple:
        """
        Función que se encarga de obtener todas las localidades de
        un municipio
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}'
            }

            # Realizar solicitud a la API
            respuesta_localidades = requests.get(f"{ENDPOINT_BASE}/{identificador_municipio}/localidades", headers=cabeceras)

            # Obtener el código de estado de la respuesta
            codigo_estado = respuesta_localidades.status_code

            # Intentar parsear la respuesta JSON
            localidades = respuesta_localidades.json()

            return localidades, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener todas las localides: {error}.")
            raise Exception("Ocurrió un error al obtener las localides.")

    # Método para obtener todas las localidades sin necesidad de su municipio
    @staticmethod
    async def obtener_todos_complejos_sin_localidad(token: str) -> tuple:
        """
        Función que se encarga de obtener todos los complejos
        sin necesidad de su localidad
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}'
            }

            # Realizar solicitud a la API
            respuesta_complejos = requests.get(f"{ENDPOINT_BASE}/obtener_todos_complejos", headers=cabeceras)

            # Obtener el código de estado de la respuesta
            codigo_estado = respuesta_complejos.status_code

            # Intentar parsear la respuesta JSON
            complejos = respuesta_complejos.json()

            return complejos, codigo_estado
        except Exception as error:
            print(f"Ocurrió un erro al consultar todos los complejos sin localidad: {error}")
            raise Exception(f"Ocurrió un erro al consultar los complejos sin localidad.")

    # Método para obtener todos los complejos
    @staticmethod
    async def obtener_todos_complejos(identificador_localidad: str, token: str, tipo_complejo: Optional[str] = None) -> tuple:
        """
        Función que se encarga de obtener todos los complejos residenciales
        de una localidad, se hace uso de un filtro por tipo de complejo
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}'
            }

            # Verificar que exista el filtro de tipo de complejo
            if tipo_complejo:
                URL_consulta = f"{ENDPOINT_BASE}/{identificador_localidad}/complejo_residencial/?tipo_complejo={tipo_complejo}"
            else:
                URL_consulta = f"{ENDPOINT_BASE}/{identificador_localidad}/complejo_residencial/"

            # Realizar solicitud a la API
            respuesta_complejos = requests.get(URL_consulta, headers=cabeceras)

            # Obtener el código de estado de la respuesta
            codigo_estado = respuesta_complejos.status_code

            # Intentar parsear la respuesta JSON
            complejos = respuesta_complejos.json()

            return complejos, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener los complejos residenciales: {error}.")
            raise Exception("Ocurrió un error al obtener todos los complejos residenciales")


    # Método para obtener las secciones para filtros
    @staticmethod
    async def obtener_secciones_filtro(identificador_complejo: str, token: str) -> tuple:
        """
        Función que se encarga de obtener las secciones de un complejo para utilizarlas
        como filtro de búsqueda
        """
        try:
            # Variable de respuesta
            secciones = None

            # Cabecera de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}'
            }

            # Realizar solicitud a la API
            respuesta_secciones = requests.get(f"{ENDPOINT_BASE}/{identificador_complejo}/secciones", headers=cabeceras)

            # Obtener el código de estado de la respuesta
            codigo_estado = respuesta_secciones.status_code

            # Intentar parsear la respuesta JSON
            secciones = respuesta_secciones.json()

            return secciones, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener las secciones: {error}.")
            raise Exception("Ocurrió un error al obtener las secciones")

    # Método para obtener todos los lotes
    @staticmethod
    async def obtener_todos_lotes(identificador_complejo: str, token: str, numero_seccion: Optional[int] = None,
                                  tamano: Optional[str] = None, estado_vendido: Optional[int] = None, pagina: int = 1,
                                  tamano_pagina: int = 10, nombre_lote: Optional[str] = None) -> tuple:
        """
        Función que se encarga de obtener todos los lotes de un complejo
        residencial en base a su nombre
        """
        try:
            # Cabecera de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}'
            }
            URL_consulta = f"{ENDPOINT_BASE}/{identificador_complejo}/lotes/"

            # Parámetros de consulta
            query_params = {'pagina': pagina, 'tamano': tamano_pagina}

            # Verificar que exista el filtro de tipo de sección
            if numero_seccion:
                query_params['numero_seccion'] = numero_seccion

            # Verificar que exista el filtro de tamaño
            if tamano:
                # Obtener el tamaño minimo y máximo
                min_tamano, max_tamano = map(int, tamano.split('-'))

                query_params['min_tamano'] = min_tamano
                query_params['max_tamano'] = max_tamano

            # Verificar que exista el filtro de estado
            if estado_vendido:
                query_params['estado_vendido'] = estado_vendido

            # Verificar que exista el filtro nombre lote
            if nombre_lote:
                query_params['nombre_lote'] = nombre_lote


            # Convertir los parametros a URL y añadirlos a la URL original
            query_string = urlencode(query_params)
            URL_consulta = urljoin(URL_consulta, f"?{query_string}")

            # Realizar solicitud a la API
            respuesta_lotes = requests.get(URL_consulta, headers=cabeceras)

            # Verificar el código de estado
            codigo_estado = respuesta_lotes.status_code

            # Intentar parsear la respuesta JSON
            datos = respuesta_lotes.json()

            # Verificar respuesta
            if respuesta_lotes and codigo_estado == 200:
                total = datos['Total de lotes']
                lotes = datos['Lotes']
            else:
                total, lotes = 0, datos

            return lotes, total, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener los complejos residenciales: {error}.")
            raise Exception("Ocurrrió un error al obtener todos los complejos.")

    # Método para obtener un lote en especifico
    @staticmethod
    async def obtener_lote_especifico(identificador_lote: int, token: str) -> tuple:
        """
        Función que se encarga de obtener la información de un lote
        en especifico
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}'
            }

            # Realizar solicitud a la API
            respuesta_lote = requests.get(f'{ENDPOINT_BASE}/{identificador_lote}/lote_especifico', headers=cabeceras)

            # Obtener código de estado
            codigo_estado = respuesta_lote.status_code

            # Intentar parserar a JSON la respuesta
            lote = respuesta_lote.json()

            return lote, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener la información del lote: {error}")
            raise Exception("Ocurrió un error al obtener la información del lote")

    # Método para obtener un lote con información extra
    @staticmethod
    async def obtener_lote_extra(identificador_lote: str, token: str) -> tuple:
        """
        Función que se encarga de obtener la información extra de un lote
        en especifico
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}'
            }

            # Realizar solicitud a la API
            respuesta_lote = requests.get(f"{ENDPOINT_OBTENER_LOTE}/{identificador_lote}", headers=cabeceras)

            # Obtener código de estado de la solicitud
            codigo_estado = respuesta_lote.status_code

            # Intentar parsear la respuesta a JSON
            lote = respuesta_lote.json()

            return lote, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al botener la información del lote: {error}")
            raise Exception("Ocurrió un error al botener la información del lote")

    # Método para obtener la ubicación de un lote
    @staticmethod
    async def obtener_ubicacion_lote(identificador_lote: str, token: str) -> tuple:
        """
        Función que se encarga de obtener la ubicación de un lote en
        específico
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}'
            }

            # Realizar solicitud a la API
            respuesta_ubicacion = requests.get(f"{ENDPOINT_OBTENER_UBICACION}/{identificador_lote}", headers=cabeceras)

            # Obtener código de estado de la solicitud
            codigo_estado = respuesta_ubicacion.status_code

            # Intentar parsear la respuesta a JSON
            ubicacion = respuesta_ubicacion.json()

            return ubicacion, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener la ubicación de un lote: {error}.")
            raise Exception("Ocurrió un error al obtener la ubicaciń de un lote")

    @staticmethod
    async def obtener_lote_venta(identificador: str, token: str) -> tuple:
        """
        Función que se encarga de obtener la información extra
        de un lote vendido
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}'
            }

            # Realizar la solicitud a la API
            respuesta_lote = requests.get(f'{ENDPOINT_OBTENER_LOTE_VENTA}/{identificador}', headers=cabeceras)

            # Obtener el código de estado de la solicitud
            codigo_estado = respuesta_lote.status_code

            # Intentar parsear la respuesta a JSON
            lote = respuesta_lote.json()

            return lote, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener la información extra del lote: {error}")
            raise Exception("Ocurrió un error al obtener la información extra del lote")

    # Función que se encarga de obtener un estado en especifico
    @staticmethod
    async def obtener_estado_especifico(identificador: str, token: str) -> tuple:
        """"
        Función que se encarga de obtener la información
        de un estado en especifico
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}'
            }

            # Realizar solicitud a la API
            respuesta_estado = requests.get(f'{ENDPOINT_OBTENER_ESTADO}/{identificador}', headers=cabeceras)

            # Obtener código de estado de la solicitud
            codigo_estado = respuesta_estado.status_code

            # Intentar parsear la respuesta a JSON
            estado = respuesta_estado.json()

            return estado, codigo_estado
        except Exception as error:
            print(f"Ocurrrió un error al obter un estado en especifico: {error}")
            raise Exception("Ocurrrió un error al obter un estado en especifico")

    # Función que se encarga de agregar un nuevo estaod
    @staticmethod
    async def agregar_nuevo_estado(estado: dict, token: str) -> tuple:
        """
        Función que se encarga de enviar los datos a la API
        para agregar un nuevo estado
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            # Realizar solicitud a la API
            respuesta_estado = requests.post(ENDPOINT_AGREGAR_ESTADO, json=estado, headers=cabeceras)

            # Obtener código de estado de la respuesta
            codigo_estado = respuesta_estado.status_code

            # Intentar parsear la respuesta a JSON
            estado = respuesta_estado.json()

            return estado, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al enviar los datos para agregar un nuevo estado: {error}")
            raise Exception("Ocurrió un error al enviar los datos para agregar un nuevo estado.")

    # Función que se encarga de obtener un municipio en especifico
    @staticmethod
    async def obtener_municipio_especifico(identificador: str, token: str) -> tuple:
        """"
        Función que se encarga de obtener la información
        de un municipio en especifico
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}'
            }

            # Realizar solicitud a la API
            respuesta_municipio = requests.get(f'{ENDPOINT_OBTENER_MUNICIPIO}/{identificador}', headers=cabeceras)

            # Obtener código de municipio de la solicitud
            codigo_municipio = respuesta_municipio.status_code

            # Intentar parsear la respuesta a JSON
            municipio = respuesta_municipio.json()

            return municipio, codigo_municipio
        except Exception as error:
            print(f"Ocurrrió un error al obter un municipio en especifico: {error}")
            raise Exception("Ocurrrió un error al obter un municipio en especifico")

    @staticmethod
    async def agregar_nuevo_municipio(municipio: dict, token: str) -> tuple:
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            # Realizar solicitud a la API
            respuesta_municipio = requests.post(ENDPOINT_AGREGAR_MUNICIPIO, json=municipio, headers=cabeceras)

            # Obtener código de estado de la respuesta
            codigo_estado = respuesta_municipio.status_code

            # Intentar parsear la respuesta JSON
            municipio = respuesta_municipio.json()

            return municipio, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al enviar los datos para agregar un nuevo municipio: {error}")
            raise Exception("Ocurrió un error al enviar los datos para agregar un nuevo municipio.")

    # Función que se encarga de obtener una localidad en especifico
    @staticmethod
    async def obtener_localidad_especifica(identificador: str, token: str) -> tuple:
        """"
        Función que se encarga de obtener la información
        de una localidad en especifico
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}'
            }

            # Realizar solicitud a la API
            respuesta_localidad = requests.get(f'{ENDPOINT_OBTENER_LOCALIDAD}/{identificador}', headers=cabeceras)

            # Obtener código de localidad de la solicitud
            codigo_localidad = respuesta_localidad.status_code

            # Intentar parsear la respuesta a JSON
            localidad = respuesta_localidad.json()

            return localidad, codigo_localidad
        except Exception as error:
            print(f"Ocurrrió un error al obter una localidad en especifico: {error}")
            raise Exception("Ocurrrió un error al obtener una localidad en especifica")

    @staticmethod
    async def agregar_nueva_localidad(localidad: dict, token: str) -> tuple:
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            # Realizar solicitud a la API
            respuesta_localidad = requests.post(ENDPOINT_AGREGAR_LOCALIDAD, json=localidad, headers=cabeceras)

            # Obtener código de estado de la respuesta
            codigo_estado = respuesta_localidad.status_code

            # Intentar parsear la respuesta a JSON
            localidad = respuesta_localidad.json()

            return localidad, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al enviar los datos para agregar una nueva localidad: {error}")
            raise Exception("Ocurrió un error al enviar los datos para agregar una nueva localidad.")

    # Función que se encarga de obtener una complejo en especifico
    @staticmethod
    async def obtener_complejo_especifico(identificador: str, token: str) -> tuple:
        """"
        Función que se encarga de obtener la información
        de un complejo en especifico
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}'
            }

            # Realizar solicitud a la API
            respuesta_complejo = requests.get(f'{ENDPOINT_OBTENER_COMPLEJO}/{identificador}', headers=cabeceras)

            # Obtener código de complejo de la solicitud
            codigo_complejo = respuesta_complejo.status_code

            # Intentar parsear la respuesta a JSON
            complejo = respuesta_complejo.json()

            return complejo, codigo_complejo
        except Exception as error:
            print(f"Ocurrrió un error al obter un complejo en especifico: {error}")
            raise Exception("Ocurrrió un error al obtener un complejo en especifica")

    @staticmethod
    async def agregar_nuevo_complejo(complejo: dict, token: str) -> tuple:
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            # Realizr solicitud a la API
            respuesta_complejo = requests.post(ENDPOINT_AGREGAR_COMPLEJO, json=complejo, headers=cabeceras)

            # Obtener código de estado de la respuesta
            codigo_estado = respuesta_complejo.status_code

            # Intentar parsear la respuesta a JSON
            complejo = respuesta_complejo.json()

            return complejo, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al enviar los datos para agregar un nuevo complejo: {error}")
            raise Exception("Ocurrió un error al enviar los datos para agregar un nuevo complejo.")

    @staticmethod
    async def agregar_nueva_seccion(seccion: dict, token: str) -> tuple:
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            # Realizar solicitud a la API
            respuesta_seccion = requests.post(ENDPOINT_AGREGAR_SECCION, json=seccion, headers=cabeceras)

            # Obtener código de estado de la API
            codigo_estado = respuesta_seccion.status_code

            # Intentar parsear la respuesta a JSON
            seccion = respuesta_seccion.json()

            return seccion, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al enviar los datos para agregar una nuevo seccion: {error}")
            raise Exception("Ocurrió un error al enviar los datos para agregar una nueva seccion.")

    @staticmethod
    async def agregar_nuevo_lote(lote: dict, token: str) -> tuple:
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            # Realizar solicitud a la API
            respuesta_lote = requests.post(ENDPOINT_AGREGAR_LOTE, json=lote, headers=cabeceras)

            # Obtener código de estado de la respuesta
            codigo_estado = respuesta_lote.status_code

            # Intentar parsear la respuesta a JSON
            lote = respuesta_lote.json()

            return lote, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al enviar los datos para agregar un nuevo lote: {error}")
            raise Exception("Ocurrió un error al enviar los datos para agregar un nuevo lote.")

    @staticmethod
    async def actualizar_un_lote(lote_actualizar: dict, identificador_lote: str, token: str) -> tuple:
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            # Realizar solicitud a la API
            respuesta_lote = requests.put(f"{ENDPOINT_ACTUALIZAR_LOTE}/{identificador_lote}", json=lote_actualizar, headers=cabeceras)

            # Obtener código de estado de la respuesta
            codigo_estado = respuesta_lote.status_code

            # Intentar parsear la resupueta a JSON
            lote = respuesta_lote.json()

            return lote, codigo_estado
        except Exception:
            raise Exception("Ocurrió un error al enviar los datos para actualizar un lote")

    @staticmethod
    async def eliminar_un_lote(identificador_lote: str, token: str) -> tuple:
        """
        Función que se encarga de enviar el identificador
        de un lote para ser eliminado
        """
        try:
            # Cabeceras de acceso
            cabeceras ={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            # Realizar la solicitud a la API
            respuesta_lote = requests.delete(f"{ENDPOINT_ELIMINAR_LOTE}/{identificador_lote}", headers=cabeceras)

            # Obtener el código de estado de la solicitud
            codigo_estado = respuesta_lote.status_code

            # Intentar parsear la respuesta a JSON
            lote = respuesta_lote.json()

            return lote, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al enviar los datos para eliminar un lote: {error}")
            raise Exception("Ocurrió un error al enviar los datos para eliminar un lote")

    # Método para actualizar una sección
    @staticmethod
    async def actualizar_una_seccion(seccion: dict, identificador_seccion: str, token: str) -> tuple:
        """
        Función que se encarga de enviar los datos actualizados
        de una sección
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            # Realizar solicitud a la API
            respuesta_seccion = requests.put(f"{ENDPOINT_ACTUALIZAR_SECCION}/{identificador_seccion}", json=seccion, headers=cabeceras)

            # Obtener código de estado de la solicitud
            codigo_estado = respuesta_seccion.status_code

            # Parsear la respuesta a JSON
            seccion = respuesta_seccion.json()

            return seccion, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al enviar los datos para actualizar la sección: {error}")
            raise Exception("Ocurrió un error al enviar los datos para actualizar la sección")


    # Método para eliminar una sección
    @staticmethod
    async def eliminar_una_seccion(identificador_seccion: str, token: str) -> tuple:
        """
        Función que se encarga de enviar el identificador a la API
        para eliminar una sección
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            # Realizar solicitud a la API
            respuesta_seccion = requests.delete(f"{ENDPOINT_ELIMINAR_SECCOIN}/{identificador_seccion}", headers=cabeceras)

            # Obtener código de estado de la solicitud
            codigo_estado = respuesta_seccion.status_code

            # Intentar parsear la respuesta a JSON
            seccion = respuesta_seccion.json

            return seccion, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al enviar los datos para eliminar una sección: {error}")
            raise Exception("Ocurrió un error al enviar los datos para eliminar una sección")


    # Método para actualizar un complejo
    @staticmethod
    async def actualizar_un_complejo(complejo: dict, identificador_complejo: str, token: str) -> tuple:
        """
        Función que se encarga de enviar los datos actualizados
        de un complejo
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            # Realizar solicitud a la API
            respuesta_complejo = requests.put(f"{ENDPOINT_ACTUALIZAR_COMPLEJO}/{identificador_complejo}", json=complejo, headers=cabeceras)

            # Obtener código de la respuesta
            codigo_estado = respuesta_complejo.status_code

            # Intentar parsear la respuesta a JSON
            complejo = respuesta_complejo.json()

            return complejo, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al enviar los datos actualizados del complejo: {error}")
            raise Exception("Ocurrió un error al enviar los datos actualizados del complejo")


    # Método para eliminar un complejo
    @staticmethod
    async def eliminar_un_complejo(identificador_complejo: str, token: str) -> tuple:
        """
        Función que se encarga de enviar los datos para
        eliminar un complejo
        """
        try:
            cabeceras = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            # Realizar solicitud a la API
            respuesta_complejo = requests.delete(f"{ENDPOINT_ELIMINAR_COMPLEJO}/{identificador_complejo}", headers=cabeceras)

            # Obtener código de estado de la respuesta
            codigo_estado = respuesta_complejo.status_code

            # Intentar parsear la respuesta a JSON
            complejo = respuesta_complejo.json()

            return complejo, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al enviar los datos para eliminar un complejo: {error}")
            raise Exception("Ocurrió un error al enviar los datos para eliminar un complejo")


    # Método para actualizar una localidad
    @staticmethod
    async def actualizar_una_localidad(localidad: dict, identificador_localidad: str, token: str) -> tuple:
        """
        Función que se encarga de enviar los datos actualizados
        de una localidad
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            # Realizar solicitud a la API
            respuesta_localidad = requests.put(f"{ENDPOINT_ACTUALIZAR_LOCALIDAD}/{identificador_localidad}", json=localidad, headers=cabeceras)

            # Obtener código de estado de la solicitud
            codigo_estado = respuesta_localidad.status_code

            # Intentar parsear la respuesta a JSON
            localidad = respuesta_localidad.json()

            return localidad, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al enviar los datos para actualizaruna localidad: {error}")
            raise Exception("Ocurrió un error al enviar los datos para actualizaruna localidad")

    # Método para eliminar una localidad
    @staticmethod
    async def eliminar_una_localidad(identificador_localidad: str, token: str) -> tuple:
        """
        Función que se encarga de enviar los datos para eliminar
        una localidad
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            # Realizar solicitud a la API
            respuesta_localidad = requests.delete(f"{ENDPOINT_ELIMINAR_LOCALIDAD}/{identificador_localidad}", headers=cabeceras)

            # Obtener código de estado de la respuesta
            codigo_estado = respuesta_localidad.status_code

            # Intentar parsear la respuesta a JSON
            localidad = respuesta_localidad.json()

            return localidad, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al enviar los datos para eliminar una localidad: {error}")
            raise Exception("Ocurrió un error al enviar los datos para eliminar una localidad")

    # Método para actualizar un municipio
    @staticmethod
    async def actualizar_un_municipio(municipio: dict, identificador_municipio: str, token: str) -> tuple:
        """
        Función que se encarga de enviar los datos actualizados
        de una municipio
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            # Realizar solicitud a la API
            respuesta_municipio = requests.put(f"{ENDPOINT_ACTUALIZAR_MUNICIPIO}/{identificador_municipio}", json=municipio, headers=cabeceras)

            # Obtener código de estado de la solicitud
            codigo_estado = respuesta_municipio.status_code

            # Intentar parsear la respuesta a JSON
            municipio = respuesta_municipio.json()

            return municipio, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al enviar los datos para actualizaruna municipio: {error}")
            raise Exception("Ocurrió un error al enviar los datos para actualizaruna municipio")

    # Método para eliminar un municipio
    @staticmethod
    async def eliminar_un_municipio(identificador_municipio: str, token: str) -> tuple:
        """
        Función que se encarga de enviar los datos para eliminar
        una municipio
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            # Realizar solicitud a la API
            respuesta_municipio = requests.delete(f"{ENDPOINT_ELIMINAR_MUNICIPIO}/{identificador_municipio}", headers=cabeceras)

            # Obtener código de estado de la respuesta
            codigo_estado = respuesta_municipio.status_code

            # Intentar parsear la respuesta a JSON
            municipio = respuesta_municipio.json()

            return municipio, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al enviar los datos para eliminar una municipio: {error}")
            raise Exception("Ocurrió un error al enviar los datos para eliminar una municipio")


    # Método para actualizar un estado:
    @staticmethod
    async def actualizar_un_estado(estado: dict, identificador_estado: str, token: str) -> tuple:
        """
        Función que se encarga de enviar los datos actualizados
        de una estado
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            # Realizar solicitud a la API
            respuesta_estado = requests.put(f"{ENDPOINT_ACTUALIZAR_ESTADO}/{identificador_estado}", json=estado, headers=cabeceras)

            # Obtener código de estado de la solicitud
            codigo_estado = respuesta_estado.status_code

            # Intentar parsear la respuesta a JSON
            estado = respuesta_estado.json()

            return estado, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al enviar los datos para actualizaruna estado: {error}")
            raise Exception("Ocurrió un error al enviar los datos para actualizaruna estado")

    # Método para eliminar un estado:
    @staticmethod
    async def eliminar_un_estado(identificador_estado: str, token: str) -> tuple:
        """
        Función que se encarga de enviar los datos para eliminar
        una estado
        """
        try:
            # Cabeceras de acceso
            cabeceras = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            # Realizar solicitud a la API
            respuesta_estado = requests.delete(f"{ENDPOINT_ELIMINAR_ESTADO}/{identificador_estado}", headers=cabeceras)

            # Obtener código de estado de la respuesta
            codigo_estado = respuesta_estado.status_code

            # Intentar parsear la respuesta a JSON
            estado = respuesta_estado.json()

            return estado, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al enviar los datos para eliminar una estado: {error}")
            raise Exception("Ocurrió un error al enviar los datos para eliminar una estado")
