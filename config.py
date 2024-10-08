"""
    Archivo de configuración para la aplicación
    Flask
"""
import os

DEBUG = False
SECRET_KEY = os.getenv('SECRET_FLASK')
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'Lax'

