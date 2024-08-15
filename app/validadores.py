"""
    Archivo que almacena las operaciones de validación
    en los distintos escenarios y partes del código
"""
import re

def validar_correo(correo_eletronico: str) -> bool:
    """
    Función que se encarga de validar el correo electrónico
    """
    patron = re.compile(r'^[a-zA-ZñÑ0-9._%+-]+@[a-zA-ZñÑ0-9.-]+\.[a-zA-ZñÑ]{2,}$')
    return bool(patron.match(correo_eletronico))

def validar_string(dato: str) -> bool:
    """
    Función que se encarga de validar cadenas de textos
    """
    patron = re.compile(r'^[a-zA-Z\sáéíóúÁÉÍÓÚñÑ]+$')
    return bool(patron.match(dato))

def validar_codigo_postal(codigo_postal: str) -> bool:
    """
    Función que se encarga de validar el código postal
    """
    patron = re.compile(r'^\d{5}$')
    return bool(patron.match(codigo_postal))

def validar_RFC(rfc: str) -> bool:
    """
    Función que se encarga de valir el RFC
    """
    patron = re.compile(r'^[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}$')
    return bool(patron.match(rfc))

def validar_CURP(curp: str) -> bool:
    """
    Función que se encarga de validar un CURP
    """
    patron = re.compile(r'^([A-Z][AEIOUX][A-Z]{2}\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])[HM](?:AS|B[CS]|C[CLMSH]|D[FG]|G[TR]|HG|JC|M[CNS]|N[ETL]|OC|PL|Q[TR]|S[PLR]|T[CSL]|VZ|YN|ZS)[B-DF-HJ-NP-TV-Z]{3}[A-Z\d])(\d)$')
    return bool(patron.match(curp))

def validar_numero(numero: str) -> bool:
    """
    Función que se encarga de validar un número
    """
    patron = re.compile(r'^[0-9]+$')
    return bool(patron.match(numero))

def validar_numero_telefono(numero_telefono: str) -> bool:
    """
    Función que se encarga de validar un número de télefono
    """
    patron = re.compile(r'^\d{10}$')
    return bool(patron.match(numero_telefono))

def validar_nombre_seccion(nombre_seccion: str) -> bool:
    """
    Función que se encarga de validar el nombre de la sección
    """
    patron = re.compile(r'^Sección \d+$')
    return bool(patron.match(nombre_seccion))

def validar_numero_decimal(numero):
    """
    Función que se encarga de validar un número decimal
    """
    patron = re.compile(r'^[0-9]+(\.[0-9]+)?$')
    return bool(patron.match(numero))

def validar_fecha(fecha):
    """
    Función que se encarga de validar la fecha
    """
    patron = re.compile(r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$')
    return bool(patron.match(fecha))

# Función principal que se encarga de validar el formulario ingresado
def validar_formulario(formulario: dict) -> dict:
    """
    Función que se encarga de validar el formulario enviado desde
    el frontend

    Args:
        formulario (dict): El formulario obtenido desde el FrontEnd

    Returns:
        dict: Los errores obtenidos. Puede ser un diccionario vacío o con los
            errores obtenidos en la validación
    """

    # Inicializar diccionario de validación
    errores_validacion = {}

    valores_reutilizable = [
        'nombres_vendedor', 'primer_apellido_vendedor', 'estado', 'municipio', 'colonia',
        'calle', 'nombre_estado', 'nombre_municipio', 'nombre_localidad', 'nombre_complejo',
        'nombres_cliente', 'primer_apellido_cliente', 'estado_civil', 'ocupacion',
        'tipo_pago', 'estado_compra',
    ]
    valores_reutilizables_numeros = [
        'id_estado', 'id_municipio', 'id_localidad', 'id_complejo_residencial',
        'cantidad_lotes', 'id_seccion', 'numero_lote', 'id_lote', 'id_vendedor',
        'id_compra', 'cantidad_total_plazos', 'numero_plazo', 'id_plazo', 'id_detalle_pago'
    ]

    valores_numeros_opciones = [
        'medida_norte', 'medida_sur', 'medida_oeste', 'medida_este', 'medida_total',
        'medida_total', 'precio_total', 'precio_inicial', 'enganche', 'cantidad_esperada',
        'cantidad_dada', 'total_compra'
    ]

    valores_texto_opcionales = [
        'segundo_apellido_vendedor', 'segundo_apellido_cliente'
    ]

    valores_telefonos = [
        'numero_telefono', 'telefono_contacto'
    ]

    valores_fecha = [
        'fecha_entrega', 'fecha_esperada'
    ]

    tipos_validos_complejos = ['Fraccionamiento', 'Privada', 'Residencial']

    # Iterar por cada elemento (clave, valor) del diccianario enviado
    for clave, valor in formulario.items():

        # Verificar cada posible caso del diccionari
        match clave:
            case 'correo_electronico':
                if valor and not validar_correo(valor):
                    errores_validacion[clave] = 'Correo electrónico no válido'
            case clave if clave in valores_reutilizable:
                if not validar_string(valor):
                    errores_validacion[clave] = f'{clave.replace('_', ' ')} no válido'
            case 'nombre_seccion':
                if not validar_nombre_seccion(valor):
                    errores_validacion[clave] = 'Nombre de sección no válido'
            case 'tipo_complejo':
                if not validar_string(valor) or valor not in tipos_validos_complejos:
                    errores_validacion[clave] = 'Tipo complejo no es válido'
            case clave if clave in valores_texto_opcionales:
                if valor and not validar_string(valor):
                    errores_validacion[clave] = 'Segundo apellido no válido'
            case clave if clave in valores_telefonos:
                if not validar_numero_telefono(valor):
                    errores_validacion[clave] = 'Número de télefono no válido'
            case 'codigo_postal':
                if not validar_codigo_postal(valor):
                    errores_validacion[clave] = 'Código postal no válido'
            case 'RFC_vendedor':
                if valor and not validar_RFC(valor):
                    errores_validacion[clave] = 'RFC no válido'
            case 'CURP_cliente':
                if not validar_CURP(valor):
                    errores_validacion[clave] = 'CURP no válido'
            case 'numero_exterior':
                if valor and not validar_numero(valor):
                    errores_validacion[clave] = 'Numero exterior no válido'
            case clave if clave in valores_reutilizables_numeros:
                if not validar_numero(valor):
                    errores_validacion[clave] = f'{clave.replace('_', ' ')} no válido'
            case clave if clave in valores_numeros_opciones:
                if valor and not validar_numero_decimal(valor):
                    errores_validacion[clave] = f'{clave.replace('_', ' ')} no válido'
            case clave if clave in valores_fecha:
                if not validar_fecha(valor):
                    errores_validacion[clave] = 'Fecha ingresada no válida'
            case _:
                pass

    return errores_validacion