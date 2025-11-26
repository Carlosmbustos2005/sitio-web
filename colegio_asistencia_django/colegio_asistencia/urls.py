from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views
from asistencia import views as asistencia_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', asistencia_views.logout_view, name='logout'),
    # raíz explícita -> lista_cursos
    path('', asistencia_views.lista_cursos, name='home'),
    path('', include(('asistencia.urls', 'asistencia'), namespace='asistencia')),
]