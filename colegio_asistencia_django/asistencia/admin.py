from django.contrib import admin
from .models import Curso, Estudiante, Asistencia, CostoProyecto

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'curso', 'activo')
    list_filter = ('curso', 'activo')
    search_fields = ('nombres', 'apellidos')

@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'curso', 'fecha', 'estado', 'docente')
    list_filter = ('curso', 'fecha', 'estado')
    search_fields = ('estudiante__nombres', 'estudiante__apellidos')

@admin.register(CostoProyecto)
class CostoProyectoAdmin(admin.ModelAdmin):
    list_display = ('nombre_proyecto', 'licencias', 'sueldos', 'costo_despliegue', 'dominio', 'correos', 'viaticos', 'total')