from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina_principal, name='main'),
    path('alumnos/', views.alumnos, name='alumnos'),
    path('profesores/', views.profesores, name='profesores'),
    path('subir/',views.profesores_subir,name='subir'),
    path('grupos/',views.grupos, name='grupos'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('horario/',views.horarios, name='horario')
]