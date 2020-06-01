from django.urls import path
from . import views

urlpatterns = [
    path('movil/taxista/', views.ver_taxista, name='Ver Taxista'),
    path('movil/taxista/<int:id_usuario>/', views.ver_taxista_id, name='Ver Taxista por ID'),
]