import os
from django.core.wsgi import get_wsgi_application

# ...nuevo: registrar PyMySQL si está instalado (opcional; requiere pip install pymysql)
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except Exception:
    # si PyMySQL no está instalado, seguimos y Django fallará si no hay otro conector
    pass

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'colegio_asistencia.settings')

application = get_wsgi_application()