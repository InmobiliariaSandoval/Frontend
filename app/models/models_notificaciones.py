"""
    Archivo que almacena el modelo de la esctructura
    de datos de notificaciones
"""
from datetime import date
from pydantic import BaseModel

# Clase base de notificaciones
class NotificacionesBase(BaseModel):
    id_notificacion: int
    titulo_notificacion:str
    descripcion: str
    fecha: date
    estado_leido: bool
    id_plazo: int

class ConfiguracionBase(BaseModel):
    id_configuracion: int
    nombre_usuario: str
    nombre_empresa: str
    correo_empresa: str