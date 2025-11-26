from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db import OperationalError
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from .models import Curso, Estudiante, Asistencia, CostoProyecto

@login_required
def lista_cursos(request):
    try:
        cursos = Curso.objects.all()
    except OperationalError:
        return HttpResponse(
            "Error: no existe la tabla 'asistencia_curso'. Ejecuta:\n"
            "  python manage.py makemigrations asistencia\n"
            "  python manage.py migrate\n",
            status=500,
            content_type="text/plain"
        )
    return render(request, 'asistencia/lista_cursos.html', {'cursos': cursos})

def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('login'))

@login_required
def pasar_lista(request, curso_id):
    try:
        curso = get_object_or_404(Curso, pk=curso_id)
    except OperationalError:
        return HttpResponse(
            "Error: base de datos no preparada. Ejecuta las migraciones antes de usar la app.",
            status=500,
            content_type="text/plain"
        )
    estudiantes = curso.estudiantes.filter(activo=True).order_by('apellidos', 'nombres')
    fecha_hoy = timezone.localdate()

    if not request.user.is_staff:
        return render(request, 'asistencia/curso_personas.html', {'curso': curso, 'estudiantes': estudiantes})

    if request.method == 'POST':
        for estudiante in estudiantes:
            estado = request.POST.get(f'estado_{estudiante.id}')
            if estado:
                Asistencia.objects.update_or_create(
                    estudiante=estudiante,
                    fecha=fecha_hoy,
                    defaults={'curso': curso, 'estado': estado, 'docente': request.user}
                )
        return render(request, 'asistencia/confirmacion.html', {'curso': curso, 'fecha': fecha_hoy})
    return render(request, 'asistencia/pasar_lista.html', {'curso': curso, 'estudiantes': estudiantes, 'fecha_hoy': fecha_hoy})

@user_passes_test(lambda u: u.is_staff)
def ver_costos(request):
    try:
        costos = CostoProyecto.objects.all()
    except OperationalError:
        return HttpResponse(
            "Error: base de datos no preparada. Ejecuta las migraciones antes de usar la app.",
            status=500,
            content_type="text/plain"
        )
    return render(request, 'asistencia/ver_costos.html', {'costos': costos})

@user_passes_test(lambda u: u.is_staff)
def casos_de_uso(request):
    casos = [
        {
            'codigo': 'CU1',
            'nombre': 'Pasar lista diaria',
            'descripcion': 'El docente selecciona un curso y registra la asistencia de cada estudiante para la fecha actual.'
        },
        {
            'codigo': 'CU2',
            'nombre': 'Ver asistencia diaria de un curso',
            'descripcion': 'El docente revisa el resumen de asistencia de un curso en una fecha determinada.'
        },
        {
            'codigo': 'CU3',
            'nombre': 'Consultar historial de asistencia de un estudiante',
            'descripcion': 'El docente consulta todas las asistencias registradas para un estudiante específico.'
        },
    ]
    return render(request, 'asistencia/casos_de_uso.html', {'casos': casos})