from django.urls import path
from . import views

urlpatterns = [
    path('registrarse/', views.RegistrarseAPIView.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('user/', views.UsuarioRetrieveUpdateAPIView.as_view()),
    path('login_social/', views.SocialLoginView.as_view()),
    path('usuario/perfil/', views.getPerfil),
    path('empresario/perfil/', views.getPerfil_empresario),
    path('lista/', views.getUsuariosList),
    path('usuario/editar/', views.editar_usuario),
    path('usuario/cambiar_contrasena/', views.cambiar_contrasena),
    path('usuario/<pk>/', views.getDetalleUsuario),
    
    path('taxistas/libres/', views.getTaxistasLibres),
    path('taxistas/ocupados/', views.getTaxistasOcupados),
    path('taxistas/no_disponibles/', views.getTaxistasNoDisponibles),
    path('cliente/activos/', views.getClientes_activos),
    path('cliente/inactivos/', views.getClientes_inactivos),
    path('empresario/activos/', views.getEmpresarios_activos),
    path('empresario/inactivos/', views.getEmpresarios_inactivos),
    path('taxista/activos/', views.getTaxistas_activos),
    path('taxista/inactivos/', views.getTaxistas_inactivos),

    # path('empresario/crear/', views.crear_empresario),
    path('android/<str:app>/', views.get_last_version),
    path('atencion/ciudad/<int:id_ciudad>/', views.get_responsable_ciudad),

    path('usuario/horario/crear/', views.crear_horario),
    path('usuario/horario/<int:id_horario>/editar/', views.editar_horario),
    path('usuario/horario/<int:id_horario>/ver/', views.ver_horario),
    path('usuario/horario/lista/', views.lista_horarios),
]