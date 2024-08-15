"""
    Archivo que almancena los módelos de datos
    del apartado de clientes
"""
from pydantic import BaseModel
from typing import Optional

class ClienteBase(BaseModel):
    CURP_cliente: str
    nombres_cliente: str
    primer_apellido_cliente: str
    segundo_apellido_cliente: Optional[str]
    estado_civil: str
    ocupacion: str
    telefono_contacto: str
    calle: str
    numero_exterior: Optional[str]
    colonia: str
    municipio: str
    codigo_postal: str
    estado: str
    entrega_curp: bool
    entrega_credencial_elector: bool
    entrega_comprobante_domicilio: bool
