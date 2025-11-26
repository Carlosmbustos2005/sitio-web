from django.db import models
from django.contrib.auth.models import User

class Curso(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Estudiante(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='estudiantes')
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.curso})"

class Asistencia(models.Model):
    ESTADOS = [
        ('P', 'Presente'),
        ('A', 'Ausente'),
        ('J', 'Justificado'),
        ('T', 'Atrasado'),
    ]

    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='asistencias')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='asistencias')
    fecha = models.DateField()
    estado = models.CharField(max_length=1, choices=ESTADOS)
    docente = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('estudiante', 'fecha')

    def __str__(self):
        return f"{self.estudiante} - {self.fecha} - {self.get_estado_display()}"

class CostoProyecto(models.Model):
    nombre_proyecto = models.CharField(max_length=150, default='Sistema de Asistencia Escolar')
    licencias = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sueldos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    costo_despliegue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    dominio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    correos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    viaticos = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def total(self):
        return self.licencias + self.sueldos + self.costo_despliegue + self.dominio + self.correos + self.viaticos

    def __str__(self):
        return f"Costos del proyecto: {self.nombre_proyecto}"