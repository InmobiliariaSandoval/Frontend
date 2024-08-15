"""
    Archivo que almacena el modelo de la esctructura
    de datos de vendedores
"""
from pydantic import BaseModel
from typing import Optional

# Clase base de notificaciones
class VendedoresBase(BaseModel):
    id_vendedor: int
    RFC_vendedor : Optional[str] = None
    nombres_vendedor: str
    primer_apellido_vendedor: str
    segundo_apellido_vendedor: Optional[str] = None
    numero_telefono: str
    correo_electronico: Optional[str] = None
    estado: str
    municipio: str
    colonia: str
    calle: str
    numero_exterior: Optional[str] = None
    codigo_postal: str
    lotes_vendidos: int
    estado_vendedor: bool
