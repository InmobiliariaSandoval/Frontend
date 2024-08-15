"""
    Archivo que almacena el modelo de la estructura
    de datos de elementos de lotes
"""
from pydantic import BaseModel
from typing import Optional, Text

# Clase base de estados
class EstadosBase(BaseModel):
    id_estado: int
    nombre_estado: str

class MunicipiosBase(BaseModel):
    id_municipio: int
    nombre_municipio: str
    id_estado: int

class LocalidadesBase(BaseModel):
    id_localidad: int
    nombre_localidad: str
    id_municipio: int

class ComplejosResidencialesBase(BaseModel):
    id_complejo_residencial: int
    nombre_complejo: str
    tipo_complejo: str
    id_localidad: int

class LotesBase(BaseModel):
    id_lote: int
    nombre_seccion: str
    numero_lote: int
    id_seccion: int
    color_seccion: str
    estado_terreno: str

class LoteSeccionExtendido(BaseModel):
    id_seccion: int
    id_lote: int
    nombre_seccion: str
    nombre_complejo: str
    numero_lote: int
    estado_terreno: str
    medida_total: float
    medida_norte: float
    medida_sur: float
    medida_este: float
    medida_oeste: float
    otras_medidas: Optional[str]
    servicio_agua: bool
    servicio_electricidad: bool
    servicio_drenaje: bool
    otros_servicios: Optional[str]

class LotesUnico(BaseModel):
    id_lote: int
    numero_lote: int
    estado_terreno: str
    medida_total: float
    medida_norte: float
    medida_sur: float
    medida_este: float
    medida_oeste: float
    otras_medidas: Optional[str]
    servicio_agua: bool
    servicio_electricidad: bool
    servicio_drenaje: bool
    otros_servicios: Optional[str]
    id_seccion: int
    nombre_seccion: str

class SeccionesFiltro(BaseModel):
    id_seccion: int
    nombre_seccion: str
    color_seccion: str
    cantidad_lotes: int

class UbicacionLote(BaseModel):
    nombre_complejo: str
    nombre_localidad: str
    nombre_municipio: str
    nombre_estado: str

class VentaLotes(BaseModel):
    id_compra: int
    id_lote: int
    id_vendedor: int
    nombres_vendedor: str
    primer_apellido_vendedor: str
    segundo_apellido_vendedor: str
    CURP_cliente: str
    nombres_cliente: str
    primer_apellido_cliente : str
    segundo_apellido_cliente: str
