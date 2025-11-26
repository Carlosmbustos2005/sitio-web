from django.urls import path
from . import views

app_name = 'asistencia'

urlpatterns = [
    path('cursos/', views.lista_cursos, name='lista_cursos'),
    path('cursos/<int:curso_id>/pasar-lista/', views.pasar_lista, name='pasar_lista'),
    path('costos/', views.ver_costos, name='ver_costos'),
    path('casos-de-uso/', views.casos_de_uso, name='casos_de_uso'),
]