"""
    Archivo que se encarga de administrar
    los módelos del apartado de ventas / compras
"""
from pydantic import BaseModel
from datetime import date

class VentasMostrar(BaseModel):
    nombres_cliente: str
    primer_apellido_cliente: str
    segundo_apellido_cliente: str
    estado_compra: str
    CURP_cliente: str
    id_compra: int
    fecha_compra: date


class Ventas(BaseModel):
    tipo_pago: str
    precio_total: float
    cantidad_total_plazos: int
    estado_compra: str
    fecha_compra: date
    id_vendedor: int
    CURP_cliente: str
    id_lote: int
    id_compra: int

class Plazos(BaseModel):
    numero_plazo: int
    cantidad_esperada: float
    fecha_esperada: date
    comprobante: bool
    id_compra: int
    restante: float
    id_plazo: int

class DetallesPlazo(BaseModel):
    id_detalle_pago: int
    fecha_entrega: date
    cantidad_dada: float
    total_compra: float
    id_plazo: int