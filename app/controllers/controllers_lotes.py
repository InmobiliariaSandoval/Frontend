"""
    Archivo que administra los métodos de las operaciones
    relacionadas con los lotes
"""
# Importamos el módelo de estados así como el de servicio
from ..models.models_lotes import EstadosBase, MunicipiosBase, LocalidadesBase, \
    ComplejosResidencialesBase, LotesBase, LotesUnico, SeccionesFiltro, UbicacionLote, \
    LoteSeccionExtendido, VentaLotes
from ..services.lotes_services import LotesAPI
from typing import Optional

# Crear objeto de LotesAPI
LOTES = LotesAPI()

# Clase con las operaciones referentes al apartado de lotes
class LotesController():

    @staticmethod
    async def obtener_todos_estados(token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener y mapear todos lo estados
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para obtener todos los estados
            estados, codigo_estado = await LOTES.obtener_todos_estados(token=token_acceso)

            # Verificar el valor de estados
            if estados and codigo_estado == 200:

                # Iterar en cada elemento de la lista
                # mapear el valor en base al modelo
                for estado in estados:
                    respuesta.append(EstadosBase(**estado))
            else:
                respuesta.append(estados)

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al pasear los estados: {error}")
            raise Exception("Ocurrió un error al parsear los estados.")

    @staticmethod
    async def obtener_todos_municipios_sin_estado(token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener y mapear todos los estados
        sin necesidad del identificador del estado
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para obtener todos los municipios
            municipios, codigo_estado = await LOTES.obtener_todos_municipios_sin_estado(token=token_acceso)

            # Verificar municipio
            if municipios and codigo_estado == 200:

                # Iterar en cada elemento de la lista
                # mapear el valor en base al módelo
                for municipio in municipios:
                    respuesta.append(MunicipiosBase(**municipio))
            else:
                respuesta.append(municipios)

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener todos os municipios sin contar el estado: {error}")
            raise Exception("Ocurrió un error al obtener todos os municipios sin contar el estado.")

    @staticmethod
    async def obtener_todos_municipios(identificador_estado: str, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener y mapear todos los municipios en base
        a su estado
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para obtener todos los muncipios
            municipios, codigo_estado = await LOTES.obtener_todos_municipios(identificador_estado=identificador_estado, token=token_acceso)

            # Verificar el valor de municipios:
            if municipios and codigo_estado == 200:

                # Iterar en cada elemento de la lista
                # mapear el valor en base al módelo
                for municipio in municipios:
                    respuesta.append(MunicipiosBase(**municipio))
            else:
                respuesta.append(municipios)

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al parsear los municipios: {error}.")
            raise Exception("Ocurrió un error al parsear los municipios.")

    @staticmethod
    async def obtener_todas_localidades_sin_municipio(token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener y mapear todos las localidades
        sin necesidad del identificador del municipio
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para obtener todos los municipios
            localidades, codigo_estado = await LOTES.obtener_todas_localidades_sin_municipio(token=token_acceso)

            # Verificar municipio
            if localidades and codigo_estado == 200:

                # Iterar en cada elemento de la lista
                # mapear el valor en base al módelo
                for localidad in localidades:
                    respuesta.append(LocalidadesBase(**localidad))
            else:
                respuesta.append(localidades)

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener todos las localidades sin contar el municipio: {error}")
            raise Exception("Ocurrió un error al obtener todos las localidades sin contar el municipio.")

    @staticmethod
    async def obtener_todas_localidades(identificador_municipio: str, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener y mapear todos los municipios
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para obtener todas las localidades
            localidades, codigo_estado = await LOTES.obtener_todas_localidades(identificador_municipio=identificador_municipio, token=token_acceso)

            # Veificar el valor de localidades
            if localidades and codigo_estado == 200:

                # Iterar en cada elemento de la lista
                # mapear el valor en base al módelo
                for localidad in localidades:
                    respuesta.append(LocalidadesBase(**localidad))
            else:
                respuesta.append(localidades)

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al mapear las localiddes: {error}.")
            raise Exception("Ocurrió un error al mapear las localides.")

    @staticmethod
    async def obtener_todos_complejos_sin_localidad(token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener y mapear todos los complejos
        sin necesidad del identificador de su localidad
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para obtener todos los municipios
            complejos, codigo_estado = await LOTES.obtener_todos_complejos_sin_localidad(token=token_acceso)

            # Verificar municipio
            if complejos and codigo_estado == 200:

                # Iterar en cada elemento de la lista
                # mapear el valor en base al módelo
                for complejo in complejos:
                    respuesta.append(ComplejosResidencialesBase(**complejo))
            else:
                respuesta.append(complejos)

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener todos las localidades sin contar el municipio: {error}")
            raise Exception("Ocurrió un error al obtener todos las localidades sin contar el municipio.")

    @staticmethod
    async def obtener_todos_complejos(identificador_localidad: str, token_acceso: str, tipo_complejo: Optional[str] = None) -> tuple:
        """
        Función que se encarga de obtener y mapear todos los complejos
        residenciales de una localidad
        """
        try:
            # Variabe de respuesta
            respuesta = []

            # Llamar a la función para obtener todos los complejos
            complejos, codigo_estado = await LOTES. \
                obtener_todos_complejos(identificador_localidad=identificador_localidad, token=token_acceso, tipo_complejo=tipo_complejo)

            # Verificar el valor de complejos
            if complejos and codigo_estado == 200:

                # Iterar en cada elemento de la lista
                # mapear el valor en base al módelo
                for complejo in complejos:
                    respuesta.append(ComplejosResidencialesBase(**complejo))
            else:
                respuesta.append(complejos)

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al mapear los complejos: {error}")
            raise Exception("Ocurrió un error  al mapear todos los complejos.")

    @staticmethod
    async def obtener_secciones_filtro(identificador_complejo: str, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener y mapear todas las secciones
        para el filtro de lotes
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para obtener todas las secciones para filtro
            secciones, codigo_estado = await LOTES.obtener_secciones_filtro(identificador_complejo=identificador_complejo, token=token_acceso)

            # Verificar el valor de las seccoines
            if secciones and codigo_estado == 200:

                # Iterar en cada elemento de la lista
                # mapear el valor en base al módelo
                for seccion in secciones:
                    respuesta.append(SeccionesFiltro(**seccion))
            else:
                respuesta.append(secciones)

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un erro al mapear las secciones: {error}")
            raise Exception("Ocurrió un error al mapear las secciones.")

    @staticmethod
    async def obtener_todos_lotes(identificador_complejo: str, token_acceso: str, numero_seccion: Optional[int] = None, tamano: Optional[str] = None,
                                  estado_vendido: Optional[str] = None, pagina: int = 1, tamano_pagina: int = 10, nombre_lote: Optional[str] = None) -> tuple:
        """
        Función que se encarga de obtener y mapear todos los lotes de un
        complejo residencial
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para obtener todos los lotes
            lotes, total, codigo_estado = await LOTES.obtener_todos_lotes(
                identificador_complejo=identificador_complejo,
                token=token_acceso, numero_seccion=numero_seccion,
                tamano=tamano, estado_vendido=estado_vendido, pagina=pagina, tamano_pagina=tamano_pagina,
                nombre_lote=nombre_lote)

            # Verificar el valor de los lotes
            if lotes and codigo_estado == 200:

                # Iterar por cada elemento de la lista
                # mapear el valor en base al modelo
                for lote in lotes:
                    respuesta.append(LotesBase(**lote))
            elif lotes and codigo_estado != 200:
                respuesta.append(lotes)
            else:
                respuesta = lotes

            return respuesta, total, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al intentar mapear los lotes: {error}.")
            raise Exception("Ocurrió un error al intentar mapear todos los lotes")

    @staticmethod
    async def obtener_lote_especifico(identificador_lote: int, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener y mapear la información referente a un lote
        en especifico
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la funcion para obtener el lote en especifico
            lote, codigo_estado = await LOTES.obtener_lote_especifico(identificador_lote=identificador_lote, token=token_acceso)

            # Verificar el valor del lote y su código de estado
            if lote and codigo_estado == 200:

                # Iterar por cada elemento de la lista
                # mapear el valor en base al módelo
                for valor in lote:
                    respuesta.append(LotesUnico(**valor))
            else:
                respuesta.append(lote)

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al intentar mapear el lote: {error}.")
            raise Exception("Ocurrió un error al intentar mapear el lote")

    @staticmethod
    async def obtener_lote_extra(identificador_lote: str, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener y mapear la informaión referente a un lote
        en especifico
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para obtener el lote
            lote, codigo_estado = await LOTES.obtener_lote_extra(identificador_lote=identificador_lote, token=token_acceso)

            # Verificar el valor de la respuesta
            if lote and codigo_estado == 200:

                # Iterar por ada elemento de la lista
                # mapera el valor en base al modelo
                for valor in lote:
                    respuesta.append(LoteSeccionExtendido(**valor))
            else:
                respuesta.append(lote)

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al intentar mapera el lote con información extra: {error}")
            raise Exception("Ocurrió un error al intentar mapera el lote con información extra")

    @staticmethod
    async def obtener_ubicacon_lote(identificador_lote: str, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtenener y mapear la ubicacion de un
        lote en especifico
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para obtener la ubicación de un lote
            ubicacion, codigo_estado = await LOTES.obtener_ubicacion_lote(identificador_lote=identificador_lote, token=token_acceso)

            # Verificar el valor del lote y su código de estado
            if ubicacion and codigo_estado == 200:

                # Iterar por cada elemento de la lista
                # mapear el valor en base al módelo
                respuesta.append(UbicacionLote(**ubicacion))
            else:
                respuesta.append(ubicacion)

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al mapear la ubicación de un lote: {error}")
            raise Exception("Ocurrió un error al mapear la ubicación de un lote")

    @staticmethod
    async def obtener_lote_venta(identificador_lote: str, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener y mapear la información extra
        de un lote vendido
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para obtener la información
            lote, codigo_estado = await LOTES. \
                obtener_lote_venta(identificador=identificador_lote, token=token_acceso)

            if lote and codigo_estado == 200:

                # Iterar por cada elemento de la lista
                # mapear el valor en base al módelo
                respuesta.append(VentaLotes(**lote))
            else:
                respuesta.append(lote)

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al mapear la información del lote vendido: {error}")
            raise Exception("Ocurrió un error al mapear la información del lote vendido")

    @staticmethod
    async def obtener_estado_especifico(identificador_estado: str, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener y mapear la información
        de un estado en especifico
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para obtener la información del estado
            respuesta_estado, codigo_estado = await LOTES.obtener_estado_especifico(identificador_estado, token_acceso)

            # Verificar el valor de la respuesta
            if respuesta_estado and codigo_estado == 200:

                # Iterar por vada valor de la lista
                # mapear el valo en base al módelo
                for dato in respuesta_estado:
                    respuesta.append(EstadosBase(**dato))
            elif respuesta_estado and codigo_estado != 200:
                respuesta.append(respuesta_estado)
            else:
                respuesta = respuesta_estado

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al mapear los datos del estado: {error}")
            raise Exception("Ocurrió un error al mapear los datos del estado")

    @staticmethod
    async def agregar_estado(estado_agregar: dict, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener los datos del estado y enviarlos a la
        función que maneja la comunicación con la API
        """
        try:
            # Varible de respuesta
            respuesta = []

            # Llamar a la función para enviar los datos a la API
            estado, codigo_estado = await LOTES.agregar_nuevo_estado(estado=estado_agregar, token=token_acceso)

            # Verificar el valor
            if estado:
                respuesta.append(estado)
            else:
                respuesta = estado

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener y enviar los valores de estado: {error}")
            raise Exception("Ocurrió un error al obtener y enviar los valores de estado.")

    @staticmethod
    async def obtener_municipio_especifico(identificador_municipio: str, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener y mapear la información
        de un municipio en especifico
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para obtener la información del municipio
            respuesta_municipio, codigo_municipio = await LOTES.obtener_municipio_especifico(identificador_municipio, token_acceso)

            # Verificar el valor de la respuesta
            if respuesta_municipio and codigo_municipio == 200:

                # Iterar por vada valor de la lista
                # mapear el valo en base al módelo
                for dato in respuesta_municipio:
                    respuesta.append(MunicipiosBase(**dato))
            elif respuesta_municipio and codigo_municipio != 200:
                respuesta.append(respuesta_municipio)
            else:
                respuesta = respuesta_municipio

            return respuesta, codigo_municipio
        except Exception as error:
            print(f"Ocurrió un error al mapear los datos del municipio: {error}")
            raise Exception("Ocurrió un error al mapear los datos del municipio")

    @staticmethod
    async def agregar_municipio(municipio_agregar: dict, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener los datos del municipio y enviarlos a la
        función que maneja la comunicación con la API
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para enviar los datos a la API
            municipio, codigo_estado = await LOTES.agregar_nuevo_municipio(municipio=municipio_agregar, token=token_acceso)

            # Verificar el valor
            if municipio:
                respuesta.append(municipio)
            else:
                respuesta = municipio

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener y enviar los valores del municipio: {error}")
            raise Exception("Ocurrió un error al obtener y enviar los valores del municipio.")

    @staticmethod
    async def obtener_localidad_especifica(identificador_localidad: str, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener y mapear la información
        de un localidad en especifico
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para obtener la información de la localidad
            respuesta_localidad, codigo_localidad = await LOTES.obtener_localidad_especifica(identificador_localidad, token_acceso)

            # Verificar el valor de la respuesta
            if respuesta_localidad and codigo_localidad == 200:

                # Iterar por vada valor de la lista
                # mapear el valo en base al módelo
                for dato in respuesta_localidad:
                    respuesta.append(LocalidadesBase(**dato))
            elif respuesta_localidad and codigo_localidad != 200:
                respuesta.append(respuesta_localidad)
            else:
                respuesta = respuesta_localidad

            return respuesta, codigo_localidad
        except Exception as error:
            print(f"Ocurrió un error al mapear los datos de la localidad: {error}")
            raise Exception("Ocurrió un error al mapear los datos de la localidad")

    @staticmethod
    async def agregar_localidad(localidad_agregar: dict, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener los datos de la localidad y enviarlos a
        la función que maneja la comunicación con la API
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para enviar los datos a la API
            localidad, codigo_estado = await LOTES.agregar_nueva_localidad(localidad=localidad_agregar, token=token_acceso)

            # Verificar el valor
            if localidad:
                respuesta.append(localidad)
            else:
                respuesta = localidad

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener y enviar los valores de la localidad: {error}")
            raise Exception("Ocurrió un error al obtener y enviar los valores de la localidad.")

    @staticmethod
    async def obtener_complejo_especifico(identificador_complejo: str, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener y mapear la información
        de un complejo en especifico
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para obtener la información de la complejo
            respuesta_complejo, codigo_complejo = await LOTES.obtener_complejo_especifico(identificador_complejo, token_acceso)

            # Verificar el valor de la respuesta
            if respuesta_complejo and codigo_complejo == 200:

                # Iterar por vada valor de la lista
                # mapear el valo en base al módelo
                for dato in respuesta_complejo:
                    respuesta.append(ComplejosResidencialesBase(**dato))
            elif respuesta_complejo and codigo_complejo != 200:
                respuesta.append(respuesta_complejo)
            else:
                respuesta = respuesta_complejo

            return respuesta, codigo_complejo
        except Exception as error:
            print(f"Ocurrió un error al mapear los datos de la complejo: {error}")
            raise Exception("Ocurrió un error al mapear los datos de la complejo")

    @staticmethod
    async def agregar_complejo(complejo_agregar: dict, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener los datos del complejo y enviarlos a
        la función que maneja la comunicación con la API
        """
        try:
            # Varible de respuesta
            respuesta = []

            # Llamar a la función para enviar los datos a la API
            complejo, codigo_estado = await LOTES.agregar_nuevo_complejo(complejo=complejo_agregar, token=token_acceso)

            # Verificar el valor
            if complejo:
                respuesta.append(complejo)
            else:
                respuesta = complejo

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener y enviar los valores del complejo: {error}")
            raise Exception("Ocurrió un error al obtener y enviar los valores del complejo.")

    @staticmethod
    async def agregar_seccion(seccion_agregar: dict, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener los datos de la sección y enviarlos a
        la función que maneja la comunicación con la API
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para enviar los datos a la API
            seccion, codigo_estado = await LOTES.agregar_nueva_seccion(seccion=seccion_agregar, token=token_acceso)

            # Verificar el valor
            if seccion:
                respuesta.append(seccion)
            else:
                respuesta = seccion

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener y enviar los valores de la sección: {error}")
            raise Exception("Ocurrió un error al obtener y enviar los valores de la sección.")

    @staticmethod
    async def agregar_lote(lote_agregar: dict, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener los datos del lote y enviarlos a
        la función que majea la comunicación con la API
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para enviar los datos a la API
            lote, codigo_estado = await LOTES.agregar_nuevo_lote(lote=lote_agregar, token=token_acceso)

            # Verificar el valor
            if lote:
                respuesta.append(lote)
            else:
                respuesta = lote

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error obtener y enviar los valores de los lotes: {error}")
            raise Exception(f"Ocurrió un error obtener y enviar los valores de los lotes: {error}")

    @staticmethod
    async def actualizar_un_lote(lote_actualizar: dict, identificador_lote: str, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener los datos para actualizar
        un lote existente
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para enviar los valores a la API
            respuesta_lote, codigo_estado = await LOTES. \
                actualizar_un_lote(lote_actualizar=lote_actualizar, identificador_lote=identificador_lote, token=token_acceso)

            # Verificar respuesta
            if respuesta_lote:
                respuesta.append(respuesta_lote)
            else:
                respuesta = respuesta_lote

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un erro al obtener y enviar los datos del lote: {error}")
            raise Exception("Ocurrió un erro al obtener y enviar los datos del lote")

    @staticmethod
    async def eliminar_un_lote(identificador_lote: str, token_acceso: str) -> bool:
        """
        Función que se encarga de obtener y enviar la información de un lote
        para ser eliminado
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para enviar los valores a la API
            respuesta_lote, codigo_estado = await LOTES. \
                eliminar_un_lote(identificador_lote=identificador_lote, token=token_acceso)

            # Verificar respuesta
            if respuesta_lote:
                respuesta.append(respuesta)
            else:
                respuesta = respuesta_lote

            return respuesta_lote, codigo_estado
        except Exception as error:
            print(f"Ocurrrió un error al obtener y enviar la información para eliminar un lote: {error}")
            raise Exception("Ocurrrió un error al obtener y enviar la información para eliminar un lote")


    # Método para actualizar una sección
    @staticmethod
    async def actualizar_una_seccion(seccion_actualizar: dict, identificador_seccion: str, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener y enviar los datos actualizados
        de una sección
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para enviar los valores a la API
            respuesta_seccion, codigo_estado = await LOTES. \
                actualizar_una_seccion(seccion=seccion_actualizar, identificador_seccion=identificador_seccion, token=token_acceso)

            # Verificar respuesta
            if respuesta_seccion:
                respuesta.append(respuesta_seccion)
            else:
                respuesta = respuesta_seccion

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al actualizar una sección: {error}")
            raise Exception("Ocurrió un error al actualizar una sección")

    # Método para eliminar una sección
    @staticmethod
    async def eliminar_una_seccion(identificador_seccion: str, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener y enviar los datos
        para eliminar una sección
        """
        try:
            # Variable de respuesta
            respuesta = []


            # LLamar a la función para enviar los valores a la API
            respuesta_seccion, codigo_estado = await LOTES. \
                eliminar_una_seccion(identificador_seccion=identificador_seccion, token=token_acceso)

            # Verificar respuesta
            if respuesta_seccion:
                respuesta.append(respuesta_seccion)
            else:
                respuesta = respuesta_seccion

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener y enviar los datos para eliminar una sección: {error}")
            raise Exception("Ocurrió un error al obtener y enviar los datos para eliminar una sección")

    # Método para actualizar un complejo
    @staticmethod
    async def actualizar_un_complejo(complejo_actualizar: dict, identificador_complejo: str, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtenre y enviar los valores actualizados
        de un complejo
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para enviar los valores a la API
            respuesta_seccion, codigo_estado = await LOTES. \
                actualizar_un_complejo(complejo=complejo_actualizar, identificador_complejo=identificador_complejo, token=token_acceso)

            # Verificar respuesta
            if respuesta_seccion:
                respuesta.append(respuesta_seccion)
            else:
                respuesta = respuesta_seccion

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener y enviar los valores actualizados de um complejo: {error}")
            raise Exception("Ocurrió un error al obtener y enviar los valores actualizados de um complejo")

    # Método para eliminar un complejo
    @staticmethod
    async def eliminar_un_complejo(identificador_complejo: str, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener y enviar los datos
        para eliminar un complejo
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para enviar los datos de la API
            respuesta_complejo, codigo_estado = await LOTES. \
                eliminar_un_complejo(identificador_complejo=identificador_complejo, token=token_acceso)

            # Verificar respuesta
            if respuesta_complejo:
                respuesta.append(respuesta_complejo)
            else:
                respuesta = respuesta_complejo

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener los datos para eliminar un complejo: {error}")
            raise Exception("Ocurrió un error al obtener los datos para eliminar un complejo")

    # Método para actualizar una localidad
    @staticmethod
    async def actualizar_una_localidad(localidad_actualizar: dict, identificador_localidad: str, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener y enviar los datos actuaizados
        de una localidad
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para enviar los datos a la API
            respuesta_localidad, codigo_estado = await LOTES. \
                actualizar_una_localidad(localidad=localidad_actualizar, identificador_localidad=identificador_localidad, token=token_acceso)

            # Verificar la respuesta
            if respuesta_localidad:
                respuesta.append(respuesta_localidad)
            else:
                respuesta = respuesta_localidad

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener y enviar los datos actualizados de una localida: {error}")
            raise Exception("Ocurrió un error al obtener y enviar los datos actualizados de una localida")

    # Método para eliminar una localidad
    @staticmethod
    async def eliminar_una_localidad(identificador_localidad: str, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener y enviar los datos
        para eliminar una localidad
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para enviar los datos a la API
            respuesta_localidad, codigo_estado = await LOTES. \
                eliminar_una_localidad(identificador_localidad=identificador_localidad, token=token_acceso)

            # Verificar respuesta
            if respuesta_localidad:
                respuesta.append(respuesta_localidad)
            else:
                respuesta = respuesta_localidad

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener y enviar los datos para eliminar una localidad: {error}")
            raise Exception("Ocurrió un error al obtener y enviar los datos para eliminar una localidad")

    # Método para actualizar un municipio
    @staticmethod
    async def actualizar_un_municipio(municipio_actualizar: dict, identificador_municipio: str, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener y enviar los datos actuaizados
        de una municipio
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para enviar los datos a la API
            respuesta_municipio, codigo_estado = await LOTES. \
                actualizar_un_municipio(municipio=municipio_actualizar, identificador_municipio=identificador_municipio, token=token_acceso)

            # Verificar la respuesta
            if respuesta_municipio:
                respuesta.append(respuesta_municipio)
            else:
                respuesta = respuesta_municipio

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener y enviar los datos actualizados de un municipio: {error}")
            raise Exception("Ocurrió un error al obtener y enviar los datos actualizados de un municipio")

    # Método para eliminar un municipio
    @staticmethod
    async def eliminar_un_municipio(identificador_municipio: str, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener y enviar los datos
        para eliminar una municipio
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para enviar los datos a la API
            respuesta_municipio, codigo_estado = await LOTES. \
                eliminar_un_municipio(identificador_municipio=identificador_municipio, token=token_acceso)

            # Verificar respuesta
            if respuesta_municipio:
                respuesta.append(respuesta_municipio)
            else:
                respuesta = respuesta_municipio

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener y enviar los datos para eliminar una municipio: {error}")
            raise Exception("Ocurrió un error al obtener y enviar los datos para eliminar una municipio")


    # Método para actualizar un estado:
    @staticmethod
    async def actualizar_un_estado(estado_actualizar: dict, identificador_estado: str, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener y enviar los datos actuaizados
        de una estado
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para enviar los datos a la API
            respuesta_estado, codigo_estado = await LOTES. \
                actualizar_un_estado(estado=estado_actualizar, identificador_estado=identificador_estado, token=token_acceso)

            # Verificar la respuesta
            if respuesta_estado:
                respuesta.append(respuesta_estado)
            else:
                respuesta = respuesta_estado

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener y enviar los datos actualizados de un estado: {error}")
            raise Exception("Ocurrió un error al obtener y enviar los datos actualizados de un estado")


    # Método para eliminar un estado:
    @staticmethod
    async def eliminar_un_estado(identificador_estado: str, token_acceso: str) -> tuple:
        """
        Función que se encarga de obtener y enviar los datos
        para eliminar una estado
        """
        try:
            # Variable de respuesta
            respuesta = []

            # Llamar a la función para enviar los datos a la API
            respuesta_estado, codigo_estado = await LOTES. \
                eliminar_un_estado(identificador_estado=identificador_estado, token=token_acceso)

            # Verificar respuesta
            if respuesta_estado:
                respuesta.append(respuesta_estado)
            else:
                respuesta = respuesta_estado

            return respuesta, codigo_estado
        except Exception as error:
            print(f"Ocurrió un error al obtener y enviar los datos para eliminar una estado: {error}")
            raise Exception("Ocurrió un error al obtener y enviar los datos para eliminar una estado")
