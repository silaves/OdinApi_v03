from django.urls import path
from . import views

urlpatterns = [
    # CATEGORIA
    path('periodico/categoria/<str:estado>/', views.get_categorias, name='Lista de Categorias'),
    path('periodico/categoria/<str:estado>/nivel/', views.get_categorias_niveles, name='Lista de Categorias por NIVELES'),
    path('periodico/categoria/<int:id_categoria>/<str:estado>/hijo/', views.get_categorias_hijo, name='Lista de Categorias por HIJO'),
    path('periodico/categoria/<int:id_categoria>/<str:estado>/hijo_nivel/', views.get_categorias_hijo_niveles, name='Lista de Categorias por HIJOS NIVELES'),
    # NOTICIA
    path('periodico/noticia/<int:id_noticia>/', views.ver_noticia, name='Ver Noticia'),

    path('periodico/noticia/<str:estado>/todo/', views.get_noticias_all, name='Lista Todas Noticias by estado'),
    path('periodico/noticia/<str:estado>/todo/cursor/', views.get_noticias_all_paginacion_cursor, name='Lista Todas Noticias by estado - PAGINADOR CURSOR'),

    path('periodico/<int:id_empresa>/noticia/<str:estado>/', views.get_noticias_by_empresa, name='Lista Todas Noticias by Empresa'),
    path('periodico/<int:id_empresa>/noticia/<str:estado>/cursor/', views.get_noticias_by_empresa_paginacion_cursor, name='Lista Todas Noticias by Empresa - PAGINADOR CURSOR'),

    path('periodico/noticia/<str:estado>/categoria/<int:id_categoria>/', views.get_noticias_by_categoria, name='Lista Todas Noticias by Categoria'),
    path('periodico/noticia/<str:estado>/categoria/<int:id_categoria>/cursor/', views.get_noticias_by_categoria_paginacion_cursor, name='Lista Todas Noticias by Categoria - PAGINADOR CURSOR'),

]